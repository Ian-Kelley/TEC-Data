#initial attempt at plotting data from npz format using matplotlib
#this uses pcolormesh command, as opposed to contour or imshow
#(I thought this method looked the best of all of them)
#rectangular and polar plots generated

import os
import numpy as np
import numpy.ma as ma
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs

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


#actual plotting of TEC data
with np.load(year + month + day + '.npz') as data:
    tec = data['tec']
    dtec = data['dtec']
    Z = tec[:,:,time]
    Zm = ma.masked_where(np.isnan(Z),Z)#masks NaNs to display as white on plot
    
    
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)
    
    
    plt.figure(figsize=(11, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    
    #uncomment the following line for geographic projection (I'm not sure if it's accurate)
    #ax.coastlines()
    

    ax.pcolormesh(lon, lat, Zm, cmap='jet', vmax=30)
    plt.title('Global Total Electron Content for ' + month + '/' + day + '/' + year + ' at ' + uthour + ':' + utminute + ' UT')
    plt.show()
    

