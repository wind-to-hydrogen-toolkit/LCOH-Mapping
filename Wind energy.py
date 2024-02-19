# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:47:30 2022

@author: quang
"""

import pandas as pd
import math
import numpy as np
import xarray as xr
from netCDF4 import Dataset 



ds = xr.open_dataset('Weibull_c_k_150m.nc')

k = ds.k.values
c = ds.c.values
df = pd.read_csv('Power curve.csv')
# Turbine
ro = 1.225

Vcin = 4
Vcout = 25
Vrate = 11
Prate = 15000 #kW 15MW
D = 248;
A = math.pi*D**2/4;
do = xr.Dataset()

do['AEP'] = ds['k']*0

time = 365*24;


for i in range(0,26):
    
    #if ((~np.isnan(ds.k)) and (~np.isnan(ds.c)) == True):
    Cpeq = df.Cp[i]    
    
    fv = k/c*(i/c)**(k-1)*np.exp(-(i/c)**k)
    do.AEP.values = do.AEP.values + df.Power[i]*fv*time
    '''
    if i >= Vcin and i<Vrate:
        do.AEP.values = do.AEP.values + 0.5*ro*A*Cpeq*i**3/1000*fv*time
    if i >= Vrate and i <= Vcout:
        do.AEP.values = do.AEP.values + Prate*fv*time
    '''
do.to_netcdf('AEP_150m.nc')

'''
for i in range(0,26):
    
    #if ((~np.isnan(ds.k)) and (~np.isnan(ds.c)) == True):
        
    fv = k/c*(i/c)**(k-1)*np.exp(-(i/c)**k)
    
    if i >= Vcin and i<Vrate:
        do.AEP.values = do.AEP.values + 0.5*ro*A*Cpeq*i**3/1000*fv*time
    if i >= Vrate and i <= Vcout:
        do.AEP.values = do.AEP.values + Prate*fv*time

do.to_netcdf('AEP_150m.nc')        
''' 





