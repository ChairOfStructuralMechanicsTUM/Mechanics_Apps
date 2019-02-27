import Cantilever_beam_classes as functions
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource
from bokeh.layouts import row, column, widgetbox
from bokeh.models import Slider, LabelSet, Div
from bokeh.models import Arrow, NormalHead, OpenHead, VeeHead
from os.path import dirname, join, split
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Button, CheckboxGroup, RadioButtonGroup
from bokeh.models.glyphs import ImageURL, Patch
import numpy as np
# Define basic beam parameters and loading
length = 5.0
height = 1.0
thickness = 1.0
E = 1000000000.0
Py = 0.0 #-1000
Pz = 0.0 #2000

global cross_section_options_i
cross_section_options_i = 0

global stress_options_i
stress_options_i = 0

# Define mesh for visualization
noElementsX = 80
noElementsY = 20
noElementsZ = 20
elementSizeX = length / noElementsX
elementSizeY = height / noElementsY
elementSizeZ = thickness / noElementsZ
amplificationFactor = 100

# Cross Section Source:
CrossSection1 = "2D_cantilever_beam/static/images/Rectangular.png"
CrossSection2 = "2D_cantilever_beam/static/images/Circular.png"
CrossSection3 = "2D_cantilever_beam/static/images/DoubleT.png"
CrossSectionSource1 = ColumnDataSource(data=dict(sp1=[], x=[] , y=[]))
CrossSectionSource2 = ColumnDataSource(data=dict(sp2=[], x=[] , y=[]))
CrossSectionSource3 = ColumnDataSource(data=dict(sp3=[], x=[] , y=[]))

# Source & Initialization of Internal Element Plot:
XYElement = "2D_cantilever_beam/static/images/XYElement.png"
XYElementSource = ColumnDataSource(data=dict(sp4=[], x=[] , y=[]))
XYElementSource.data = dict(sp4=[XYElement], x = [0], y = [0])
XYBeam = "2D_cantilever_beam/static/images/XYBeam.png"
XYBeamSource = ColumnDataSource(data=dict(sp5=[], x=[] , y=[]))
XYBeamSource.data = dict(sp5=[XYBeam], x = [0], y = [0])

# Sigma and tau sources in "XY-Element" plot:
Sigmaplot_l_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Sigmaplot_r_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_l_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_r_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_u_Source = ColumnDataSource(data=dict(x=[] , y=[]))
# Arrow sources in "XY-Element" plot:
SigmaArrowSource1 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
SigmaArrowSource2 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
SigmaArrowSource3 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
SigmaArrowSource4 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
SigmaArrowSource5 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
SigmaArrowSource6 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
TauArrowSource1 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
TauArrowSource2 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
TauArrowSource3 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))
TauArrowSource4 = ColumnDataSource(data = dict(xs=[], ys=[], xe=[], ye=[]))





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
                                                                                      amplificationFactor, 
                                                                                      cross_section_options_i
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
                                                                                      amplificationFactor,
                                                                                      cross_section_options_i
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

#def undeformed_cantilever_beam_determiner( 
#                                          length, height, thickness, E, Py, Pz,
#                                          noElementsX, noElementsY, 
#                                          noElementsZ, elementSizeX, 
#                                          elementSizeY, elementSizeZ,
#                                          amplificationFactor 
#                                         ):
#    
#    # Construct The undeformed beam's center line
#    undeformedBeamXY, undeformedBeamXZ = functions.construct_undeformed_beam_centerline( 
#                                                                                            noElementsX, 
#                                                                                            noElementsY, 
#                                                                                            noElementsZ,
#                                                                                            elementSizeX
#                                                                                       )
#
#    # Construct normal vectors for both XY and XZ projections of the beam
#    normalVecrtorsXYUpperUndef, normalVectorsXYLowerUndef = functions.construct_normal_vectors( undeformedBeamXY )
#    normalVecrtorsXZUpperUndef, normalVectorsXZLowerUndef = functions.construct_normal_vectors( undeformedBeamXZ )
#
#    # Construct mesh for the undeformed and the deformed beams    
#    listUndeformedElementsXY = functions.construct_deformed_elements( 
#                                                                        undeformedBeamXY,
#                                                                        elementSizeX,
#                                                                        elementSizeY,
#                                                                        noElementsX,
#                                                                        noElementsY,
#                                                                        normalVecrtorsXYUpperUndef,
#                                                                        normalVectorsXYLowerUndef
#                                                                    )
#    listUndeformedElementsXZ = functions.construct_deformed_elements( 
#                                                                        undeformedBeamXZ,
#                                                                        elementSizeX,
#                                                                        elementSizeZ,
#                                                                        noElementsX,
#                                                                        noElementsZ,
#                                                                        normalVecrtorsXZUpperUndef,
#                                                                        normalVectorsXZLowerUndef
#                                                                    )
#    
#    # Determine the patches' X,Y,Z coordinates
#    XCoordsUndefXY , YCoordsUndefXY = functions.create_coordinates_list( listUndeformedElementsXY )
#    XCoordsUndefXZ , YCoordsUndefXZ = functions.create_coordinates_list( listUndeformedElementsXZ )
#
#    # Detemine the color of the elements
#    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
#                                                                                                        Py, Pz,
#                                                                                                        length,
#                                                                                                        height,
#                                                                                                        thickness,
#                                                                                                        E, elementSizeX
#                                                                                                   )
#    # Coloring the undeformed elements
#    colorListUndeformedXY = functions.elements_color_determiner(
#                                                                    False,
#                                                                    'XY',
#                                                                    listUndeformedElementsXY,
#                                                                    noElementsX,
#                                                                    noElementsY,
#                                                                    E, height, thickness,
#                                                                    length, Py, 
#                                                                    smallestValue, biggestValue,
#                                                                    listValuesLowerXZ
#                                                               )    
#    colorListUndeformedXZ = functions.elements_color_determiner(
#                                                                    False,
#                                                                    'XZ',
#                                                                    listUndeformedElementsXZ,
#                                                                    noElementsX,
#                                                                    noElementsZ,
#                                                                    E, thickness, height,
#                                                                    length, Pz, 
#                                                                    biggestValue, smallestValue,
#                                                                    listValuesUpperXY
#                                                               )
#
#    return (
#                listUndeformedElementsXY, listUndeformedElementsXY,
#                XCoordsUndefXY, XCoordsUndefXZ,
#                YCoordsUndefXY, YCoordsUndefXZ, 
#                colorListUndeformedXY, colorListUndeformedXZ,
#                biggestValue, smallestValue
#           )    

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

## Construct the undeformed beams in XY and XZ planes
#(listUndeformedElementsXY, listUndeformedElementsXZ, XCoordsUndefXY,
# XCoordsUndefXZ, YCoordsUndefXY, YCoordsUndefXZ,
# colorListUndeformedXY, colorListUndeformedXZ,
# biggestValue, smallestValue) = undeformed_cantilever_beam_determiner( 
#                               length, height, thickness, E, Py, Pz,
#                               noElementsX, noElementsY, noElementsZ,
#                               elementSizeX, elementSizeY, elementSizeZ,
#                               amplificationFactor
#                           )
    
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

    ##################################
    # Update Stresses acting on internal XY-Element:
    sigma_x_l,sigma_x_r,tau_xy = functions.calculate_stresses_xy_element(length,height,thickness,cross_section_options_i,Py,Pz,E)
    

    ## IF SIGMA BUTTON IS ACTIVATED:
    if (stress_options_i==0):
        ## DELETE TAU PLOTS
        Tauplot_l_Source.data = dict(x = [], y = [])
        Tauplot_r_Source.data = dict(x = [], y = [])
        Tauplot_u_Source.data = dict(x = [], y = [])   
        ## DELETE TAU ARROWS
        TauArrowSource1.data = dict(xs=[] , xe= [], ys=[] , ye=[])            
        TauArrowSource2.data = dict(xs=[] , xe= [], ys=[] , ye=[])        
        TauArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])            
        TauArrowSource4.data = dict(xs=[] , xe= [], ys=[] , ye=[])

        ## SCALING AND POSITION OF SIGMA GLYPHS
        sigmascaling = 0.000005
        sigma_l_pos = 1.5
        sigma_r_pos = 3.5

        ## SIGMA_X LEFT END DATA SOURCE:
        sigma_x_l_scaled = np.linspace(0, 0, len(sigma_x_l))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_l)): 
            sigma_x_l_scaled[i]=sigma_x_l[len(sigma_x_l)-i-1]*sigmascaling
        SigmaPlot_l_x = np.hstack((np.linspace(sigma_l_pos, sigma_l_pos, len(sigma_x_l)), sigma_l_pos-abs(sigma_x_l_scaled)))
        SigmaPlot_l_y = np.hstack((np.linspace(-0.525, 0, len(sigma_x_l)),np.linspace(0, -0.525, len(sigma_x_l))))
        Sigmaplot_l_Source.data = dict(x = SigmaPlot_l_x, y = SigmaPlot_l_y)
        ## SIGMA_X RIGHT END DATA SOURCE:
        sigma_x_r_scaled = np.linspace(0, 0, len(sigma_x_r))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_r)): 
            sigma_x_r_scaled[i]=sigma_x_r[len(sigma_x_r)-i-1]*sigmascaling
        SigmaPlot_r_x = np.hstack((np.linspace(sigma_r_pos, sigma_r_pos, len(sigma_x_r)), sigma_r_pos+abs(sigma_x_r_scaled)))
        SigmaPlot_r_y = np.hstack((np.linspace(-0.525, 0, len(sigma_x_r)),np.linspace(0, -0.525, len(sigma_x_r))))
        Sigmaplot_r_Source.data = dict(x = SigmaPlot_r_x, y = SigmaPlot_r_y)
        
        # SCALING AND POSITIONING OF SIGMA ARROWS
        arrow_scale = 0.7
        arrow_adjust_x = 0.05
        # Arrows left end    
        if (Py<-1500):
            SigmaArrowSource1.data = dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4])
            SigmaArrowSource2.data = dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] )
            # SigmaTauArrowSource3.data = dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*1.0/5.0))]] , ys=[-0.1] , ye=[-0.1] )
            SigmaArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        elif (Py>1500):
            SigmaArrowSource1.data = dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4])
            SigmaArrowSource2.data = dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] )
            # SigmaTauArrowSource3.data = dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*1.0/5.0))]] , ys=[-0.1] , ye=[-0.1] )        
            SigmaArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])        
        else:
            SigmaArrowSource1.data = dict(xs=[] , xe= [], ys=[] , ye=[])
            SigmaArrowSource2.data = dict(xs=[] , xe= [], ys=[] , ye=[])
            SigmaArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        # Arrows right end
        arrow_scale = 0.7
        arrow_adjust_x = 0.05
        if (Py<-1500):
            SigmaArrowSource4.data = dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4])
            SigmaArrowSource5.data = dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] )
            # SigmaTauArrowSource6.data = dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*1.0/5.0))]] , ys=[-0.1] , ye=[-0.1] )
            SigmaArrowSource6.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        elif (Py>1500):
            SigmaArrowSource4.data = dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4])
            SigmaArrowSource5.data = dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] )
            # SigmaTauArrowSource6.data = dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*1.0/5.0))]] , ys=[-0.1] , ye=[-0.1] )        
            SigmaArrowSource6.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        else:
            SigmaArrowSource4.data = dict(xs=[] , xe= [], ys=[] , ye=[])
            SigmaArrowSource5.data = dict(xs=[] , xe= [], ys=[] , ye=[])
            SigmaArrowSource6.data = dict(xs=[] , xe= [], ys=[] , ye=[])

    ## IF TAU BUTTON IS ACTIVATED:
    if (stress_options_i==1):    
        ## DELETE SIGMA PLOTS
        Sigmaplot_l_Source.data = dict(x = [], y = [])
        Sigmaplot_r_Source.data = dict(x = [], y = [])
        ## DELETE SIGMA ARROWS
        SigmaArrowSource1.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        SigmaArrowSource2.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        SigmaArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        SigmaArrowSource4.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        SigmaArrowSource5.data = dict(xs=[] , xe= [], ys=[] , ye=[])
        SigmaArrowSource6.data = dict(xs=[] , xe= [], ys=[] , ye=[])

        ## SCALING AND POSITION OF TAU GLYPHS
        tau_xy_scaling = 0.00001
        tau_xy_l_pos_x = 1.5
        tau_xy_r_pos_x = 3.5
        tau_xy_u_pos_x = 2.5        

        ## TAU LEFT END DATA SOURCE:
        tau_xy_l_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list 
        for i in range(len(tau_xy)): 
            tau_xy_l_scaled[i]=tau_xy[len(tau_xy)-i-1]*tau_xy_scaling
        TauPlot_l_x = np.hstack((np.linspace(tau_xy_l_pos_x, tau_xy_l_pos_x, len(tau_xy)), tau_xy_l_pos_x-abs(tau_xy_l_scaled)))
        TauPlot_l_y = np.hstack((np.linspace(-0.525, 0, len(tau_xy)),np.linspace(0, -0.525, len(tau_xy))))
        Tauplot_l_Source.data = dict(x = TauPlot_l_x, y = TauPlot_l_y)
        
        ## TAU RIGHT END DATA SOURCE:
        tau_xy_r_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list 
        for i in range(len(tau_xy)): 
            tau_xy_r_scaled[i]=tau_xy[len(tau_xy)-i-1]*tau_xy_scaling
        TauPlot_r_x = np.hstack((np.linspace(tau_xy_r_pos_x, tau_xy_r_pos_x, len(tau_xy)), tau_xy_r_pos_x+abs(tau_xy_r_scaled)))
        TauPlot_r_y = np.hstack((np.linspace(-0.525, 0, len(tau_xy)),np.linspace(0, -0.525, len(tau_xy))))
        Tauplot_r_Source.data = dict(x = TauPlot_r_x, y = TauPlot_r_y)

        ## TAU UPPER BORDER DATA SOURCE
        tau_xy_u_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list consisting of tau_max value: 
        for i in range(len(tau_xy)): 
            tau_xy_u_scaled[i]=tau_xy[len(tau_xy)-1]*tau_xy_scaling
        TauPlot_u_x = np.hstack((np.linspace(tau_xy_u_pos_x-1, tau_xy_u_pos_x+1, len(tau_xy)), np.linspace(tau_xy_u_pos_x+1, tau_xy_u_pos_x-1, len(tau_xy))))
        TauPlot_u_y = np.hstack((np.linspace(0, 0, len(tau_xy)), abs(tau_xy_u_scaled)))
        Tauplot_u_Source.data = dict(x = TauPlot_u_x, y = TauPlot_u_y)

        ### SCALING AND POSITIONING OF ARROWS:
        # Position arrows into tau glyph
        arrow_adjust_x = max(abs(tau_xy_l_scaled))/4.0
        # Make arrow size grow with increasing tau stress, but restrict length of arrows to dimensions of tau glyph
        if (max(abs(tau_xy_u_scaled))/2.0 >= 0.15):
            arrow_adjust_y = 0.15
        else:
            arrow_adjust_y = max(abs(tau_xy_u_scaled))/2.0
        arrow_move_y = 0.04    
        
        ## ARROW LEFT END:
        tau_xy_l_pos_y = -0.25                 
        if (Py<-1500):
            TauArrowSource1.data = dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], ys=[tau_xy_l_pos_y+arrow_adjust_y+arrow_move_y] , ye=[tau_xy_l_pos_y-arrow_adjust_y+arrow_move_y])
        elif (Py>1500):
            TauArrowSource1.data = dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], ys=[tau_xy_l_pos_y-arrow_adjust_y+arrow_move_y] , ye=[tau_xy_l_pos_y+arrow_adjust_y+arrow_move_y])
        else:            
            TauArrowSource1.data = dict(xs=[] , xe= [], ys=[] , ye=[])  
        
        ## ARROWS RIGHT END:             
        tau_xy_r_pos_y = -0.25           
        if (Py<-1500):
            TauArrowSource2.data = dict(xs=[tau_xy_r_pos_x+arrow_adjust_x] , xe= [tau_xy_r_pos_x+arrow_adjust_x], ys=[tau_xy_r_pos_y-arrow_adjust_y+arrow_move_y] , ye=[tau_xy_r_pos_y+arrow_adjust_y+arrow_move_y])
        elif (Py>1500):
            TauArrowSource2.data = dict(xs=[tau_xy_r_pos_x+arrow_adjust_x] , xe= [tau_xy_r_pos_x+arrow_adjust_x], ys=[tau_xy_r_pos_y+arrow_adjust_y+arrow_move_y] , ye=[tau_xy_r_pos_y-arrow_adjust_y+arrow_move_y])
        else:            
            TauArrowSource2.data = dict(xs=[] , xe= [], ys=[] , ye=[])  

        ## ARROWS UPPER BORDER:
        tau_xy_u_pos_y = 0.0            
        # New arrow scaling and positioning for upper tau stress
        if (max(abs(tau_xy_u_scaled)) >= 0.3):
            arrow_adjust_x = 0.3
        else:
            arrow_adjust_x = max(abs(tau_xy_u_scaled))
        arrow_adjust_y = max(abs(tau_xy_u_scaled))/2.0
        if (Py<-1500):
            TauArrowSource3.data = dict(xs=[(tau_xy_u_pos_x-0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)+arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y])            
            TauArrowSource4.data = dict(xs=[(tau_xy_u_pos_x+0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)+arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y])                                  
        elif (Py>1500):
            TauArrowSource3.data = dict(xs=[(tau_xy_u_pos_x-0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)-arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y])            
            TauArrowSource4.data = dict(xs=[(tau_xy_u_pos_x+0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)-arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y])
        else:
            TauArrowSource3.data = dict(xs=[] , xe= [], ys=[] , ye=[])            
            TauArrowSource4.data = dict(xs=[] , xe= [], ys=[] , ye=[])   


    ##################################

        
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
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-2][2]+1.5*abs(Pz)/5000.0+0.25],
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
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]-1.5*abs(Pz)/5000.0-0.25],
                                      xe=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ye=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]],
                                 )
        sourceFzLabel.data = dict(
                                      x= sourceArrowXZ.data['xs'],
                                      y= [sourceArrowXZ.data['ys'][0] - 0.5],
                                      f= ['Fz']
                                 )
        
    update_colorBar_extremas(smallestValue,biggestValue)

    ##################################
    # Update Stresses acting on internal XY-Element:
    # x_pos = 2.5
    # y_pos = -height/2
    # z_pos = 0
    # length_of_element = 2.0
    # height_of_element = height/2.0
    functions.calculate_stresses_xy_element(length,height,thickness,cross_section_options_i,Py,Pz,E)
    ##################################



##########################

def fun_change_Cross_Section(attrname, old, new):
    # global Pz, listDeformedElementsXZ 
    # global radio_button_group.active
    # print radio_button_group.active
    if (radio_button_group.active == 0 ):
        CrossSectionSource1.data = dict(sp1=[CrossSection1], x = [0], y = [0])
        CrossSectionSource2.data = dict(sp2=[], x = [], y = [])
        CrossSectionSource3.data = dict(sp3=[], x = [], y = [])
    elif (radio_button_group.active == 1):
        CrossSectionSource1.data = dict(sp1=[], x = [], y = [])
        CrossSectionSource2.data = dict(sp2=[CrossSection2], x = [0], y = [0])
        CrossSectionSource3.data = dict(sp3=[], x = [], y = [])
    elif (radio_button_group.active == 2):
        CrossSectionSource1.data = dict(sp1=[], x = [], y = [])
        CrossSectionSource2.data = dict(sp2=[], x = [], y = [])
        CrossSectionSource3.data = dict(sp3=[CrossSection3], x = [0], y = [0])
    
    global cross_section_options_i
    cross_section_options_i = radio_button_group.active
    global stress_options_i
    stress_options_i = radio_button_group2.active





##########################
        
def init_data():

    Yforce_slider.value = 0
    Zforce_slider.value = 0
    # Xpos_slider.value   = 0
    radio_button_group.active = 0
    radio_button_group2.active = 0

    fun_change_Py(None,None, None)
    fun_change_Pz(None,None, None)
    fun_change_Cross_Section(None,None,None)
    

# Construct the source file of all the beams
sourceXYdef   = ColumnDataSource(data=dict( x=XCoordsDefXY,   y=YCoordsDefXY,   c =colorListDeformedXY,   a=alphaList ))
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
Yforce_slider = Slider(title="Y-direction of the force (N)", value=0.0, start=-5000.0, end=5000.0, step=100.0)
Zforce_slider = Slider(title="Z-direction of the force (N)", value=0.0, start=-5000.0, end=5000.0, step=100.0)

# Construct radio button to choose between geometries of cross section
radio_button_group = RadioButtonGroup(name="Geometry of cross section",labels=["Rectangular", "Circular", "Double-T"], active=cross_section_options_i)

# Construct radio button to choose between plot of sigma(y) or tau(y)
radio_button_group2 = RadioButtonGroup(name="Plot of sigma or tau",labels=["Sigma", "Tau"], active=stress_options_i)

# # Construct slider to choose x-position of visualized cross section
# Xpos_slider = Slider(title="X-position", value=0.0, start=0.0, end=5.0, step=0.5)

# Construct reset button
Reset_button = Button(label="Reset", button_type="success")




#                         x_range = ( 0,6 ) ,
#                         y_range= ( -3,3 ) ,
#                         title = 'Undefromed Cofiguration in XY plane',
#                         tools = '',
#                    )
#plotUndefXY.xaxis.major_tick_line_color=None
#plotUndefXY.xaxis.major_label_text_color=None
#plotUndefXY.xaxis.minor_tick_line_color=None
#plotUndefXY.yaxis.major_tick_line_color=None
#plotUndefXY.yaxis.major_label_text_color=None
#plotUndefXY.yaxis.minor_tick_line_color=None
#plotUndefXY.grid.visible = False
#plotUndefXY.title.text_font_size="12.5pt"
#plotUndefXY.xaxis.axis_label_text_font_size="14pt"
#plotUndefXY.yaxis.axis_label_text_font_size="14pt"
#plotUndefXY.xaxis.axis_label="x"
#plotUndefXY.yaxis.axis_label="y"

plotDefXY = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in X-Y plane',
                       tools = ''
                  )
plotDefXY.xaxis.major_tick_line_color=None
plotDefXY.xaxis.major_label_text_color=None
plotDefXY.xaxis.minor_tick_line_color=None
plotDefXY.xaxis.axis_line_color=None
plotDefXY.yaxis.major_tick_line_color=None
plotDefXY.yaxis.major_label_text_color=None
plotDefXY.yaxis.minor_tick_line_color=None
plotDefXY.yaxis.axis_line_color=None
plotDefXY.grid.visible = False
plotDefXY.toolbar.logo = None
plotDefXY.title.text_font_size="12.5pt"
#plotDefXY.xaxis.axis_label_text_font_size="12pt"
#plotDefXY.yaxis.axis_label_text_font_size="12pt"
#plotDefXY.xaxis.axis_label="x"
#plotDefXY.yaxis.axis_label="y"
labelXY = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     y=[2.7,-.3],
                                     text=['y','x']))
plotDefXY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-3, 
                           x_end=0, 
                           y_end=2.9, 
                           ))

plotDefXY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=-.5, 
                           y_start=0, 
                           x_end=5.9, 
                           y_end=0, 
                           ))
plotDefXY.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXY
                                )
                    )

#plotUndefXZ = Figure(    
#                         plot_width=350    , 
#                         plot_height=350   ,
#                         x_range = ( 0,6 ) ,
#                         y_range= ( -3,3 ) ,
#                         title = 'Undefromed Cofiguration in XZ plane',
#                         tools = ''
#                    )
#plotUndefXZ.xaxis.major_tick_line_color=None
#plotUndefXZ.xaxis.major_label_text_color=None
#plotUndefXZ.xaxis.minor_tick_line_color=None
#plotUndefXZ.yaxis.major_tick_line_color=None
#plotUndefXZ.yaxis.major_label_text_color=None
#plotUndefXZ.yaxis.minor_tick_line_color=None
#plotUndefXZ.grid.visible = False
#plotUndefXZ.title.text_font_size="12.5pt"
#plotUndefXZ.xaxis.axis_label_text_font_size="14pt"
#plotUndefXZ.yaxis.axis_label_text_font_size="14pt"
#plotUndefXZ.xaxis.axis_label="x"
#plotUndefXZ.yaxis.axis_label="z"

plotDefXZ = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in X-Z plane',
                       tools = ''
                  )
plotDefXZ.xaxis.major_tick_line_color=None
plotDefXZ.xaxis.major_label_text_color=None
plotDefXZ.xaxis.minor_tick_line_color=None
plotDefXZ.xaxis.axis_line_color=None
plotDefXZ.yaxis.major_tick_line_color=None
plotDefXZ.yaxis.major_label_text_color=None
plotDefXZ.yaxis.minor_tick_line_color=None
plotDefXZ.yaxis.axis_line_color=None
plotDefXZ.grid.visible = False
plotDefXZ.toolbar.logo = None
plotDefXZ.title.text_font_size="12.5pt"

labelXZ = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     y=[-2.7,-.3],
                                     text=['z','x']))
plotDefXZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=3, 
                           x_end=0, 
                           y_end=-2.9, 
                           ))

plotDefXZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=-.5, 
                           y_start=0, 
                           x_end=5.9, 
                           y_end=0, 
                           ))
plotDefXZ.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXZ
                                )
                    )


######################
plotDefYZ = Figure(    
                       plot_width=300    , 
                       plot_height=300   ,
                       x_range = ( -5,5 ) ,
                       y_range= ( -5,5 ) ,
                       title = 'Selected Cross Section',
                       tools = ''
                  )
plotDefYZ.xaxis.major_tick_line_color=None
plotDefYZ.xaxis.major_label_text_color=None
plotDefYZ.xaxis.minor_tick_line_color=None
plotDefYZ.xaxis.axis_line_color=None
plotDefYZ.yaxis.major_tick_line_color=None
plotDefYZ.yaxis.major_label_text_color=None
plotDefYZ.yaxis.minor_tick_line_color=None
plotDefYZ.yaxis.axis_line_color=None
plotDefYZ.grid.visible = False
plotDefYZ.toolbar.logo = None
plotDefYZ.title.text_font_size="12.5pt"

labelYZ = ColumnDataSource(data=dict(x=[0.5,-3.5],
                                     y=[4.0,-1.0],
                                     text=['y','z']))
plotDefYZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-4, 
                           x_end=0, 
                           y_end=4, 
                           ))

plotDefYZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_end=-4, 
                           y_start=0, 
                           x_start=4, 
                           y_end=0, 
                           ))
plotDefYZ.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelYZ
                                )
                    )
plotDefYZ.add_glyph(CrossSectionSource1,ImageURL(url="sp1", x=-5.0/3.0, y=5.0/3.0, w=10.0/3.0, h=10.0/3.0))
plotDefYZ.add_glyph(CrossSectionSource2,ImageURL(url="sp2", x=-5.0/3.0, y=5.0/3.0, w=10.0/3.0, h=10.0/3.0))
plotDefYZ.add_glyph(CrossSectionSource3,ImageURL(url="sp3", x=-5.0/3.0, y=5.0/3.0, w=10.0/3.0, h=10.0/3.0))

####################


#################################
plotXYElement = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Stresses of XY-Element',
                       tools = ''
                  )
plotXYElement.xaxis.major_tick_line_color=None
plotXYElement.xaxis.major_label_text_color=None
plotXYElement.xaxis.minor_tick_line_color=None
plotXYElement.xaxis.axis_line_color=None
plotXYElement.yaxis.major_tick_line_color=None
plotXYElement.yaxis.major_label_text_color=None
plotXYElement.yaxis.minor_tick_line_color=None
plotXYElement.yaxis.axis_line_color=None
plotXYElement.grid.visible = False
plotXYElement.toolbar.logo = None
plotXYElement.title.text_font_size="12.5pt"
#plotDefXY.xaxis.axis_label_text_font_size="12pt"
#plotDefXY.yaxis.axis_label_text_font_size="12pt"
#plotDefXY.xaxis.axis_label="x"
#plotDefXY.yaxis.axis_label="y"
labelXYElement = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     y=[2.7,-.3],
                                     text=['y','x']))
plotXYElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-3, 
                           x_end=0, 
                           y_end=2.9, 
                           ))

plotXYElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=-.5, 
                           y_start=0, 
                           x_end=5.9, 
                           y_end=0, 
                           ))
plotXYElement.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXYElement
                                )
                    )

plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource1))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource2))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource3))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource4))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource5))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = SigmaArrowSource6))

plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = TauArrowSource1))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = TauArrowSource2))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = TauArrowSource3))
plotXYElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['ys'][0], x_end=['xe'][0], y_end=['ye'][0], source = TauArrowSource4))
                      

# labelXYElement = ColumnDataSource(data=dict(x=[3.5],
#                                      y=[-1.0],
#                                      text=['x']))

# plotXYElement.add_layout( 
#                      Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
#                            x_start=0, 
#                            y_start=-4, 
#                            x_end=0, 
#                            y_end=4, 
#                            ))

# plotXYElement.add_layout( 
#                      Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
#                            x_end=4, 
#                            y_start=0, 
#                            x_start=-4, 
#                            y_end=0, 
#                            ))
# plotXYElement.add_layout(
#                       LabelSet(
#                                   x='x', y='y',
#                                   text='text',
#                                   text_color='black',text_font_size="12pt",
#                                   level='glyph',text_baseline="middle",text_align="center",
#                                   source=labelXYElement
#                                 )
#                     )

plotXYElement.add_glyph(XYBeamSource,ImageURL(url="sp5", x=0, y=0.5, w=5, h=1.04))
plotXYElement.add_glyph(XYElementSource,ImageURL(url="sp4", x=1.5, y=0, w=2, h=0.535))


Sigmaplot_l_Glyph = Patch(x="x", y="y", fill_color='#0065BD', fill_alpha=0.5)
plotXYElement.add_glyph(Sigmaplot_l_Source, Sigmaplot_l_Glyph)

Sigmaplot_r_Glyph = Patch(x="x", y="y", fill_color='#0065BD', fill_alpha=0.5)
plotXYElement.add_glyph(Sigmaplot_r_Source, Sigmaplot_r_Glyph)


Tauplot_l_Glyph = Patch(x="x", y="y", fill_color='#E37222', fill_alpha=0.5)
plotXYElement.add_glyph(Tauplot_l_Source, Tauplot_l_Glyph)

Tauplot_r_Glyph = Patch(x="x", y="y", fill_color='#E37222', fill_alpha=0.5)
plotXYElement.add_glyph(Tauplot_r_Source, Tauplot_r_Glyph)

Tauplot_u_Glyph = Patch(x="x", y="y", fill_color='#E37222', fill_alpha=0.5)
plotXYElement.add_glyph(Tauplot_u_Source, Tauplot_u_Glyph)
#####################################


# Construct the color-bar figure
colorBar = Figure(
                      title = '',
                      title_location="below",
                      plot_width=800   ,
                      plot_height=75,
                      x_range=(0,5),
                      y_range=(-0.5,0.5),   
                      tools = ''
                 )
colorBar.xaxis.visible = False
colorBar.yaxis.visible = False
colorBar.toolbar.logo = None
colorBar.title.text_font_size="12pt"

# create colorBar patches
colorBarXCoords = list()
colorBarYCoords = list()
for i in range(50):
    lowerLeft = [float(i)/10, -0.5]
    upperLeft = [float(i)/10, 0.5]
    lowerRight= [float(i)/10 + 1.0/10.0, -0.5]
    upperRight= [float(i)/10 + 1.0/10.0, 0.5]

    colorBarXCoords.append([lowerLeft[0], upperLeft[0], upperRight[0], lowerRight[0]])
    colorBarYCoords.append([lowerLeft[1], upperLeft[1], upperRight[1], lowerRight[1]])
colorBarColorList = list()
colorBarAlphaList = list()

# Determine the color distribution in the color bar
smallestValue,biggestValue = 0.0,10.0
valuesRange = list()
for i in range(50):
    valuesRange.append(smallestValue + (float(i)/49.0)*(biggestValue - smallestValue))

for i in range(50):
    colorBarColorList.append(functions.color_determiner( smallestValue, biggestValue, valuesRange[i] ))
    colorBarAlphaList.append( 1 )

def update_colorBar_extremas(smallesValue, biggestValue):
    colorBar.title.text = str(smallesValue)+" Pa" + " "*50 + "normal stress" + " "*50 + str(biggestValue)+" Pa"

# Construct the source file for the color bar
colorBarSource = ColumnDataSource(data=dict( x=colorBarXCoords, y=colorBarYCoords, c =colorBarColorList, a=colorBarAlphaList ))

# Construct the patches 
colorBar.patches( xs='x', ys='y', source=colorBarSource, color = 'c', alpha = 'a' )
plotDefXY.patches  (xs='x', ys='y', source=sourceXYdef  , color = 'c', alpha = 'a')
plotDefXZ.patches  (xs='x', ys='y', source=sourceXZdef  , color = 'c', alpha = 'a')


###################
# plotDefYZ.patches  (xs='x', ys='y', source=sourceXZdef  , color = 'c', alpha = 'a')
######################


# Construct the arrows
plotDefXY.add_layout( 
                     Arrow(end=NormalHead(line_color="black",line_width=3,size=10),
                           line_width=3,
                           x_start=['xs'][0],
                           y_start=['ys'][0],
                           x_end=['xe'][0], 
                           y_end=['ye'][0], 
                           source = sourceArrowXY) 
                    )
plotDefXZ.add_layout( 
                     Arrow(end=NormalHead(line_color="black",line_width=3,size=10),
                           line_width=3,
                           x_start=['xs'][0], 
                           y_start=['ys'][0], 
                           x_end=['xe'][0], 
                           y_end=['ye'][0], 
                           source = sourceArrowXZ)
                    )
###############
# plotDefYZ.add_layout( 
#                      Arrow(end=OpenHead(line_color="black",line_width=3,size=10),
#                            x_start=['xs'][0], 
#                            y_start=['ys'][0], 
#                            x_end=['xe'][0], 
#                            y_end=['ye'][0], 
#                            source = sourceArrowXZ)
#                     )
########################                
            


# Construct the force labels
plotDefXY.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='f',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFyLabel
                              )
                    )

plotDefXZ.add_layout(
                      LabelSet(
                                  x='x', y='y',
                                  text='f',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFzLabel
                              )
                    )


########################
# plotDefYZ.add_layout(
#                       LabelSet(
#                                   x='x', y='y',
#                                   text='f',
#                                   text_color='black',text_font_size="12pt",
#                                   level='glyph',text_baseline="middle",text_align="center",
#                                   source=sourceFzLabel
#                               )
#                     )
#########################


# x Axis                     
#plotDefXY.line([0, 6], [0, 0], line_width=1, line_color="black")
#plotDefXZ.line([0, 6], [0, 0], line_width=1, line_color="black", line_dash='dotted')
                        
# Notify the corresponding functions to carry out the changes characterized by
# the sliders
Yforce_slider.on_change('value',fun_change_Py)
Zforce_slider.on_change('value',fun_change_Pz)
radio_button_group.on_change('active',fun_change_Cross_Section,fun_change_Py,fun_change_Pz)
radio_button_group2.on_change('active',fun_change_Cross_Section,fun_change_Py,fun_change_Pz)
# Xpos_slider.on_change('value',fun_change_Py,fun_change_Pz)
Reset_button.on_click(init_data)

init_data()    

# **For visualization purposes, there is a magnification factor of 100 that exaggerates the deformation""", render_as_text=False, width=400)
# add app description
description_filename = join(dirname(__file__), "description.html")

description = Div(text=open(description_filename).read(), render_as_text=False, width=1200)

curdoc().add_root(
                    column(
                            description,
                            row(
                                column(
                                    plotDefYZ,
                                    widgetbox(radio_button_group),
                                    Yforce_slider,
                                    Zforce_slider,
                                    Reset_button
                                        #   Spacer(height=30),
                                        #   area_image
                                ),
                                column(
                                    row(
                                        column(row(plotDefXY, plotDefXZ),colorBar),
                                        column(plotXYElement,row(Spacer(width=150),radio_button_group2))
                                ),

                               )
                          )
                     ) 
                 )
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '