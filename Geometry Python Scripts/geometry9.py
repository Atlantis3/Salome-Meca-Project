# Created on 26.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creating the loft between two different shapes

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


point1 = geompy.MakeVertex(0,0,0)
point2 = geompy.MakeVertex(2,0,0)
point3 = geompy.MakeVertex(2,2,0)
point4 = geompy.MakeVertex(0,2,0)

line1 = geompy.MakeLineTwoPnt(point1,point2)
line2 = geompy.MakeLineTwoPnt(point2,point3)
line3 = geompy.MakeLineTwoPnt(point3,point4)
line4 = geompy.MakeLineTwoPnt(point4,point1)

face1 = geompy.MakeFaceWires([line1,line2,line3,line4],1)

circle_point = geompy.MakeVertex(1,1,4)
# create a circle from a point, a vector and a radius
circle1 = geompy.MakeCircle(circle_point, OZ, 0.5)

geompy.addToStudy(face1,'face1')
geompy.addToStudy(circle1,'circle1')


centre_point = geompy.MakeVertex(1,1,0)
path_line = geompy.MakeLineTwoPnt(centre_point,circle_point)

final = geompy.MakePipeWithDifferentSectionsBySteps([face1,circle1],[],path_line)
geompy.addToStudy(final,'final')

# simple extrude points
extrude_point_1 = geompy.MakeVertex(2,1,0)
extrude_point_2 = geompy.MakeVertex(0,1,0)

extrude_line_1 = geompy.MakeLineTwoPnt(point1,point2)
extrude_line_2 = geompy.MakeLineTwoPnt(point2,extrude_point_1)
extrude_line_3 = geompy.MakeLineTwoPnt(extrude_point_1,extrude_point_2)
extrude_line_4 = geompy.MakeLineTwoPnt(extrude_point_2,point1)

extrude_face = geompy.MakeFaceWires([extrude_line_1,extrude_line_2,extrude_line_3,extrude_line_4],1)
extrude = geompy.MakePrismVecH(extrude_face, OZ, 4)
geompy.addToStudy(extrude,'extrude')