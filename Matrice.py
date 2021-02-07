# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 10:38:59 2021

@author: lollo
"""

import folium
import numpy as np
import pandas as pd
import os
from geopy.distance import geodesic
from tqdm import tqdm
from icecream import ic
from timeit import default_timer as timer


start = timer()

ic('Importazione Dati...')

path = os.path.join('NA_hubs.csv')

df = pd.read_csv(path)
df = df.drop(columns=['Unnamed: 0'],axis=0)

N_siti = len(df)

A = pd.DataFrame(np.zeros(shape=(N_siti,N_siti)))
A.columns = df['Name']
A.index = df['Name']

path = os.path.join('Routes_A_to_B.csv')

routes = pd.read_csv(path)

with open('PaesiNA.txt', 'r') as f:
    paesi = []
    for line in f:
        line = line.strip('\n')
        paesi += [line]  
  
ic('Creazione Matrice di Adiacenza...') 
start_matrix_process = timer()
selezionatiNA = pd.DataFrame()   
for k in tqdm(routes.index):
    if routes['Country_x'][k] in paesi and routes['Country_y'][k] in paesi:
     if routes['Name_x'][k] in list(df['Name']) and routes['Name_y'][k] in list(df['Name']):
        selezionatiNA = selezionatiNA.append(routes.iloc[k], ignore_index=True) 
        coordinates_x = (routes['Latitude_x'][k],routes['Longitude_x'][k])
        coordinates_y = (routes['Latitude_y'][k],routes['Longitude_y'][k])
        A.at[routes['Name_x'][k],routes['Name_y'][k]] = geodesic(coordinates_x,coordinates_y).km
        A.at[routes['Name_y'][k],routes['Name_x'][k]] = geodesic(coordinates_x,coordinates_y).km
     
A.to_csv('MatAdj.txt')      
     
end_matrix_process = timer()
   
# ic('Creazione Grafo...') 
# start_drawing_process = timer() 
# adj_matrix = A.to_numpy()
# G = nx.from_numpy_matrix(adj_matrix)
# nx.draw(G)
# end_drawing_process = timer() 

ic('Creazione Mappa...') 
start_mapping_process = timer()

m = folium.Map(location=[-99.84374999999999,47.39834920035926], zoom_start=0.5)

Data = os.path.join('NA.json')

folium.GeoJson(Data, name='Nord America').add_to(m)  

# marker_cluster = MarkerCluster().add_to(m)


già_stampati = []
for k in tqdm(selezionatiNA.index):
    
    partenza = selezionatiNA['Name_x'][k]
    grado_p = np.count_nonzero(np.array(A.loc[partenza]))
    coordinates_p = (selezionatiNA['Latitude_x'][k],selezionatiNA['Longitude_x'][k])
    
    arrivo = selezionatiNA['Name_y'][k]
    grado_a = np.count_nonzero(np.array(A.loc[arrivo]))
    coordinates_a = (selezionatiNA['Latitude_y'][k],selezionatiNA['Longitude_y'][k])
    if grado_p >= 30 and grado_a >= 30:
        if coordinates_p not in già_stampati:
           folium.Marker(coordinates_p, popup= selezionatiNA['Name_x'][k]).add_to(m)
        if coordinates_a not in già_stampati:
           folium.Marker(coordinates_a, popup= selezionatiNA['Name_y'][k]).add_to(m)
        
        folium.PolyLine((coordinates_p,coordinates_a), color='red', weight=0.8).add_to(m)
        
        già_stampati += [coordinates_p]
        già_stampati += [coordinates_a]
        

m.save('NordAmerica.html')
end_mapping_process = timer()

stop = timer()

print('\n')
print('Tempi di Esecuzione:')
print('Totale: ', stop-start)
print('Matrice: ', end_matrix_process - start_matrix_process)
# print('Grafo: ', end_drawing_process - start_drawing_process)
print('Mappa: ', end_mapping_process - start_mapping_process)