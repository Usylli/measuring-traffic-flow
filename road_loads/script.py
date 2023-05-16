from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import folium
from folium.plugins import HeatMapWithTime



def load_data():
    # Load the data from the CSV file into a Pandas DataFrame
    df = pd.read_csv('data.csv', nrows=100000, parse_dates=['datetime'], date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%y %H:%M'))
    return df


def cluster_data(df):
    # Select the latitude and longitude columns from the DataFrame
    X = df[['latitude', 'longitude']]

    # Use the KMeans algorithm to cluster the data into 10 groups
    kmeans = KMeans(n_clusters=100).fit(X)

    # Add a new column to the DataFrame that specifies the cluster for each row
    df['cluster'] = kmeans.labels_

    return df


def hourly_load(df):
    # Calculate the hourly load for each cluster
    hourly_load = df.groupby(['cluster', pd.Grouper(key='datetime', freq='1H')]).size().reset_index(name='load')

    return hourly_load


def create_map(df, date=None):
    # Create a map using the Folium library
    m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=12)
    # Add a circle marker for each cluster
    for index, row in df.drop_duplicates(subset='cluster').iterrows():
        cluster_df = df[df['cluster'] == row['cluster']]
        hourly_load = cluster_df.groupby(pd.Grouper(key='datetime', freq='1H')).size().reset_index(name='load')
        for _, load_row in hourly_load.iterrows():
            folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=load_row['load']/10, 
                                color='red', fill=True, fill_opacity=0.7, fill_color='red', 
                                tooltip=f"Load: {load_row['load']}").add_to(m)

    # Add a heatmap layer to show the load of cars in each area over time
    hm_data = []
    date = '2020-12-11'
    date = pd.to_datetime(date).date()
    if date is not None:
        df = df[df['datetime'].dt.date == date]
    for index, row in df.iterrows():
        hm_data.append([row['latitude'], row['longitude'], row['datetime'].to_pydatetime()])

    folium.plugins.HeatMapWithTime(hm_data, auto_play=True, radius=12, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'},
                                   min_opacity=0.5, max_opacity=0.8, overlay=True).add_to(m)

    return m


if __name__ == '__main__':
    df = load_data()
    df = cluster_data(df)
    hourly_load = hourly_load(df)
    m = create_map(df)
    m.save('map.html')