# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================

import numpy as np
from math import sin,radians,cosh
amplitude1 = 1.0
wavelength1 = 2.0
n_data_points1 = 121
# creating the list for x_cordinates and y_cordinates
amplitude1 = amplitude1/2.0
x_cordinate = np.linspace(0.0,wavelength1,n_data_points1)
x_cordinate[1] = x_cordinate[1]-((wavelength1/(n_data_points1-1))/2.0)
x_cordinate[-2] = x_cordinate[-2]+((wavelength1/(n_data_points1-1))/2.0)
total_lines = n_data_points1-1
y_cordinate = []
theta_list = np.linspace(-90,270,n_data_points1)
for count,value in enumerate(x_cordinate):
    theta = theta_list[count]
    y = (amplitude1*(sin(radians(theta))))+amplitude1
    #y = amplitude1*cosh(theta/1.0)
    y_cordinate.append(y)

x_cordinates = x_cordinate
y_cordinates = y_cordinate

amplitude = 5.0
n_flutes_y = 2
flute_thickness = 0.2
liner_thickness = 0.2



# ========================================================
# ======== Mesh parameterisation =====================
# ========================================================
max_curvature_element_size = flute_thickness/6.0
min_curvature_element_size = flute_thickness/2.0
average_element_size = (max_curvature_element_size+min_curvature_element_size)/2.0
min_element_size = flute_thickness/4.0
max_element_size = flute_thickness


# for the liner, also making suer that there is atleast one node common to both the flute ans the liner
n_elements_thickness = 2
one_elem_length = liner_thickness/n_elements_thickness
liner_full_length = x_cordinates[-1]*n_flutes_y
n_elements_load_line = int(liner_full_length/one_elem_length)




#----------------------------------------------
#----------------------------------------------

# Importing important modules for calculations
from math import sin,radians,floor,ceil,sqrt,atan2,cos
import numpy as np




# creating the original values for x and y cordinates
x_cordinates = np.array(x_cordinates)*amplitude
y_cordinates = np.array(y_cordinates)*amplitude
n_data_points = len(x_cordinates)
wavelength = x_cordinates[-1]


# creating the list for new x_cordinates and y_cordinates (offset from the original one)
new_x_cordinates = []
new_y_cordinates = []
# creating a new list of cordinates for thickned line

def calculate_offset_point(Ax, Ay, Bx, By, Cx, Cy, offset_distance):
    angle1 = atan2((By-Ay),(Bx-Ax))
    angle2 = atan2((Cy-By),(Cx-Bx))
    half_angle = ((np.pi)+angle1-angle2)/2.0
    mid_vector_length = offset_distance/sin(half_angle)
    other_angle = half_angle-angle1
    dx = mid_vector_length*sin(other_angle)
    dy = mid_vector_length*cos(other_angle)
    return (dx,dy)



for count,value in enumerate (x_cordinates):
        if count==int(n_data_points-1) :
            x2 = x_cordinates[count]
            y2 = y_cordinates[count]
            angle11 = atan2((y_cordinates[-2]-y_cordinates[-1]),(x_cordinates[-2]-x_cordinates[-1]))
            angle11 = angle11-(np.pi/2)
            new_thickness = flute_thickness/np.sin(angle11)
            new_x_cordinates.append(x2)
            new_y_cordinates.append(y2+new_thickness)
            #print(new_thickness)


        elif count==0 :
            x2 = x_cordinates[count]
            y2 = y_cordinates[count]
            angle11 = atan2((y_cordinates[1]-y_cordinates[0]),(x_cordinates[1]-x_cordinates[0]))
            angle11 = (np.pi/2)-angle11
            new_thickness = flute_thickness/np.sin(angle11)
            new_x_cordinates.append(x2)
            new_y_cordinates.append(y2+new_thickness)
            #print(new_thickness)

        
        else:
            x1 = x_cordinates[count]
            x2 = x_cordinates[count+1]
            y1 = y_cordinates[count]
            y2 = y_cordinates[count+1]
            x0 = x_cordinates[count-1]
            y0 = y_cordinates[count-1]
            final_dx,final_dy = calculate_offset_point(x0,y0,x1,y1,x2,y2,flute_thickness)
            
            if x1-final_dy < 0 :
                
                new_x_cordinates.append(0)
                new_y_cordinates.append(y1+final_dx)
            elif x1-final_dy > x_cordinates[-1] :
                
                new_x_cordinates.append(x_cordinates[-1])
                new_y_cordinates.append(y1+final_dx)
            else :
                
                new_x_cordinates.append(x1-final_dy)
                new_y_cordinates.append(y1+final_dx)
        



flute_amplitude = max(new_y_cordinates)

# creating the variables for the liner mesh
max_length = wavelength*n_flutes_y
min_arg = np.argmax(new_y_cordinates)
min_length = new_x_cordinates[min_arg]
#n_elements_load_line = int(n_elements_load_line*n_flutes_y)



import sys
import salome
salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

#=======================================================================
#============ Geometry module ==========================================
#=======================================================================

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
for count,value in enumerate (x_cordinates):
    globals()[f'Vertex_{int(count+1)}'] = geompy.MakeVertex(x_cordinates[count],y_cordinates[count],0.0)
    #geompy.addToStudy(globals()[f'Vertex_{int(count+1)}'],'Vertex_'+str(count+1))

# creating the lines and joining them
all_lines = []
for count in range(1,len(x_cordinates)):
    globals()[f'Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f'Vertex_{int(count)}'],globals()[f'Vertex_{int(count+1)}'])
    #geompy.addToStudy(globals()[f'Line_{int(count)}'],'Line_'+str(count))
    all_lines.append(globals()[f'Line_{int(count)}'])

# Making the Fuse of all the lines
Single_flute_line = geompy.MakeFuseList(all_lines,True,True)
#geompy.addToStudy(Single_flute_line,'Single_flute_line')


# creating the points for the top lines
for count,value in enumerate (new_x_cordinates):
    globals()[f't_Vertex_{int(count+1)}'] = geompy.MakeVertex(new_x_cordinates[count],new_y_cordinates[count],0.0)
    #geompy.addToStudy(globals()[f't_Vertex_{int(count+1)}'],'t_Vertex_'+str(count+1))

# creating the lines and joining them
all_lines_top = []
for count in range(1,len(new_x_cordinates)):
    globals()[f't_Line_{int(count)}'] = geompy.MakeLineTwoPnt(globals()[f't_Vertex_{int(count)}'],globals()[f't_Vertex_{int(count+1)}'])
    #geompy.addToStudy(globals()[f't_Line_{int(count)}'],'t_Line_'+str(count))
    all_lines_top.append(globals()[f't_Line_{int(count)}'])

# Making the Fuse of all the lines
Single_flute_line_top = geompy.MakeFuseList(all_lines_top,True,True)
#geompy.addToStudy(Single_flute_line_top,'Single_flute_line_top')

# Creating the flute
Flute_lines =  geompy.MakeFuseList([Single_flute_line,Single_flute_line_top],True,True)
flute_line_ext = geompy.MakeMultiTranslation1D(Flute_lines, None, wavelength, n_flutes_y)
Join_line_1 = geompy.MakeLineTwoPnt(globals()[f'Vertex_{int(1)}'],globals()[f't_Vertex_{int(1)}'])
Join_lines = geompy.MakeMultiTranslation1D(Join_line_1, None, n_flutes_y*wavelength, 2)
flute = geompy.MakeFaceWires([flute_line_ext,Join_lines], 1)
geompy.addToStudy(flute,'flute')

# creating the groups for the flute for top contact analysis
full_top_contact_1 =  geompy.MakeMultiTranslation1D(Single_flute_line_top, None, wavelength, n_flutes_y)
full_top_contact_obj = geompy.GetInPlace(flute,full_top_contact_1,True)
full_top_contact = geompy.CreateGroup(flute, geompy.ShapeType["EDGE"])
geompy.UnionList(full_top_contact,[full_top_contact_obj])
geompy.addToStudyInFather(flute,full_top_contact,'full_top_contact')




# creating the groups for the bottom contact analysis
full_bottom_contact_1 = geompy.MakeMultiTranslation1D(Single_flute_line, None, wavelength, n_flutes_y)
full_bottom_contact_obj = geompy.GetInPlace(flute,full_bottom_contact_1,True)
full_bottom_contact = geompy.CreateGroup(flute, geompy.ShapeType["EDGE"])
geompy.UnionList(full_bottom_contact,[full_bottom_contact_obj])
geompy.addToStudyInFather(flute,full_bottom_contact,'full_bottom_contact')


# creating the group of edges for the extreme side edges
# creating the geometry for the fixed_edges
extrm_side_edges_obj = geompy.GetInPlace(flute,Join_lines,True)
extrm_side_edges = geompy.CreateGroup(flute, geompy.ShapeType["EDGE"])
geompy.UnionList(extrm_side_edges,[extrm_side_edges_obj])
geompy.addToStudyInFather(flute,extrm_side_edges,'extrm_side_edges')


# create the group for the flutes
flute_all_obj = geompy.GetInPlace(flute,flute,True)
flute_all = geompy.CreateGroup(flute, geompy.ShapeType["FACE"])
geompy.UnionList(flute_all,[flute_all_obj])
geompy.addToStudyInFather(flute,flute_all,'flute_all')






# getting the maximum amplitude from the y_cordinate list
single_rect_height = flute_amplitude/5.0

# Creating the areas where the mesh would be really fine
rect_1_point_1 = geompy.MakeVertex(0, 0.0,0.0 )
rect_1_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, 0.0, 0.0 )
rect_1_point_3 = geompy.MakeVertex(wavelength*n_flutes_y,single_rect_height, 0.0)
rect_1_point_4 = geompy.MakeVertex(0, single_rect_height, 0.0 )

rect_1_line_1 = geompy.MakeLineTwoPnt(rect_1_point_1,rect_1_point_2)
rect_1_line_2 = geompy.MakeLineTwoPnt(rect_1_point_2,rect_1_point_3)
rect_1_line_3 = geompy.MakeLineTwoPnt(rect_1_point_3,rect_1_point_4)
rect_1_line_4 = geompy.MakeLineTwoPnt(rect_1_point_4,rect_1_point_1)

rect_1 = geompy.MakeFaceWires([rect_1_line_1,rect_1_line_2,rect_1_line_3,rect_1_line_4],1)
geompy.addToStudy(rect_1,'rect_1')

# Rectangle 2
rect_2_point_1 = geompy.MakeVertex(0, single_rect_height,0.0 )
rect_2_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, single_rect_height, 0.0 )
rect_2_point_3 = geompy.MakeVertex(wavelength*n_flutes_y,single_rect_height*2, 0.0)
rect_2_point_4 = geompy.MakeVertex(0, single_rect_height*2, 0.0 )

rect_2_line_1 = geompy.MakeLineTwoPnt(rect_2_point_1,rect_2_point_2)
rect_2_line_2 = geompy.MakeLineTwoPnt(rect_2_point_2,rect_2_point_3)
rect_2_line_3 = geompy.MakeLineTwoPnt(rect_2_point_3,rect_2_point_4)
rect_2_line_4 = geompy.MakeLineTwoPnt(rect_2_point_4,rect_2_point_1)

rect_2 = geompy.MakeFaceWires([rect_2_line_1,rect_2_line_2,rect_2_line_3,rect_2_line_4],1)
geompy.addToStudy(rect_2,'rect_2')


# Rectangle 3
rect_3_point_1 = geompy.MakeVertex(0, single_rect_height*2,0.0 )
rect_3_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, single_rect_height*2, 0.0 )
rect_3_point_3 = geompy.MakeVertex(wavelength*n_flutes_y,single_rect_height*3, 0.0)
rect_3_point_4 = geompy.MakeVertex(0, single_rect_height*3, 0.0 )

rect_3_line_1 = geompy.MakeLineTwoPnt(rect_3_point_1,rect_3_point_2)
rect_3_line_2 = geompy.MakeLineTwoPnt(rect_3_point_2,rect_3_point_3)
rect_3_line_3 = geompy.MakeLineTwoPnt(rect_3_point_3,rect_3_point_4)
rect_3_line_4 = geompy.MakeLineTwoPnt(rect_3_point_4,rect_3_point_1)

rect_3 = geompy.MakeFaceWires([rect_3_line_1,rect_3_line_2,rect_3_line_3,rect_3_line_4],1)
geompy.addToStudy(rect_3,'rect_3')


# Rectangle 4
rect_4_point_1 = geompy.MakeVertex(0, single_rect_height*3,0.0 )
rect_4_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, single_rect_height*3, 0.0 )
rect_4_point_3 = geompy.MakeVertex(wavelength*n_flutes_y,single_rect_height*4, 0.0)
rect_4_point_4 = geompy.MakeVertex(0, single_rect_height*4, 0.0 )

rect_4_line_1 = geompy.MakeLineTwoPnt(rect_4_point_1,rect_4_point_2)
rect_4_line_2 = geompy.MakeLineTwoPnt(rect_4_point_2,rect_4_point_3)
rect_4_line_3 = geompy.MakeLineTwoPnt(rect_4_point_3,rect_4_point_4)
rect_4_line_4 = geompy.MakeLineTwoPnt(rect_4_point_4,rect_4_point_1)

rect_4 = geompy.MakeFaceWires([rect_4_line_1,rect_4_line_2,rect_4_line_3,rect_4_line_4],1)
geompy.addToStudy(rect_4,'rect_4')


# Rectangle 5
rect_5_point_1 = geompy.MakeVertex(0, single_rect_height*4,0.0 )
rect_5_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, single_rect_height*4, 0.0 )
rect_5_point_3 = geompy.MakeVertex(wavelength*n_flutes_y,single_rect_height*5, 0.0)
rect_5_point_4 = geompy.MakeVertex(0, single_rect_height*5, 0.0 )

rect_5_line_1 = geompy.MakeLineTwoPnt(rect_5_point_1,rect_5_point_2)
rect_5_line_2 = geompy.MakeLineTwoPnt(rect_5_point_2,rect_5_point_3)
rect_5_line_3 = geompy.MakeLineTwoPnt(rect_5_point_3,rect_5_point_4)
rect_5_line_4 = geompy.MakeLineTwoPnt(rect_5_point_4,rect_5_point_1)

rect_5 = geompy.MakeFaceWires([rect_5_line_1,rect_5_line_2,rect_5_line_3,rect_5_line_4],1)
geompy.addToStudy(rect_5,'rect_5')


#create the top liner and the bottom liner
top_liner_point_1 = geompy.MakeVertex(0, flute_amplitude,0.0 )
top_liner_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, flute_amplitude, 0.0 )
top_liner_point_3 = geompy.MakeVertex(wavelength*n_flutes_y, flute_amplitude+liner_thickness, 0.0)
top_liner_point_4 = geompy.MakeVertex(0, flute_amplitude+liner_thickness, 0.0 )



t_l_line_1 = geompy.MakeLineTwoPnt(top_liner_point_1,top_liner_point_2)
t_l_line_2 = geompy.MakeLineTwoPnt(top_liner_point_2,top_liner_point_3)
t_l_line_3 = geompy.MakeLineTwoPnt(top_liner_point_3,top_liner_point_4)
t_l_line_4 = geompy.MakeLineTwoPnt(top_liner_point_4,top_liner_point_1)

top_liner = geompy.MakeFaceWires([t_l_line_1,t_l_line_2,t_l_line_3,t_l_line_4],1)
geompy.addToStudy(top_liner,'top_liner')

# creating the bottom liner
bottom_liner_point_1 = geompy.MakeVertex(0, y_cordinates[0], 0.0)
bottom_liner_point_2 = geompy.MakeVertex(wavelength*n_flutes_y, y_cordinates[0], 0.0)
bottom_liner_point_3 = geompy.MakeVertex(wavelength*n_flutes_y, y_cordinates[0]-liner_thickness, 0.0)
bottom_liner_point_4 = geompy.MakeVertex(0, y_cordinates[0]-liner_thickness, 0.0)

b_l_line_1 = geompy.MakeLineTwoPnt(bottom_liner_point_1,bottom_liner_point_2)
b_l_line_2 = geompy.MakeLineTwoPnt(bottom_liner_point_2,bottom_liner_point_3)
b_l_line_3 = geompy.MakeLineTwoPnt(bottom_liner_point_3,bottom_liner_point_4)
b_l_line_4 = geompy.MakeLineTwoPnt(bottom_liner_point_4,bottom_liner_point_1)

bottom_liner = geompy.MakeFaceWires([b_l_line_1,b_l_line_2,b_l_line_3,b_l_line_4],1)
geompy.addToStudy(bottom_liner,'bottom_liner')


'''#creatng the rectangle for the fine refinement of the mesh in the top and the bottom liner
point_1_percent = (1.0-fine_refinement_percent)/2.0
point_2_percent = point_1_percent+fine_refinement_percent


f_top_liner_point_1 = geompy.MakeVertex(wavelength*point_1_percent, flute_amplitude,0.0 )
f_top_liner_point_2 = geompy.MakeVertex(wavelength*point_2_percent, flute_amplitude, 0.0 )
f_top_liner_point_3 = geompy.MakeVertex(wavelength*point_2_percent, flute_amplitude+liner_thickness, 0.0)
f_top_liner_point_4 = geompy.MakeVertex(wavelength*point_1_percent, flute_amplitude+liner_thickness, 0.0 )

f_t_l_line_1 = geompy.MakeLineTwoPnt(f_top_liner_point_1,f_top_liner_point_2)
f_t_l_line_2 = geompy.MakeLineTwoPnt(f_top_liner_point_2,f_top_liner_point_3)
f_t_l_line_3 = geompy.MakeLineTwoPnt(f_top_liner_point_3,f_top_liner_point_4)
f_t_l_line_4 = geompy.MakeLineTwoPnt(f_top_liner_point_4,f_top_liner_point_1)
#geompy.addToStudy(f_t_l_line_1,'f_t_l_line_1')
#geompy.addToStudy(f_t_l_line_2,'f_t_l_line_2')
#geompy.addToStudy(f_t_l_line_3,'f_t_l_line_3')
#geompy.addToStudy(f_t_l_line_4,'f_t_l_line_4')

f_top_liner = geompy.MakeFaceWires([f_t_l_line_1,f_t_l_line_2,f_t_l_line_3,f_t_l_line_4],1)
fm_top_liner = geompy.MakeMultiTranslation1D(f_top_liner, None, wavelength, n_flutes_y)

geompy.addToStudy(fm_top_liner,'fm_top_liner')


fine_mesh_top_liner_obj = geompy.GetInPlace(top_liner,fm_top_liner,True)
fine_mesh_top_liner = geompy.CreateGroup(top_liner, geompy.ShapeType["FACE"])
geompy.UnionList(fine_mesh_top_liner,[fine_mesh_top_liner_obj])
geompy.addToStudyInFather(top_liner,fine_mesh_top_liner,'fine_mesh_top_liner')'''








# creating the groups for top and bottom liner and adding them to the study
load_line = geompy.CreateGroup(top_liner, geompy.ShapeType["EDGE"])
geompy.UnionIDs(load_line, [8])
tl_contact = geompy.CreateGroup(top_liner, geompy.ShapeType["EDGE"])
geompy.UnionIDs(tl_contact, [3])
tl_full = geompy.CreateGroup(top_liner, geompy.ShapeType["FACE"])
geompy.UnionIDs(tl_full, [1])
tl_left_line = geompy.CreateGroup(top_liner, geompy.ShapeType["EDGE"])
geompy.UnionIDs(tl_left_line, [10])

geompy.addToStudyInFather( top_liner, load_line, 'load_line' )
geompy.addToStudyInFather( top_liner, tl_contact, 'tl_contact' )
geompy.addToStudyInFather( top_liner, tl_full, 'tl_full' )
geompy.addToStudyInFather( top_liner, tl_left_line, 'tl_left_line' )

fixed_line = geompy.CreateGroup(bottom_liner,geompy.ShapeType["EDGE"])
geompy.UnionIDs(fixed_line, [8])
bl_contact = geompy.CreateGroup(bottom_liner,geompy.ShapeType["EDGE"])
geompy.UnionIDs(bl_contact,[3])

bl_full = geompy.CreateGroup(bottom_liner, geompy.ShapeType["FACE"])
geompy.UnionIDs(bl_full, [1])

bl_left_line = geompy.CreateGroup(bottom_liner, geompy.ShapeType["EDGE"])
geompy.UnionIDs(bl_left_line, [10])



geompy.addToStudyInFather( bottom_liner, fixed_line, 'fixed_line' )
geompy.addToStudyInFather( bottom_liner, bl_contact, 'bl_contact' )
geompy.addToStudyInFather( bottom_liner, bl_full, 'bl_full' )
geompy.addToStudyInFather( bottom_liner, bl_left_line, 'bl_left_line' )






###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

flute_mesh = smesh.Mesh(flute)
NETGEN_1D_2D = flute_mesh.Triangle(algo=smeshBuilder.NETGEN_1D2D)
NETGEN_2D_Parameters_1 = NETGEN_1D_2D.Parameters()
NETGEN_2D_Parameters_1.SetMaxSize( max_element_size )
NETGEN_2D_Parameters_1.SetMinSize(min_element_size )
NETGEN_2D_Parameters_1.SetSecondOrder( 0 )
NETGEN_2D_Parameters_1.SetOptimize( 1 )
NETGEN_2D_Parameters_1.SetFineness( 2 )
NETGEN_2D_Parameters_1.SetChordalError( -1 )
NETGEN_2D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_2D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_2D_Parameters_1.SetFuseEdges( 1 )
NETGEN_2D_Parameters_1.SetUseDelauney( 0 )
NETGEN_2D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(rect_1, max_curvature_element_size)
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(rect_2, average_element_size)
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(rect_3, min_curvature_element_size)
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(rect_4, average_element_size)
NETGEN_2D_Parameters_1.SetLocalSizeOnShape(rect_5, max_curvature_element_size)
NETGEN_2D_Parameters_1.SetWorstElemMeasure( 21956 )
NETGEN_2D_Parameters_1.SetCheckChartBoundary( 1 )

# groups for the edges
full_top_contact_1 = flute_mesh.GroupOnGeom(full_top_contact,'full_top_contact',SMESH.EDGE)
full_bottom_contact_1 = flute_mesh.GroupOnGeom(full_bottom_contact,'full_bottom_contact',SMESH.EDGE)
extrm_side_edges_1 = flute_mesh.GroupOnGeom(extrm_side_edges,'extrm_side_edges',SMESH.EDGE)
flute_all_1 = flute_mesh.GroupOnGeom(flute_all,'flute_all',SMESH.FACE)

# groups for the nodes
full_top_contact_2 = flute_mesh.GroupOnGeom(full_top_contact,'full_top_contact',SMESH.NODE)
full_bottom_contact_2 = flute_mesh.GroupOnGeom(full_bottom_contact,'full_bottom_contact',SMESH.NODE)
extrm_side_edges_2 = flute_mesh.GroupOnGeom(extrm_side_edges,'extrm_side_edges',SMESH.NODE)

isDone = flute_mesh.Compute()


## Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D.GetAlgorithm(), 'NETGEN 1D-2D')
smesh.SetName(NETGEN_2D_Parameters_1, 'NETGEN 2D Parameters_1')
smesh.SetName(flute_mesh.GetMesh(), 'flute_mesh')



top_liner_mesh = smesh.Mesh(top_liner)
Regular_1D_6 = top_liner_mesh.Segment()
Number_of_Segments_1 = Regular_1D_6.NumberOfSegments(n_elements_thickness)
Quadrangle_2D = top_liner_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)

# create the groups for the edges
load_line_1 = top_liner_mesh.GroupOnGeom(load_line,'load_line',SMESH.EDGE)
tl_contact_1 = top_liner_mesh.GroupOnGeom(tl_contact,'tl_contact',SMESH.EDGE)
tl_full_1 = top_liner_mesh.GroupOnGeom(tl_full,'tl_full',SMESH.FACE)

# Groups for the nodes
load_line_2 = top_liner_mesh.GroupOnGeom(load_line,'load_line',SMESH.NODE)
tl_contact_2 = top_liner_mesh.GroupOnGeom(tl_contact,'tl_contact',SMESH.NODE)



#sub meshes
Regular_1D_6_1 = top_liner_mesh.Segment(geom=tl_contact)
Number_of_Segments_1_1 = Regular_1D_6_1.NumberOfSegments(n_elements_load_line)
Regular_1D_6_2 = top_liner_mesh.Segment(geom=tl_left_line)
Number_of_Segments_1_2 = Regular_1D_6_2.NumberOfSegments(n_elements_thickness)
Regular_1D_6_3 = top_liner_mesh.Segment(geom=load_line)
Number_of_Segments_1_3 = Regular_1D_6_3.NumberOfSegments(n_elements_load_line)
isDone = top_liner_mesh.Compute()
Sub_mesh_1_1 = Regular_1D_6_1.GetSubMesh()
Sub_mesh_2_2 = Regular_1D_6_2.GetSubMesh()
Sub_mesh_3_3 = Regular_1D_6_3.GetSubMesh()



bottom_liner_mesh = smesh.Mesh(bottom_liner)

Regular_1D_8 = bottom_liner_mesh.Segment()
Number_of_Segments_2 = Regular_1D_8.NumberOfSegments(n_elements_thickness)
Quadrangle_2D_2 = bottom_liner_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)

# groups for the edges
fixed_line_1 = bottom_liner_mesh.GroupOnGeom(fixed_line,'fixed_line',SMESH.EDGE)
bl_contact_1 = bottom_liner_mesh.GroupOnGeom(bl_contact,'bl_contact',SMESH.EDGE)
bl_full_1 = bottom_liner_mesh.GroupOnGeom(bl_full,'bl_full',SMESH.FACE)


#group for the nodes
fixed_line_2 = bottom_liner_mesh.GroupOnGeom(fixed_line,'fixed_line',SMESH.NODE)
bl_contact_2 = bottom_liner_mesh.GroupOnGeom(bl_contact,'bl_contact',SMESH.NODE)

#Sub meshes
Regular_1D_8_1 = bottom_liner_mesh.Segment(geom=bl_contact)
Number_of_Segments_2_1 = Regular_1D_8_1.NumberOfSegments(n_elements_load_line)
Regular_1D_8_2 = bottom_liner_mesh.Segment(geom=bl_left_line)
Number_of_Segments_2_2 = Regular_1D_8_2.NumberOfSegments(n_elements_thickness)
Regular_1D_8_3 = bottom_liner_mesh.Segment(geom=fixed_line)
Number_of_Segments_2_3 = Regular_1D_8_3.NumberOfSegments(n_elements_load_line)


isDone = bottom_liner_mesh.Compute()

Sub_mesh_1_4 = Regular_1D_8_1.GetSubMesh()
Sub_mesh_2_5 = Regular_1D_8_2.GetSubMesh()
Sub_mesh_3_6 = Regular_1D_8_3.GetSubMesh()


bottom_liner_mesh.Reorient2D(bottom_liner_mesh,[ 0, 0, 1 ],[ 0, 0, 0 ])


# create the final mesh
Final_mesh = smesh.Concatenate( [ flute_mesh.GetMesh(), top_liner_mesh.GetMesh(), bottom_liner_mesh.GetMesh() ], 1, 1, 1e-05, False )
[ full_top_contact_3, full_bottom_contact_3, extrm_side_edges_3,flute_all_3, full_top_contact_4, full_bottom_contact_4, extrm_side_edges_4, load_line_3, tl_contact_3, tl_full_2, load_line_4, tl_contact_4, fixed_line_3, bl_contact_3, bl_full_2, fixed_line_4, bl_contact_4 ] = Final_mesh.GetGroups()
smesh.SetName(Final_mesh.GetMesh(), 'Final_mesh')


aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,full_top_contact_4,SMESH.FT_Undefined,SMESH.FT_LogicalAND)
aCriteria.append(aCriterion)
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,tl_contact_4)
aCriteria.append(aCriterion)
aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_1.SetMesh(Final_mesh.GetMesh())
common_nodes_tl = Final_mesh.GroupOnFilter( SMESH.NODE, 'common_nodes_tl', aFilter_1 )

aCriteria = []
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,full_bottom_contact_4,SMESH.FT_Undefined,SMESH.FT_LogicalAND)
aCriteria.append(aCriterion)
aCriterion = smesh.GetCriterion(SMESH.NODE,SMESH.FT_BelongToMeshGroup,SMESH.FT_Undefined,bl_contact_4)
aCriteria.append(aCriterion)
aFilter_2 = smesh.GetFilterFromCriteria(aCriteria)
aFilter_2.SetMesh(Final_mesh.GetMesh())
common_nodes_bl = Final_mesh.GroupOnFilter( SMESH.NODE, 'common_nodes_bl', aFilter_2 )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
