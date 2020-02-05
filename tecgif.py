#Plots all data for the day in gif form in both polar and cartesian coordinates
#Memory Heavy!
#Currently trying to reduce computing load while running this file so I can increase fig size

import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import gc
from PIL import Image

#Specify date here, 10/20/17 is already in the github repo, else download the date with hdf5_to_npz.py
year = '2017'
month = '10'
day = '20'



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

def plotter(Zm, time, lat, lon):
    uthour, utminute = timeconvert(time)
    plt.figure(figsize=(20, 15))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    
    #uncomment the following line for coastline projection 
    ax.coastlines()
    
    mesh = ax.pcolormesh(lon, lat, Zm, cmap='jet', vmax=30, transform=ccrs.PlateCarree()) 
    clrbar = plt.colorbar(mesh, shrink=0.5)
    clrbar.set_label('Total Electron Content (TECU)')
    plt.title("TEC for " + month + "/" + day + "/" + year + " at " + uthour + ':' + utminute +' UT')
    plt.savefig(str(time) + '.png', format="png", bbox_inches = 'tight')#saves figure as png
    
    #uncomment to show plot in IDE
    #plt.show()
    
    gc.collect()
    plt.close()


with np.load(year + month + day + '.npz') as data:
    tec = data['tec']
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)
    images = []
    time = 0
    while time < 288:
        Z = tec[:,:,time]        
        Zm = ma.masked_where(np.isnan(Z),Z)#masks NaNs to display as white on plot
        del Z#Hoping to save a little memory
        plotter(Zm, time, lat, lon)
        del Zm
        images.append(Image.open(str(time) + '.png'))
        
        
        time = time + 1
        
    images[0].save('tec1.gif',save_all=True, append_images=images[1:], optimize=True)
    del images
    i = 0
    while i < 288:
        os.remove(str(i) + '.png')
        i = i + 1
