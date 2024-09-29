# Created on 29.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creation of the complex geometry (Unit cells for geometry)
import numpy as np
# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
unitcell_size = 10.0      # size of the unit cell
radius = 0.3              # radius of the strut
shape_type = 'BCC'
n_cells_x = 10            # number of cells in x-direction
n_cells_y = 4             # number of cells in y-direction
n_cells_z = 2             # number of cells in z-direction





#------------------------------------------------------------------------------------
# Geometry post processing calculations
strut_length = unitcell_size/(np.sqrt(2))
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
#strut_1 = geompy.MakeCylinder(O, v1, radius, height)

if shape_type == 'BCC' :
    p1 = geompy.MakeVertex(0,unitcell_size,0)
    v1 = geompy.MakeVectorDXDYDZ(1,1,0)
    v2 = geompy.MakeVectorDXDYDZ(-1,1,0)
    v3 = geompy.MakeVectorDXDYDZ(0,1,1)
    v4 = geompy.MakeVectorDXDYDZ(0,1,-1)
    strut_1 = geompy.MakeCylinder(O, v1, radius, strut_length)
    strut_2 = geompy.MakeCylinder(O, v2, radius, strut_length)
    strut_3 = geompy.MakeCylinder(O, v3, radius, strut_length)
    strut_4 = geompy.MakeCylinder(O, v4, radius, strut_length)

    #geompy.addToStudy(strut_1,'strut_1')
    #geompy.addToStudy(strut_2,'strut_2')
    #geompy.addToStudy(strut_3,'strut_3')
    #geompy.addToStudy(strut_4,'strut_4')

    v5 = geompy.MakeVectorDXDYDZ(1,-1,0)
    v6 = geompy.MakeVectorDXDYDZ(-1,-1,0)
    v7 = geompy.MakeVectorDXDYDZ(0,-1,1)
    v8 = geompy.MakeVectorDXDYDZ(0,-1,-1)


    strut_5 = geompy.MakeCylinder(p1, v5, radius, strut_length)
    strut_6 = geompy.MakeCylinder(p1, v6, radius, strut_length)
    strut_7 = geompy.MakeCylinder(p1, v7, radius, strut_length)
    strut_8 = geompy.MakeCylinder(p1, v8, radius, strut_length)

    #geompy.addToStudy(strut_5,'strut_5')
    #geompy.addToStudy(strut_6,'strut_6')
    #geompy.addToStudy(strut_7,'strut_7')
    #geompy.addToStudy(strut_8,'strut_8')

    strut_9 = geompy.MakeCylinder(O,OY,radius,unitcell_size)
    #geompy.addToStudy(strut_9,'strut_9')

    # Fuse the struts together
    fused_struts = geompy.MakeFuseList([strut_1, strut_2, strut_3, strut_4, strut_5, strut_6, strut_7, strut_8, strut_9], True, True)

    # Create the extrusions for the unwanted edges
    trimface1 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(0,0,0)),geompy.MakeVertex(0,1,0)), 3*radius, 3*radius)
    trimface1_extrusion = geompy.MakePrismVecH(trimface1, OY, -1)
    
    trimface2 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(0,unitcell_size,0)),geompy.MakeVertex(0,unitcell_size-1,0)), 3*radius, 3*radius)
    trimface2_extrusion = geompy.MakePrismVecH(trimface2, OY, 1)

    trimface3 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(unitcell_size/2,unitcell_size/2,0)),geompy.MakeVertex(0,unitcell_size/2,0)), 3*radius, 3*radius)
    trimface3_extrusion = geompy.MakePrismVecH(trimface3, OX, 1)

    trimface4 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(-unitcell_size/2,unitcell_size/2,0)),geompy.MakeVertex(0,unitcell_size/2,0)), 3*radius, 3*radius)
    trimface4_extrusion = geompy.MakePrismVecH(trimface4, OX, -1)

    trimface5 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(0,unitcell_size/2,unitcell_size/2)),geompy.MakeVertex(0,unitcell_size/2,0)), 3*radius, 3*radius)
    trimface5_extrusion = geompy.MakePrismVecH(trimface5, OZ, 1)

    trimface6 = geompy.MakeFaceObjHW(geompy.MakeLineTwoPnt((geompy.MakeVertex(0,unitcell_size/2,-unitcell_size/2)),geompy.MakeVertex(0,unitcell_size/2,0)), 3*radius, 3*radius)
    trimface6_extrusion = geompy.MakePrismVecH(trimface6, OZ, -1)


    
    unit_cell = geompy.MakeCutList(fused_struts, [trimface1_extrusion,trimface2_extrusion,trimface3_extrusion,trimface4_extrusion,trimface5_extrusion,trimface6_extrusion], True)
    geompy.addToStudy(unit_cell,'unit_cell')



    #pass
else :
    raise Exception('The script for other type of shape is not yet written')


# multiple translation
Multi_Translation_1 = geompy.MakeMultiTranslation2D(unit_cell, OX, unitcell_size, n_cells_x, OY, unitcell_size, n_cells_y)
cellular_core = geompy.MakeMultiTranslation1D(Multi_Translation_1, OZ, unitcell_size, n_cells_z)

geompy.addToStudy(cellular_core,'cellular_core')

