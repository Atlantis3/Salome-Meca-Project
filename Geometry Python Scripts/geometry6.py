# Created on 26.09.2024 author @ akram.metar@stud.tu-darmstadt.de
# Salome Meca Python script for creating the wing of the D45 Project at Akaflieg Darmstadt
# This file contains the python script for creating the geometry of the D45 Project wing

import numpy as np
#import pandas as pd



# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 5

# 2. The location of the profile from the wing root in mm
profile_x_cordinates = np.array([0.4005700570057006,4.435503550355036, 5.960356035603561, 6.907660766076608, 7.500220022002201])/1000.0     

# 3. The location of the profile from the wing root in mm
profile_y_cordinates = np.array([0.7342962755033171, 0.6084542900928411, 0.48261230468236516, 0.3567703192718892, 0.23092833386141318])/1000.0   

# 4. location to dat file for the airfoil profile
profile_1 = np.loadtxt('/home/akram_metar/D_Drive/Akaflieg/D45 Wing Data/Wing profiles 20240805/D45-1-132-15-F0-V6.csv',delimiter=',')



#------------------------------------------------------------------------------------
# Pre calculations for the preparation of the CAD Model

# check if the input data is correct
if len(profile_x_cordinates) != n_profiles :
    raise Exception('The number of profiles and the locations for x cordinates do not match, Please check the input data !')
elif len(profile_y_cordinates) != n_profiles:
    raise Exception('The number of profiles and the locations for the y cordinates do not match. Please check the input data !')

profile_1_x_cordinates = profile_1[:,0]
profile_1_y_cordinates = profile_1[:,1]






#=======================================================================
#============ Geometry module Salome Meca ==============================
#=======================================================================
import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/akram_metar/D_Drive/Github/Git/Salome Meca Project/Geometry Python Scripts')

###
### SHAPER component
###

from salome.shaper import model

model.begin()
partSet = model.moduleDocument()

### Create Part
Part_1 = model.addPart(partSet)
Part_1_doc = Part_1.document()

model.do()


### Create Part
Part_2 = model.addPart(partSet)
Part_2_doc = Part_2.document()

### Create Point
Point_2 = model.addPoint(Part_2_doc, 0, 0, 0)

### Create Point
Point_3 = model.addPoint(Part_2_doc, 5, 2, 0)

### Create Point
Point_4 = model.addPoint(Part_2_doc, 3, 4, 0)

### Create Point
Point_5 = model.addPoint(Part_2_doc, 0, 0, 6)

### Create Point
Point_6 = model.addPoint(Part_2_doc, 6, 3, 6)

### Create Point
Point_7 = model.addPoint(Part_2_doc, 3, 4, 6)

# create a polyline
### Create Polyline
Polyline_1_objects = [Point_2.result(),Point_3.result(),Point_4.result()]
Polyline_1 = model.addPolyline3D(Part_2_doc, Polyline_1_objects, True)
Polyline_2_objects = [Point_5.result(),Point_6.result(),Point_7.result()]
Polyline_2 = model.addPolyline3D(Part_2_doc,Polyline_2_objects,True)
Loft_1 = model.addLoft(Part_2_doc,Polyline_1.result(), Polyline_2.result())