# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 18:31:01 2021

@author: lollo
"""

import pandas as pd
from geopy.distance import geodesic
import numpy as np

#----------------------------------------------------------------------------------------------------------------------------#

def importa_paesi(continente, args):
    
    '''La function crea una lista con i paesi appartenenti al continente considerato.'''
    
    #importazione della lista dei paesi del continente considerato
    with open(args.storage + f'{continente}/Paesi_{continente}.txt', 'r') as infile:
        paesi = []
        for line in infile:
            line = line.strip('\n')
            paesi += [line]
            
    return paesi        
            
#----------------------------------------------------------------------------------------------------------------------------#            

def selezione_infrastrutture(paesi, args, sites, continente):

    '''La function crea un file con le infrastrutture di tipo 'aeroporto' nel continente considerato.'''
    
    #selezione delle infrastrutture nel continente considerato
    Infrastructures = pd.DataFrame()
    for k in sites.index:
        if sites['Country'][k] in paesi and sites['Type'][k] == 'airport':
            Infrastructures = Infrastructures.append(sites.iloc[k], ignore_index = True)
    
    #pulizia e salvataggio delle informazioni    
    Infrastructures = Infrastructures[['Name', 'City', 'Country', 'IATA', 'Latitude', 'Longitude', 'Altitude', 'Type']]        
    Infrastructures = Infrastructures.drop_duplicates()  
    Infrastructures.to_csv(args.storage + f'{continente}/Infrastrutture_{continente}.csv')
    
    return Infrastructures
    
#----------------------------------------------------------------------------------------------------------------------------#

def matrice_di_adiacenza(Infrastructures, args, continente, paesi):

    '''La function crea la matrice di adiacenza basandosi sulle rotte e utilizzando come peso la distanza geodetica 
       tra i due nodi.'''
    
    #creazione di un dataframe/matrice di adiacenza con le infrastrutture del continente considerato   
    N_siti = len(Infrastructures)
    
    A = pd.DataFrame(np.zeros(shape = (N_siti,N_siti)))
    A.columns = Infrastructures['Name']
    A.index = Infrastructures['Name']
    
    #importazione dataframe delle rotte aggiornato
    routes = pd.read_csv(args.routes_data_updated)
    
    #calcolo dei pesi nella matrice di adiacenza e seleziono delle rotte nel continente considerato
    selezionati = pd.DataFrame()   
    for k in routes.index: 
        if routes['Country_x'][k] in paesi and routes['Country_y'][k] in paesi:
         if routes['Name_x'][k] in list(Infrastructures['Name']) and routes['Name_y'][k] in list(Infrastructures['Name']):
            selezionati = selezionati.append(routes.iloc[k], ignore_index = True) 
            
            coordinates_x = (routes['Latitude_x'][k], routes['Longitude_x'][k])
            coordinates_y = (routes['Latitude_y'][k], routes['Longitude_y'][k])
            
            A.at[routes['Name_x'][k], routes['Name_y'][k]] = geodesic(coordinates_x, coordinates_y).km
            A.at[routes['Name_y'][k], routes['Name_x'][k]] = geodesic(coordinates_x, coordinates_y).km
    
    #salvataggio dei dati
    selezionati.to_csv(args.storage + f'{continente}/Rotte_{continente}.csv')        
    A.to_csv(args.storage + f'{continente}/MatAdj_{continente}.csv') 
    
    return A, selezionati