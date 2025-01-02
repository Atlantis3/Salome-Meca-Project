# D45 Wing Design; Foambau ADP Winter semester 2024-25
import numpy as np
from math import atan2,sin,cos

# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 6

# 2. The distance of the profile from the centreline of the fuselage in the direction of the wing tip in mm
wing_section_y_cordinates = np.array([0.35,2.1774,4.5496,6.0039,6.948,7.5])*-1000.0/2.0     

# 3. The distance of the profile leading edge from the wing root in the direction of the tariling edge in mm
wing_section_x_cordinates = np.array([0.0,0.014025,0.10489,0.214318,0.3234744,0.430468])*1000.0/2.0   

# 4. The length of the chordline of the profile in mm
wing_section_chord_length = np.array([0.7319,0.7154,0.6085,0.4826,0.3568,0.2309])*1000.0/2.0

# 5. location to dat file for the airfoil profile for 0 degree flap position
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-1-132-15-trim_straight_te.csv',delimiter=',')
profile_2 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-2-132-15-trim_straight_te.csv',delimiter=',')
profile_3 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-3-131-15-trim_straight_te.csv',delimiter=',')
profile_4 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-4-129-155-trim_straight_te.csv',delimiter=',')
profile_5 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-5-127-163-trim_straight_te.csv',delimiter=',')
profile_6 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/straight_te_flap_trim_cordinates/D45-6-125-17-trim_straight_te.csv',delimiter=',')


# 6. the dimensions for the foam in mm
foam_length = 2000 
foam_width = 600
foam_thickness = 60

# 7. Resin Escape path dimensions in mm; The extar length of the wing that you want to create which would later be trimmmed after fabrication of the wing
resin_escape_length = 10.0

# 8. Fillet radius
fillet_radius = 2.0

# 9. Faom alignment cut in the leading edge 
foam_align_le_length = 20.0     # the length from the resin escape cut to the beginning of the alignment cut
faom_align_le_depth = 20.0      # the thickness of the cut in a single foam mold
foam_align_le_gap = 40.0        # the width of the cut or the gap in the cut

foam_align_te_length = 20.0
faom_align_te_depth = 20.0
foam_align_te_gap = 40.0


# 10. Helping foam mold in the Leading edge
helping_foam_mold_extra_length = 30.0   # the extra length of the helping foam mold from the alignment cut
helping_foam_mold_gap_p1 = 4.0          # the maximum gap between the helping foam mold and the upper foam mold for profile 1
helping_foam_mold_gap_p2 = 4.0          # the maximum gap between the helping foam mold and the upper foam mold for profile 2
helping_foam_mold_gap_p3 = 3.5          # the maximum gap between the helping foam mold and the upper foam mold for profile 3
helping_foam_mold_gap_p4 = 3.0          # the maximum gap between the helping foam mold and the upper foam mold for profile 4
helping_foam_mold_gap_p5 = 1.5          # the maximum gap between the helping foam mold and the upper foam mold for profile 5
helping_foam_mold_gap_p6 = 0.8          # the maximum gap between the helping foam mold and the upper foam mold for profile 6
helping_foam_mold_ratio = 0.10          # perecetange of chord length used for helping foam mold


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
#geompy.addToStudy(profile_1_polyline,'profile_1_polyline')

profile_1_face = geompy.MakeFaceWires([profile_1_polyline], 1)
geompy.addToStudy(profile_1_face,'profile_1_face')


# profile2
profile_2_all_points = []
for count,value in enumerate (profile_2_x_cordinates):
    globals()[f'Profile_2_Point_{int(count+1)}'] = geompy.MakeVertex(profile_2_x_cordinates[count],profile_2_y_cordinates[count],wing_section_y_cordinates[1])
    profile_2_all_points.append(globals()[f'Profile_2_Point_{int(count+1)}'])
    
profile_2_polyline = geompy.MakePolyline(profile_2_all_points,True)
#geompy.addToStudy(profile_2_polyline,'profile_2_polyline')

profile_2_face = geompy.MakeFaceWires([profile_2_polyline], 1)
geompy.addToStudy(profile_2_face,'profile_2_face')


# profile3
profile_3_all_points = []
for count,value in enumerate (profile_3_x_cordinates):
    globals()[f'Profile_3_Point_{int(count+1)}'] = geompy.MakeVertex(profile_3_x_cordinates[count],profile_3_y_cordinates[count],wing_section_y_cordinates[2])
    profile_3_all_points.append(globals()[f'Profile_3_Point_{int(count+1)}'])
    
profile_3_polyline = geompy.MakePolyline(profile_3_all_points,True)
#geompy.addToStudy(profile_3_polyline,'profile_3_polyline')

profile_3_face = geompy.MakeFaceWires([profile_3_polyline], 1)
geompy.addToStudy(profile_3_face,'profile_3_face')

# profile4
profile_4_all_points = []
for count,value in enumerate (profile_4_x_cordinates):
    globals()[f'Profile_4_Point_{int(count+1)}'] = geompy.MakeVertex(profile_4_x_cordinates[count],profile_4_y_cordinates[count],wing_section_y_cordinates[3])
    profile_4_all_points.append(globals()[f'Profile_4_Point_{int(count+1)}'])
    
profile_4_polyline = geompy.MakePolyline(profile_4_all_points,True)
#geompy.addToStudy(profile_4_polyline,'profile_4_polyline')

profile_4_face = geompy.MakeFaceWires([profile_4_polyline], 1)
geompy.addToStudy(profile_4_face,'profile_4_face')



# profile5
profile_5_all_points = []
for count,value in enumerate (profile_5_x_cordinates):
    globals()[f'Profile_5_Point_{int(count+1)}'] = geompy.MakeVertex(profile_5_x_cordinates[count],profile_5_y_cordinates[count],wing_section_y_cordinates[4])
    profile_5_all_points.append(globals()[f'Profile_5_Point_{int(count+1)}'])
    
profile_5_polyline = geompy.MakePolyline(profile_5_all_points,True)
#geompy.addToStudy(profile_5_polyline,'profile_5_polyline')

profile_5_face = geompy.MakeFaceWires([profile_5_polyline], 1)
geompy.addToStudy(profile_5_face,'profile_5_face')


# profile6
profile_6_all_points = []
for count,value in enumerate (profile_6_x_cordinates):
    globals()[f'Profile_6_Point_{int(count+1)}'] = geompy.MakeVertex(profile_6_x_cordinates[count],profile_6_y_cordinates[count],wing_section_y_cordinates[5])
    profile_6_all_points.append(globals()[f'Profile_6_Point_{int(count+1)}'])
    
profile_6_polyline = geompy.MakePolyline(profile_6_all_points,True)
#geompy.addToStudy(profile_6_polyline,'profile_6_polyline')

profile_6_face = geompy.MakeFaceWires([profile_6_polyline], 1)
geompy.addToStudy(profile_6_face,'profile_6_face')

# create the wing
wing = geompy.MakeThruSections([profile_1_polyline,profile_2_polyline,profile_3_polyline,profile_4_polyline,profile_5_polyline,profile_6_polyline],1,1e-8,1)
geompy.addToStudy(wing,'wing')




# calculate the overlapping distance and create the foam
overlap_distance = abs(profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]-(profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0)))
box_full_thickness = (2*foam_thickness)-overlap_distance
box_dist_le = (foam_width-wing_section_chord_length[0])/2.0

le_x_profile1 = np.min(profile_1_x_cordinates)
le_y_profile1 = profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]
le_z_profile1 = wing_section_y_cordinates[0]


boxp1 = geompy.MakeVertex(le_x_profile1-box_dist_le,le_y_profile1-foam_thickness,le_z_profile1)
boxp2 = geompy.MakeVertexWithRef(boxp1,foam_width,box_full_thickness,wing_section_y_cordinates[5]-wing_section_y_cordinates[0])
foam = geompy.MakeBoxTwoPnt(boxp1, boxp2)
#geompy.addToStudy(foam,'foam')

# cut the wing from the foam
foam_cut = geompy.MakeCut(foam, wing, checkSelfInte=True)
#geompy.addToStudy(foam_cut,'foam_cut')


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
#geompy.addToStudy(rect1,'rect1')


# Partition the foam into two parts
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
#geompy.addToStudy(rect2,'rect2')

Partition_1 = geompy.MakePartition([foam_cut], [rect1, rect2])
#geompy.addToStudy(Partition_1,'Partition_1')
[bottom_foam,upper_foam]= geompy.ExtractShapes(Partition_1, geompy.ShapeType["SOLID"], True)



# create the resin escape path at the trailing edge of the foam

# For the profile 1
resin_escape_1_point_1 = geompy.MakeVertex(profile_1_x_cordinates[-1],profile_1_y_cordinates[-1],wing_section_y_cordinates[0])
resin_escape_1_point_2 = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length,profile_1_y_cordinates[-1],wing_section_y_cordinates[0])
resin_escape_1_point_3 = geompy.MakeVertex(profile_1_x_cordinates[0]+resin_escape_length,profile_1_y_cordinates[0],wing_section_y_cordinates[0])
resin_escape_1_point_4 = geompy.MakeVertex(profile_1_x_cordinates[0],profile_1_y_cordinates[0],wing_section_y_cordinates[0])

resin_escape_1_polyline = geompy.MakePolyline([resin_escape_1_point_1,resin_escape_1_point_2,resin_escape_1_point_3,resin_escape_1_point_4],True)


# For the profile 2
resin_escape_2_point_1 = geompy.MakeVertex(profile_2_x_cordinates[-1],profile_2_y_cordinates[-1],wing_section_y_cordinates[1])
resin_escape_2_point_2 = geompy.MakeVertex(profile_2_x_cordinates[-1]+resin_escape_length,profile_2_y_cordinates[-1],wing_section_y_cordinates[1])
resin_escape_2_point_3 = geompy.MakeVertex(profile_2_x_cordinates[0]+resin_escape_length,profile_2_y_cordinates[0],wing_section_y_cordinates[1])
resin_escape_2_point_4 = geompy.MakeVertex(profile_2_x_cordinates[0],profile_2_y_cordinates[0],wing_section_y_cordinates[1])

resin_escape_2_polyline = geompy.MakePolyline([resin_escape_2_point_1,resin_escape_2_point_2,resin_escape_2_point_3,resin_escape_2_point_4],True)


# For the profile 3
resin_escape_3_point_1 = geompy.MakeVertex(profile_3_x_cordinates[-1],profile_3_y_cordinates[-1],wing_section_y_cordinates[2])
resin_escape_3_point_2 = geompy.MakeVertex(profile_3_x_cordinates[-1]+resin_escape_length,profile_3_y_cordinates[-1],wing_section_y_cordinates[2])
resin_escape_3_point_3 = geompy.MakeVertex(profile_3_x_cordinates[0]+resin_escape_length,profile_3_y_cordinates[0],wing_section_y_cordinates[2])
resin_escape_3_point_4 = geompy.MakeVertex(profile_3_x_cordinates[0],profile_3_y_cordinates[0],wing_section_y_cordinates[2])

resin_escape_3_polyline = geompy.MakePolyline([resin_escape_3_point_1,resin_escape_3_point_2,resin_escape_3_point_3,resin_escape_3_point_4],True)


# For the profile 4
resin_escape_4_point_1 = geompy.MakeVertex(profile_4_x_cordinates[-1],profile_4_y_cordinates[-1],wing_section_y_cordinates[3])
resin_escape_4_point_2 = geompy.MakeVertex(profile_4_x_cordinates[-1]+resin_escape_length,profile_4_y_cordinates[-1],wing_section_y_cordinates[3])
resin_escape_4_point_3 = geompy.MakeVertex(profile_4_x_cordinates[0]+resin_escape_length,profile_4_y_cordinates[0],wing_section_y_cordinates[3])
resin_escape_4_point_4 = geompy.MakeVertex(profile_4_x_cordinates[0],profile_4_y_cordinates[0],wing_section_y_cordinates[3])

resin_escape_4_polyline = geompy.MakePolyline([resin_escape_4_point_1,resin_escape_4_point_2,resin_escape_4_point_3,resin_escape_4_point_4],True)


# For the profile 5
resin_escape_5_point_1 = geompy.MakeVertex(profile_5_x_cordinates[-1],profile_5_y_cordinates[-1],wing_section_y_cordinates[4])
resin_escape_5_point_2 = geompy.MakeVertex(profile_5_x_cordinates[-1]+resin_escape_length,profile_5_y_cordinates[-1],wing_section_y_cordinates[4])
resin_escape_5_point_3 = geompy.MakeVertex(profile_5_x_cordinates[0]+resin_escape_length,profile_5_y_cordinates[0],wing_section_y_cordinates[4])
resin_escape_5_point_4 = geompy.MakeVertex(profile_5_x_cordinates[0],profile_5_y_cordinates[0],wing_section_y_cordinates[4])

resin_escape_5_polyline = geompy.MakePolyline([resin_escape_5_point_1,resin_escape_5_point_2,resin_escape_5_point_3,resin_escape_5_point_4],True)

# For the profile 6
resin_escape_6_point_1 = geompy.MakeVertex(profile_6_x_cordinates[-1],profile_6_y_cordinates[-1],wing_section_y_cordinates[5])
resin_escape_6_point_2 = geompy.MakeVertex(profile_6_x_cordinates[-1]+resin_escape_length,profile_6_y_cordinates[-1],wing_section_y_cordinates[5])
resin_escape_6_point_3 = geompy.MakeVertex(profile_6_x_cordinates[0]+resin_escape_length,profile_6_y_cordinates[0],wing_section_y_cordinates[5])
resin_escape_6_point_4 = geompy.MakeVertex(profile_6_x_cordinates[0],profile_6_y_cordinates[0],wing_section_y_cordinates[5])

resin_escape_6_polyline = geompy.MakePolyline([resin_escape_6_point_1,resin_escape_6_point_2,resin_escape_6_point_3,resin_escape_6_point_4],True)

# make the resin escape solid
resin_escape_solid = geompy.MakeThruSections([resin_escape_1_polyline,resin_escape_2_polyline,resin_escape_3_polyline,resin_escape_4_polyline,resin_escape_5_polyline,resin_escape_6_polyline],1,1e-8,1)

# remove the material from the bottom foam
bottom_foam = geompy.MakeCut(bottom_foam, resin_escape_solid, checkSelfInte=True)


upper_foam = geompy.MakeCut(upper_foam, resin_escape_solid, checkSelfInte=True)


# create a cylinder to make the fillet in the bottom foam
cyl_resin_escape_bf_point = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length-fillet_radius,profile_1_y_cordinates[-1],wing_section_y_cordinates[0]+10.0)
cyl_resin_escape_bf_axis = geompy.MakeLineTwoPnt(cyl_resin_escape_bf_point,geompy.MakeVertex(profile_6_x_cordinates[-1]+resin_escape_length-fillet_radius,profile_6_y_cordinates[-1],wing_section_y_cordinates[5]))
cylinder_bf_resin_escape = geompy.MakeCylinder(cyl_resin_escape_bf_point, cyl_resin_escape_bf_axis, fillet_radius, wing_section_y_cordinates[0]-wing_section_y_cordinates[5]+100.0)
#geompy.addToStudy(cylinder_bf_resin_escape,'cylinder_bf_resin_escape')
bottom_foam = geompy.MakeCut(bottom_foam, cylinder_bf_resin_escape, checkSelfInte=True)



# create a cylinder to make the fillet in the upper foam
cyl_resin_escape_uf_point = geompy.MakeVertex(profile_1_x_cordinates[0]+resin_escape_length-fillet_radius,profile_1_y_cordinates[0],wing_section_y_cordinates[0]+10.0)
cyl_resin_escape_uf_axis = geompy.MakeLineTwoPnt(cyl_resin_escape_uf_point,geompy.MakeVertex(profile_6_x_cordinates[0]+resin_escape_length-fillet_radius,profile_6_y_cordinates[0],wing_section_y_cordinates[5]))


c_uf_re_c_1_point = geompy.MakeVertex(profile_1_x_cordinates[0]+resin_escape_length-fillet_radius,profile_1_y_cordinates[0],wing_section_y_cordinates[0])
c_uf_re_c_2_point = geompy.MakeVertex(profile_2_x_cordinates[0]+resin_escape_length-fillet_radius,profile_2_y_cordinates[0],wing_section_y_cordinates[1])
c_uf_re_c_3_point = geompy.MakeVertex(profile_3_x_cordinates[0]+resin_escape_length-fillet_radius,profile_3_y_cordinates[0],wing_section_y_cordinates[2])
c_uf_re_c_4_point = geompy.MakeVertex(profile_4_x_cordinates[0]+resin_escape_length-fillet_radius,profile_4_y_cordinates[0],wing_section_y_cordinates[3])
c_uf_re_c_5_point = geompy.MakeVertex(profile_5_x_cordinates[0]+resin_escape_length-fillet_radius,profile_5_y_cordinates[0],wing_section_y_cordinates[4])
c_uf_re_c_6_point = geompy.MakeVertex(profile_6_x_cordinates[0]+resin_escape_length-fillet_radius,profile_6_y_cordinates[0],wing_section_y_cordinates[5])




c_uf_re_c_1_vector = geompy.MakeLineTwoPnt(c_uf_re_c_1_point,c_uf_re_c_2_point)
c_uf_re_c_2_vector = geompy.MakeLineTwoPnt(c_uf_re_c_2_point,c_uf_re_c_3_point)
c_uf_re_c_3_vector = geompy.MakeLineTwoPnt(c_uf_re_c_3_point,c_uf_re_c_4_point)
c_uf_re_c_4_vector = geompy.MakeLineTwoPnt(c_uf_re_c_4_point,c_uf_re_c_5_point)
c_uf_re_c_5_vector = geompy.MakeLineTwoPnt(c_uf_re_c_5_point,c_uf_re_c_6_point)
c_uf_re_c_6_vector = geompy.MakeLineTwoPnt(c_uf_re_c_6_point,c_uf_re_c_1_point)





cyl_uf_resin_escape_circle_1 = geompy.MakeCircle(c_uf_re_c_1_point,c_uf_re_c_1_vector,fillet_radius)
cyl_uf_resin_escape_circle_2 = geompy.MakeCircle(c_uf_re_c_2_point,c_uf_re_c_2_vector,fillet_radius)
cyl_uf_resin_escape_circle_3 = geompy.MakeCircle(c_uf_re_c_3_point,c_uf_re_c_3_vector,fillet_radius)
cyl_uf_resin_escape_circle_4 = geompy.MakeCircle(c_uf_re_c_4_point,c_uf_re_c_4_vector,fillet_radius)
cyl_uf_resin_escape_circle_5 = geompy.MakeCircle(c_uf_re_c_5_point,c_uf_re_c_5_vector,fillet_radius)
cyl_uf_resin_escape_circle_6 = geompy.MakeCircle(c_uf_re_c_6_point,c_uf_re_c_6_vector,fillet_radius)




cylinder_uf_resin_escape = geompy.MakeCylinder(cyl_resin_escape_uf_point, cyl_resin_escape_uf_axis, fillet_radius, wing_section_y_cordinates[0]-wing_section_y_cordinates[5]+100.0)
upper_foam = geompy.MakeCut(upper_foam, cylinder_uf_resin_escape, checkSelfInte=True)







# create the cuts for the foam alignment for the tip and the bottom foam and also in the y_direction of the workbench
foam_align_le_point_1 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-foam_align_le_length,profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]-faom_align_le_depth,wing_section_y_cordinates[0]+10.0)
foam_align_le_point_2 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-foam_align_le_length,profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]+faom_align_le_depth,wing_section_y_cordinates[0]+10.0)
foam_align_le_point_3 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-foam_align_le_length-foam_align_le_gap,profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]-faom_align_le_depth,wing_section_y_cordinates[0]+10.0)
foam_align_le_point_4 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-foam_align_le_length-foam_align_le_gap,profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]+faom_align_le_depth,wing_section_y_cordinates[0]+10.0)

foam_align_le_polyline = geompy.MakePolyline([foam_align_le_point_1,foam_align_le_point_2,foam_align_le_point_4,foam_align_le_point_3],True)
foam_align_le_face = geompy.MakeFaceWires([foam_align_le_polyline],True)

foam_align_le = geompy.MakePrismVecH(foam_align_le_face, OZ, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)
#geompy.addToStudy(foam_align_le,'foam_align_le')

bottom_foam = geompy.MakeCut(bottom_foam, foam_align_le, checkSelfInte=True)


upper_foam = geompy.MakeCut(upper_foam, foam_align_le, checkSelfInte=True)




# create the cuts for the foam alignment for the tip and the bottom foam and also in the y_direction of the workbench
foam_align_te_point_1 = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length+foam_align_te_length,profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0)-faom_align_te_depth,wing_section_y_cordinates[0]+10.0)
foam_align_te_point_2 = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length+foam_align_te_length,profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0)+faom_align_te_depth,wing_section_y_cordinates[0]+10.0)
foam_align_te_point_3 = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length+foam_align_te_length+foam_align_te_gap,profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0)+faom_align_te_depth,wing_section_y_cordinates[0]+10.0)
foam_align_te_point_4 = geompy.MakeVertex(profile_1_x_cordinates[-1]+resin_escape_length+foam_align_te_length+foam_align_te_gap,profile_1_y_cordinates[0]-((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0)-faom_align_te_depth,wing_section_y_cordinates[0]+10.0)

foam_align_te_polyline = geompy.MakePolyline([foam_align_te_point_1,foam_align_te_point_2,foam_align_te_point_3,foam_align_te_point_4],True)
foam_align_te_face = geompy.MakeFaceWires([foam_align_te_polyline],True)

foam_align_te = geompy.MakePrismVecH(foam_align_te_face, OZ, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)


bottom_foam = geompy.MakeCut(bottom_foam, foam_align_te, checkSelfInte=True)


upper_foam = geompy.MakeCut(upper_foam, foam_align_te, checkSelfInte=True)



# create the cylinders for the fillet in the foam alignment gaps in the leading edge and trailing edge

cyl_le_uf_1_point = geompy.MakeVertexWithRef(foam_align_le_point_4, fillet_radius,0,0)
cyl_le_uf_1 = geompy.MakeCylinder(cyl_le_uf_1_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_le_uf_2_point = geompy.MakeVertexWithRef(foam_align_le_point_2, -fillet_radius,0,0)
cyl_le_uf_2 = geompy.MakeCylinder(cyl_le_uf_2_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_le_lf_1_point = geompy.MakeVertexWithRef(foam_align_le_point_3, fillet_radius,0,0)
cyl_le_lf_1 = geompy.MakeCylinder(cyl_le_lf_1_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_le_lf_2_point = geompy.MakeVertexWithRef(foam_align_le_point_1, -fillet_radius,0,0)
cyl_le_lf_2 = geompy.MakeCylinder(cyl_le_lf_2_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

# for the trailing edge
cyl_te_uf_1_point = geompy.MakeVertexWithRef(foam_align_te_point_2, fillet_radius,0,0)
cyl_te_uf_1 = geompy.MakeCylinder(cyl_te_uf_1_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_te_uf_2_point = geompy.MakeVertexWithRef(foam_align_te_point_3, -fillet_radius,0,0)
cyl_te_uf_2 = geompy.MakeCylinder(cyl_te_uf_2_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_te_lf_1_point = geompy.MakeVertexWithRef(foam_align_te_point_1, fillet_radius,0,0)
cyl_te_lf_1 = geompy.MakeCylinder(cyl_te_lf_1_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

cyl_te_lf_2_point = geompy.MakeVertexWithRef(foam_align_te_point_4, -fillet_radius,0,0)
cyl_te_lf_2 = geompy.MakeCylinder(cyl_te_lf_2_point, OZ, fillet_radius, wing_section_y_cordinates[5]-wing_section_y_cordinates[0]-100.0)

# remove the cylinders from the upper foam and the lower foam
bottom_foam = geompy.MakeCutList(bottom_foam, [cyl_le_lf_1,cyl_le_lf_2,cyl_te_lf_1,cyl_te_lf_2], checkSelfInte=True)
upper_foam = geompy.MakeCutList(upper_foam, [cyl_le_uf_1,cyl_le_uf_2,cyl_te_uf_1,cyl_te_uf_2], checkSelfInte=True)

#geompy.addToStudy(bottom_foam,'bottom_foam')
#geompy.addToStudy(upper_foam,'upper_foam')


# make the cutting plane for dividing the foam molds
dividing_plane_point_1 = geompy.MakeVertex(wing_section_chord_length[0]/2.0,0,wing_section_y_cordinates[0]-2000.0)
dividing_plane_point_2 = geompy.MakeVertex(wing_section_chord_length[0]/2.0,0,wing_section_y_cordinates[0]-1000.0)

dividing_plane = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt(dividing_plane_point_1,dividing_plane_point_2), 1.50*foam_width, foam_thickness*2*1.50)
#geompy.addToStudy(dividing_plane,'dividing_plane')



# Split the upper foam and then extract the molds

upper_foam_partition = geompy.MakePartition([upper_foam], [dividing_plane])
[mold_2_upper_foam_section_2,mold_1_upper_foam_section_1] = geompy.ExtractShapes(upper_foam_partition, geompy.ShapeType["SOLID"], True)
 
bottom_foam_partition = geompy.MakePartition([bottom_foam], [dividing_plane])
[mold_4_bottom_foam_section_2,mold_3_bottom_foam_section_1] = geompy.ExtractShapes(bottom_foam_partition, geompy.ShapeType["SOLID"], True)

geompy.addToStudy(mold_1_upper_foam_section_1,'mold_1_upper_foam_section_1')
geompy.addToStudy(mold_2_upper_foam_section_2,'mold_2_upper_foam_section_2')
geompy.addToStudy(mold_3_bottom_foam_section_1,'mold_3_bottom_foam_section_1')
geompy.addToStudy(mold_4_bottom_foam_section_2,'mold_4_bottom_foam_section_2')

# making the helping foam mold for the leading edge


# define a function that takes in the ratio and outputs the argument where the helping foam molds begins

def get_arguments(x_cordinates,chord_length,ratio):
    min_x = np.min(x_cordinates)
    length = chord_length*ratio
    desired_x = min_x+length
    
    for count,value in enumerate(x_cordinates):
        if value > desired_x:
            pass
        else :
            arg_first = count
            break

    return np.argmin(x_cordinates)-30,np.argmin(x_cordinates)



def calculate_offset_point(Ax, Ay, Bx, By, Cx, Cy, offset_distance):
    angle1 = atan2((By-Ay),(Bx-Ax))
    angle2 = atan2((Cy-By),(Cx-Bx))
    half_angle = ((np.pi)+angle1-angle2)/2.0
    mid_vector_length = offset_distance/sin(half_angle)
    other_angle = half_angle-angle1
    dx = mid_vector_length*sin(other_angle)
    dy = mid_vector_length*cos(other_angle)
    return (Bx+dx,By-dy)


def get_polyline_points (first_arg,second_arg,all_points,gap,thick_y_cordinate,width_x_cordinate,z_cordinate,factor):
    help_line_points = all_points[first_arg:second_arg]
    offset_list = np.linspace(gap,0.0,np.size(help_line_points))
    polyline_points = []

    

    for count,point in enumerate(help_line_points):
        if count == 0 :
            pass
        elif count == np.size(help_line_points)-1:
            polyline_points.append(geompy.MakeVertex(geompy.PointCoordinates(point)[0],geompy.PointCoordinates(point)[1],geompy.PointCoordinates(point)[2]))
        else:

            Ax = geompy.PointCoordinates(help_line_points[count-1])[0]
            Ay = geompy.PointCoordinates(help_line_points[count-1])[1]
            Bx = geompy.PointCoordinates(help_line_points[count])[0]
            By = geompy.PointCoordinates(help_line_points[count])[1]
            Cx = geompy.PointCoordinates(help_line_points[count+1])[0]
            Cy = geompy.PointCoordinates(help_line_points[count+1])[1]
            offset_distance = offset_list[count]

            angle1 = atan2((By-Ay),(Bx-Ax))
            angle2 = atan2((Cy-By),(Cx-Bx))
            half_angle = ((np.pi)+angle1-angle2)/2.0
            mid_vector_length = offset_distance/sin(half_angle)
            other_angle = half_angle-angle1
            dx = mid_vector_length*sin(other_angle)
            dy = mid_vector_length*cos(other_angle)
            x = Bx-factor*dx
            y = By+factor*dy
               

            polyline_points.append(geompy.MakeVertex(x,y,z_cordinate))

    polyline_points.append(geompy.MakeVertex(width_x_cordinate,geompy.PointCoordinates(point)[1],z_cordinate))
    polyline_points.append(geompy.MakeVertex(width_x_cordinate,thick_y_cordinate,z_cordinate))
    polyline_points.append(geompy.MakeVertex(geompy.PointCoordinates(polyline_points[0])[0],thick_y_cordinate,z_cordinate))
    return polyline_points



# Arguments for the helping foam
hf_width_x_cordinate = np.min(profile_1_x_cordinates)-foam_align_le_length-helping_foam_mold_extra_length-foam_align_le_gap
hf_high_y_cordinate = geompy.PointCoordinates(boxp2)[1]

# create the polyline and then just make them visible to the study
p1_first_arg,p1_second_arg = get_arguments(profile_1_x_cordinates,wing_section_chord_length[0],0.15)

p1_polyline_points = get_polyline_points(p1_first_arg,p1_second_arg+1,profile_1_all_points,helping_foam_mold_gap_p1,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[0],2.0)
p1_polyline = geompy.MakePolyline(p1_polyline_points,True)
geompy.addToStudy(p1_polyline,'p1_polyline')


# create the polyline and then just make them visible to the study
p2_first_arg,p2_second_arg = get_arguments(profile_2_x_cordinates,wing_section_chord_length[1],0.15)

p2_polyline_points = get_polyline_points(p2_first_arg+1,p2_second_arg+2,profile_2_all_points,helping_foam_mold_gap_p2,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[1],2.0)
p2_polyline = geompy.MakePolyline(p2_polyline_points,True)
geompy.addToStudy(p2_polyline,'p2_polyline')

# create the polyline and then just make them visible to the study
p3_first_arg,p3_second_arg = get_arguments(profile_3_x_cordinates,wing_section_chord_length[2],0.14)

p3_polyline_points = get_polyline_points(p3_first_arg,p3_second_arg+1,profile_3_all_points,helping_foam_mold_gap_p3,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[2],2.0)
p3_polyline = geompy.MakePolyline(p3_polyline_points,True)
geompy.addToStudy(p3_polyline,'p3_polyline')

# create the polyline and then just make them visible to the study
p4_first_arg,p4_second_arg = get_arguments(profile_4_x_cordinates,wing_section_chord_length[3],0.14)

p4_polyline_points = get_polyline_points(p4_first_arg+1,p4_second_arg+2,profile_4_all_points,helping_foam_mold_gap_p4,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[3],2.0)
p4_polyline = geompy.MakePolyline(p4_polyline_points,True)
geompy.addToStudy(p4_polyline,'p4_polyline')


# create the polyline and then just make them visible to the study
p5_first_arg,p5_second_arg = get_arguments(profile_5_x_cordinates,wing_section_chord_length[4],0.11)

p5_polyline_points = get_polyline_points(p5_first_arg,p5_second_arg+1,profile_5_all_points,helping_foam_mold_gap_p5,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[4],2.0)
p5_polyline = geompy.MakePolyline(p5_polyline_points,True)
geompy.addToStudy(p5_polyline,'p5_polyline')


# create the polyline and then just make them visible to the study
p6_first_arg,p6_second_arg = get_arguments(profile_6_x_cordinates,wing_section_chord_length[5],0.07)

p6_polyline_points = get_polyline_points(p6_first_arg-1,p6_second_arg,profile_6_all_points,helping_foam_mold_gap_p6,hf_high_y_cordinate,hf_width_x_cordinate,wing_section_y_cordinates[5],2.0)
p6_polyline = geompy.MakePolyline(p6_polyline_points,True)
geompy.addToStudy(p6_polyline,'p6_polyline')


helping_foam_mold = geompy.MakeThruSections([p1_polyline,p2_polyline,p3_polyline,p4_polyline,p5_polyline,p6_polyline],1,1e-8,1)

print(np.size(p1_polyline_points))
print(np.size(p2_polyline_points))
print(np.size(p3_polyline_points))
print(np.size(p4_polyline_points))
print(np.size(p5_polyline_points))
print(np.size(p6_polyline_points))

helping_foam_mold = geompy.MakeCutList(helping_foam_mold, [foam_align_le,cyl_le_uf_1,cyl_le_uf_2], checkSelfInte=True)
#geompy.addToStudy(helping_foam_mold,'helping_foam_mold')



# create the rectangles for cutting the extra helping foam mold

# define a function to make rectangle from two points
def MakeRectTwoPnt(point1,point2):
    
    point1_x = geompy.PointCoordinates(point1)[0]
    point1_y = geompy.PointCoordinates(point1)[1]
    point1_z = geompy.PointCoordinates(point1)[2]

    point2_x = geompy.PointCoordinates(point2)[0]
    point2_y = geompy.PointCoordinates(point2)[1]
    point2_z = geompy.PointCoordinates(point2)[2]
    
    point3 = geompy.MakeVertex(point1_x,point2_y,point2_z)
    point4 = geompy.MakeVertex(point2_x,point1_y,point1_z)

    rect_polyline = geompy.MakePolyline([point1,point3,point2,point4],True)
    return rect_polyline



# make 6 rectangles for the cutting the profile
hf_p1_rec_point_1 = geompy.MakeVertex(np.min(profile_1_x_cordinates)+(wing_section_chord_length[0]*helping_foam_mold_ratio),profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)],wing_section_y_cordinates[0])
hf_p1_rec_point_2 = geompy.MakeVertex(np.min(profile_1_x_cordinates)+(wing_section_chord_length[0]*helping_foam_mold_ratio*5),profile_1_y_cordinates[np.argmin(profile_1_x_cordinates)]+foam_thickness,wing_section_y_cordinates[0])
hf_p1_rec = MakeRectTwoPnt(hf_p1_rec_point_1,hf_p1_rec_point_2)


hf_p2_rec_point_1 = geompy.MakeVertex(np.min(profile_2_x_cordinates)+(wing_section_chord_length[1]*helping_foam_mold_ratio),profile_2_y_cordinates[np.argmin(profile_2_x_cordinates)],wing_section_y_cordinates[1])
hf_p2_rec_point_2 = geompy.MakeVertex(np.min(profile_2_x_cordinates)+(wing_section_chord_length[1]*helping_foam_mold_ratio*5),profile_2_y_cordinates[np.argmin(profile_2_x_cordinates)]+foam_thickness,wing_section_y_cordinates[1])
hf_p2_rec = MakeRectTwoPnt(hf_p2_rec_point_1,hf_p2_rec_point_2)

hf_p3_rec_point_1 = geompy.MakeVertex(np.min(profile_3_x_cordinates)+(wing_section_chord_length[2]*helping_foam_mold_ratio),profile_3_y_cordinates[np.argmin(profile_3_x_cordinates)],wing_section_y_cordinates[2])
hf_p3_rec_point_2 = geompy.MakeVertex(np.min(profile_3_x_cordinates)+(wing_section_chord_length[2]*helping_foam_mold_ratio*5),profile_3_y_cordinates[np.argmin(profile_3_x_cordinates)]+foam_thickness,wing_section_y_cordinates[2])
hf_p3_rec = MakeRectTwoPnt(hf_p3_rec_point_1,hf_p3_rec_point_2)

hf_p4_rec_point_1 = geompy.MakeVertex(np.min(profile_4_x_cordinates)+(wing_section_chord_length[3]*helping_foam_mold_ratio),profile_4_y_cordinates[np.argmin(profile_4_x_cordinates)],wing_section_y_cordinates[3])
hf_p4_rec_point_2 = geompy.MakeVertex(np.min(profile_4_x_cordinates)+(wing_section_chord_length[3]*helping_foam_mold_ratio*5),profile_4_y_cordinates[np.argmin(profile_4_x_cordinates)]+foam_thickness,wing_section_y_cordinates[3])
hf_p4_rec = MakeRectTwoPnt(hf_p4_rec_point_1,hf_p4_rec_point_2)

hf_p5_rec_point_1 = geompy.MakeVertex(np.min(profile_5_x_cordinates)+(wing_section_chord_length[4]*helping_foam_mold_ratio),profile_5_y_cordinates[np.argmin(profile_5_x_cordinates)],wing_section_y_cordinates[4])
hf_p5_rec_point_2 = geompy.MakeVertex(np.min(profile_5_x_cordinates)+(wing_section_chord_length[4]*helping_foam_mold_ratio*5),profile_5_y_cordinates[np.argmin(profile_5_x_cordinates)]+foam_thickness,wing_section_y_cordinates[4])
hf_p5_rec = MakeRectTwoPnt(hf_p5_rec_point_1,hf_p5_rec_point_2)

hf_p6_rec_point_1 = geompy.MakeVertex(np.min(profile_6_x_cordinates)+(wing_section_chord_length[5]*helping_foam_mold_ratio),profile_6_y_cordinates[np.argmin(profile_6_x_cordinates)],wing_section_y_cordinates[5])
hf_p6_rec_point_2 = geompy.MakeVertex(np.min(profile_6_x_cordinates)+(wing_section_chord_length[5]*helping_foam_mold_ratio*5),profile_6_y_cordinates[np.argmin(profile_6_x_cordinates)]+foam_thickness,wing_section_y_cordinates[5])
hf_p6_rec = MakeRectTwoPnt(hf_p6_rec_point_1,hf_p6_rec_point_2)




hf_rec_solid = geompy.MakeThruSections([hf_p1_rec,hf_p2_rec,hf_p3_rec,hf_p4_rec,hf_p5_rec,hf_p6_rec],1,1e-8,1)
#geompy.addToStudy(hf_rec_solid,'hf_rec_solid')

# rectangel to make the bottom part flat
hf_bottom_rec_point_1 = geompy.MakeVertex(np.min(profile_1_x_cordinates)-foam_width,y1_for_rect1-foam_thickness,wing_section_y_cordinates[5])
hf_bottom_rec_point_2 = geompy.MakeVertex(np.min(profile_1_x_cordinates)+10.0,y1_for_rect1,wing_section_y_cordinates[0])
hf_bottom_rec_solid = geompy.MakeBoxTwoPnt(hf_bottom_rec_point_1,hf_bottom_rec_point_2)
#geompy.addToStudy(hf_bottom_rec_solid,'hf_bottom_rec_soilid')


helping_foam_mold = geompy.MakeCutList(helping_foam_mold, [hf_rec_solid,hf_bottom_rec_solid], checkSelfInte=True)


helping_foam_mold_partition = geompy.MakePartition([helping_foam_mold], [dividing_plane])
[mold_6_helping_foam_section_2,mold_5_helping_foam_section_1] = geompy.ExtractShapes(helping_foam_mold_partition, geompy.ShapeType["SOLID"], True)
geompy.addToStudy(mold_5_helping_foam_section_1,'mold_5_helping_foam_section_1')
geompy.addToStudy(mold_6_helping_foam_section_2,'mold_6_helping_foam_section_2')

