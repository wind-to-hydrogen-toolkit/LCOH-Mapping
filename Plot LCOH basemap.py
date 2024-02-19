# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 11:51:06 2022

@author: quang
"""

import pandas as pd
import string, os, sys
import netCDF4
import matplotlib.pyplot as plt
from wrf import to_np, getvar, smooth2d, get_basemap, latlon_coords
import numpy as np
from mpl_toolkits.basemap import Basemap
import xarray as xr
sys.path.append('../common/')
#from common import *
import cartopy.crs as ccrs
import matplotlib as mpl
import shapefile

def findIndexnear (lat_grid,lon_grid,lat_point, lon_point):
    
    abslat = np.abs(lat_grid-lat_point)
    abslon= np.abs(lon_grid-lon_point)

    lat_id = np.argmin(abslat)
    lon_id = np.argmin(abslon)
    
    return lat_id, lon_id

dco = xr.open_dataset('LCOH 150 2030.nc')

Ws =  dco.LCOH.values
x, y = dco.lon.values, dco.lat.values
fsize = (6,8.5)
fig  =  plt.figure(figsize=fsize)
clevs = np.arange(2,6,0.2)
ax    = plt.axes([0.1,0.15,0.8,0.8])

cmap = plt.get_cmap("Blues")#"jet")
norm = mpl.colors.BoundaryNorm(clevs, cmap.N)

m = Basemap(projection='merc',llcrnrlat=50.5,urcrnrlat=56.1,\
            #llcrnrlat=7,urcrnrlat=24,\
            #llcrnrlon=74,urcrnrlon=150,lat_ts=20,resolution='i')
        llcrnrlon=-12,urcrnrlon=-3.5,lat_ts=20,resolution='i')


m.drawcoastlines(linewidth=0.3)
m.drawcountries(linewidth=0.35)
m.fillcontinents(color='0.9',lake_color='1')#paleturquoise

# draw parallels
m.drawparallels(np.arange(50,56.2,1),linewidth=0,labels=[1,0,0,0],size=10)
# draw meridians
m.drawmeridians(np.arange(-12,-3,2),linewidth=0,labels=[0,0,0,1],size=10)
#m.readshapefile(shp,'hanoi')
xx, yy = np.meshgrid(dco.lon.values, dco.lat.values)
x, y  = m(xx, yy)
ax.contourf(x, y, Ws,levels = clevs,norm = mpl.colors.BoundaryNorm(clevs, cmap.N),cmap= cmap)
'''
df = pd.read_csv('sample point.csv')
lat_grid = dco.lat.values
lon_grid = dco.lon.values
j = 1
for i in range(len(df)):
    latst = df.lat[i];
    lonst = df.lon[i];
    lat_id, lon_id = findIndexnear(lat_grid,lon_grid,latst,lonst)
    x, y = m(lon_grid[lon_id], lat_grid[lat_id])
    plt.scatter(x, y,s=50 , alpha=1,zorder=5, color='r')
    plt.text(x,y,'Point '+str(j), fontsize = 10, color = 'k',weight = 'bold',zorder=5)
    j = j+1

'''

cb = mpl.colorbar.ColorbarBase(plt.axes([0.1, 0.17, 0.8,0.02]), 
                            cmap=cmap,
                            norm = mpl.colors.BoundaryNorm(clevs, cmap.N),
                            orientation='horizontal',
                            #label='Wind speed (m/s)',fontsize=16,
                            #extend='both',
                            format='%.1f')
cb.ax.tick_params(labelsize=15)
cb.set_label(label='LCOH (€/kg)',fontsize=15)

plt.show()
#if not os.path.exists('fig'): os.makedirs('fig')
#fig.savefig('LCOH.png')
fig.savefig('LCOH 2030.svg', format = 'svg')
#fig.savefig('Figures/CF_datacorrection_2080_2099.png')

