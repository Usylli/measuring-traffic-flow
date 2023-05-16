import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

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

# Group the data by latitude and longitude
groups = selected_df.groupby(['latitude', 'longitude']).size().reset_index(name='count')

# Create a map centered around the city
map_center = (df['latitude'].mean(), df['longitude'].mean())
m = folium.Map(location=map_center, zoom_start=12)

# # Create points on the map for each group
# for _, group in groups.iterrows():
#     folium.CircleMarker(
#         location=(group['latitude'], group['longitude']),
#         radius=5,
#         color='blue',
#         fill=True,
#         fill_color='blue'
#     ).add_to(m)

# Create hourly load data for HeatMapWithTime
hourly_load_data = []
for hour in range(24):
    hour_data = selected_df[selected_df['datetime'].dt.hour == hour]
    hourly_load_data.append(hour_data[['latitude', 'longitude']].values.tolist())

# Add HeatMapWithTime to the map
HeatMapWithTime(hourly_load_data).add_to(m)
# Create a legend
legend_html = """
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 150px; height: 90px; 
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color: #FFFFFF;
                ">
     &nbsp; Load Legend <br>
     &nbsp; Low: <i class="fa fa-circle fa-1x" style="color:#00FF00"></i><br>
     &nbsp; Medium: <i class="fa fa-circle fa-1x" style="color:#FFFF00"></i><br>
     &nbsp; High: <i class="fa fa-circle fa-1x" style="color:#FF0000"></i>
      </div>
     """

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map as an HTML file
#m.save('load_map.html')
print(m.save('load_map.geojson'))