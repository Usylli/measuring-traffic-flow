import csv
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="127.0.0.1",
    database="devdb",
    user="devuser",
    password="123456"
)

# Open the CSV file and read the data
with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        guid, datetime, latitude, longitude = row
        print(guid, datetime, latitude, longitude)
        break
        # Insert the data into the PostgreSQL database
        # cur = conn.cursor()
        # cur.execute(
        #     "INSERT INTO car_location (guid, datetime, latitude, longitude) VALUES (%s, %s, %s, %s)",
        #     (guid, datetime, latitude, longitude)
        # )
        # conn.commit()

# Close the database connection
conn.close()
