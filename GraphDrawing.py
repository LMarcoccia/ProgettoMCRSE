# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:05:49 2021

@author: lollo
"""

import pandas as pd
from scipy.sparse.csgraph import laplacian
import scipy.linalg as la
import seaborn as sns
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------------------------------------------------------#

def calcola_autovettori_dal_laplaciano(A):

    '''La function calcola il laplaciano della matrice di adiacenza del continente considerato e trova gli autovettori.
       K raggruppa il secondo e il terzo autovettore (caso 2D).''' 
    
    #conversione da dataframe a matrice
    Adj = A.to_numpy()      
    
    #calcolo laplaciano
    L = laplacian(Adj)
    
    #calcolo autovettori e autovalori
    eigs = la.eig(L)
    
    eigenvectors = eigs[1]
    
    K = eigenvectors[:,[1,3]]
    
    return K

#------------------------------------------------------------------------------------------------------------------------------#

def scatterplot_autovettori(K, args, continente):

    '''La function crea lo scatterplot delle coordinate sulle righe dell'oggetto K ricavato con 
       calcola_autovettori_dal_laplaciano e successivamente salva il grafico nella cartella preposta.'''  

    #plot di ciascun punto
    plt.figure()
    sns.set_theme()
    
    for j in K:
        x = j[0]
        y = j[1]
        if x == 0j:
           x = 0.0   
        elif y == 0j:
           y = 0.0 
        plt.scatter(x,y)
    
    #salvataggio dei dati    
    plt.title(f'Scatterplot dei valori degli autovettori in {continente}')
    plt.savefig(args.results + f"{continente}/ScatterplotAutovettori_{continente}.png", dpi = 300)
    plt.close()     