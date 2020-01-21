#hdf5 download to numpy npz file format
#generates a 3d matrix for both tec and dtec for the day
#once zipped, should compress the full day to ~10 MB or so

import os
from madrigalWeb import *
import numpy

import h5py

url = "http://cedar.openmadrigal.org/"
username = "Ian Kelley"
email = "ikelley@vt.edu"
affiliation = "Virginia Tech"
instrument = 8000 #TEC instruments



startyear = '2017'
startmonth = '10'
startday = '20'
starthour = '0'
startmin = '0'
startsec = '0'


MadrigalData = MadrigalData(url)
experimentarray = MadrigalData.getExperiments(instrument, startyear, startmonth, startday, starthour, startmin, startsec, startyear, startmonth, startday, starthour, startmin, startsec, 1)

print("Downloading: ", startyear, startmonth, startday)
filearray = MadrigalData.getExperimentFiles(experimentarray[1].id, getNonDefault=False) #need to use index 1 since madrigal returns the previos day at index 0 
MadrigalData.downloadFile(filearray[0].name, '/home/ian/TEC/tempfile.hdf5', username, email, affiliation, format='hdf5')
print("raw hdf5 file downloaded successfully")

        


tempfilename = '/home/ian/TEC/tempfile.hdf5'

f = h5py.File( tempfilename, 'r')
data = f['Data']['Array Layout']['2D Parameters']
tec = data['tec']
dtec = data['dtec']

#numpy.save('tec', tec)
#numpy.save('dtec', dtec)
print("saving to compressed .npz file format")
numpy.savez_compressed(startyear + startmonth + startday + '.npz', tec=tec, dtec=dtec)

os.remove(tempfilename)
