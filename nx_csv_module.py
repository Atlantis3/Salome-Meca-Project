# import all the necessary modules
import NXOpen
import csv

# ========================================================
# ======== Geometry parameterisation =====================
# ========================================================
# 1. number of profiles in the wing
n_profiles = 6

# 2. The distance of the profile from the centreline of the fuselage in the direction of the wing tip in mm
wing_section_y_cordinates = [0.35,2.1774,4.5496,6.0039,6.948,7.5]     
wing_section_y_cordinates = [x*-1000.0/2.0 for x in wing_section_y_cordinates]

# 3. The distance of the profile leading edge from the wing root in the direction of the tariling edge in mm
wing_section_x_cordinates = [0.0,0.014025,0.10489,0.214318,0.3234744,0.430468] 
wing_section_x_cordinates = [x*1000.0/2.0 for x in wing_section_x_cordinates]

# 4. The length of the chordline of the profile in mm
wing_section_chord_length = [0.7319,0.7154,0.6085,0.4826,0.3568,0.2309]
wing_section_chord_length = [x*1000.0/2.0 for x in wing_section_chord_length]

# 5. location to csv file 
profile_1_path = ''
profile_2_path = ''
profile_3_path = ''
profile_4_path = ''
profile_5_path = ''
profile_6_path = ''

# 6. the dimensions for the foam in mm
foam_length = 2000 
foam_width = 625
foam_thickness = 80

#-------------------------------------------------------------------------------------------
#------ Creation of the data --------------------------------------------------------
#-------------------------------------------------------------------------------------------

# check if the input data is correct
if len(wing_section_y_cordinates) != n_profiles :
    raise Exception('The number of profiles and the locations for it in the y-direction do not match, Please check the input data !')
elif len(wing_section_x_cordinates) != n_profiles:
    raise Exception('The number of profiles and the locations for it in the  x-direction do not match. Please check the input data !')
elif len(wing_section_chord_length) != n_profiles:
    raise Exception('The number of profiles and the locations for it in the  x-direction do not match. Please check the input data !')

profile_paths = [profile_1_path,profile_2_path,profile_3_path,profile_4_path,profile_5_path,profile_6_path]


for count,value in enumerate (profile_paths):
    with open(value, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = []
        for row in csv_reader:
            data.append(row)
    
    # Read the data
    
    
    globals()[f'profile_{count+1}_x_cordinates'] = []
    globals()[f'profile_{count+1}_y_cordinates'] = []
    for count2,value2 in enumerate (data):
        x_value = float(value2[0])
        y_value = float(value2[1])
        globals()[f'profile_{count+1}_x_cordinates'].append(x_value*wing_section_chord_length[count]+wing_section_x_cordinates[count])
        globals()[f'profile_{count+1}_y_cordinates'].append(y_value*wing_section_chord_length[count])


points = []
for count,value in enumerate(profile_1_x_cordinates):
    point = workPart.Points.CreatePoint(NXOpen.Point3d(profile_1_x_cordinates[count], profile_1_y_cordinates[count], wing_section_y_cordinates[0]))
    points.append(point)
    point.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)

# Create lines between the points
lines = []
for i in range(len(points)):
    start_point = points[i]
    end_point = points[(i + 1) % len(points)]  # Loop back to the first point
    line = workPart.Curves.CreateLine(start_point, end_point)
    line.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
    lines.append(line)

