# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:55:27 2022

@author: quang
"""

import xarray as xr
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt
import pandas as pd

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def Cost_foundation(Windfarm_size, num_tur, water_depth, D_port):
    
    if water_depth < 30:    # Monopile
        Cost_manu = 196.4522;    # k euro
        day_install = 1;
    elif water_depth < 60:  # Jacket
        Cost_manu = 258.4282;  # k euro
        day_install = 3;
    else:                   # Floating
        Cost_manu = 366.4892; # k euro
        day_install = 2;
        
    n_per = 5;              # Number foundation per visit
    Cost_vessel = 92.1      # k euro/day
    hour_workingday = 24;   # h
    V_vessel = 20;      # km/h
    num_travel = math.ceil(num_tur/n_per)
    day_to_site = 2*D_port/(V_vessel*hour_workingday)
    
    Cost = Cost_manu*Windfarm_size + (day_to_site*num_travel + day_install*num_tur)*Cost_vessel

    return Cost

def Cost_installation(num_tur, D_port):
    
    T_install = 2;      # days time of installation of turbine
    V_vessel = 20;     # km/h average speed of vessel
    Cost_vessel = 92.1;   # k euro/day
    n_tur_trip = 5;     # number of turbines carried per trip
    num_travel = math.ceil(num_tur/n_tur_trip)
    Cost = (num_tur*T_install + 2*D_port*num_travel/V_vessel)*Cost_vessel; # k euro
    return Cost

def CAPEX_Windfarm(Windfarm_size,num_tur, water_depth, D_port, D_inject):
    
    Cost_DC = 142.14*Windfarm_size;    # k euro
    tur_size = Windfarm_size/num_tur
    Cost_tur = 902.45*Windfarm_size;   #k euro
    Cost_found = Cost_foundation(Windfarm_size, num_tur, water_depth, D_port)
    Cost_inst = Cost_installation(num_tur, D_port)
    
    Capex_wf = Cost_DC + Cost_tur + Cost_found + Cost_inst;
    return Capex_wf

def CAPEX_pipeline (D_inject):
    
    Elec_cap = Windfarm_size;
    P_rate = 0.0055;        # kg/s/MW
    ro = 8;                 # kg/m3
    v = 15;                 # m/s
    Cost = (16000*Elec_cap*P_rate/(ro*v*math.pi) +1197.2*math.sqrt(Elec_cap*P_rate/(ro*v*math.pi)) + 329)*D_inject
    
    Cost = Cost/(1+0.05)**9 # NPV from 2021 to 2030
    return Cost

def CAPEX_H2plant(Windfarm_size, day_hydro):

    P_H2_plant = Windfarm_size #MW
    Cost_electrolyser = 600 # k euro / MW
    Capex_elec = Cost_electrolyser*P_H2_plant;
    
    Cost_compress = 0.1724;     # keuro/(ton/day)
    Capex_compress = Cost_compress*day_hydro;
    
    Capex_h2plant = Capex_elec + Capex_compress;
    return Capex_h2plant, Capex_elec, Capex_compress

def OPEX_fun(Capex_windfarm, Capex_elec, Capex_compress, Capex_pipeline, Windfarm_size, lifetime, discount_rate):

    persent_wf = 3 # 3% of Capex_wf
    Opex_windfarm = persent_wf/100*Capex_windfarm;
    
    
    persent_elec = 2 #2% of electrolyser
    Opex_elec = persent_elec/100*Capex_elec;

    persent_compress = 6 #2% of compressor
    Opex_compress = persent_compress/100*Capex_compress;    
        
    persent_pipeline = 2 #2% of Capex_pipeline
    Opex_pipeline = persent_pipeline/100*Capex_pipeline
    
    Opex_annual = Opex_windfarm + Opex_elec + Opex_compress + Opex_pipeline;
    
    r = discount_rate/100
    Opex_total = 0
    for i in range(1,lifetime+1):
        tmp = Opex_annual/(1+r)**i
        Opex_total = Opex_total+tmp;
        
    Cost_stack = 150*Windfarm_size; # stack life time 12.5
    
    Opex_total = Opex_total + Cost_stack/(1+r)**12.5 + Cost_stack/(1+r)**25
    
    return Opex_total

def DECEX_fun(Capex_windfarm, Capex_h2plant, Capex_pipeline, lifetime, discount_rate):

    persent_wf = 5 # 3% of Capex_wf
    Decex_windfarm = persent_wf/100*Capex_windfarm;
    
    
    persent_h2plant = 2 #2% of Capex_h2plant
    Decex_h2plant = persent_h2plant/100*Capex_h2plant;
    

    
    Decex_total = Decex_windfarm + Decex_h2plant
    
    # Discount rate 5%
    r = discount_rate/100;
    Decex_project = Decex_total/(1+r)**lifetime
    
    return Decex_project

def findIndexnear (lat_grid,lon_grid,lat_point, lon_point):
    
    abslat = np.abs(lat_grid-lat_point)
    abslon= np.abs(lon_grid-lon_point)

    lat_id = np.argmin(abslat)
    lon_id = np.argmin(abslon)
    
    return lat_id, lon_id

def getdistance (num_point,lat_grid,lon_grid,lat_point, lon_point):
    
    tmp = [0]*num_point
    for i in range(num_point):
        lat2 = lat_grid[i]
        lon2 = lon_grid[i]
        tmp[i] = distance(lat_point, lat2, lon_point, lon2)
        
    D = min(tmp)
    return D

# Assumtion
Windfarm_size = 510; #      MW (34 turbine 15MW)
num_tur = 34;

life_time = 30;         # year
discount_rate = 5;      # %

water_depth = xr.open_dataset('gebco_cut.nc')
lat_wd = water_depth.lat.values
lon_wd = water_depth.lon.values

sea_port = pd.read_csv('List port check.csv')
num_port = len(sea_port)
lat_port = sea_port.lat.values;
lon_port = sea_port.lon.values

inject_point = pd.read_csv('List injection point.csv')
num_inject = len(inject_point)
lat_inject = inject_point.lat.values;
lon_inject = inject_point.lon.values

dco = xr.open_dataset('AHP_150m.nc')
num_lat = len(dco.lat)
num_lon = len(dco.lon)
print(num_lat)

ds= dco*0
ds=ds.rename({'AHP': 'LCOH'})

r = discount_rate/100

dco2 = dco*0
dco2 = dco2.rename({'AHP': 'Hytotal'})

for k in range(1,life_time+1):
    tmp1 = dco.AHP.values*1000  #kg
    tmp = tmp1/(1+r)**k         # kg
    dco2.Hytotal.values = dco2.Hytotal.values+tmp;


for i in range(num_lat):
    print(i)
    for j in range(num_lon):
        Hy_total = dco2.Hytotal[i,j]
        if math.isnan(Hy_total):
            continue
        
        lat_point = dco.lat[i].values
        lon_point = dco.lon[j].values

        lat_id, lon_id = findIndexnear(lat_wd,lon_wd,lat_point,lon_point)
        water_dp = -water_depth.z[lat_id,lon_id].values
        
        D_port = getdistance(num_port,lat_port,lon_port,lat_point,lon_point)

        D_inject = getdistance(num_inject,lat_inject,lon_inject,lat_point,lon_point)
        
        #
        Capex_windfarm = CAPEX_Windfarm(Windfarm_size, num_tur, water_dp, D_port, D_inject)
        
        day_hydro = Hy_total/365/1000;  # ton/day
        Capex_h2plant, Capex_elec, Capex_compress = CAPEX_H2plant(Windfarm_size, day_hydro)
        
        Capex_pipeline = CAPEX_pipeline(D_inject)

        CAPEX_project = Capex_windfarm + Capex_h2plant + Capex_pipeline;
        OPEX_project = OPEX_fun(Capex_windfarm, Capex_elec, Capex_compress, Capex_pipeline, Windfarm_size, life_time, discount_rate)
        DECEX_project = DECEX_fun(Capex_windfarm, Capex_h2plant, Capex_pipeline, life_time, discount_rate)
        total_cost = (CAPEX_project+OPEX_project+DECEX_project)*1000
             
    
        #print('total cost: ',total_cost)
        #print('Hydro: ', Hy_total)
        ds.LCOH[i,j] = total_cost/Hy_total

ds.to_netcdf('LCOH 2030 150.nc')
    