# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 18:36:01 2020

@author: lollo

"""

import time 
import pandas as pd
import os
import argparse
from tqdm import tqdm
import folium
import numpy as np
from geopy.distance import geodesic
from icecream import ic
from timeit import default_timer as timer



parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--storage", help = "Cartella di Posizionamento dei Dataset",
                type = str, default = "./Data/")

parser.add_argument("-i2", "--sites_data", help = "File CSV delle Infrastrutture",
                type = str, default = "./Data/sites.csv")

parser.add_argument("-i3", "--routes_data", help = "File CSV delle Rotte",
                type = str, default = "./Data/routes.csv")

args = parser.parse_args()

#========================================================__main__=============================================================#

start = time.perf_counter()





with open("C:\\Users\\lollo\\OneDrive\\Desktop\\MCRSE\\Tesina\\ProgettoMCRSE\\Data\\Paesi_per_Continenti\\PaesiSA.txt", 'r') as f:
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





stop = time.perf_counter() - start