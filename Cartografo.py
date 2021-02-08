# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 18:58:22 2021

@author: lollo
"""

import folium
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster

#----------------------------------------------------------------------------------------------------------------------------#

def crea_mappa(continente, args, selezionati, A):

    '''La function crea una mappa in cui viene evidenziato il continente considerato. Successivamente vengono
       plottati gli aeroporti su di essa e collegati se esiste un collegamento tra di loro. La mappa viene poi
       salvata in formato html nella cartella preposta.'''

    #creazione mappa
    m = folium.Map(location = [-99.84374999999999,47.39834920035926], zoom_start=0.5)
    
    Data = args.storage + f'{continente}/Geojson_{continente}.json'
    
    #plot in rilievo del continente considerato
    folium.GeoJson(Data, name = continente).add_to(m)  
    
    #plot dei nodi e delle rotte
    già_stampati = []
    for k in selezionati.index:
        
        partenza = selezionati['Name_x'][k]
        grado_p = np.count_nonzero(np.array(A.loc[partenza]))
        coordinates_p = (selezionati['Latitude_x'][k], selezionati['Longitude_x'][k])
        
        arrivo = selezionati['Name_y'][k]
        grado_a = np.count_nonzero(np.array(A.loc[arrivo]))
        coordinates_a = (selezionati['Latitude_y'][k], selezionati['Longitude_y'][k])
        
        if grado_p >= 30 and grado_a >= 30:
            
            if coordinates_p not in già_stampati:
               folium.Marker(coordinates_p, popup = selezionati['Name_x'][k]).add_to(m)
            if coordinates_a not in già_stampati:
               folium.Marker(coordinates_a, popup = selezionati['Name_y'][k]).add_to(m)
            
            folium.PolyLine((coordinates_p, coordinates_a), color='red', weight=0.8).add_to(m)
            
            già_stampati += [coordinates_p]
            già_stampati += [coordinates_a]
            
    #salvataggio dei dati        
    m.save(args.results + f'{continente}/Mappa_{continente}.html')
    
#----------------------------------------------------------------------------------------------------------------------------#    
    
def crea_mappa_per_confronto_scatterplot(Infrastructures, continente, args):
    
    '''La function crea una mappa con tutti gli hub del continente considerato per un confronto con lo scatterplot
       ottenuto dagli autovettori.'''
       
    m = folium.Map(location = [-99.84374999999999,47.39834920035926], zoom_start=0.5)
    
    Data = args.storage + f'{continente}/Geojson_{continente}.json'
    
    folium.GeoJson(Data, name = continente).add_to(m)    
    
    #aggiunta di un meccanismo di clusterizzazione per rinforzare il confronto
    marker_cluster = MarkerCluster().add_to(m)
    
    #plot delle infrastrutture
    for k in Infrastructures.index:
        coordinates = (Infrastructures['Latitude'][k], Infrastructures['Longitude'][k])
        folium.Marker(coordinates, popup = Infrastructures['Name'][k]).add_to(marker_cluster)
            
    #salvataggio dei dati    
    m.save(args.results + f'{continente}/MappaPerConfronto_{continente}.html')