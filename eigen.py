# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 10:47:19 2021

@author: lollo
"""

import os
import pandas as pd
from scipy.sparse.csgraph import laplacian
import scipy.linalg as la
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt


df_path = os.path.join('NA_hubs.csv')

df = pd.read_csv(df_path)

mat_path = os.path.join('MatAdj.txt')

A = pd.read_csv(mat_path)       
A = A.set_index('Name')

Adj = A.to_numpy()      

L = laplacian(Adj)

eigs = la.eig(L)

eigenvectors = eigs[1]

K = eigenvectors[:,[1,3]]

sns.set_theme()
for j in tqdm(K):
    x = j[0]
    y = j[1]
    if x == 0j:
       x = 0.0   
    elif y == 0j:
       y = 0.0 
    
    plt.scatter(x,y)   

 