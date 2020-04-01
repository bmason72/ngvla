#
# ngVLA core / SBA / TP time ratio calculation
#
#  1apr2020 bsm
#  also requires timeRatios.py at https://github.com/bmason72/casapy
#     --> 3f9cf6c3f3f07a1dc34d8156062ec4e5ca35b1e0 used for this calculation
#

import numpy as np
import timeRatios as tr

#
# set the configs; the dish diameters; and the beam_ind values (which index in the beam uv taper array to use)
#  nominally the uv taper array has the tapers to match cfg1 with cfg2 
#  always check the files' coord system cannot be geodetic=XYZ. note "loc" below is just to avoid CASA using
#   canned configs it does not denote LOC(al tangent plane) projection.
#  
cfg_pair = [ {'cfgA': 'ngvla-sba-revC_loc-utm', 'dA': 6.0, 'cfgB':'tp','dB': 18.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':1},
             {'cfgA': 'ngvla-core-revC_loc-utm', 'dA': 18.0, 'cfgB':'ngvla-sba-revC_loc-utm','dB': 6.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2},
             {'cfgA': 'ngvla-core-revB-utm', 'dA': 18.0, 'cfgB':'ngvla-sba-revB-utm','dB': 6.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2},
             {'cfgA': 'SWcore-utm', 'dA': 18.0, 'cfgB':'ngvla-sba-revC_loc-utm','dB': 6.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2}]

# null taper, TP, 7m, c43-1 -- etc. @ 100 GHz = 0.003 m
beams = np.array([0.00001,42.8,10.6,0.5])
lam = 0.003

# ALMA test case TP, 7m, c43-1 -- etc. @ 100 GHz = 0.003 m
#beams = np.array([0.00000001,60.0,12.5,3.38,2.3,1.42,0.918,0.545,0.306,0.211,0.096,0.056,0.042])
#cfg_pair = [ {'cfgA': 'alma.cycle7.1', 'dA': 12.0, 'cfgB':'aca.cycle7','dB': 7.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2},
#             {'cfgA': 'alma.cycle7.2', 'dA': 12.0, 'cfgB':'aca.cycle7','dB': 7.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2},
#             {'cfgA': 'alma.cycle7.3', 'dA': 12.0, 'cfgB':'aca.cycle7','dB': 7.0, 'tptg': 0.0, 'tmos': 0.0, 'nb1': 0.0, 'nb2': 0.0,'bmind':2}]

##########

uvtapers = tr.arcsec2uv(beams, lam = lam)

print "*** Results with double taper (for comparison):"             
tr.runTimeRatios(uvtapers,cfg_pair,usenull=False)

print "*** Results without double taper (use these!):"
tr.runTimeRatios(uvtapers,cfg_pair,usenull=True)

#
# RESULTS
#*** Results with double taper (for comparison):
#cfg1   cfg2   t2/t1(perPtg)   t2/t1(mosaic)    nb1   nb2
# CAUTION: tp times are for a single antenna
#ngvla-sba-revC_loc-utm tp 0.776474597593 6.98827137833 31.4472212025 0.5
#ngvla-core-revC_loc-utm ngvla-sba-revC_loc-utm 12.1240671683 1.34711857425 19.5188016108 130.403676302
#ngvla-core-revB-utm ngvla-sba-revB-utm 12.1240671683 1.34711857425 19.5188016108 130.403676302
#SWcore-utm ngvla-sba-revC_loc-utm 25.0355064305 2.78172293673 40.3052108226 130.403676302
#
#*** Results without double taper (use these!):
#cfg1   cfg2   t2/t1(perPtg)   t2/t1(mosaic)    nb1   nb2
# CAUTION: tp times are for a single antenna
#ngvla-sba-revC_loc-utm tp 0.776474597593 6.98827137833 31.4472212025 0.5
#ngvla-core-revC_loc-utm ngvla-sba-revC_loc-utm 9.24574813144 1.02730534794 19.5188016108 171.0
#ngvla-core-revB-utm ngvla-sba-revB-utm 9.24574813144 1.02730534794 19.5188016108 171.0
#SWcore-utm ngvla-sba-revC_loc-utm 19.0919419686 2.1213268854 40.3052108226 171.0
#
# For mosaics:
#
#  t_TP(N=4)/t_SBA   1.75
#  t_SBA/t_core      1.03
#
# Per pointing (better since you can scale it to actual map sizes)
#  t_TP(N=4)/t_SBA   0.19
#  t_SBA/t_core      9.25
#

