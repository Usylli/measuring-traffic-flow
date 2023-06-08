import cv2
import geojson
import numpy as np
from flask import Flask, Response, render_template, send_file, request
from flask_cors import CORS, cross_origin

import pandas as pd
import folium
from folium.plugins import HeatMapWithTime

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def center_handle(x, y, w, h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx, cy


@app.route('/')
@cross_origin(origin='*')
def index():
    return render_template('index.html')


def generate():
    cap = cv2.VideoCapture('video.mp4')

    min_width_react = 80
    min_height_react = 80

    count_line_position = 600

    algo = cv2.createBackgroundSubtractorMOG2()
    detect = []
    offset = 6
    counter = 0
    frame_counter = 0
    while True:
        # if frame_counter < 10:
        #     frame_counter += 1
        #     continue
        ret, frame1 = cap.read()
        if not ret:
            break
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)

        img_sub = algo.apply(blur)
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        counterShape, h = cv2.findContours(
            dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position),
                 (150, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position),
                 (150, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position+offset),
                 (520, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position-offset),
                 (520, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (720, count_line_position+offset),
                 (1060, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (720, count_line_position-offset),
                 (1060, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position),
                 (150, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (150, count_line_position),
                 (150, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (520, count_line_position),
                 (520, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (520, count_line_position),
                 (520, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (720, count_line_position),
                 (720, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (720, count_line_position),
                 (720, count_line_position-offset), (255, 127, 0), 3)
        cv2.line(frame1, (1060, count_line_position),
                 (1060, count_line_position+offset), (255, 127, 0), 3)
        cv2.line(frame1, (1060, count_line_position),
                 (1060, count_line_position-offset), (255, 127, 0), 3)

        for (i, c) in enumerate(counterShape):
            (x, y, w, h) = cv2.boundingRect(c)
            validate_counter = (w >= min_width_react) and (
                h >= min_height_react)
            if not validate_counter:
                continue

            # cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame1, "Vehicle" + str(counter), (x, y - 20), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 244, 0), 2)

            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)

            for (x, y) in detect:
                if ((y < (count_line_position + offset) and y > (count_line_position - offset))
                        and ((x > 150 and x < 520) or (x > 720 and x < 1060))):
                    counter += 1
                # cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
                detect.remove((x, y))
                # print("Vehicle Counter:" + str(counter))

        cv2.putText(frame1, "VEHICLE COUNTER :" + str(counter),
                    (600, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Encode the output image to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame = jpeg.tobytes()
        # frame_counter = 0

        # Yield the output image as a byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/video_feed')
@cross_origin(origin='*')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/road_loads_dates')
@cross_origin(origin='*')
def get_dates():
    # Read the CSV file
    df = pd.read_csv('data.csv')

    # Convert the 'datetime' column to a pandas datetime object
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Get unique dates from the 'datetime' column
    unique_dates = df['datetime'].dt.date.unique()
    unique_dates.sort(axis=0)

    return dict(enumerate([date.strftime('%Y-%m-%d') for date in unique_dates], 1))


@app.route('/road_loads')
@cross_origin(origin='*')
def get_html():
    args = request.args

    # Read the CSV file
    df = pd.read_csv('data.csv')

    # Convert the 'datetime' column to a pandas datetime object
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Get unique dates from the 'datetime' column
    unique_dates = df['datetime'].dt.date.unique()

    inputed_date = args.get('date')
    selected_date_index = int(inputed_date) - 1
    selected_date = unique_dates[selected_date_index]

    # Filter the data for the selected date
    selected_df = df[df['datetime'].dt.date == selected_date]

    # Group the data by latitude and longitude
    groups = selected_df.groupby(
        ['latitude', 'longitude']).size().reset_index(name='count')

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
        hourly_load_data.append(
            hour_data[['latitude', 'longitude']].values.tolist())

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
    m.save('templates/load_map.html')
    return send_file('load_map.html')


@app.route('/road_loads_geojson')
@cross_origin(origin='*')
def get_geojson():
    args = request.args

    # Read the CSV file
    df = pd.read_csv('data.csv')

    # Convert the 'datetime' column to a pandas datetime object
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Get unique dates from the 'datetime' column
    unique_dates = df['datetime'].dt.date.unique()

    inputed_date = args.get('date')
    selected_date_index = int(inputed_date) - 1
    selected_date = unique_dates[selected_date_index]

    selected_df = df[df['datetime'].dt.date == selected_date]

    # Group the data by latitude, longitude, and hour
    groups = selected_df.groupby(
        ['latitude', 'longitude', selected_df['datetime'].dt.hour]).size().reset_index(name='count')

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

    return geojson_object
