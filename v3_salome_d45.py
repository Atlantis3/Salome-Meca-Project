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
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-1-132-15-trim_straight_te.csv',delimiter=',')
profile_2 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-2-132-15-trim_straight_te.csv',delimiter=',')
profile_3 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-3-131-15-trim_straight_te.csv',delimiter=',')
profile_4 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-4-129-155-trim_straight_te.csv',delimiter=',')
profile_5 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-5-127-163-trim_straight_te.csv',delimiter=',')
profile_6 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-6-125-17-trim_straight_te.csv',delimiter=',')


# 5. the dimensions for the foam in mm
foam_length = 2000 
foam_width = 625
foam_thickness = 80




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


# profile2
profile_2_all_points = []
for count,value in enumerate (profile_2_x_cordinates):
    globals()[f'Profile_2_Point_{int(count+1)}'] = geompy.MakeVertex(profile_2_x_cordinates[count],profile_2_y_cordinates[count],wing_section_y_cordinates[1])
    profile_2_all_points.append(globals()[f'Profile_2_Point_{int(count+1)}'])
    
profile_2_polyline = geompy.MakePolyline(profile_2_all_points,True)
geompy.addToStudy(profile_2_polyline,'profile_2_polyline')

profile_2_face = geompy.MakeFaceWires([profile_2_polyline], 1)
geompy.addToStudy(profile_2_face,'profile_2_face')


# profile3
profile_3_all_points = []
for count,value in enumerate (profile_3_x_cordinates):
    globals()[f'Profile_3_Point_{int(count+1)}'] = geompy.MakeVertex(profile_3_x_cordinates[count],profile_3_y_cordinates[count],wing_section_y_cordinates[2])
    profile_3_all_points.append(globals()[f'Profile_3_Point_{int(count+1)}'])
    
profile_3_polyline = geompy.MakePolyline(profile_3_all_points,True)
geompy.addToStudy(profile_3_polyline,'profile_3_polyline')

profile_3_face = geompy.MakeFaceWires([profile_3_polyline], 1)
geompy.addToStudy(profile_3_face,'profile_3_face')

# profile4
profile_4_all_points = []
for count,value in enumerate (profile_4_x_cordinates):
    globals()[f'Profile_4_Point_{int(count+1)}'] = geompy.MakeVertex(profile_4_x_cordinates[count],profile_4_y_cordinates[count],wing_section_y_cordinates[3])
    profile_4_all_points.append(globals()[f'Profile_4_Point_{int(count+1)}'])
    
profile_4_polyline = geompy.MakePolyline(profile_4_all_points,True)
geompy.addToStudy(profile_4_polyline,'profile_4_polyline')

profile_4_face = geompy.MakeFaceWires([profile_4_polyline], 1)
geompy.addToStudy(profile_4_face,'profile_4_face')



# profile5
profile_5_all_points = []
for count,value in enumerate (profile_5_x_cordinates):
    globals()[f'Profile_5_Point_{int(count+1)}'] = geompy.MakeVertex(profile_5_x_cordinates[count],profile_5_y_cordinates[count],wing_section_y_cordinates[4])
    profile_5_all_points.append(globals()[f'Profile_5_Point_{int(count+1)}'])
    
profile_5_polyline = geompy.MakePolyline(profile_5_all_points,True)
geompy.addToStudy(profile_5_polyline,'profile_5_polyline')

profile_5_face = geompy.MakeFaceWires([profile_5_polyline], 1)
geompy.addToStudy(profile_5_face,'profile_5_face')


# profile6
profile_6_all_points = []
for count,value in enumerate (profile_6_x_cordinates):
    globals()[f'Profile_6_Point_{int(count+1)}'] = geompy.MakeVertex(profile_6_x_cordinates[count],profile_6_y_cordinates[count],wing_section_y_cordinates[5])
    profile_6_all_points.append(globals()[f'Profile_6_Point_{int(count+1)}'])
    
profile_6_polyline = geompy.MakePolyline(profile_6_all_points,True)
geompy.addToStudy(profile_6_polyline,'profile_6_polyline')

profile_6_face = geompy.MakeFaceWires([profile_6_polyline], 1)
geompy.addToStudy(profile_6_face,'profile_6_face')

# create the wing
path_1 = geompy.MakePolyline([profile_1_all_points[0],profile_2_all_points[-1],profile_3_all_points[1],profile_4_all_points[1],profile_5_all_points[1],profile_6_all_points[1]])
#wing = geompy.MakePipeShellsWithoutPath([profile_1_face,profile_2_face,profile_3_face,profile_4_face,profile_5_face,profile_6_face],[profile_1_all_points[0],profile_2_all_points[0],profile_3_all_points[0],profile_4_all_points[0],profile_5_all_points[0],profile_6_all_points[0]])
wing = geompy.MakeThruSections([profile_1_polyline,profile_2_polyline,profile_3_polyline,profile_4_polyline,profile_5_polyline,profile_6_polyline],1,1e-8,1)

geompy.addToStudy(path_1,'path_1')
geompy.addToStudy(wing,'wing')

# create a trimmin box for making the flap side perfectly straight
trim_box_point_1 = geompy.MakeVertex(profile_1_x_cordinates[0]-1.5,profile_1_y_cordinates[0]+10.0,wing_section_y_cordinates[0])
trim_box_point_2 = geompy.MakeVertex(profile_1_x_cordinates[0]+20.0,profile_1_y_cordinates[0]-30.0,wing_section_y_cordinates[5])
trim_box_1 = geompy.MakeBoxTwoPnt(trim_box_point_1,trim_box_point_2)

#wing2 = geompy.MakeCut(wing, trim_box_1, checkSelfInte=True)
#geompy.addToStudy(wing,'wing')
#geompy.addToStudy(wing2,'wing2')
geompy.addToStudy(trim_box_1,'trim_box_1')


# calculate the overlapping distance
overlap_distance = abs(profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]-profile_1_y_cordinates[0])
box_full_thickness = (2*foam_thickness)-overlap_distance
box_dist_le = (foam_width-wing_section_chord_length[0])/2.0

le_x_profile1 = np.min(profile_1_x_cordinates)
le_y_profile1 = profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]
le_z_profile1 = wing_section_y_cordinates[0]


boxp1 = geompy.MakeVertex(le_x_profile1-box_dist_le,le_y_profile1-foam_thickness,le_z_profile1)
boxp2 = geompy.MakeVertex(le_x_profile1-box_dist_le+foam_width,le_y_profile1-foam_thickness+box_full_thickness,wing_section_y_cordinates[5])
foam = geompy.MakeBoxTwoPnt(boxp1, boxp2)
geompy.addToStudy(foam,'foam')

# cut the wing from the foam
foam_cut = geompy.MakeCut(foam, wing, checkSelfInte=True)
geompy.addToStudy(foam_cut,'foam_cut')


#create two points rectangles
y1_for_rect1 = profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]

rect1_point_00 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-100-box_dist_le,y1_for_rect1,wing_section_y_cordinates[0])
rect1_point_01 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-100-box_dist_le,y1_for_rect1,wing_section_y_cordinates[5])
rect1_point_1 = geompy.MakeVertex(np.min(profile_1_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[0])
rect1_point_2 = geompy.MakeVertex(np.min(profile_2_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[1])
rect1_point_3 = geompy.MakeVertex(np.min(profile_3_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[2])
rect1_point_4 = geompy.MakeVertex(np.min(profile_4_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[3])
rect1_point_5 = geompy.MakeVertex(np.min(profile_5_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[4])
rect1_point_6 = geompy.MakeVertex(np.min(profile_6_x_cordinates)+10,y1_for_rect1,wing_section_y_cordinates[5])




rect1_line1 = geompy.MakeLineTwoPnt(rect1_point_00,rect1_point_1)
rect1_line2 = geompy.MakeLineTwoPnt(rect1_point_1,rect1_point_2)
rect1_line3 = geompy.MakeLineTwoPnt(rect1_point_2,rect1_point_3)
rect1_line4 = geompy.MakeLineTwoPnt(rect1_point_3,rect1_point_4)
rect1_line5 = geompy.MakeLineTwoPnt(rect1_point_4,rect1_point_5)
rect1_line6 = geompy.MakeLineTwoPnt(rect1_point_5,rect1_point_6)
rect1_line7 = geompy.MakeLineTwoPnt(rect1_point_6,rect1_point_01)
rect1_line8 = geompy.MakeLineTwoPnt(rect1_point_01,rect1_point_00)

rect1 = geompy.MakeFaceWires([rect1_line1,rect1_line2,rect1_line3,rect1_line4,rect1_line5,rect1_line6,rect1_line7,rect1_line8],1)
geompy.addToStudy(rect1,'rect1')


# for rectangle 2
#create two points rectangles
rect2_point_1_x = (profile_1_x_cordinates[0]-((profile_1_x_cordinates[0]-profile_1_x_cordinates[-1])/2.0))+100.0+box_dist_le
rect2_point_1_y = profile_1_y_cordinates[0]-(abs((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0))
rect2_point_1_z = wing_section_y_cordinates[0]

rect2_point_2_x = (profile_1_x_cordinates[0]-((profile_1_x_cordinates[0]-profile_1_x_cordinates[-1])/2.0))
rect2_point_2_y = profile_1_y_cordinates[0]-(abs((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0))
rect2_point_2_z = wing_section_y_cordinates[0]

rect2_point_3_x = (profile_1_x_cordinates[0]-((profile_1_x_cordinates[0]-profile_1_x_cordinates[-1])/2.0))
rect2_point_3_y = profile_1_y_cordinates[0]-(abs((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0))
rect2_point_3_z = wing_section_y_cordinates[5]

rect2_point_4_x = (profile_1_x_cordinates[0]-((profile_1_x_cordinates[0]-profile_1_x_cordinates[-1])/2.0))+100.0+box_dist_le
rect2_point_4_y = profile_1_y_cordinates[0]-(abs((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0))
rect2_point_4_z = wing_section_y_cordinates[5]


rect2_point_1 = geompy.MakeVertex(rect2_point_1_x,rect2_point_1_y,rect2_point_1_z)
rect2_point_2 = geompy.MakeVertex(rect2_point_2_x,rect2_point_2_y,rect2_point_2_z)
rect2_point_3 = geompy.MakeVertex(rect2_point_3_x,rect2_point_3_y,rect2_point_3_z)
rect2_point_4 = geompy.MakeVertex(rect2_point_4_x,rect2_point_4_y,rect2_point_4_z)

rect2_line1 = geompy.MakeLineTwoPnt(rect2_point_1,rect2_point_2)
rect2_line2 = geompy.MakeLineTwoPnt(rect2_point_2,rect2_point_3)
rect2_line3 = geompy.MakeLineTwoPnt(rect2_point_3,rect2_point_4)
rect2_line4 = geompy.MakeLineTwoPnt(rect2_point_4,rect2_point_1)




rect2 = geompy.MakeFaceWires([rect2_line1,rect2_line2,rect2_line3,rect2_line4],0)
geompy.addToStudy(rect2,'rect2')

Partition_1 = geompy.MakePartition([foam_cut], [rect1, rect2])
geompy.addToStudy(Partition_1,'Partition_1')
[bottom_foam,upper_foam]= geompy.ExtractShapes(Partition_1, geompy.ShapeType["SOLID"], True)
geompy.addToStudy(bottom_foam,'bottom_foam')
geompy.addToStudy(upper_foam,'upper_foam')