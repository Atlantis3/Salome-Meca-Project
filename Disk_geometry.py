# Created on 28.07.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for Finite Element Simulation of a 2d disk problem
# This file contains the python script for creating the geometry and the mesh for a simple 2d disk problem using the geompy module and the smesh module

# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
length = 20.0        # The length of the disk (mm)
height = 0.4         # The height of the disk (mm)

# ========================================================
# ======== Mesh parameterisation =====================
# ========================================================
local_length_element = height/4.0         # The local size of the element (mm)



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

# Creating the geometry of the disk
top_liner_point_1 = geompy.MakeVertex(0.0, 0.0,0.0 )
top_liner_point_2 = geompy.MakeVertex(length, 0.0, 0.0 )
top_liner_point_3 = geompy.MakeVertex(length, height, 0.0)
top_liner_point_4 = geompy.MakeVertex(0, height, 0.0 )

t_l_line_1 = geompy.MakeLineTwoPnt(top_liner_point_1,top_liner_point_2)
t_l_line_2 = geompy.MakeLineTwoPnt(top_liner_point_2,top_liner_point_3)
t_l_line_3 = geompy.MakeLineTwoPnt(top_liner_point_3,top_liner_point_4)
t_l_line_4 = geompy.MakeLineTwoPnt(top_liner_point_4,top_liner_point_1)

disk = geompy.MakeFaceWires([t_l_line_1,t_l_line_2,t_l_line_3,t_l_line_4],1)
geompy.addToStudy(disk,'disk')

# Creating the group for the disk
fixed_line_obj = geompy.GetInPlace(disk,t_l_line_1,True)
fixed_line = geompy.CreateGroup(disk, geompy.ShapeType["EDGE"])
geompy.UnionList(fixed_line,[fixed_line_obj])
geompy.addToStudyInFather(disk,fixed_line,'fixed_line')

load_line_obj = geompy.GetInPlace(disk,t_l_line_3,True)
load_line = geompy.CreateGroup(disk,geompy.ShapeType["EDGE"])
geompy.UnionList(load_line,[load_line_obj])
geompy.addToStudyInFather(disk,load_line,'load_line')


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

disk_mesh = smesh.Mesh(disk)
Regular_1D = disk_mesh.Segment()
Local_Length_1 = Regular_1D.LocalLength(local_length_element,None,1e-07)
Quadrangle_2D = disk_mesh.Quadrangle(algo=smeshBuilder.QUADRANGLE)

fixed_line_1 = disk_mesh.GroupOnGeom(fixed_line,'fixed_line',SMESH.EDGE)
load_line_1 = disk_mesh.GroupOnGeom(load_line,'load_line',SMESH.EDGE)

fixed_line_2 = disk_mesh.GroupOnGeom(fixed_line,'fixed_line',SMESH.NODE)
load_line_2 = disk_mesh.GroupOnGeom(load_line,'load_line',SMESH.NODE)

isDone = disk_mesh.Compute()


## Set names of Mesh objects
smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
smesh.SetName(Quadrangle_2D.GetAlgorithm(), 'Quadrangle_2D')
smesh.SetName(Local_Length_1, 'Local Length_1')
smesh.SetName(disk_mesh.GetMesh(), 'disk_mesh')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()

