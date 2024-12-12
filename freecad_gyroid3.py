# creating the surface geometry for the in freecad

import FreeCAD as App
import Part

# Dimensions for the gyroids
size = 3.0              # size of the gyroids
radius = 0.5      # radius of the arc
thickness = 0.2

# create the new document
doc = App.newDocument('Gyroids')

# Creating the cordinate points for the gyroid structures
point1 = App.Vector(0, 0, 0)
point2 = App.Vector(size, 0, 0)
point3 = App.Vector(size, 0, size)
point4 = App.Vector(size, size, size)
point5 = App.Vector(0, size, size)
point6 = App.Vector(0, size, 0)


point7 = App.Vector(size-radius, 0, size/2)
point8 = App.Vector(size, size/2, size-radius)
point9 = App.Vector(size/2, size-radius, size)
point10 = App.Vector(radius, size, size/2)
point11 = App.Vector(0, size/2, radius)
point12 = App.Vector(size/2, radius, 0)

curve1 = Part.Arc(point2,point7,point3)
curve2 = Part.Arc(point3,point8,point4)
curve3 = Part.Arc(point4,point9,point5)
curve4 = Part.Arc(point5,point10,point6)
curve5 = Part.Arc(point6,point11,point1)
curve6 = Part.Arc(point1,point12,point2)

'''
Part.show(curve1.toShape())
Part.show(curve2.toShape())
Part.show(curve3.toShape())
Part.show(curve4.toShape())
Part.show(curve5.toShape())
Part.show(curve6.toShape())
'''


wire1 = Part.Wire([curve1.toShape(),curve2.toShape(),curve3.toShape(),curve4.toShape(),curve5.toShape(),curve6.toShape()])
Part.show(wire1,'wire1')
face1 = Part.makeFilledSurface([wire1])
Part.show(face1,'face1')



# create the gyroid face 2 offset at some distance
point13 = App.Vector(0,0,thickness)
point14 = App.Vector(size-(1.888*thickness),0,thickness)
point15 = App.Vector(size,0,size+thickness)
point16 = App.Vector(size,size-thickness,size)
point17 = App.Vector(0,size-thickness,size)
point18 = App.Vector(0,size-0.88*thickness,2*thickness)

point19 = App.Vector(size-radius-thickness,0,size/2)
point20 = App.Vector(size,size/2,size-radius+thickness)
point21 = App.Vector(size/2,size-radius-thickness,size)
point22 = App.Vector(radius,size-thickness,size/2)
point23 = App.Vector(0,size/2,radius+thickness)
point24 = App.Vector(size/2,radius,thickness)


curve7 = Part.Arc(point14,point19,point15)
curve8 = Part.Arc(point15,point20,point16)
curve9 = Part.Arc(point16,point21,point17)
curve10 = Part.Arc(point17,point22,point18)
curve11 = Part.Arc(point18,point23,point13)
curve12 = Part.Arc(point13,point24,point14)

wire2 = Part.Wire([curve7.toShape(),curve8.toShape(),curve9.toShape(),curve10.toShape(),curve11.toShape(),curve12.toShape()])
Part.show(wire2,'wire2')
face2 = Part.makeFilledSurface([wire2])
Part.show(face2,'face2')



# making the lines for joining
line1 = Part.LineSegment(point1,point13)
line2 = Part.LineSegment(point2,point14)
line3 = Part.LineSegment(point3,point15)
line4 = Part.LineSegment(point4,point16)
line5 = Part.LineSegment(point5,point17)
line6 = Part.LineSegment(point6,point18)


# make the surface
hwire1 =  Part.Wire([line1.toShape(),curve6.toShape(),line2.toShape(),curve12.toShape()])
surf1 = Part.makeFilledSurface([hwire1])
Part.show(surf1,'surf1')

hwire2 =  Part.Wire([line2.toShape(),curve1.toShape(),line3.toShape(),curve7.toShape()])
surf2 = Part.makeFilledSurface([hwire2])
Part.show(surf2,'surf2')

hwire3 =  Part.Wire([line3.toShape(),curve2.toShape(),line4.toShape(),curve8.toShape()])
surf3 = Part.makeFilledSurface([hwire3])
Part.show(surf3,'surf3')

hwire4 =  Part.Wire([line4.toShape(),curve3.toShape(),line5.toShape(),curve9.toShape()])
surf4 = Part.makeFilledSurface([hwire4])
Part.show(surf4,'surf4')

hwire5 =  Part.Wire([line6.toShape(),curve10.toShape(),line5.toShape(),curve4.toShape()])
surf5 = Part.makeFilledSurface([hwire5])
Part.show(surf5,'surf5')

hwire6 =  Part.Wire([line6.toShape(),curve5.toShape(),line1.toShape(),curve11.toShape()])
surf6 = Part.makeFilledSurface([hwire6])
Part.show(surf6,'surf6')

# create a solid from them
shell1 = Part.makeShell([face1,face2,surf1,surf2,surf3,surf4,surf5,surf6])
solid1 = Part.makeSolid(shell1)
Part.show(solid1,'solid1')


solid2 = solid1.translate(App.Vector(size,0,0))
Part.show(solid2,'solid2')

solid3 = solid1.translate(App.Vector(0,size,0))
Part.show(solid3,'solid3')


solid4 = solid1.translate(App.Vector(-size,0,0))
Part.show(solid4,'solid4')


solid5 = solid1.translate(App.Vector(0,0,size))
Part.show(solid5,'solid5')


solid6 = solid1.translate(App.Vector(size,0,0))
Part.show(solid6,'solid6')


solid7 = solid1.translate(App.Vector(0,-size,0))
Part.show(solid7,'solid7')


solid8 = solid1.translate(App.Vector(-size,0,0))
Part.show(solid8,'solid8')


solid7.rotated(App.Vector(size/2,size/2,size/2),App.Vector(0,0,1),180)





Gui.ActiveDocument.ActiveView.setAxisCross(True)
'''
thick = face1.makeOffsetShape(thickness,0.01,fill=True)
Part.show(thick,'thickened gyro')

box1 = Part.makeBox(size-thickness,size-thickness,size-thickness,App.Vector(-1e-5,-1e-5,-1e-5))
Part.show(box1,'box1')

new_gyrod = thick.common(box1,1e-11)
Part.show(new_gyrod,'new_gyrod')

final_length = size-thickness+1e-5

thick2 = face1.rotated(App.Vector(size/2,size/2,size/2),App.Vector(0,0,1),180)
thick2.translate(App.Vector(size,0,0))
Part.show(thick2,'thick2')

thick3 = thick2.fuse(face1)
Part.show(thick3,'thick3')

face4 = thick3.makeOffsetShape(thickness,0.01,fill=True)
'''