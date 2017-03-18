import vtk

image = vtk.vtkImageData()
image.SetDimensions(200,200,1)
image.SetOrigin(-1,-1,0)
image.SetSpacing(.02,.02,0)


data = vtk.vtkDoubleArray()
data.SetNumberOfComponents(1)
data.SetNumberOfTuples(image.GetNumberOfPoints())
data.SetName("Values")

for i in range(image.GetNumberOfPoints()):
    x,y,z = image.GetPoint(i)
    data.SetValue(i,x**2+y**2+z**2)

image.GetPointData().AddArray(data)

image.AllocateScalars(vtk.VTK_DOUBLE, 1)
for z_id in range(image.GetDimensions()[2]):
    for y_id in range(image.GetDimensions()[1]):
        for x_id in range(image.GetDimensions()[0]):
            id = image.ComputePointId((x_id, y_id, z_id))
            value = image.GetPointData().GetArray("Values").GetValue(id)
            image.SetScalarComponentFromDouble(x_id, y_id, z_id, 0, value)


ms = vtk.vtkMarchingSquares()
ms.SetInputData(image)
ms.SetValue(0, .5)
ms.SetValue(1, 1.0)
ms.SetImageRange(0, image.GetDimensions()[0], 0, image.GetDimensions()[1], 0, 0)
ms.Update()

poly = ms.GetOutput()

from matplotlib import pyplot as plt
import numpy as np

xx = np.zeros(poly.GetNumberOfPoints())
yy = np.zeros(poly.GetNumberOfPoints())
for i in range(poly.GetNumberOfPoints()):
    x,y,z = poly.GetPoint(i)
    xx[i] = x
    yy[i] = y

lines = poly.GetLines()

lines.InitTraversal
lineIds = vtk.vtkIdList()

x_list = []
y_list = []

pts_x = []
pts_y = []
for i in range(poly.GetNumberOfPoints()):
    x,y,z = poly.GetPoint(i)
    pts_x.append(x)
    pts_y.append(y)

lineIndexArray = []
while lines.GetNextCell(lineIds):
    line = (lineIds.GetId(0),lineIds.GetId(1))
    lineIndexArray.append(line)

for i1, i2 in lineIndexArray:
    plt.plot([pts_x[i1], pts_x[i2]], [pts_y[i1], pts_y[i2]])