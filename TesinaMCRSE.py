# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 18:36:01 2020

@author: lollo

"""

import argparse
from timeit import default_timer as timer
import DataManager as dm
import ProcessSequence as ps
from multiprocessing import Process

#============================================================================================================================#
parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--storage", help = "Cartella di Posizionamento dei Dataset",
                type = str, default = "./Data/")

parser.add_argument("-i2", "--sites_data", help = "File CSV delle Infrastrutture",
                type = str, default = "./Data/Sites.csv")

parser.add_argument("-i3", "--routes_data", help = "File CSV delle Rotte",
                type = str, default = "./Data/Routes.csv")

parser.add_argument("-i4", "--sites_url", help = "Link dei dati sulle infrastrutture",
                type = str, default = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports-extended.dat")

parser.add_argument("-i5", "--routes_url", help = "Link dei dati sulle rotte",
                type = str, default = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat")

parser.add_argument("-i6", "--results", help = "Cartella di Posizionamento dei File in Output",
                type = str, default = "./Results/")

parser.add_argument("-i7", "--routes_data_updated", help = "File CSV delle Rotte Aggiornato",
                type = str, default = "./Data/UpdatedRoutes.csv")

args = parser.parse_args()

#========================================================__main__============================================================#

#avvio timer prestazionale
start = timer()
    
if __name__ == '__main__':
    
    #definizione della lista dei continenti
    continenti = ['AF','AS','EU','NA','OC','SA']
    
    #creazione directories per l'organizzazione dei file in output
    dm.crea_directories(continenti, args)
    
    #creazione dataframe delle infrastrutture e delle rotte
    sites, routes = dm.importa_dati(args)
    
    #pulizia dataframe delle rotte
    routes = dm.pulizia_dati(sites, routes, args)
    
    #parallelizzazione dei processi
    prcs = [Process(target = ps.routine_continente_singolo, args = (args, continente, sites, routes)) for continente in continenti]
    for t in prcs:
        t.start()
    for t in prcs:
        t.join()
       
stop = timer() - start 

print('\nI risultati sono pronti!')
print('\nTempo Di Esecuzione: ', stop/60, 'min')