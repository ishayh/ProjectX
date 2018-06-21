import os
import pandas as pd
import gpxpy
import gpxpy.gpx
import glob
import gmplot
from sqlalchemy import create_engine
import pymysql
import numpy as np
import geopy.distance
import requests
from requests.auth import HTTPDigestAuth
import json
from geopy import distance
import math
import urllib


pymysql.install_as_MySQLdb()
API_KEY = 'AIzaSyC34UXx4v-s8keP7i2yM7V5B0J58ra7gDo'
SQL_USER = 'Josh'
SQL_PWD = 123
DISK_ENGINE = create_engine('mysql+mysqldb://{user}:{pwd}@localhost/running'.format(user=SQL_USER, pwd=SQL_PWD))


def generate_coords():
    path = '../data/runs_coords/'
    all_files = glob.glob(path + "/*.gpx")

    df_coords = pd.DataFrame()

    for gpx_file in all_files:
        gpx_file = open(gpx_file, 'r')
        gpx = gpxpy.parse(gpx_file)
        listing_coords = []
        run_id = gpx_file.name[25:-4]

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat = point.latitude
                    lng = point.longitude
                    listing_coords.extend([lat, lng])
                    df1 = pd.DataFrame(listing_coords)
                    df1.columns = ['lat']
                    df2 = pd.DataFrame({'lat': df1.lat.values[::2], 'lng': df1.lat.values[1::2]})
                    df2['run_id'] = run_id
            df_coords = df_coords.append(df2, ignore_index=True)

    # add manually for now - geolocator service errors
    # df_coords['location'] = df_coords['coords'].apply(lambda location_geo: geolocator.reverse(location_geo))
    df_coords['city'] = 'NYC'

    generate_heat_map(df_coords)
    # convert_to_sql(df_coords, 'coordinates')

    return df_coords


def generate_routes():
    path = '../data/runs_data/'

    all_files = glob.glob(path + "/*.csv")
    df_routes = pd.DataFrame()
    list_ = []
    for file_path in all_files:
        df = pd.read_csv(file_path, index_col=None, header=0)
        run_id = os.path.basename(file_path)[6:-4]
        df['run_id'] = run_id
        list_.append(df)
    df_routes = pd.concat(list_)

    df_routes.run_id.unique()

    # convert_to_sql(df_routes, 'routes')
    return df_routes


def generate_heat_map(df_coords):
    # center in Central Park
    gmap = gmplot.GoogleMapPlotter(40.7829, -73.9654, 12)
    gmap.heatmap(df_coords['lat'], df_coords['lng'])
    gmap.draw("nyc_heatmap.html")


# def convert_to_sql(df, table_name):
#     # disk_engine = create_engine('mysql+mysqldb://Josh:123@localhost/running')
#     df.to_sql(table_name, con=DISK_ENGINE, if_exists='replace', index=False)
#     # print (df)

#
# def query_data():
#     sql = '''select * from routes limit 20'''
#     conn = DISK_ENGINE.connect()
#     df = pd.read_sql_query(sql, con=conn)
#     print (df)

def hottest_point(starting_location):
    df = generate_coords()
    lat = np.array(df.lat)
    lng = np.array(df.lng)
    coords = np.c_[lat, lng]

    distances = []
    for i in coords:
        distances.append(distance.distance(i, starting_location).km)

    min_coords = coords[distances.index(np.min(distances))]
    print ("in hottest point function:" + str(min_coords))
    min_lat = min_coords[0]
    min_lng = min_coords[1]

    return min_lat, min_lng, coords_distance(min_lat, min_lng, starting_location[0],starting_location[1])


def coords_distance(lat1, lng1, lat2, lng2):

    origins = str(lat1) + ',' + str(lng1)
    destination = str(lat2) + "," + str(lng2)
    payload = {'units': 'metric', 'origins': origins, 'destination': destination, 'key':API_KEY}
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origins}&destinations={destination}&key={key}".format(key=API_KEY,origins=origins,destination=destination)
    r = requests.get(url)
    print (r.url)
    data = r.json()
    distance = data["rows"][0]["elements"][0]["distance"]["value"]
    print (distance)

    return distance

def main():
    generate_coords()
    generate_routes()
    # query_data()
    hottest_point([40.7829,-73.9654])

if __name__ == '__main__':
    main()
