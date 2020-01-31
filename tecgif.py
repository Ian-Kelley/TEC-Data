#Plots all data for the day in gif form in both polar and cartesian coordinates
#Memory Heavy!

import os
import numpy as np
import numpy.ma as ma
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import imageio
#Specify date here, 10/20/17 is already in the github repo, else download the date with hdf5_to_npz.py
year = '2017'
month = '10'
day = '20'
time = 0#madrigal's time index, starts at 0 being 0:02UT and increments by 5 minutes
#range is 0-288 with 288 being 23:57 UT


def timeconvert(time):
    #UT time conversion to displayable string
    utminute = (time * 5) + 2
    uthour = str(int(utminute / 60))
    utminute = (utminute % 60)
    if (utminute < 10):
        utminute = '0' + str(utminute)
    else:
        utminute = str(utminute)
    return uthour, utminute

def plotter(Zm, time):
    uthour, utminute = timeconvert(time)
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)
    ax0 = plt.subplot(2, 2, 1, projection=ccrs.Orthographic(0, 90))
    ax1 = plt.subplot(2, 2, 2, projection=ccrs.Orthographic(0, -90))
    ax3 = plt.subplot(2, 1, 2, projection=ccrs.PlateCarree())
    ax0.set_global()
    ax1.set_global()
    ax3.set_global()
    #uncomment the following line for coastline projection (I'm not sure if it's accurate)
    ax0.coastlines()
    ax1.coastlines()
    ax3.coastlines()
    ax0.pcolormesh(lon, lat, Zm, cmap='jet', vmax=30, transform=ccrs.PlateCarree())
    ax1.pcolormesh(lon, lat, Zm, cmap='jet', vmax=30, transform=ccrs.PlateCarree())
    ax3.pcolormesh(lon, lat, Zm, cmap='jet', vmax=30, transform=ccrs.PlateCarree())    
    plt.suptitle("TEC for " + month + "/" + day + "/" + year + " at " + uthour + ':' + utminute +' UT')
    plt.savefig(str(time) + '.png', format="png")


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
    images = []
    while time < 288:
        Z = tec[:,:,time]
        Zm = ma.masked_where(np.isnan(Z),Z)#masks NaNs to display as white on plot
    
        plotter(Zm, time)
        #cbar = plt.colorbar(shrink=0.5)
        #cbar.set_label('Total Electron Content (TECU)')
        images.append(imageio.imread(str(time) + '.png'))
        plt.close()
        os.remove(str(time)+'.png')
        time = time + 1
        
    imageio.mimsave('movie.gif', images)
