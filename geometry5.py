# Created on 26.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creating the wing of the D45 Project at Akaflieg Darmstadt
# This file contains the python script for creating the geometry of the D45 Project wing

import numpy as np
#import pandas as pd



# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 5

# 2. The location of the profile from the wing root in mm
profile_x_cordinates = np.array([0.4005700570057006,4.435503550355036, 5.960356035603561, 6.907660766076608, 7.500220022002201])/1000.0     

# 3. The location of the profile from the wing root in mm
profile_y_cordinates = np.array([0.7342962755033171, 0.6084542900928411, 0.48261230468236516, 0.3567703192718892, 0.23092833386141318])/1000.0   

# 4. location to dat file for the airfoil profile
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing profiles 20240805/D45-1-132-15-F0-V6.csv',delimiter=',')
profile_2 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing profiles 20240805/D45-1-132-15-F0-V6.csv',delimiter=',')


#------------------------------------------------------------------------------------
# Pre calculations for the preparation of the CAD Model

# check if the input data is correct
if len(profile_x_cordinates) != n_profiles :
    raise Exception('The number of profiles and the locations for x cordinates do not match, Please check the input data !')
elif len(profile_y_cordinates) != n_profiles:
    raise Exception('The number of profiles and the locations for the y cordinates do not match. Please check the input data !')

profile_1_x_cordinates = profile_1[:,0]
profile_1_y_cordinates = profile_1[:,1]

profile_2_x_cordinates = profile_2[:,0]
profile_2_y_cordinates = profile_2[:,1]




#=======================================================================
#============ Geometry module Salome Meca ==============================
#=======================================================================
import sys
import salome
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New()
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

# creating the the points for the flute geometry from x and y_cordinate lists

for count,value in enumerate (profile_1_x_cordinates):
    globals()[f'Profile_1_point_{int(count+1)}'] = geompy.MakeVertex(profile_1_x_cordinates[count],profile_1_y_cordinates[count],0.0)
    #geompy.addToStudy(globals()[f'Profile_1_point_{int(count+1)}'],'Profile_1_point_'+str(count+1))

profile_1_all_lines = []
for count in range(1,len(profile_1_x_cordinates)):

    if count == len(profile_1_x_cordinates)-1:
        globals()[f'Profile_1_Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_1_point_{int(count)}'],globals()[f'Profile_1_point_{int(count+1)}'])
        #globals()[f'Profile_1_Line_{int(count+1)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_1_point_{int(count+1)}'],globals()[f'Profile_1_point_{int(1)}'])
        profile_1_all_lines.append(globals()[f'Profile_1_Line_{int(count)}'])
        #profile_1_all_lines.append(globals()[f'Profile_1_Line_{int(count+1)}'])
    else:
        globals()[f'Profile_1_Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_1_point_{int(count)}'],globals()[f'Profile_1_point_{int(count+1)}'])
        #geompy.addToStudy(globals()[f'Line_{int(count)}'],'Line_'+str(count))
        profile_1_all_lines.append(globals()[f'Profile_1_Line_{int(count)}'])

# Making the Fuse of all the lines
profile_1_line = geompy.MakeFuseList(profile_1_all_lines,True,True)
geompy.addToStudy(profile_1_line,'profile_1_line')

profile_1_wire = geompy.MakeWire(profile_1_all_lines)
geompy.addToStudy(profile_1_wire,'profile_1_wire')
 

for count,value in enumerate (profile_2_x_cordinates):
    globals()[f'Profile_2_point_{int(count+1)}'] = geompy.MakeVertex(profile_2_x_cordinates[count],profile_2_y_cordinates[count],4.0)
    #geompy.addToStudy(globals()[f'Profile_1_point_{int(count+1)}'],'Profile_1_point_'+str(count+1))

profile_2_all_lines = []
for count in range(1,len(profile_2_x_cordinates)):

    if count == len(profile_2_x_cordinates)-1:
        globals()[f'Profile_2_Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_2_point_{int(count)}'],globals()[f'Profile_2_point_{int(count+1)}'])
        #globals()[f'Profile_2_Line_{int(count+1)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_2_point_{int(count+1)}'],globals()[f'Profile_2_point_{int(1)}'])
        profile_2_all_lines.append(globals()[f'Profile_2_Line_{int(count)}'])
        #profile_2_all_lines.append(globals()[f'Profile_2_Line_{int(count+1)}'])
    else:
        globals()[f'Profile_2_Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f'Profile_2_point_{int(count)}'],globals()[f'Profile_2_point_{int(count+1)}'])
        #geompy.addToStudy(globals()[f'Line_{int(count)}'],'Line_'+str(count))
        profile_2_all_lines.append(globals()[f'Profile_2_Line_{int(count)}'])


# Making the Fuse of all the lines
profile_2_line = geompy.MakeFuseList(profile_2_all_lines,True,True)
geompy.addToStudy(profile_2_line,'profile_2_line')

profile_2_wire = geompy.MakeWire(profile_2_all_lines)
geompy.addToStudy(profile_2_wire,'profile_2_wire')
