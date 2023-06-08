import pandas as pd
import geojson

# Read the CSV file
df = pd.read_csv('data.csv')

# Convert the 'datetime' column to a pandas datetime object
df['datetime'] = pd.to_datetime(df['datetime'])

# Get unique dates from the 'datetime' column
unique_dates = df['datetime'].dt.date.unique()

# Prompt the user to choose a specific date
print("Select a date to analyze the load:")
for i, date in enumerate(unique_dates):
    print(f"{i+1}. {date.strftime('%Y-%m-%d')}")
selected_date_index = int(input("Enter the number corresponding to the date: ")) - 1
selected_date = unique_dates[selected_date_index]

# Filter the data for the selected date
selected_df = df[df['datetime'].dt.date == selected_date]

# Group the data by latitude, longitude, and hour
groups = selected_df.groupby(['latitude', 'longitude', selected_df['datetime'].dt.hour]).size().reset_index(name='count')

# Create a GeoJSON object
features = []
for _, group in groups.iterrows():
    feature = geojson.Feature(
        geometry=geojson.Point((group['longitude'], group['latitude'])),
        properties={
            'load': group['count'],
            'time': group['datetime']
        }
    )
    features.append(feature)

geojson_object = geojson.FeatureCollection(features)

# Save the GeoJSON object to a file
with open('load_data.geojson', 'w') as f:
    geojson.dump(geojson_object, f)
