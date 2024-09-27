# Python script for creating more complex geometry in the salome meca shaper module

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
Part_1 = model.addPart(partSet)
Part_1_doc = Part_1.document()
Sketch_1 = model.addSketch(Part_1_doc, model.standardPlane("XOZ"))
SketchPoint_1 = Sketch_1.addPoint(0, 0)
SketchProjection_1 = Sketch_1.addProjection(model.selection("VERTEX", "PartSet/Origin"), False)
SketchPoint_2 = SketchProjection_1.createdFeature()
SketchConstraintCoincidence_1 = Sketch_1.setCoincident(SketchPoint_1.coordinates(), SketchPoint_2.result())
SketchPoint_3 = Sketch_1.addPoint(366.6774716369531, 93.63371150729334)
SketchPoint_4 = Sketch_1.addPoint(365.3679092382498, 149.9448946515397)
SketchPoint_5 = Sketch_1.addPoint(0, 63.51377633711508)
SketchArc_1 = Sketch_1.addArc(117.6592100296317, 304.023390311361, 0, 0, 366.6774716369531, 93.63371150729334, False)
SketchConstraintCoincidence_2 = Sketch_1.setCoincident(SketchPoint_1.coordinates(), SketchArc_1.startPoint())
SketchConstraintCoincidence_3 = Sketch_1.setCoincident(SketchPoint_3.coordinates(), SketchArc_1.endPoint())
SketchArc_2 = Sketch_1.addArc(109.8002031148921, 414.8288304894933, 0, 63.51377633711508, 365.3679092382498, 149.9448946515397, False)
SketchConstraintCoincidence_4 = Sketch_1.setCoincident(SketchPoint_5.coordinates(), SketchArc_2.startPoint())
SketchConstraintCoincidence_5 = Sketch_1.setCoincident(SketchPoint_4.coordinates(), SketchArc_2.endPoint())
SketchLine_1 = Sketch_1.addLine(0, 63.51377633711508, 0, 0)
SketchConstraintCoincidence_6 = Sketch_1.setCoincident(SketchPoint_5.coordinates(), SketchLine_1.startPoint())
SketchConstraintCoincidence_7 = Sketch_1.setCoincident(SketchPoint_1.coordinates(), SketchLine_1.endPoint())
SketchLine_2 = Sketch_1.addLine(365.3679092382498, 149.9448946515397, 366.6774716369531, 93.63371150729333)
SketchConstraintCoincidence_8 = Sketch_1.setCoincident(SketchPoint_4.coordinates(), SketchLine_2.startPoint())
SketchConstraintCoincidence_9 = Sketch_1.setCoincident(SketchPoint_3.coordinates(), SketchLine_2.endPoint())
model.do()
Revolution_1 = model.addRevolution(Part_1_doc, [model.selection("FACE", "Sketch_1/Face-SketchArc_1_2f-SketchLine_2r-SketchArc_2_2r-SketchLine_1f")], model.selection("EDGE", "Sketch_1/SketchLine_1"), 90, 0)
model.do()
model.end()

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()