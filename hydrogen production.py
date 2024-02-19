# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 17:14:28 2022

@author: quang
"""
import xarray as xr
import numpy as np

ds = xr.open_dataset('AEP_150m.nc') # energy/turbine
# wind farm have 34 turbines 15MW
# wind farm size 510 MW
num_tur = 34;
size_tur = 15000;       #kW
size_wf = num_tur*size_tur; #kW

E_pcl = 3;              #kWh/kg
E_elec = 50;            # kWh/kg
n_conv = 0.93;          # %
d1 = xr.Dataset()

d1['AHP'] = ds['AEP']*num_tur*0.9/(E_elec/n_conv+E_pcl)/1000; # tons

d1.to_netcdf('AHP_150m.nc')

