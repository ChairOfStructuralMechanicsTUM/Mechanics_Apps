import Cantilever_beam_classes as functions
from bokeh.io import curdoc
from bokeh.plotting import Figure, ColumnDataSource, output_file , show
from bokeh.layouts import row, column, widgetbox, layout
from bokeh.models import Slider, LabelSet, Div
from bokeh.models import Arrow, NormalHead, OpenHead, VeeHead
from os.path import dirname, join, split, abspath
from bokeh.models.layouts import Spacer
from bokeh.models.widgets import Button, CheckboxGroup, RadioButtonGroup
from bokeh.models.glyphs import ImageURL, Patch, Quadratic, Rect
import numpy as np
import math
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



# Define basic beam parameters and loading
length = 5.0
height = 1.0
thickness = height
E = 50000000.0
Py = 0.0 #-1000
Pz = 0.0 #2000

global glCantileverCrossSection
glCantileverCrossSection = 0

global glCantileverStress
glCantileverStress = 0

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
CrossSection2 = "2D_cantilever_beam/static/images/DoubleT.png"
CrossSection3 = "2D_cantilever_beam/static/images/Circular.png"
CrossSection4 = "2D_cantilever_beam/static/images/Triangular.png"
CrossSectionSource1 = ColumnDataSource(data=dict(sp1=[], x=[] , y=[]))
CrossSectionSource2 = ColumnDataSource(data=dict(sp2=[], x=[] , y=[]))
CrossSectionSource3 = ColumnDataSource(data=dict(sp3=[], x=[] , y=[]))
CrossSectionSource4 = ColumnDataSource(data=dict(sp4=[], x=[] , y=[]))

# Source & Initialization of Internal Element Plot:
XYElement = "2D_cantilever_beam/static/images/XYElement.png"
XYElementSource = ColumnDataSource(data=dict(sp4=[], x=[] , y=[]))
XYElementSource.data = dict(sp4=[XYElement], x = [0], y = [0])
XYElement2 = "2D_cantilever_beam/static/images/XYElement.png"
XYElement2Source = ColumnDataSource(data=dict(sp4=[], x=[] , y=[]))
XYElement2Source.data = dict(sp4=[XYElement], x = [0], y = [0])
XYBeam = "2D_cantilever_beam/static/images/XYBeam.png"
XYBeamSource = ColumnDataSource(data=dict(sp5=[], x=[] , y=[]))
XYBeamSource.data = dict(sp5=[XYBeam], x = [0], y = [0])



# Construct source files of dynamic labels:
labelXY = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     y=[2.7,-.3],
                                     text=['y','x']))
labelXZ = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     y=[-2.7,-.3],
                                     text=['z','x']))     
labelXYElement = ColumnDataSource(dict(x=[-.3,5.8,0.7,0.7], y=[2.7,-.3,0.7,-0.7], text=['y','x','\\frac{a}{2}','-\\frac{a}{2}']))                                                           
                                     
# Construct the source files for the force labels
sourceFyLabel = ColumnDataSource(data=dict( x=[length], y=[height+0.5], f=['Fy'] ))
sourceFzLabel = ColumnDataSource(data=dict( x=[length], y=[height+0.5], f=['Fz'] ))

# Construct source files of dynamic axis:
CoordArrowXYSource = ColumnDataSource(data=dict(xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0])) 
CoordArrowXZSource = ColumnDataSource(data=dict(xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]))  
CoordArrowXYESource = ColumnDataSource(data=dict(xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]))     


# Sigma and tau sources in "XY-Element" plot:
Sigmaplot_l_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Sigmaplot_r_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_l_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_r_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Tauplot_u_Source = ColumnDataSource(data=dict(x=[] , y=[]))
Sigmaplot_Label_Source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
Tauplot_Label_Source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
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
                                                                                      glCantileverCrossSection
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
    XCoordsDefXY , YCoordsDefXY = functions.create_coordinates_list( listDeformedElementsXY)
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
                                                                                                        Py, Pz,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX,
                                                                                                        glCantileverCrossSection
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXY = functions.elements_color_determiner(
                                                                  True,
                                                                  'XY',
                                                                  listDeformedElementsXY,
                                                                  noElementsX,
                                                                  noElementsY,
                                                                  E, height, thickness,
                                                                  length, Py, Pz,
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXZ,
                                                                  glCantileverCrossSection
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
                                                                                      glCantileverCrossSection
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
    XCoordsDefXZ , YCoordsDefXZ = functions.create_coordinates_list( listDeformedElementsXZ)
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ = functions.values_determiner( 
                                                                                                        Py, Pz,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX,
                                                                                                        glCantileverCrossSection
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXZ = functions.elements_color_determiner(
                                                                  True,
                                                                  'XZ',
                                                                  listDeformedElementsXZ,
                                                                  noElementsX,
                                                                  noElementsZ,
                                                                  E, thickness, height,
                                                                  length, Py, Pz, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXY,
                                                                  glCantileverCrossSection
                                                             )

    return (
                listDeformedElementsXZ,
                XCoordsDefXZ,
                YCoordsDefXZ,
                listValuesLowerXZ,
                colorListDeformedXZ,
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

# Create alpha list for the transparency of the colored patches
alphaList = list()
for index in range(len(listDeformedElementsXY)):
    alphaList.append(1)

# Update stresses along xy-Element (sigma and tau)
def fun_update_xy_element_stresses(length,height,thickness,glCantileverCrossSection,Py,Pz):

    x_pos = 2.5
    y_pos = -height/2.0
    if(glCantileverCrossSection==3):
        y_pos = -height*2.0/3.0
    sigma_x_l,sigma_x_r,tau_xy = functions.calculate_stresses_xy_element(x_pos,y_pos,length,height,thickness,glCantileverCrossSection,Py,Pz)
    
    ## IF SIGMA BUTTON IS ACTIVATED:
    if (glCantileverStress==0):
        ## DELETE TAU PLOTS
        Tauplot_l_Source.data = dict(x = [], y = [])
        Tauplot_r_Source.data = dict(x = [], y = [])
        Tauplot_u_Source.data = dict(x = [], y = [])   
        ## DELETE TAU LABELS
        Tauplot_Label_Source.data = dict(x=[], y=[], names=[])
        ## DELETE TAU ARROWS
        TauArrowSource1.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        TauArrowSource2.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        TauArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        TauArrowSource4.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)

        ## SCALING AND POSITION OF SIGMA GLYPHS
        sigmascaling = 0.0000025*50
        sigma_l_pos = 1.5
        sigma_r_pos = 3.5

        ## SIGMA_X LEFT END DATA SOURCE:
        sigma_x_l_scaled = np.linspace(0, 0, len(sigma_x_l))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_l)): 
            sigma_x_l_scaled[i]=sigma_x_l[len(sigma_x_l)-i-1]*sigmascaling
        SigmaPlot_l_x = np.hstack((np.linspace(sigma_l_pos, sigma_l_pos, len(sigma_x_l)), sigma_l_pos-abs(sigma_x_l_scaled)))
        if (glCantileverCrossSection==3):        
            SigmaPlot_l_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(sigma_x_l)),np.linspace(1.0/6.0, -0.525, len(sigma_x_l))))
        else:
            SigmaPlot_l_y = np.hstack((np.linspace(-0.525, 0, len(sigma_x_l)),np.linspace(0, -0.525, len(sigma_x_l))))
        Sigmaplot_l_Source.data = dict(x = SigmaPlot_l_x, y = SigmaPlot_l_y)

        ## SIGMA_X RIGHT END DATA SOURCE:
        sigma_x_r_scaled = np.linspace(0, 0, len(sigma_x_r))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_r)): 
            sigma_x_r_scaled[i]=sigma_x_r[len(sigma_x_r)-i-1]*sigmascaling
        SigmaPlot_r_x = np.hstack((np.linspace(sigma_r_pos, sigma_r_pos, len(sigma_x_r)), sigma_r_pos+abs(sigma_x_r_scaled)))
        if (glCantileverCrossSection==3):
            SigmaPlot_r_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(sigma_x_r)),np.linspace(1.0/6.0, -0.525, len(sigma_x_r))))
        else:
            SigmaPlot_r_y = np.hstack((np.linspace(-0.525, 0, len(sigma_x_r)),np.linspace(0, -0.525, len(sigma_x_r))))
        Sigmaplot_r_Source.data = dict(x = SigmaPlot_r_x, y = SigmaPlot_r_y)

        # POSITION SIGMA LABELS
        if(glCantileverCrossSection==3):
            Sigmaplot_Label_Source.data = dict(
                x=[max(sigma_r_pos+abs(sigma_x_r_scaled))+0.1,min(sigma_l_pos-abs(sigma_x_l_scaled))-0.6], 
                y=[-0.3, -0.3], names=["\\sigma_{xx}","\\sigma_{xx}"])            
        else:   
            Sigmaplot_Label_Source.data = dict(
                x=[max(sigma_r_pos+abs(sigma_x_r_scaled))+0.1,min(sigma_l_pos-abs(sigma_x_l_scaled))-0.6], 
                y=[-0.4, -0.4], names=["\\sigma_{xx}","\\sigma_{xx}"])
        
        # SCALING AND POSITIONING OF SIGMA ARROWS
        arrow_scale = 0.7
        arrow_adjust_x = 0.05

        # Arrows left end 
        if (sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))] < -0.05): 
            SigmaArrowSource1.stream(dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4]),rollover=1)
            SigmaArrowSource2.stream(dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] ),rollover=1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        elif (sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))] > 0.05): 
            SigmaArrowSource1.stream(dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4]),rollover=1)
            SigmaArrowSource2.stream(dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] ),rollover=1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        else:
            SigmaArrowSource1.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
            SigmaArrowSource2.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)

        # Arrows right end
        if (sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))] < -0.05): 
            SigmaArrowSource4.stream(dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4]),rollover=1)
            SigmaArrowSource5.stream(dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] ),rollover=1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        elif (sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))] > 0.05): 
            SigmaArrowSource4.stream(dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], ys=[-0.4] , ye=[-0.4]),rollover=1)
            SigmaArrowSource5.stream(dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , ys=[-0.25] , ye=[-0.25] ),rollover=1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        else:
            SigmaArrowSource4.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
            SigmaArrowSource5.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)

    ## IF TAU BUTTON IS ACTIVATED:
    if (glCantileverStress==1):    
        ## DELETE SIGMA PLOTS
        Sigmaplot_l_Source.data = dict(x = [], y = [])
        Sigmaplot_r_Source.data = dict(x = [], y = [])
        ## DELETE SIGMA LABELS
        Sigmaplot_Label_Source.data = dict(x=[], y=[], names=[])
        ## DELETE SIGMA ARROWS
        SigmaArrowSource1.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        SigmaArrowSource2.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        SigmaArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        SigmaArrowSource4.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        SigmaArrowSource5.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        SigmaArrowSource6.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)

        ## SCALING AND POSITION OF TAU GLYPHS
        tau_xy_scaling = 0.000005*50
        tau_xy_l_pos_x = 1.5
        tau_xy_r_pos_x = 3.5
        tau_xy_u_pos_x = 2.5        

        ## TAU LEFT END DATA SOURCE:
        tau_xy_l_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list 
        for i in range(len(tau_xy)): 
            tau_xy_l_scaled[i]=tau_xy[len(tau_xy)-i-1]*tau_xy_scaling
        TauPlot_l_x = np.hstack((np.linspace(tau_xy_l_pos_x, tau_xy_l_pos_x, len(tau_xy)), tau_xy_l_pos_x-abs(tau_xy_l_scaled)))
        if (glCantileverCrossSection==3):        
            TauPlot_l_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(tau_xy)),np.linspace(1.0/6.0, -0.525, len(tau_xy))))
        else:    
            TauPlot_l_y = np.hstack((np.linspace(-0.525, 0, len(tau_xy)),np.linspace(0, -0.525, len(tau_xy))))            
        Tauplot_l_Source.data = dict(x = TauPlot_l_x, y = TauPlot_l_y)
        
        ## TAU RIGHT END DATA SOURCE:
        tau_xy_r_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list 
        for i in range(len(tau_xy)): 
            tau_xy_r_scaled[i]=tau_xy[len(tau_xy)-i-1]*tau_xy_scaling
        TauPlot_r_x = np.hstack((np.linspace(tau_xy_r_pos_x, tau_xy_r_pos_x, len(tau_xy)), tau_xy_r_pos_x+abs(tau_xy_r_scaled)))
        if (glCantileverCrossSection==3):       
            TauPlot_r_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(tau_xy)),np.linspace(1.0/6.0, -0.525, len(tau_xy))))
        else:
            TauPlot_r_y = np.hstack((np.linspace(-0.525, 0, len(tau_xy)),np.linspace(0, -0.525, len(tau_xy))))            
        Tauplot_r_Source.data = dict(x = TauPlot_r_x, y = TauPlot_r_y)

        ## TAU UPPER BORDER DATA SOURCE
        tau_xy_u_scaled = np.linspace(0, 0, len(tau_xy))
        # Create scaled and reversed list consisting of tau_max value: 
        for i in range(len(tau_xy)): 
            tau_xy_u_scaled[i]=tau_xy[len(tau_xy)-1]*tau_xy_scaling
        TauPlot_u_x = np.hstack((np.linspace(tau_xy_u_pos_x-1, tau_xy_u_pos_x+1, len(tau_xy)), np.linspace(tau_xy_u_pos_x+1, tau_xy_u_pos_x-1, len(tau_xy))))
        if (glCantileverCrossSection==3):              
            TauPlot_u_y = np.hstack((np.linspace(1.0/6.0, 1.0/6.0, len(tau_xy)), abs(tau_xy_u_scaled)+1.0/6.0)) 
        else:
            TauPlot_u_y = np.hstack((np.linspace(0, 0, len(tau_xy)), abs(tau_xy_u_scaled)))            
        Tauplot_u_Source.data = dict(x = TauPlot_u_x, y = TauPlot_u_y)

        # POSITION TAU LABELS
        if(glCantileverCrossSection==3):
            Tauplot_Label_Source.data = dict(
                x=[max(tau_xy_r_pos_x+abs(tau_xy_r_scaled))+0.1, min(tau_xy_l_pos_x-abs(tau_xy_l_scaled))-0.5, tau_xy_l_pos_x+0.7], 
                y=[-0.3, -0.3, max(abs(tau_xy_u_scaled))+0.3 ], names=['\\tau_{xy}','\\tau_{xy}','\\tau_{yx}'])
        else:    
            Tauplot_Label_Source.data = dict(
                x=[max(tau_xy_r_pos_x+abs(tau_xy_r_scaled))+0.1, min(tau_xy_l_pos_x-abs(tau_xy_l_scaled))-0.5, tau_xy_l_pos_x+0.7], 
                y=[-0.4, -0.4, max(abs(tau_xy_u_scaled))+0.15 ], names=['\\tau_{xy}','\\tau_{xy}','\\tau_{yx}'])

        ### SCALING AND POSITIONING OF ARROWS:
        # Position arrows into tau glyph
        arrow_adjust_x = max(abs(tau_xy_l_scaled))/4.0
        # Make arrow size grow with increasing tau stress, but restrict length of arrows to dimensions of tau glyph
        if (max(abs(tau_xy_u_scaled))/2.0 >= 0.15):
            arrow_adjust_y = 0.15
        else:
            arrow_adjust_y = max(abs(tau_xy_u_scaled))/2.0
        if (glCantileverCrossSection==3):
            arrow_move_y = 0.04 + 1.0/12.0    
        else:
            arrow_move_y = 0.04    
        
        ## ARROW LEFT END:
        tau_xy_l_pos_y = -0.25                 
        if (Py<0): 
            TauArrowSource1.stream(dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], ys=[tau_xy_l_pos_y+arrow_adjust_y+arrow_move_y] , ye=[tau_xy_l_pos_y-arrow_adjust_y+arrow_move_y]),rollover=1)
        elif (Py>0):
            TauArrowSource1.stream(dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], ys=[tau_xy_l_pos_y-arrow_adjust_y+arrow_move_y] , ye=[tau_xy_l_pos_y+arrow_adjust_y+arrow_move_y]),rollover=1)
        else:            
            TauArrowSource1.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)
        
        ## ARROWS RIGHT END:             
        tau_xy_r_pos_y = -0.25           
        if (Py<-30):
            TauArrowSource2.stream(dict(xs=[tau_xy_r_pos_x+arrow_adjust_x] , xe= [tau_xy_r_pos_x+arrow_adjust_x], ys=[tau_xy_r_pos_y-arrow_adjust_y+arrow_move_y] , ye=[tau_xy_r_pos_y+arrow_adjust_y+arrow_move_y]),rollover=1)
        elif (Py>30):
            TauArrowSource2.stream(dict(xs=[tau_xy_r_pos_x+arrow_adjust_x] , xe= [tau_xy_r_pos_x+arrow_adjust_x], ys=[tau_xy_r_pos_y+arrow_adjust_y+arrow_move_y] , ye=[tau_xy_r_pos_y-arrow_adjust_y+arrow_move_y]),rollover=1)
        else:            
            TauArrowSource2.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)

        ## ARROWS UPPER BORDER:
        tau_xy_u_pos_y = 0.0            
        # New arrow scaling and positioning for upper tau stress
        if (max(abs(tau_xy_u_scaled)) >= 0.3):
            arrow_adjust_x = 0.3
        else:
            arrow_adjust_x = max(abs(tau_xy_u_scaled))
        if (glCantileverCrossSection==3):
            arrow_adjust_y = max(abs(tau_xy_u_scaled))/2.0 + 1.0/6.0
        else:            
            arrow_adjust_y = max(abs(tau_xy_u_scaled))/2.0
        if (Py<-30):
            TauArrowSource3.stream(dict(xs=[(tau_xy_u_pos_x-0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)+arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y]),rollover=1)
            TauArrowSource4.stream(dict(xs=[(tau_xy_u_pos_x+0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)+arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y]),rollover=1)                     
        elif (Py>30):
            TauArrowSource3.stream(dict(xs=[(tau_xy_u_pos_x-0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)-arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y]),rollover=1)
            TauArrowSource4.stream(dict(xs=[(tau_xy_u_pos_x+0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)-arrow_adjust_x], ys=[tau_xy_u_pos_y+arrow_adjust_y] , ye=[tau_xy_u_pos_y+arrow_adjust_y]),rollover=1)
        else:
            TauArrowSource3.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)        
            TauArrowSource4.stream(dict(xs=[] , xe= [], ys=[] , ye=[]),rollover=-1)



# The function to be excuted whenever the force in the y direction changes
def fun_change_Py(attrname, old, new):
    global Py,Pz, listDeformedElementsXY
    
    # Change the value of the applied force according to the slider value
    Py = Yforce_slider.value*100.0

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
                                                                  length, Py, Pz, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXY,
                                                                  glCantileverCrossSection
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXZdef.data   = dict( x=sourceXZdef.data['x'], y=sourceXZdef.data['y'], c=colorListDeformedXZ, a=alphaList)
    sourceXYdef.data   = dict( x=XCoordsDefXY,   y=YCoordsDefXY,   c =colorListDeformedXY,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards

    if Py == 0:
        sourceArrowXY.stream(dict(xs=[], ys=[],xe=[], ye=[]),rollover=-1)
        sourceFyLabel.data = dict(x= [],y= [],f= [])                                 
    else:
        if sourceXYdef.data['y'][0][3] <= 0:
            sourceArrowXY.stream(dict(
                                      xs=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ys=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-2][2]+1.5*abs(Py)/5000+0.25],
                                      xe=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ye=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-2][2]],
                                 ),rollover=1)
            sourceFyLabel.stream(dict(
                                      x= sourceArrowXY.data['xs'],
                                      y= [sourceArrowXY.data['ys'][0] + 0.5],
                                      f= ['Fy']
                                 ),rollover=1)
        else:
            sourceArrowXY.stream(dict(
                                      xs=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ys=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-1][2]-1.5*abs(Py)/5000-0.25],
                                      xe=[sourceXYdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ye=[sourceXYdef.data['y'][len( sourceXZdef.data['y'])-1][2]],
                                 ),rollover=1)
            sourceFyLabel.stream(dict(
                                      x= sourceArrowXY.data['xs'],
                                      y= [sourceArrowXY.data['ys'][0] - 0.5],
                                      f= ['Fy']
                                 ),rollover=1)
        
    update_colorBar_extremas(smallestValue,biggestValue)
    fun_update_xy_element_stresses(length,height,thickness,glCantileverCrossSection,Py,Pz)
    

# The function to be excuted whenever the force in the z direction changes
def fun_change_Pz(attrname, old, new):
    global Py,Pz, listDeformedElementsXZ
    
    # Change the value of the applied force according to the slider value
    Pz = Zforce_slider.value*100.0

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
                                                                  length, Py, Pz,
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXZ,
                                                                  glCantileverCrossSection
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXYdef.data   = dict( x=sourceXYdef.data['x'], y=sourceXYdef.data['y'], c=colorListDeformedXY, a=alphaList)
    sourceXZdef.data   = dict( x=XCoordsDefXZ,   y=YCoordsDefXZ,   c =colorListDeformedXZ,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards

    if Pz == 0:
        sourceArrowXZ.stream(dict(xs=[],ys=[],xe=[],ye=[]),rollover=-1)
        sourceFzLabel.data = dict(x=[],y=[],f=[])
    else:
        if sourceXZdef.data['y'][0][3] <= 0:
            sourceArrowXZ.stream(dict(
                                      xs=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-2][2]+1.5*abs(Pz)/5000.0+0.25],
                                      xe=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-2][2]], 
                                      ye=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-2][2]],
                                 ),rollover=1)
            sourceFzLabel.stream(dict(
                                      x= sourceArrowXZ.data['xs'],
                                      y= [sourceArrowXZ.data['ys'][0] + 0.5],
                                      f= ['Fz']
                                 ),rollover=1)
        else:
            sourceArrowXZ.stream(dict(
                                      xs=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ys=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]-1.5*abs(Pz)/5000.0-0.25],
                                      xe=[sourceXZdef.data['x'][len( sourceXZdef.data['x'])-1][2]], 
                                      ye=[sourceXZdef.data['y'][len( sourceXZdef.data['y'])-1][2]],
                                 ),rollover=1)
            sourceFzLabel.stream(dict(
                                      x= sourceArrowXZ.data['xs'],
                                      y= [sourceArrowXZ.data['ys'][0] - 0.5],
                                      f= ['Fz']
                                 ),rollover=1)
        
    update_colorBar_extremas(smallestValue,biggestValue)
    fun_update_xy_element_stresses(length,height,thickness,glCantileverCrossSection,Py,Pz)

# Function that is called, when change in selected cross section occurs
def fun_change_Cross_Section(attrname, old, new):
    if (radio_button_group.active == 0 ):
        CrossSectionSource1.data = dict(sp1=[CrossSection1], x = [0], y = [0])
        CrossSectionSource2.data = dict(sp2=[], x = [], y = [])
        CrossSectionSource3.data = dict(sp3=[], x = [], y = [])
        CrossSectionSource4.data = dict(sp4=[], x = [], y = [])
        CoordArrowXYSource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)
        CoordArrowXZSource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)
        CoordArrowXYESource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)
        labelXY.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])  
        labelXZ.data=dict(x=[-.3,5.8], y=[-2.7,-.3], text=['z','x'])      
        labelXYElement.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])                          
        XYElementSource.data = dict(sp4=[XYElement], x = [0], y = [0])   
        XYElement2Source.data = dict(sp4=[], x = [], y = [])          
    elif (radio_button_group.active == 1):
        CrossSectionSource1.data = dict(sp1=[], x = [], y = [])
        CrossSectionSource2.data = dict(sp2=[CrossSection2], x = [0], y = [0])
        CrossSectionSource3.data = dict(sp3=[], x = [], y = [])
        CrossSectionSource4.data = dict(sp4=[], x = [], y = [])        
        CoordArrowXYSource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)   
        CoordArrowXYESource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)  
        labelXY.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])                           
        labelXYElement.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])                                         
        XYElementSource.data = dict(sp4=[XYElement], x = [0], y = [0])           
        XYElement2Source.data = dict(sp4=[], x = [], y = [])        
    elif (radio_button_group.active == 2):
        CrossSectionSource1.data = dict(sp1=[], x = [], y = [])
        CrossSectionSource2.data = dict(sp2=[], x = [], y = [])
        CrossSectionSource3.data = dict(sp3=[CrossSection3], x = [0], y = [0])
        CrossSectionSource4.data = dict(sp4=[], x = [], y = [])        
        CoordArrowXYSource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)
        CoordArrowXYESource.stream(dict( xs=[-0.5], ys=[0.0],xe=[5.9], ye=[0.0]),rollover=1)            
        labelXY.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])                         
        labelXYElement.data=dict(x=[-.3,5.8], y=[2.7,-.3], text=['y','x'])    
        XYElementSource.data = dict(sp4=[XYElement], x = [0], y = [0])   
        XYElement2Source.data = dict(sp4=[], x = [], y = [])                                            
    elif (radio_button_group.active == 3):
        CrossSectionSource1.data = dict(sp1=[], x = [], y = [])
        CrossSectionSource2.data = dict(sp2=[], x = [], y = [])
        CrossSectionSource3.data = dict(sp3=[], x = [], y = [])       
        CrossSectionSource4.data = dict(sp4=[CrossSection4], x = [0], y = [0]) 
        CoordArrowXYSource.stream(dict( xs=[-0.5], ys=[1.0/6.0],xe=[5.9], ye=[1.0/6.0]),rollover=1)
        CoordArrowXYESource.stream(dict( xs=[-0.5], ys=[1.0/6.0],xe=[5.9], ye=[1.0/6.0]),rollover=1)   
        labelXY.data=dict(x=[-.3,5.8], y=[2.7,-.3+1.0/6.0], text=['y','x'])
        labelXYElement.data=dict(x=[-.3,5.8], y=[2.7,-.3+1.0/6.0], text=['y','x'])    
        XYElementSource.data = dict(sp4=[], x =[], y = []) 
        XYElement2Source.data = dict(sp4=[XYElement], x = [0], y = [0])                                            

    global glCantileverCrossSection
    glCantileverCrossSection = radio_button_group.active
    global glCantileverStress
    glCantileverStress = radio_button_group2.active

# Function to initialize data
def init_data():
    Yforce_slider.value = 0
    Zforce_slider.value = 0
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

# Construct the force sliders
Yforce_slider = LatexSlider(title= 'F_y =   ', value=0.0, start=-1.0, end=1.0, step=0.1, value_unit='\cdot F_{y,max}')
Zforce_slider = LatexSlider(title= 'F_z =  ', value=0.0, start=-1.0, end=1.0, step=0.1, value_unit='\cdot F_{z,max}')

# Construct radio button to choose between geometries of cross section
radio_button_group = RadioButtonGroup(name="Geometry of cross section",labels=["Quadratic", "Double-T", "Circular","Triangular"], active=glCantileverCrossSection)

# Construct radio button to choose between plot of sigma(y) or tau(y)
radio_button_group2 = RadioButtonGroup(name="Plot of sigma or tau",labels=["Normal Stresses", "Shear Stresses"], active=glCantileverStress)

# Construct reset button
Reset_button = Button(label="Reset", button_type="success")



############ PLOT 1: YZ Cross Section PLOT ###############
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

plotDefYZ.add_glyph(CrossSectionSource1,ImageURL(url="sp1", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefYZ.add_glyph(CrossSectionSource2,ImageURL(url="sp2", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefYZ.add_glyph(CrossSectionSource3,ImageURL(url="sp3", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefYZ.add_glyph(CrossSectionSource4,ImageURL(url="sp4", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))

labelYZ = ColumnDataSource(data=dict(x=[0.5,-4.0],
                                     y=[4.0,-0.6],
                                     text=['y','z']))
plotDefYZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-4.5, 
                           x_end=0, 
                           y_end=4.5, 
                           ))

plotDefYZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_end=-4.5, 
                           y_start=0, 
                           x_start=4.5, 
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


############ PLOT 2: XY PLOT ###############
plotDefXY = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in XY-View',
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

plotDefXY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-3, 
                           x_end=0, 
                           y_end=2.9, 
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
plotDefXY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='ys',
                           x_end='xe', 
                           y_end='ye', 
                           source = CoordArrowXYSource) 
                    )

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


############ PLOT 3: XZ PLOT ###############
plotDefXZ = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in XZ-View',
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

plotDefXZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=3, 
                           x_end=0, 
                           y_end=-2.9, 
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

# Construct the arrows
plotDefXZ.add_layout( 
                     Arrow(end=NormalHead(line_color="black",line_width=3,size=10),
                           line_width=3,
                           x_start=['xs'][0], 
                           y_start=['ys'][0], 
                           x_end=['xe'][0], 
                           y_end=['ye'][0], 
                           source = sourceArrowXZ)
                    )

plotDefXZ.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='ys',
                           x_end='xe', 
                           y_end='ye', 
                           source = CoordArrowXZSource) 
                    )             

# Construct the force labels
plotDefXZ.add_layout(LabelSet(
                                  x='x', y='y',
                                  text='f',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFzLabel
                              )
                    )


############ PLOT 4: XY ELEMENT PLOT ###############
plotXYElement = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Stresses along detached Element',
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

plotXYElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=-3, 
                           x_end=0, 
                           y_end=2.9, 
                           ))

plotXYElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='ys',
                           x_end='xe', 
                           y_end='ye', 
                           source = CoordArrowXYESource) 
                    )



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

plotXYElement.add_glyph(XYBeamSource,ImageURL(url="sp5", x=0, y=0.5, w=5, h=1.04))
plotXYElement.add_glyph(XYElementSource,ImageURL(url="sp4", x=1.5, y=0, w=2, h=0.535))
plotXYElement.add_glyph(XYElement2Source,ImageURL(url="sp4", x=1.5, y=1.0/6.0, w=2, h=0.535*(1+1.0/3.0)))

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

Sigmaplot_Labels = LatexLabelSet(
    x='x', y='y', text='names', source=Sigmaplot_Label_Source, 
    text_color ="#0065BD", level='glyph', x_offset=0, y_offset=0)

Tauplot_Labels = LatexLabelSet(
    x='x', y='y', text='names', source=Tauplot_Label_Source, 
    text_color ="#E37222", level='glyph', x_offset=0, y_offset=0)    

plotXYElement.add_layout(Sigmaplot_Labels)
plotXYElement.add_layout(Tauplot_Labels)

############## PLOT 5: Color Bar ##########################
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

## Create colorBar patches with node coords 
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

## Determine the color distribution in the color bar
smallestValue,biggestValue = 0.0,10.0
valuesRange = list()
## Create equidistant vector with 50 members between smallestValue and biggestValue:
for i in range(50):
    valuesRange.append(smallestValue + (float(i)/49.0)*(biggestValue - smallestValue))
## Create vector with 50 colors corresponding to varluesRange-vector:
for i in range(50):
    colorBarColorList.append(functions.color_determiner( smallestValue, biggestValue, valuesRange[i] ))
    colorBarAlphaList.append( 1 )

## Label colorbar min-max stess range
def update_colorBar_extremas(smallesValue, biggestValue):
    colorBar.title.text =  " "*15  + "-" + " "*55 + "Normal Stress" + " "*55 + "+"

## Construct the source file for the color bar
colorBarSource = ColumnDataSource(data=dict( x=colorBarXCoords, y=colorBarYCoords, c =colorBarColorList, a=colorBarAlphaList ))

# Construct the patches 
colorBar.patches( xs='x', ys='y', source=colorBarSource, color = 'c', alpha = 'a' )
plotDefXY.patches  (xs='x', ys='y', source=sourceXYdef  , color = 'c', alpha = 'a')
plotDefXZ.patches  (xs='x', ys='y', source=sourceXZdef  , color = 'c', alpha = 'a')

# Notify the corresponding functions to carry out the changes characterized by
# the sliders
Yforce_slider.on_change('value',fun_change_Py)
Zforce_slider.on_change('value',fun_change_Pz)
radio_button_group.on_change('active',fun_change_Cross_Section,fun_change_Py,fun_change_Pz)
radio_button_group2.on_change('active',fun_change_Cross_Section,fun_change_Py,fun_change_Pz)
Reset_button.on_click(init_data)

init_data()    

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=950)

# add beam definition image
Scheme = Div( text = "<img src='/2D_cantilever_beam/static/images/3DBeam.png' width=550 height=405>",
            width = 550,
            height = 405 )


curdoc().add_root(column(row(Spacer(height=650),description, column(Spacer(height=100),Scheme)),row(
    column(plotDefYZ,widgetbox(radio_button_group),Yforce_slider,Zforce_slider,Reset_button),
    column(row(column(plotXYElement,row(Spacer(width=80),radio_button_group2)),column(row(plotDefXY, plotDefXZ),colorBar))))))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '