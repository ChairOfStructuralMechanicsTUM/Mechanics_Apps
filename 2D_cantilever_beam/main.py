import Cantilever_beam_classes as functions
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models import Slider, LabelSet, Div
from bokeh.models import Arrow, NormalHead, OpenHead
from os.path import dirname, join, split
from bokeh.models.layouts import Spacer

# Define basic beam parameters and loading
length = 5.0
height = 1.0
thickness = 1.0
E = 1000000000
Py = 0 #-1000
Pz = 0 #2000

# Define mesh for visualization
noElementsX = 80
noElementsY = 20
noElementsZ = 20
elementSizeX = length / noElementsX
elementSizeY = height / noElementsY
elementSizeZ = thickness / noElementsZ
amplificationFactor = 100

def deformed_cantilever_beam_determiner_XY( 
                                            length, height, thickness, E, Py, 
                                            Pz, noElementsX, noElementsY, 
                                            noElementsZ, elementSizeX, 
                                            elementSizeY, elementSizeZ, 
                                            amplificationFactor
                                          ):
    # Construct the deformed beam's center line
    deformedBeamXY, deformedBeamXZ = functions.construct_deformed_beam_centerLine(
                                                                                      Py, Pz, E, 
                                                                                      noElementsX,
                                                                                      thickness, height, 
                                                                                      length, elementSizeX,
                                                                                      amplificationFactor
                                                                                 )
    
    # Construct the normal vectors to the deformed beam's center line
    normalVecrtorsXYUpperDef, normalVectorsXYLowerDef = functions.construct_normal_vectors( deformedBeamXY )
    
    # Construct mesh for the deformed and the deformed beams    
    listDeformedElementsXY = functions.construct_deformed_elements(   
                                                                      deformedBeamXY,
                                                                      elementSizeX,
                                                                      elementSizeY,
                                                                      noElementsX,
                                                                      noElementsY,
                                                                      normalVecrtorsXYUpperDef,
                                                                      normalVectorsXYLowerDef
                                                                  )
    
    # Determine the patches' X,Y,Z coordinates
    XCoordsDefXY , YCoordsDefXY = functions.create_coordinates_list( listDeformedElementsXY )
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
                                                                                                        Py, Pz,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXY = functions.elements_color_determiner(
                                                                  True,
                                                                  'XY',
                                                                  listDeformedElementsXY,
                                                                  noElementsX,
                                                                  noElementsY,
                                                                  E, height, thickness,
                                                                  length, Py, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXZ
                                                             )

    return (
                listDeformedElementsXY,
                XCoordsDefXY,
                YCoordsDefXY,
                listValuesUpperXY,
                colorListDeformedXY, 
                biggestValue, smallestValue
           )
    
def deformed_cantilever_beam_determiner_XZ( 
                                           length, height, thickness, E, Py, 
                                           Pz, noElementsX, noElementsY, 
                                           noElementsZ, elementSizeX, 
                                           elementSizeY, elementSizeZ,
                                           amplificationFactor
                                          ):
    
    # Construct the deformed beam's center line
    deformedBeamXY, deformedBeamXZ = functions.construct_deformed_beam_centerLine(
                                                                                      Py, Pz, E, 
                                                                                      noElementsX,
                                                                                      thickness, height, 
                                                                                      length, elementSizeX,
                                                                                      amplificationFactor
                                                                                 )
    
    # Construct the normal vectors to the deformed beam's center line
    normalVecrtorsXZUpperDef, normalVectorsXZLowerDef = functions.construct_normal_vectors( deformedBeamXZ )
    
    # Construct mesh for the deformed and the deformed beams     
    listDeformedElementsXZ = functions.construct_deformed_elements(   
                                                                      deformedBeamXZ,
                                                                      elementSizeX,
                                                                      elementSizeZ,
                                                                      noElementsX,
                                                                      noElementsZ,
                                                                      normalVecrtorsXZUpperDef,
                                                                      normalVectorsXZLowerDef
                                                                  )
    
    # Determine the patches' X,Y,Z coordinates
    XCoordsDefXZ , YCoordsDefXZ = functions.create_coordinates_list( listDeformedElementsXZ )
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
                                                                                                        Py, Pz,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXZ = functions.elements_color_determiner(
                                                                  True,
                                                                  'XZ',
                                                                  listDeformedElementsXZ,
                                                                  noElementsX,
                                                                  noElementsZ,
                                                                  E, thickness, height,
                                                                  length, Pz, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXY
                                                             )

    return (
                listDeformedElementsXZ,
                XCoordsDefXZ,
                YCoordsDefXZ,
                listValuesLowerXZ,
                colorListDeformedXZ,
                biggestValue, smallestValue
           )

def undeformed_cantilever_beam_determiner( 
                                          length, height, thickness, E, Py, Pz,
                                          noElementsX, noElementsY, 
                                          noElementsZ, elementSizeX, 
                                          elementSizeY, elementSizeZ,
                                          amplificationFactor 
                                         ):
    
    # Construct The undeformed beam's center line
    undeformedBeamXY, undeformedBeamXZ = functions.construct_undeformed_beam_centerline( 
                                                                                            noElementsX, 
                                                                                            noElementsY, 
                                                                                            noElementsZ,
                                                                                            elementSizeX
                                                                                       )

    # Construct normal vectors for both XY and XZ projections of the beam
    normalVecrtorsXYUpperUndef, normalVectorsXYLowerUndef = functions.construct_normal_vectors( undeformedBeamXY )
    normalVecrtorsXZUpperUndef, normalVectorsXZLowerUndef = functions.construct_normal_vectors( undeformedBeamXZ )

    # Construct mesh for the undeformed and the deformed beams    
    listUndeformedElementsXY = functions.construct_deformed_elements( 
                                                                        undeformedBeamXY,
                                                                        elementSizeX,
                                                                        elementSizeY,
                                                                        noElementsX,
                                                                        noElementsY,
                                                                        normalVecrtorsXYUpperUndef,
                                                                        normalVectorsXYLowerUndef
                                                                    )
    listUndeformedElementsXZ = functions.construct_deformed_elements( 
                                                                        undeformedBeamXZ,
                                                                        elementSizeX,
                                                                        elementSizeZ,
                                                                        noElementsX,
                                                                        noElementsZ,
                                                                        normalVecrtorsXZUpperUndef,
                                                                        normalVectorsXZLowerUndef
                                                                    )
    
    # Determine the patches' X,Y,Z coordinates
    XCoordsUndefXY , YCoordsUndefXY = functions.create_coordinates_list( listUndeformedElementsXY )
    XCoordsUndefXZ , YCoordsUndefXZ = functions.create_coordinates_list( listUndeformedElementsXZ )

    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
                                                                                                        Py, Pz,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX
                                                                                                   )
    # Coloring the undeformed elements
    colorListUndeformedXY = functions.elements_color_determiner(
                                                                    False,
                                                                    'XY',
                                                                    listUndeformedElementsXY,
                                                                    noElementsX,
                                                                    noElementsY,
                                                                    E, height, thickness,
                                                                    length, Py, 
                                                                    smallestValue, biggestValue,
                                                                    listValuesLowerXZ
                                                               )    
    colorListUndeformedXZ = functions.elements_color_determiner(
                                                                    False,
                                                                    'XZ',
                                                                    listUndeformedElementsXZ,
                                                                    noElementsX,
                                                                    noElementsZ,
                                                                    E, thickness, height,
                                                                    length, Pz, 
                                                                    biggestValue, smallestValue,
                                                                    listValuesUpperXY
                                                               )

    return (
                listUndeformedElementsXY, listUndeformedElementsXY,
                XCoordsUndefXY, XCoordsUndefXZ,
                YCoordsUndefXY, YCoordsUndefXZ, 
                colorListUndeformedXY, colorListUndeformedXZ,
                biggestValue, smallestValue
           )    

# Construct the deformed beam in XY plane
(listDeformedElementsXY, XCoordsDefXY,
 YCoordsDefXY, listValuesUpperXY, colorListDeformedXY,
 biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XY( 
                               length, height, thickness, E, Py, Pz,
                               noElementsX, noElementsY, noElementsZ,
                               elementSizeX, elementSizeY, elementSizeZ,
                               amplificationFactor
                           )

# Construct the deformed beam in XZ plane
(listDeformedElementsXZ, XCoordsDefXZ,
 YCoordsDefXZ, listValuesLowerXZ, colorListDeformedXZ,
 biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XZ( 
                               length, height, thickness, E, Py, Pz,
                               noElementsX, noElementsY, noElementsZ,
                               elementSizeX, elementSizeY, elementSizeZ,
                               amplificationFactor
                           )

# Construct the undeformed beams in XY and XZ planes
(listUndeformedElementsXY, listUndeformedElementsXZ, XCoordsUndefXY,
 XCoordsUndefXZ, YCoordsUndefXY, YCoordsUndefXZ,
 colorListUndeformedXY, colorListUndeformedXZ,
 biggestValue, smallestValue) = undeformed_cantilever_beam_determiner( 
                               length, height, thickness, E, Py, Pz,
                               noElementsX, noElementsY, noElementsZ,
                               elementSizeX, elementSizeY, elementSizeZ,
                               amplificationFactor
                           )
    
# Create alpha list for the transparency of the colored patches
alphaList = list()
for index in range(len(listDeformedElementsXY)):
    alphaList.append(1)


# The function to be excuted whenever the force in the y direction changes
def fun_change_Py(attrname, old, new):
    global Py, listDeformedElementsXY
    
    # Change the value of the applied force according to the slider value
    Py = Yforce_slider.value

    # Recalculate the deformed beam's shape
    (listDeformedElementsXY, XCoordsDefXY,
     YCoordsDefXY, listValuesUpperXY, colorListDeformedXY,
     biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XY( 
                                   length, height, thickness, E, Py, Pz,
                                   noElementsX, noElementsY, noElementsZ,
                                   elementSizeX, elementSizeY, elementSizeZ,
                                   amplificationFactor
                               )
    
    # Update the global variable the describes the deformed elements
    listDeformedElementsXY = listDeformedElementsXY
    
    # Determine the change of the color in the other view (XZ plane)
    colorListDeformedXZ = functions.elements_color_determiner(
                                                                  True,
                                                                  'XZ',
                                                                  listDeformedElementsXZ,
                                                                  noElementsX,
                                                                  noElementsZ,
                                                                  E, thickness, height,
                                                                  length, Pz, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXY
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXZdef.data   = dict( x=sourceXZdef.data['x'], y=sourceXZdef.data['y'], c=colorListDeformedXZ, a=alphaList)
    sourceXYdef.data   = dict( x=XCoordsDefXY,   y=YCoordsDefXY,   c =colorListDeformedXY,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards
    if sourceXYdef.data['y'][0][3] <= 0:
        sourceArrowXY.data = dict(
                                      xs=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ys=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-2][2]+1.5*abs(Py)/5000+0.25],
                                      xe=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ye=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-2][2]],
                                 )
        sourceFyLabel.data = dict(
                                      x= sourceArrowXY.data['xs'],
                                      y= [sourceArrowXY.data['ys'][0] + 0.5],
                                      f= ['Fy']
                                 )
    else:
        sourceArrowXY.data = dict(
                                      xs=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ys=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-1][2]-1.5*abs(Py)/5000-0.25],
                                      xe=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ye=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-1][2]],
                                 )
        sourceFyLabel.data = dict(
                                      x= sourceArrowXY.data['xs'],
                                      y= [sourceArrowXY.data['ys'][0] - 0.5],
                                      f= ['Fy']
                                 )
        
    update_colorBar_extremas(smallestValue,biggestValue)

        
# The function to be excuted whenever the force in the z direction changes
def fun_change_Pz(attrname, old, new):
    global Pz, listDeformedElementsXZ
    
    # Change the value of the applied force according to the slider value
    Pz = Zforce_slider.value

    # Recalculate the deformed beam's shape
    (listDeformedElementsXZ, XCoordsDefXZ, YCoordsDefXZ, 
     listValuesLowerXZ, colorListDeformedXZ, biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XZ( 
                                   length, height, thickness, E, Py, Pz,
                                   noElementsX, noElementsY, noElementsZ,
                                   elementSizeX, elementSizeY, elementSizeZ,
                                   amplificationFactor
                               )
    
    # Update the global variable the describes the deformed elements
    listDeformedElementsXZ = listDeformedElementsXZ
    
    # Determine the change of the color in the other view (XY plane)
    colorListDeformedXY = functions.elements_color_determiner(
                                                                  True,
                                                                  'XY',
                                                                  listDeformedElementsXY,
                                                                  noElementsX,
                                                                  noElementsY,
                                                                  E, thickness, height,
                                                                  length, Py, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXZ
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXYdef.data   = dict( x=sourceXYdef.data['x'], y=sourceXYdef.data['y'], c=colorListDeformedXY, a=alphaList)
    sourceXZdef.data   = dict( x=XCoordsDefXZ,   y=YCoordsDefXZ,   c =colorListDeformedXZ,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards
    if sourceXZdef.data['y'][0][3] <= 0:
        sourceArrowXZ.data = dict(
                                      xs=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-2][2]+1.5*abs(Pz)/5000+0.25],
                                      xe=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ye=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-2][2]],
                                 )
        sourceFzLabel.data = dict(
                                      x= sourceArrowXZ.data['xs'],
                                      y= [sourceArrowXZ.data['ys'][0] + 0.5],
                                      f= ['Fz']
                                 )
    else:
        sourceArrowXZ.data = dict(
                                      xs=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]-1.5*abs(Pz)/5000-0.25],
                                      xe=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ye=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]],
                                 )
        sourceFzLabel.data = dict(
                                      x= sourceArrowXZ.data['xs'],
                                      y= [sourceArrowXZ.data['ys'][0] - 0.5],
                                      f= ['Fz']
                                 )
        
    update_colorBar_extremas(smallestValue,biggestValue)

        
def init_data():
    fun_change_Py(None,None,None)
    fun_change_Pz(None,None,None)


# Construct the source file of all the beams
sourceXYundef = ColumnDataSource(data=dict( x=XCoordsUndefXY, y=YCoordsUndefXY, c =colorListUndeformedXY, a=alphaList ))
sourceXYdef   = ColumnDataSource(data=dict( x=XCoordsDefXY,   y=YCoordsDefXY,   c =colorListDeformedXY,   a=alphaList ))
sourceXZundef = ColumnDataSource(data=dict( x=XCoordsUndefXZ, y=YCoordsUndefXZ, c =colorListUndeformedXZ, a=alphaList ))
sourceXZdef   = ColumnDataSource(data=dict( x=XCoordsDefXZ,   y=YCoordsDefXZ,   c =colorListDeformedXZ,   a=alphaList ))

# Construct the source file of both the arrows
sourceArrowXY = ColumnDataSource(
                                     data=dict( 
                                                   xs=[sourceXYdef.data['x'][len( sourceXYdef.data['x'])-2][2]], 
                                                   ys=[1.5],
                                                   xe=[sourceXYdef.data['x'][len( sourceXYdef.data['x'])-2][2]], 
                                                   ye=[sourceXYdef.data['y'][len( sourceXYdef.data['y'])-2][2]],                            
                                              )
                                )
sourceArrowXZ = ColumnDataSource(
                                     data=dict( 
                                                   xs=[sourceXZdef.data['x'][len( sourceXYdef.data['x'])-2][2]], 
                                                   ys=[1.5],
                                                   xe=[sourceXZdef.data['x'][len( sourceXYdef.data['x'])-2][2]], 
                                                   ye=[sourceXZdef.data['y'][len( sourceXYdef.data['y'])-2][2]],                            
                                              )
                                )
                                     
# Construct the source files for the force labels
sourceFyLabel = ColumnDataSource(data=dict( x=[length], y=[height+0.5], f=['Fy'] ))
sourceFzLabel = ColumnDataSource(data=dict( x=[length], y=[height+0.5], f=['Fz'] ))

# Construct the force sliders
Yforce_slider = Slider(title="Y-direction Force", value=0, start=-5000, end=5000, step=100)
Zforce_slider = Slider(title="Z-direction Force", value=0, start=-5000, end=5000, step=100)

# Construct the figures which will visulize the beams
plotUndefXY = Figure(    
                         plot_width=350    , 
                         plot_height=350   ,
                         x_range = ( 0,6 ) ,
                         y_range= ( -3,3 ) ,
                         title = 'Undefromed Cofiguration in XY plane',
                         tools = '',
                    )
plotUndefXY.xaxis.major_tick_line_color=None
plotUndefXY.xaxis.major_label_text_color=None
plotUndefXY.xaxis.minor_tick_line_color=None
plotUndefXY.yaxis.major_tick_line_color=None
plotUndefXY.yaxis.major_label_text_color=None
plotUndefXY.yaxis.minor_tick_line_color=None
plotUndefXY.grid.visible = False
plotUndefXY.title.text_font_size="12.5pt"
plotUndefXY.xaxis.axis_label_text_font_size="14pt"
plotUndefXY.yaxis.axis_label_text_font_size="14pt"
plotUndefXY.xaxis.axis_label="x"
plotUndefXY.yaxis.axis_label="y"

plotDefXY = Figure(    
                       plot_width=350    , 
                       plot_height=350   ,
                       x_range = ( 0,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Defromed Cofiguration in XY plane',
                       tools = ''
                  )
plotDefXY.xaxis.major_tick_line_color=None
plotDefXY.xaxis.major_label_text_color=None
plotDefXY.xaxis.minor_tick_line_color=None
plotDefXY.yaxis.major_tick_line_color=None
plotDefXY.yaxis.major_label_text_color=None
plotDefXY.yaxis.minor_tick_line_color=None
plotDefXY.grid.visible = False
plotDefXY.title.text_font_size="12.5pt"
plotDefXY.xaxis.axis_label_text_font_size="14pt"
plotDefXY.yaxis.axis_label_text_font_size="14pt"
plotDefXY.xaxis.axis_label="x"
plotDefXY.yaxis.axis_label="y"

plotUndefXZ = Figure(    
                         plot_width=350    , 
                         plot_height=350   ,
                         x_range = ( 0,6 ) ,
                         y_range= ( -3,3 ) ,
                         title = 'Undefromed Cofiguration in XZ plane',
                         tools = ''
                    )
plotUndefXZ.xaxis.major_tick_line_color=None
plotUndefXZ.xaxis.major_label_text_color=None
plotUndefXZ.xaxis.minor_tick_line_color=None
plotUndefXZ.yaxis.major_tick_line_color=None
plotUndefXZ.yaxis.major_label_text_color=None
plotUndefXZ.yaxis.minor_tick_line_color=None
plotUndefXZ.grid.visible = False
plotUndefXZ.title.text_font_size="12.5pt"
plotUndefXZ.xaxis.axis_label_text_font_size="14pt"
plotUndefXZ.yaxis.axis_label_text_font_size="14pt"
plotUndefXZ.xaxis.axis_label="x"
plotUndefXZ.yaxis.axis_label="z"

plotDefXZ = Figure(    
                       plot_width=350    , 
                       plot_height=350   ,
                       x_range = ( 0,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Defromed Cofiguration in XZ plane',
                       tools = ''
                  )
plotDefXZ.xaxis.major_tick_line_color=None
plotDefXZ.xaxis.major_label_text_color=None
plotDefXZ.xaxis.minor_tick_line_color=None
plotDefXZ.yaxis.major_tick_line_color=None
plotDefXZ.yaxis.major_label_text_color=None
plotDefXZ.yaxis.minor_tick_line_color=None
plotDefXZ.grid.visible = False
plotDefXZ.title.text_font_size="12.5pt"
plotDefXZ.xaxis.axis_label_text_font_size="14pt"
plotDefXZ.yaxis.axis_label_text_font_size="14pt"
plotDefXZ.xaxis.axis_label="x"
plotDefXZ.yaxis.axis_label="z"

# Construct the color-bar figure
colorBar = Figure(
                      title = '',
                      title_location="below",
                      plot_width=700,
                      plot_height=75,
                      x_range=(0,5),
                      y_range=(-0.5,0.5),   
                      tools = ''
                 )
colorBar.xaxis.visible = False
colorBar.yaxis.visible = False
colorBar.title.text_font_size="16pt"

# create colorBar patches
colorBarXCoords = list()
colorBarYCoords = list()
for i in range(50):
    lowerLeft = [i/10 , -0.5]
    upperLeft = [i/10 , 0.5]
    lowerRight= [i/10 + 1/10, -0.5]
    upperRight= [i/10 + 1/10, 0.5]

    colorBarXCoords.append([lowerLeft[0], upperLeft[0], upperRight[0], lowerRight[0]])
    colorBarYCoords.append([lowerLeft[1], upperLeft[1], upperRight[1], lowerRight[1]])
colorBarColorList = list()
colorBarAlphaList = list()

# Determine the color distribution in the color bar
smallestValue,biggestValue = 0,10
valuesRange = list()
for i in range(50):
    valuesRange.append(smallestValue + (i/49)*(biggestValue - smallestValue))
for i in range(50):
    colorBarColorList.append(functions.color_determiner( smallestValue, biggestValue, valuesRange[i] ))
    colorBarAlphaList.append( 1 )
    
def update_colorBar_extremas(smallesValue, biggestValue):
    colorBar.title.text = str(smallesValue)+" Pa                                                                      "+str(biggestValue)+" Pa"

# Construct the source file for the color bar
colorBarSource = ColumnDataSource(data=dict( x=colorBarXCoords, y=colorBarYCoords, c =colorBarColorList, a=colorBarAlphaList ))

# Construct the patches 
colorBar.patches( xs='x', ys='y', source=colorBarSource, color = 'c', alpha = 'a' )
plotUndefXY.patches(xs='x', ys='y', source=sourceXYundef, color = 'c', alpha = 'a')
plotDefXY.patches  (xs='x', ys='y', source=sourceXYdef  , color = 'c', alpha = 'a')
plotUndefXZ.patches(xs='x', ys='y', source=sourceXZundef, color = 'c', alpha = 'a')
plotDefXZ.patches  (xs='x', ys='y', source=sourceXZdef  , color = 'c', alpha = 'a')

# Construct the arrows
plotDefXY.add_layout( 
                     Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
                           x_start=['xs'][0],
                           y_start=['ys'][0],
                           x_end=['xe'][0], 
                           y_end=['ye'][0], 
                           source = sourceArrowXY) 
                    )
plotDefXZ.add_layout( 
                     Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
                           x_start=['xs'][0], 
                           y_start=['ys'][0], 
                           x_end=['xe'][0], 
                           y_end=['ye'][0], 
                           source = sourceArrowXZ)
                    )

# Construct the force labels
plotDefXY.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='f',
                                  text_color='black',text_font_size="15pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFyLabel
                              )
                    )

plotDefXZ.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='f',
                                  text_color='black',text_font_size="15pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFzLabel
                              )
                    )
                     
# Notify the corresponding functions to carry out the changes characterized by
# the sliders
Yforce_slider.on_change('value',fun_change_Py)
Zforce_slider.on_change('value',fun_change_Pz)

init_data()    

area_image = Div(text="""
<p>
<img src="/2D_cantilever_beam/static/images/picture.jpg" width=600>
</p>
<p>
3D Schematic of the Cantilever Beam with the Corresponding Geometry and Material Parameters
</p>
<p>
**For visualization purposes, there is a magnification factor of 100 that exaggerates the deformation""", render_as_text=False, width=600)

# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(row(description,row(column(row(column(plotUndefXY,plotDefXY) , column(plotUndefXZ,plotDefXZ)),colorBar),column(Yforce_slider,Zforce_slider,Spacer(height=30),area_image))))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '