import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

# Read the CSV file
df = pd.read_csv('data.csv')

# Color definitions
color_definitions = {
    'low_load': '#00FF00',       # Green
    'medium_load': '#FFFF00',    # Yellow
    'high_load': '#FF0000',      # Red
}


# Convert the 'datetime' column to a pandas datetime object
df['datetime'] = pd.to_datetime(df['datetime'])

# Calculate the load count percentiles
percentiles = df.groupby(['latitude', 'longitude']).size().reset_index(name='count')['count'].quantile([0.25, 0.75])

# Define the load level thresholds
threshold_low = percentiles[0.25]
threshold_medium = percentiles[0.75]

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

# Group the data by latitude and longitude
groups = selected_df.groupby(['latitude', 'longitude']).size().reset_index(name='count')

# Create a map centered around the city
map_center = (df['latitude'].mean(), df['longitude'].mean())
m = folium.Map(location=map_center, zoom_start=12)

# Create points on the map for each group
for _, group in groups.iterrows():
    # Determine the load level based on the count
    if group['count'] <= threshold_low:
        color = color_definitions['low_load']
    elif group['count'] <= threshold_medium:
        color = color_definitions['medium_load']
    else:
        color = color_definitions['high_load']

    folium.CircleMarker(
        location=(group['latitude'], group['longitude']),
        radius=5,
        color=color,
        fill=True,
        fill_color=color  # Fill the center of the circle with the same color
    ).add_to(m)


# Create hourly load data for HeatMapWithTime
hourly_load_data = []
for hour in range(24):
    hour_data = selected_df[selected_df['datetime'].dt.hour == hour]
    hourly_load_data.append(hour_data[['latitude', 'longitude']].values.tolist())

# Add HeatMapWithTime to the map
HeatMapWithTime(hourly_load_data).add_to(m)

# Save the map as an HTML file
m.save('load_map.html')
