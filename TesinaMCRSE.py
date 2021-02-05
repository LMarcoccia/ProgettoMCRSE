# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 18:36:01 2020

@author: lollo

"""

import time 
import pandas as pd
import os
import requests
import argparse
import os
from icecream import ic
import matplotlib.pyplot as plt
import geopy
import json
from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import geojson
import folium


parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--storage", help = "Cartella di Posizionamento dei Dataset",
                type = str, default = "./Data/")

parser.add_argument("-i2", "--sites_url", help = "Link del Dataset delle Infrastrutture",
                type = str, default = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat")

parser.add_argument("-i3", "--routes_url", help = "Link del Dataset delle Rotte",
                type = str, default = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat")

parser.add_argument("-i4", "--sites_data", help = "File CSV delle Infrastrutture",
                type = str, default = "./Data/sites.csv")

parser.add_argument("-i5", "--routes_data", help = "File CSV delle Rotte",
                type = str, default = "./Data/routes.csv")

args = parser.parse_args()

#========================================================__main__=============================================================#

start = time.perf_counter()


# sites = requests.get(args.sites_url)
# routes = requests.get(args.routes_url)


# if not os.path.exists(args.storage):
#     os.makedirs(args.storage)

# 	
# open(args.sites_data, 'wb').write(sites.content)
# open(args.routes_data, 'wb').write(routes.content)

m = folium.Map(location=[-99.84374999999999,47.39834920035926], zoom_start=0.5)

Data = os.path.join('NA.json')

folium.GeoJson(Data, name='Nord America').add_to(m)

df_sites = pd.read_csv(args.sites_data, names=['Airport_ID','Name','City','Country','IATA',
                                                'ICAO','Latitude','Longitude','Altitude','Timezone',
                                                'DST','Tz_database_time_zone','Type','Source'])

df_routes = pd.read_csv(args.routes_data, names=['Airline','Airline_ID','Source_airport',
                                                  'Source_airport_ID','Destination_airport',
                                                  'Destination_airport_ID','Codeshare',
                                                  'Stops','Equipment'])


#pulizia e preparazione dei dati
df_sites = df_sites.drop(columns=['Airport_ID','ICAO','Timezone','DST','Tz_database_time_zone','Source'],axis=0)
df_routes = df_routes.drop(columns=['Airline','Airline_ID','Source_airport_ID','Destination_airport_ID',
                                    'Codeshare','Stops','Equipment'], axis=0)

    
siti = df_sites.rename(columns={'IATA' : 'Source_airport'})
df_routes = pd.merge(df_routes, siti, on=['Source_airport'],how='left')
siti = siti.rename(columns={'Source_airport' : 'Destination_airport'})
df_routes = pd.merge(df_routes, siti, on=['Destination_airport'],how='left')
df_routes = df_routes.dropna(axis=0,how='any')

with open('PaesiNA.txt', 'r') as f:
    paesi = []
    for line in f:
        paesi += [line]

hubs = siti[['Latitude','Longitude']]
hubs = hubs.values.tolist()
for k,hub in enumerate(hubs):
    if siti['Country'][k] in paesi and siti['Type'][k] == 'airport':
       folium.Marker(hub, popup= siti['Name'][k]).add_to(m)

m.save('NordAmerica.html')
    







stop = time.perf_counter() - start