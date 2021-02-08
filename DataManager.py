# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:54:28 2021

@author: lollo
"""

import pandas as pd
import os


def importa_dati(args):
    
    '''La function importa i dati in dataframe pronti per l'utilizzo.'''
    
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
    
    return df_sites, df_routes


def pulizia_dati(df_sites,df_routes):
    
    '''La function pulisce e sistema i dati precedentemente importati e li salva nella cartella del continente
       considerato per eventuali usi futuri.'''
    
    siti = df_sites.rename(columns={'IATA' : 'Source_airport'})
    df_routes = pd.merge(df_routes, siti, on=['Source_airport'],how='left')
    
    siti = siti.rename(columns={'Source_airport' : 'Destination_airport'})
    df_routes = pd.merge(df_routes, siti, on=['Destination_airport'],how='left')
    
    df_routes = df_routes.dropna(axis=0,how='any')
    
    df_routes = df_routes.drop_duplicates()
    
    path = os.path.join(f'Routes_AtoB_{continente}.csv')

    df_routes.to_csv(path)