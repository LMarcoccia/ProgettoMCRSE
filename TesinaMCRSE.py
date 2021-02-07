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

with open('PaesiNA.txt', 'r') as f:
    paesi = []
    for line in f:
        line = line.strip('\n')
        paesi += [line]

NordAmerica = pd.DataFrame()
hubs = df_sites[['Latitude','Longitude']]
hubs = hubs.values.tolist()
for k,hub in tqdm(enumerate(hubs)):
    if df_sites['Country'][k] in paesi and df_sites['Type'][k] == 'airport':
       NordAmerica = NordAmerica.append(df_sites.iloc[k], ignore_index=True)
     
NordAmerica = NordAmerica[['Name', 'City', 'Country', 'IATA', 'Latitude', 'Longitude', 'Altitude', 'Type']]        

NordAmerica = NordAmerica.drop_duplicates()
      
NordAmerica.to_csv('NA_hubs.csv')

siti = df_sites.rename(columns={'IATA' : 'Source_airport'})
df_routes = pd.merge(df_routes, siti, on=['Source_airport'],how='left')
siti = siti.rename(columns={'Source_airport' : 'Destination_airport'})
df_routes = pd.merge(df_routes, siti, on=['Destination_airport'],how='left')
df_routes = df_routes.dropna(axis=0,how='any')

df_routes = df_routes.drop_duplicates()

path = os.path.join('Routes_A_to_B.csv')

df_routes.to_csv(path)

stop = time.perf_counter() - start