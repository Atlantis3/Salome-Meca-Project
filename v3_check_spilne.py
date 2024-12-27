#Created on 26.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creating the wing of the D45 Project at Akaflieg Darmstadt
# This file contains the python script for creating the geometry of the D45 Project wing

import numpy as np
#import pandas as pd



# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 6

# 2. The distance of the profile from the centreline of the fuselage in the direction of the wing tip in mm
wing_section_y_cordinates = np.array([0.35,2.1774,4.5496,6.0039,6.948,7.5])*-1000.0/2.0     

# 3. The distance of the profile leading edge from the wing root in the direction of the tariling edge in mm
wing_section_x_cordinates = np.array([0.0,0.014025,0.10489,0.214318,0.3234744,0.430468])*1000.0/2.0   
'''
wing_section_x_cordinates = [0]
for count,value in enumerate (wing_section_x_cordinates_uf):
    if count == 0:
        pass
    else :
        differance = wing_section_x_cordinates_uf[0]-value
        #print(value,differance)
        wing_section_x_cordinates.append(differance)
'''
#3.1 The length of the chordline of the profile in mm
wing_section_chord_length = np.array([0.7319,0.7154,0.6085,0.4826,0.3568,0.2309])*1000.0/2.0

# 4. location to dat file for the airfoil profile for 0 degree flap position
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-1-132-15-F10.csv',delimiter=',')
profile_2 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-2-132-15-F10.csv',delimiter=',')
profile_3 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-3-131-15-F10.csv',delimiter=',')
profile_4 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-4-129-155-F10.csv',delimiter=',')
profile_5 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-5-127-163-F10.csv',delimiter=',')
profile_6 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/new_flap_cordinates/D45-6-125-17-F10.csv',delimiter=',')


'''
# 4. location to dat file for the airfoil profile for 20 degree flap position
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-1-132-15-F20.csv',delimiter=',')
profile_2 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-2-132-15-F20.csv',delimiter=',')
profile_3 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-3-131-15-F20.csv',delimiter=',')
profile_4 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-4-129-155-F20.csv',delimiter=',')
profile_5 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-5-127-163-F20.csv',delimiter=',')
profile_6 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing Profiles 20241207/D45-6-125-17-F20.csv',delimiter=',')
'''





#------------------------------------------------------------------------------------
# Pre calculations for the preparation of the CAD Model

# check if the input data is correct
if len(wing_section_y_cordinates) != n_profiles :
    raise Exception('The number of profiles and the locations for it in the y-direction do not match, Please check the input data !')
elif len(wing_section_x_cordinates) != n_profiles:
    raise Exception('The number of profiles and the locations for it in the  x-direction do not match. Please check the input data !')

profile_1_x_cordinates = (profile_1[:,0]*wing_section_chord_length[0])+wing_section_x_cordinates[0]
profile_1_y_cordinates = profile_1[:,1]*wing_section_chord_length[0]

profile_2_x_cordinates = (profile_2[:,0]*wing_section_chord_length[1])+wing_section_x_cordinates[1]
profile_2_y_cordinates = profile_2[:,1]*wing_section_chord_length[1]
#profile_2_y_cordinates = (profile_2[:,1]*wing_section_chord_length[1])+0.2

profile_3_x_cordinates = (profile_3[:,0]*wing_section_chord_length[2])+wing_section_x_cordinates[2]
profile_3_y_cordinates = (profile_3[:,1]*wing_section_chord_length[2])
#profile_3_y_cordinates = (profile_3[:,1]*wing_section_chord_length[2])-0.2

profile_4_x_cordinates = (profile_4[:,0]*wing_section_chord_length[3])+wing_section_x_cordinates[3]
profile_4_y_cordinates = profile_4[:,1]*wing_section_chord_length[3]

profile_5_x_cordinates = (profile_5[:,0]*wing_section_chord_length[4])+wing_section_x_cordinates[4]
profile_5_y_cordinates = profile_5[:,1]*wing_section_chord_length[4]

profile_6_x_cordinates = (profile_6[:,0]*wing_section_chord_length[5])+wing_section_x_cordinates[5]
profile_6_y_cordinates = profile_6[:,1]*wing_section_chord_length[5]






profile_1_point_1_cut = [min(profile_1_x_cordinates),profile_1_y_cordinates[profile_1_x_cordinates.argmin()],wing_section_y_cordinates[0]]
profile_1_point_2_cut = [wing_section_chord_length[0]*0.32,profile_1_y_cordinates.max()-((profile_1_y_cordinates.max()-profile_1_y_cordinates.min())/2.0),wing_section_y_cordinates[0]]
profile_1_point_3_cut = [profile_1_x_cordinates[0],profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0),wing_section_y_cordinates[0]]

profile_2_point_1_cut = [min(profile_2_x_cordinates),profile_2_y_cordinates[profile_2_x_cordinates.argmin()],wing_section_y_cordinates[1]]
profile_2_point_2_cut = [wing_section_chord_length[1]*0.32,profile_2_y_cordinates.max()-((profile_2_y_cordinates.max()-profile_2_y_cordinates.min())/2.0),wing_section_y_cordinates[1]]
profile_2_point_3_cut = [profile_2_x_cordinates[0],profile_2_y_cordinates[0]-((profile_2_y_cordinates[0]-profile_2_y_cordinates[-1])/2.0),wing_section_y_cordinates[1]]



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
profile_1_all_points = []
for count,value in enumerate (profile_1_x_cordinates):
    globals()[f'Profile_1_Point_{int(count+1)}'] = geompy.MakeVertex(profile_1_x_cordinates[count],profile_1_y_cordinates[count],wing_section_y_cordinates[0])
    profile_1_all_points.append(globals()[f'Profile_1_Point_{int(count+1)}'])
    
profile_1_polyline = geompy.MakePolyline(profile_1_all_points,True)
geompy.addToStudy(profile_1_polyline,'profile_1_polyline')

profile_1_face = geompy.MakeFaceWires([profile_1_polyline], 1)
geompy.addToStudy(profile_1_face,'profile_1_face')


# spline cordinates
s_x_cordinates = [8,4,2,0,2,4,8]
s_y_cordinates = [4,3,2,0,-2,-3,-4]

spline_all_points = []
for count,value in enumerate(s_x_cordinates):
    globals()[f'spline_point_{int(count+1)}'] = geompy.MakeVertex(s_x_cordinates[count],s_y_cordinates[count],0)
    geompy.addToStudy(globals()[f'spline_point_{int(count+1)}'],'spline_point_'+str(count))
    spline_all_points.append(globals()[f'spline_point_{int(count+1)}'])

spline = geompy.MakeBezier(spline_all_points,theName='spline')
