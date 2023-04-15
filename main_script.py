import pandas as pd 
import numpy as np
import requests
from shapely.geometry import Point
import geopandas as gpd 
from geopy.distance import distance
import argparse

df_temp = pd.read_csv('./data/temples_api.csv')
df_bici = pd.read_csv('./data/bicimad.csv')

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

distance = []
for idx, rows_temp in df_temp.iterrows():
    for idx, rows_bici in df_bici.iterrows():
        distance.append(distance_meters(rows_temp['Latitude'],rows_temp['Longitude'],rows_bici['Latitude'],rows_bici['Longitude']))

combined_df = df_temp.merge(df_bici, how='cross')

combined_df['distance'] = combined_df.apply(lambda x: distance_meters(x['Latitude_x'], x['Longitude_x'],x['Latitude_y'], x['Longitude_y']), axis=1)

final_df = combined_df.loc[combined_df.groupby("Place of interest")["distance"].idxmin()]

final_df1 = final_df.drop(['Latitude_x','Longitude_x','Coordinates','Latitude_y','Longitude_y'], axis=1)


def argument_parser():
    parser = argparse.ArgumentParser(description= 'Application for nearest bicimad station' )
    parser.add_argument('--location', type=str, required=True, help='Location for finding the nearest BiciMAD station')
    args = parser.parse_args()
    return args


if argument_parser == 'all':
    final_df1.to_csv('./data/pipeline_df.csv', index=False)
else:
    final_df1 = final_df1[['lugar']== argument_parser]
    final_df1.to_csv('./data/pipeline_df.csv', index=False)



 






