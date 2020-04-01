#
# bsm 17apr18 - transform configuration files
#   from geocentric (XYZ) to UTM.
#  based on script from Alan Erickson
#
# This script only works for the specific UTM tile which is
#  hard wired below, basically, the vicinity of the current
#  VLA site.
#
# 1apr2020 - scripts for RevC config time ratio calculation
#

import pylab as pl
import pandas as pd
import pyproj

projEcef = pyproj.Proj("+proj=geocent")
projUtm  = pyproj.Proj("+proj=utm +zone=13 +north +datum=WGS84 +units=m +no_defs")

# **SET THIS BY HAND: note - leave off '.cfg' suffix, which is assumed present ->
#infile = 'ngvla-sba-revC_loc'
infile = 'ngvla-core-revC_loc'
#infile='SWcoreFake'

def add_utm(df):
  ecef = pyproj.transform(
    projEcef, projUtm, 
    x = df['x'].values, 
    y = df['y'].values, 
    z = df['z'].values
    )

  df['utm_x'] = ecef[0]
  df['utm_y'] = ecef[1]
  df['utm_z'] = ecef[2]

# assume two comment rows at start of file, and space separated columns ->
df=pd.read_csv(infile+'.cfg',names=['x','y','z','d','antName'],sep=' ',skiprows=2)
add_utm(df)
outfile=infile+'-utm.cfg'

with open(outfile, 'w') as f:
  f.write('# observatory=NGVLA\n')
  f.write('# coordsys=UTM\n')
  f.write('# datum=NAD27\n')
  f.write('# zone=13\n')
  f.write('# hemisphere=N\n')
  f.write('# Easting Northing el diam antName\n')

  df[['utm_x','utm_y','utm_z','d','antName']].to_csv(
    f, 
    float_format = '%.3f',
    header = False, 
    index = False,
    sep = ' '
    )

  
