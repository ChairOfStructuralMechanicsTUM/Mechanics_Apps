from bokeh.plotting import figure, output_file, show,ColumnDataSource
import numpy as np
import Cantilever_beam_classes as functions

# Create the deformed beam center-line
noElementsX = 50
noElementsY = 10

beamLength = 5.0
beamHeight = 1.0
beamThickness = 1.0

axialDirElementSize = beamLength / noElementsX
lateralDirElementSize = beamHeight / noElementsY

deformedBeam = list()
# v(x) = Px^2(3L - x)/6EI
# I = bh^3/12
# strainxx(top) = -6P(L-x)/bh^2E
# strainxx(bottom) = 6P(L-x)/bh^2E
amplificationFactor = 1000        
P = -1000
E = 1000000000
I = beamThickness*beamHeight*beamHeight*beamHeight/12
xComponent = 0.0
yComponent = 0.0
for i in range(noElementsX + 1):
    yComponent = amplificationFactor*P*xComponent*xComponent*( 3*beamLength - xComponent )/(6*E*I)
    deformedBeam.append( [xComponent, yComponent] )
    angle = np.arctan((P/E*I)*(beamLength*xComponent-xComponent*xComponent/2))
    xIncrement = axialDirElementSize*np.cos(angle)
    xComponent += xIncrement
    
# constricuting normals  
averageNormalVector1, averageNormalVector2 = functions.construct_normal_vectors( deformedBeam )

listDeformedElements = functions.construct_deformed_elements( deformedBeam,
                                                              axialDirElementSize,
                                                              lateralDirElementSize,
                                                              noElementsX,
                                                              noElementsY,
                                                              averageNormalVector1,
                                                              averageNormalVector2
                                                            )

listXCoord = list()
listYCoord = list()
for element in listDeformedElements:
    listXCoord.append([ element.lowerLeftPosition[0]  , 
                        element.upperLeftPosition[0]  ,
                        element.upperRightPosition[0] ,
                        element.lowerRightPosition[0] ])
    listYCoord.append([ element.lowerLeftPosition[1]  , 
                        element.upperLeftPosition[1]  ,
                        element.upperRightPosition[1] ,
                        element.lowerRightPosition[1] ])
    
biggestValueXY = abs(P)*beamLength / (beamHeight*beamThickness*beamThickness)
smallestValueXY = -abs(P)*beamLength / (beamHeight*beamThickness*beamThickness)
colorList = functions.elements_color_determiner( True,
                                                 listDeformedElements,
                                                 noElementsX,
                                                 noElementsY,
                                                 E, beamHeight,
                                                 beamThickness,
                                                 beamLength, P,
                                                 biggestValueXY, smallestValueXY, None
                                               )
alphaList = list()
for index in range(len(listDeformedElements)):
    alphaList.append(1)

output_file("deformedMesh.html")
p2 = figure(plot_width=1000, plot_height=1000,x_range = (0,beamLength + 1),y_range=(-beamHeight-2,beamHeight+2))
p2.patches(listXCoord, listYCoord, color = colorList, alpha = alphaList, line_width=0.5)
show(p2)
