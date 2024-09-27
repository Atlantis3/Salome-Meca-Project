# Created on 26.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creation of the complex geometry
# This file contains the python script for creating the geometry for more complex shape and exporting it to the step file

# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
wall_thickness = 2     # The wall thickness in mm
wall_radius = 30       # The radius of the curve



#------------------------------------------------------------------------------------
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


#------------------------------------------------------------------------------------------------
# creation of the private functions
def arc_centre_point(p1, p2, radius):
    # Unpack the coordinates
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    # Calculate the distance between the two points in the XY plane
    dist_xy = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Check if the radius is valid
    if dist_xy >= 2 * radius:
        raise ValueError("The radius is too small for the distance between the points.")

    # Calculate the midpoint in XY
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Calculate height from the midpoint to the center of the arc in the XY plane
    height_xy = math.sqrt(radius**2 - (dist_xy / 2)**2)

    # Calculate the direction of the line segment (perpendicular)
    dx = (y2 - y1) / dist_xy  # Perpendicular direction in XY
    dy = (x1 - x2) / dist_xy

    # Calculate the center point in XY
    center_x = mid_x + height_xy * dx
    center_y = mid_y + height_xy * dy

    # The Z coordinate of the center point can be the same as the midpoint Z
    center_z = (z1 + z2) / 2

    return [center_x, center_y, center_z]







# Creating the geometry of the disk
p1 = geompy.MakeVertex(0.0, 0.0,0.0 )
p2 = geompy.MakeVertex(30,15,0.0)
p3 = geompy.MakeVertex(30.0,15.0+wall_thickness,0.0)
p4 = geompy.MakeVertex(0,wall_thickness,0.0)

geompy.addToStudy(p1,'p1')
geompy.addToStudy(p2,'p2')
geompy.addToStudy(p3,'p3')
geompy.addToStudy(p4,'p4')

l1 = geompy.MakeLineTwoPnt(p1,p4)
l3 = geompy.MakeLineTwoPnt(p2,p3)

geompy.addToStudy(l1,'l1')
geompy.addToStudy(l3,'l3')

arc1_centre_point_cordinates = arc_centre_point(p1=list(map(float,p1.GetParameters().split(':'))),p2=list(map(float,p2.GetParameters().split(':'))),radius=wall_radius)
arc1_centre_point = geompy.MakeVertex(arc1_centre_point_cordinates[0],arc1_centre_point_cordinates[1],arc1_centre_point_cordinates[2])
geompy.addToStudy(arc1_centre_point,'arc_1_centre_point')
