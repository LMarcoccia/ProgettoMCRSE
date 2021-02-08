# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:25:55 2021

@author: lollo
"""

import ContinentData as cd
import Cartografo as cgf
import GraphDrawing as gd

#------------------------------------------------------------------------------------------------------------------------------#

def routine_continente_singolo(args, continente, sites, routes):

    '''La function rappresenta il processo da eseguire per ciascun continente al fine di conseguire 
       l'obiettivo della tesina.'''

    paesi = cd.importa_paesi(continente, args)
       
    Infrastructures = cd.selezione_infrastrutture(paesi, args, sites, continente) 
       
    A, selezionati = cd.matrice_di_adiacenza(Infrastructures, args, continente, paesi)     
    
    cgf.crea_mappa(continente, args, selezionati, A)
     
    cgf.crea_mappa_per_confronto_scatterplot(Infrastructures, continente, args)
    
    K = gd.calcola_autovettori_dal_laplaciano(A)
    
    gd.scatterplot_autovettori(K, args, continente)
