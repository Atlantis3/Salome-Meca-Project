# Plotting the data extracted from the result file of the Salome Meca 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the txt file
df1 = pd.read_csv('/home/akram_metar/D_Drive/Salome_meca/Disk_geometry/disk_top_nodes.txt',skiprows=4,sep='\s+').groupby('NUME_ORDRE')

# displacement of the nodes and extracting the load from all the nodes
displacement = np.linspace(0,-0.15,31)
df1_load = []
for count,value in enumerate(displacement):
    y = df1.get_group(count)['DY'].sum()
    df1_load.append(y)

# Plotting the results 
fig1,ax1 = plt.subplots()
ax1.plot(displacement,df1_load,label='Disk Problem')
ax1.set_title('Load Displacement Curve')
ax1.set_xlabel('Deflection in mm')
ax1.set_ylabel('Load in N')
ax1.grid()
ax1.legend()
fig1.set_figheight(5)
fig1.set_figwidth(10)
plt.show()