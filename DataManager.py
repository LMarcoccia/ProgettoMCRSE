# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:54:28 2021

@author: lollo
"""

import pandas as pd
import requests
import os

#--------------------------------------------------------------------------------------------------------------------------#

def crea_directories(continenti, args):
    
    '''La function crea le directories per l'organizzazione dei file di output.'''
    
    #creazione directories per i file di output
    for c in continenti:
        if not os.path.exists(args.results + c):
            os.makedirs(args.results + c)

#--------------------------------------------------------------------------------------------------------------------------#

def importa_dati(args):
    
    '''La function scarica da internet i dati e li importa in dataframe pronti per l'utilizzo.'''
    
    #download dei dati
    sites = requests.get(args.sites_url)
    routes = requests.get(args.routes_url)
	
    #salvataggio dei dati
    open(args.sites_data, 'wb').write(sites.content)
    open(args.routes_data, 'wb').write(routes.content)   
 
    #lettura dei dataframe
    sites = pd.read_csv(args.sites_data, names = ['Airport_ID','Name','City','Country','IATA',
                                                'ICAO','Latitude','Longitude','Altitude','Timezone',
                                                'DST','Tz_database_time_zone','Type','Source'])

    routes = pd.read_csv(args.routes_data, names = ['Airline','Airline_ID','Source_airport',
                                                  'Source_airport_ID','Destination_airport',
                                                  'Destination_airport_ID','Codeshare',
                                                  'Stops','Equipment'])

    #eliminazione colonne superflue
    sites = sites.drop(columns = ['Airport_ID','ICAO','Timezone','DST','Tz_database_time_zone','Source'], axis = 0)
    routes = routes.drop(columns = ['Airline','Airline_ID','Source_airport_ID','Destination_airport_ID',
                                        'Codeshare','Stops','Equipment'], axis = 0)
    
    return sites, routes

#--------------------------------------------------------------------------------------------------------------------------#

def pulizia_dati(sites, routes, args):
    
    '''La function pulisce e sistema i dati precedentemente importati e li salva nella cartella del continente
       considerato per eventuali usi futuri.'''
    
    #inserimento delle informazioni sull'aeroporto di partenza nel dataframe delle rotte
    sites = sites.rename(columns = {'IATA' : 'Source_airport'})
    routes = pd.merge(routes, sites, on = ['Source_airport'], how = 'left')
    
    #inserimento delle informazioni sull'aeroporto di arrivo nel dataframe delle rotte
    sites = sites.rename(columns = {'Source_airport' : 'Destination_airport'})
    routes = pd.merge(routes, sites, on = ['Destination_airport'], how = 'left')
    
    #eliminazione delle righe con valore nullo
    routes = routes.dropna(axis = 0, how = 'any')
    
    #eliminazione dei duplicati
    routes = routes.drop_duplicates()
    
    #salvataggio delle informazioni
    routes.to_csv(args.routes_data_updated)
    
    return routes