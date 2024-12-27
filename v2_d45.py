#import FreeCAD
import numpy as np
# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 6

# 2. The distance of the profile from the centreline of the fuselage in the direction of the wing tip in mm
wing_section_y_cordinates = np.array([0.35,2.1774,4.5496,6.0039,6.948,7.5])*-1000.0     

# 3. The distance of the profile leading edge from the wing root in the direction of the tariling edge in mm
wing_section_x_cordinates = np.array([0.0,0.014025,0.10489,0.214318,0.3234744,0.430468])*1000.0   
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
wing_section_chord_length = np.array([0.7319,0.7154,0.6085,0.4826,0.3568,0.2309])*1000.0

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

# find the three points for slicing the wing body
profile_1_point_1_cut = [min(profile_1_x_cordinates)-10,profile_1_y_cordinates[profile_1_x_cordinates.argmin()],wing_section_y_cordinates[0]]
profile_1_point_2_cut = [wing_section_chord_length[0]*0.132,profile_1_y_cordinates.max()-((profile_1_y_cordinates.max()-profile_1_y_cordinates.min())/2.0),wing_section_y_cordinates[0]]
profile_1_point_3_cut = [wing_section_chord_length[0]+10.0,profile_1_y_cordinates[0]+((profile_1_y_cordinates[0]-profile_1_y_cordinates[-1])/2.0),wing_section_y_cordinates[0]]



profile_1_point_1_cut_f = FreeCAD.Vector(profile_1_point_1_cut[0],profile_1_point_1_cut[1],profile_1_point_1_cut[2])
profile_1_point_2_cut_f = FreeCAD.Vector(profile_1_point_2_cut[0],profile_1_point_2_cut[1],profile_1_point_2_cut[2])
profile_1_point_3_cut_f = FreeCAD.Vector(profile_1_point_3_cut[0],profile_1_point_3_cut[1],profile_1_point_3_cut[2])





profile_1_line_1 = Part.LineSegment(profile_1_point_1_cut_f,profile_1_point_2_cut_f)
profile_1_line_2 = Part.LineSegment(profile_1_point_2_cut_f,profile_1_point_3_cut_f)


import BOPTools.SplitFeatures
f = BOPTools.SplitFeatures.makeSlice(name='Slice')
f.Base = [App.ActiveDocument.wing1, App.ActiveDocument.cut_surface_1][0]
f.Tools = [App.ActiveDocument.wing1, App.ActiveDocument.cut_surface_1][1:]
f.Mode = 'Split'
f.Proxy.execute(f)
f.purgeTouched()
for obj in f.ViewObject.Proxy.claimChildren():
    obj.ViewObject.hide()
import CompoundTools.Explode
CompoundTools.Explode.explodeCompound(f)
f.ViewObject.hide()
App.ActiveDocument.recompute()















# ========================================================
# ======== Geometry Creation in FreeCAD ==================
# ========================================================
import FreeCAD, Part, Draft

# Create a new document
doc = FreeCAD.newDocument('D45_Wing_Design')

# create the points for the profile 1
profile_1_all_points = []
for count,value in enumerate (profile_1_x_cordinates):
    globals()[f'Profile_1_Point_{int(count+1)}'] = FreeCAD.Vector(profile_1_x_cordinates[count],profile_1_y_cordinates[count],wing_section_y_cordinates[0])
    profile_1_all_points.append(globals()[f'Profile_1_Point_{int(count+1)}'])

profile_1_last_line = Draft.make_line(globals()[f'Profile_1_Point_{int(1)}'],globals()[f'Profile_1_Point_{int(len(profile_1_x_cordinates))}'])
profile_1_spline = Draft.make_bspline(profile_1_all_points,closed=False)

FreeCAD.ActiveDocument.recompute()
face1 = Part.Face(Part.Wire(Part.__sortEdges__([App.ActiveDocument.BSpline.Shape.Edge1, App.ActiveDocument.Line.Shape.Edge1, ])))

Part.show(face1,'Pface1')


# create the points for the profile 2
profile_2_all_points = []
for count,value in enumerate (profile_2_x_cordinates):
    globals()[f'Profile_2_Point_{int(count+1)}'] = FreeCAD.Vector(profile_2_x_cordinates[count],profile_2_y_cordinates[count],wing_section_y_cordinates[1])
    profile_2_all_points.append(globals()[f'Profile_2_Point_{int(count+1)}'])

profile_2_last_line = Draft.make_line(globals()[f'Profile_2_Point_{int(1)}'],globals()[f'Profile_2_Point_{int(len(profile_2_x_cordinates))}'])
profile_2_spline = Draft.make_bspline(profile_2_all_points,closed=False)
FreeCAD.ActiveDocument.recompute()
face2 = Part.Face(Part.Wire(Part.__sortEdges__([App.ActiveDocument.BSpline001.Shape.Edge1, App.ActiveDocument.Line001.Shape.Edge1, ])))

Part.show(face2,'Pface2')


profile_1_middle_line = Draft.make_line(globals()[f'Profile_1_Point_{int(1)}'],globals()[f'Profile_1_Point_{int(len(profile_1_x_cordinates)/2)}'])

FreeCAD.ActiveDocument.recompute()
#face2 = Part.Face(Part.Wire(Part.__sortEdges__([App.ActiveDocument.BSpline.Shape.Edge1, App.ActiveDocument.Line.Shape.Edge1, ])))

#Part.show(face1,'Pface1')

#wire = Part.Wire([profile_1_spline,profile_1_last_line])
#Part.show(wire,'wire')







