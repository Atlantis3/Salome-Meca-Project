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
import numpy as np
geompy = geomBuilder.New()
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

# Function to create a gyroid surface
def create_gyroid(a, resolution):
    points = []
    for i in np.linspace(-a, a, resolution):
        for j in np.linspace(-a, a, resolution):
            for k in np.linspace(-a, a, resolution):
                x = i
                y = j
                z = k
                # Gyroid equation
                if np.abs(np.sin(x) * np.cos(y) + np.sin(y) * np.cos(z) + np.sin(z) * np.cos(x)) < 0.001:
                    globals()[f'Vertex_{str(i)+str(j)+str(k)}'] = geompy.MakeVertex(x,y,z)
                    #geompy.addToStudy(globals()[f'Vertex_{str(i)+str(j)+str(k)}'],'Vertex_'+str(i)+str(j)+str(k))
                    points.append(globals()[f'Vertex_{str(i)+str(j)+str(k)}'])
    
    # Create vertices from the points
    #vertices = [geompy.MakeVertex(p[0], p[1], p[2]) for p in points]
    return points

# Parameters for the gyroid geometry
a = 2.0  # size of the domain
resolution = 30  # number of points per dimension

# Create the gyroid
gyroid_vertices = create_gyroid(a, resolution)
gyroid_surface = geompy.MakeSmoothingSurface(gyroid_vertices,2,8,0)
geompy.addToStudy(gyroid_surface,'gyroid_surface')
# Create a group for the gyroid vertices
#gyroid_group = geompy.CreateGroup(gyroid_vertices, 'GyroidVertices')

# Update the geometry
#geompy.Update()

#print("Gyroid geometry created with {} vertices.".format(len(gyroid_vertices)))
