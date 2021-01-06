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


sites = requests.get(args.sites_url)
routes = requests.get(args.routes_url)


if not os.path.exists(args.storage):
    os.makedirs(args.storage)

	
open(args.sites_data, 'wb').write(sites.content)
open(args.routes_data, 'wb').write(routes.content)


df_sites = pd.read_csv(args.sites_data, names=['Airport_ID','Name','City','Country','IATA',
                                               'ICAO','Latitude','Longitude','Altitude','Timezone',
                                               'DST','Tz_database_time_zone','Type','Source'])

df_routes = pd.read_csv(args.routes_data, names=['Airline','Airline_ID','Source_airport',
                                                 'Source_airport_ID','Destination_airport',
                                                 'Destination_airport_ID','Codeshare',
                                                 'Stops','Equipment'])

stop = time.perf_counter() - start