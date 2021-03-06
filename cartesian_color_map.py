import os
import numpy as np

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from scipy.interpolate import griddata

#Specify date here, 10/20/17 is already in the github repo, else download the date with hdf5_to_npz.py
year = '2017'
month = '10'
day = '20'
time = 0#madrigal's time index, starts at 0 being 0:02UT and increments by 5 minutes
#range is 0-288 with 288 being 23:57 UT

#UT time conversion to displayable string
utminute = (time * 5) + 2
uthour = str(int(utminute / 60))
utminute = (utminute % 60)
if (utminute < 10):
    utminute = '0' + str(utminute)
else:
    utminute = str(utminute)
intfactor = 7 #number of points needed in 3x3x3 matrix surrounding a given point to be interpolated

def interpolate(X, tec, time, factor):
    for index in np.ndindex(X.shape):
        if np.isnan(X[index]):
            Y = tec[(index[0] - 1):(index[0] + 2), (index[1] - 1) : (index[1] + 2), time - 1: time + 2]
            if np.count_nonzero(~np.isnan(Y)) > factor:
                X[index] = np.nanmedian(Y)
    return X        
    
#actual plotting of TEC data
with np.load(year + month + day + '.npz') as data:
    tec = data['tec']
    dtec = data['dtec']

    Z = tec[:,:,time]
    Z = interpolate(Z, tec, time, intfactor)
    #Zm = ma.masked_where(np.isnan(Z),Z)#masks NaNs to display as white on plot
    
    
    
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)
    
    
    plt.figure(figsize=(11, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    
    #uncomment the following line for geographic projection (I'm not sure if it's accurate)
    ax.coastlines()
    Z = interpolate(Z, tec, time, 4)
    mesh = ax.pcolormesh(lon, lat, Z, cmap='jet', vmax=30)
    clrbar = plt.colorbar(mesh, shrink=0.5)
    clrbar.set_label('Total Electron Content (TECU)')

    plt.title('Global Total Electron Content for ' + month + '/' + day + '/' + year + ' at ' + uthour + ':' + utminute + ' UT')
    plt.show()
