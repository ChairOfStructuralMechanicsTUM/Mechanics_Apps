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
Pzn = 0.0 #-1000
Pyn = 0.0 #2000

global glCantileverCrossSection
glCantileverCrossSection = 0

global glCantileverStress
glCantileverStress = 0


# Define mesh for visualization
noElementsX = 80
noElementsZn = 20
noElementsYn = 20
elementSizeX = length / noElementsX
elementSizeZn = height / noElementsZn
elementSizeYn = thickness / noElementsYn
amplificationFactor = 100


# Cross Section Source:
CrossSection1 = "2D_cantilever_beam/static/images/Rectangular.png"
CrossSection2 = "2D_cantilever_beam/static/images/DoubleT.png"
CrossSection3 = "2D_cantilever_beam/static/images/Circular.png"
CrossSection4 = "2D_cantilever_beam/static/images/Triangular.png"
CrossSectionSource1 = ColumnDataSource(data=dict(sp1=[], x=[] , zn=[]))
CrossSectionSource2 = ColumnDataSource(data=dict(sp2=[], x=[] , zn=[]))
CrossSectionSource3 = ColumnDataSource(data=dict(sp3=[], x=[] , zn=[]))
CrossSectionSource4 = ColumnDataSource(data=dict(sp4=[], x=[] , zn=[]))

# Source & Initialization of Internal Element Plot:
XZElement = "2D_cantilever_beam/static/images/XZElement.png"
XZElementSource = ColumnDataSource(data=dict(sp4=[], x=[] , zn=[]))
XZElementSource.data = dict(sp4=[XZElement], x = [0], zn = [0])
XZElement2 = "2D_cantilever_beam/static/images/XZElement.png"
XZElement2Source = ColumnDataSource(data=dict(sp4=[], x=[] , zn=[]))
XZElement2Source.data = dict(sp4=[XZElement], x = [0], zn = [0])
XZBeam = "2D_cantilever_beam/static/images/XZBeam.png"
XZBeamSource = ColumnDataSource(data=dict(sp5=[], x=[] , zn=[]))
XZBeamSource.data = dict(sp5=[XZBeam], x = [0], zn = [0])



# Construct source files of dynamic labels:
labelXZn = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     zn=[-2.7,-.3],
                                     text=['zn','x']))
labelXYn = ColumnDataSource(data=dict(x=[-.3,5.8],
                                     zn=[-2.7,-.3],
                                     text=['yn','x']))     
labelXZnElement = ColumnDataSource(dict(x=[-.3,5.8,0.7,0.7], zn=[-2.7,-.3,0.7,-0.7], text=['zn','x','\\frac{a}{2}','-\\frac{a}{2}']))                                                           
                                     
# Construct the source files for the force labels
sourceFznLabel = ColumnDataSource(data=dict( x=[length], zn=[-(height+0.5)], f=['Fz'] ))
sourceFynLabel = ColumnDataSource(data=dict( x=[length], zn=[(height+0.5)], f=['Fy'] ))

# Construct source files of dynamic axis:
CoordArrowXZnSource     = ColumnDataSource(data=dict(xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0])) 
CoordArrowXYnSource     = ColumnDataSource(data=dict(xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]))  
CoordArrowXZnESource    = ColumnDataSource(data=dict(xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]))     


# Sigma and tau sources in "XZn-Element" plot:
Sigmaplot_l_Source      = ColumnDataSource(data=dict(x=[] , zn=[]))
Sigmaplot_r_Source      = ColumnDataSource(data=dict(x=[] , zn=[]))
Tauplot_l_Source        = ColumnDataSource(data=dict(x=[] , zn=[]))
Tauplot_r_Source        = ColumnDataSource(data=dict(x=[] , zn=[]))
Tauplot_u_Source        = ColumnDataSource(data=dict(x=[] , zn=[]))
Sigmaplot_Label_Source  = ColumnDataSource(data=dict(x=[] , zn=[], names=[]))
Tauplot_Label_Source    = ColumnDataSource(data=dict(x=[] , zn=[], names=[]))
# Arrow sources in "XZn-Element" plot:
SigmaArrowSource1   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
SigmaArrowSource2   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
SigmaArrowSource3   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
SigmaArrowSource4   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
SigmaArrowSource5   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
SigmaArrowSource6   = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
TauArrowSource1     = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
TauArrowSource2     = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
TauArrowSource3     = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))
TauArrowSource4     = ColumnDataSource(data = dict(xs=[], zns=[], xe=[], zne=[]))

# colorBar source plot:
colorBarSource = ColumnDataSource(data = dict( x=[], zn=[], c=[], a=[] ))
colorDistributionNoteSource  = ColumnDataSource(data=dict(x=[5.9] , zn=[-2.8], note=['non-linear color distribution!']))


def deformed_cantilever_beam_determiner_XZn( 
                                            length, height, thickness, E, Pzn, 
                                            Pyn, noElementsX, noElementsZn, 
                                            noElementsYn, elementSizeX,  
                                            elementSizeZn, elementSizeYn, 
                                            amplificationFactor
                                          ):
    # Construct the deformed beam's center line
    deformedBeamXZn, deformedBeamXYn = functions.construct_deformed_beam_centerLine(
                                                                                      Pzn, Pyn, E, 
                                                                                      noElementsX,
                                                                                      thickness, height, 
                                                                                      length, elementSizeX,
                                                                                      amplificationFactor, 
                                                                                      glCantileverCrossSection
                                                                                 )
    
    # Construct the normal vectors to the deformed beam's center line
    normalVecrtorsXZnUpperDef, normalVectorsXZnLowerDef = functions.construct_normal_vectors( deformedBeamXZn )
    
    # Construct mesh for the deformed and the deformed beams    
    listDeformedElementsXZn = functions.construct_deformed_elements(   
                                                                      deformedBeamXZn,
                                                                      elementSizeX,
                                                                      elementSizeZn,
                                                                      noElementsX,
                                                                      noElementsZn,
                                                                      normalVecrtorsXZnUpperDef,
                                                                      normalVectorsXZnLowerDef
                                                                  )
    
    # Determine the patches' X,Zn,Yn coordinates
    XCoordsDefXZn , YCoordsDefXZn = functions.create_coordinates_list( listDeformedElementsXZn)
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXZn, listValuesLowerXYn = functions.values_determiner( 
                                                                                                        Pzn, Pyn,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX,
                                                                                                        glCantileverCrossSection
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXZn = functions.elements_color_determiner(
                                                                  True,
                                                                  'XZ',
                                                                  listDeformedElementsXZn,
                                                                  noElementsX,
                                                                  noElementsZn,
                                                                  E, height, thickness,
                                                                  length, Pzn, Pyn,
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXYn,
                                                                  glCantileverCrossSection
                                                             )

    return (
                listDeformedElementsXZn,
                XCoordsDefXZn,
                YCoordsDefXZn,
                listValuesUpperXZn,
                colorListDeformedXZn, 
                biggestValue, smallestValue
           )
    
def deformed_cantilever_beam_determiner_XYn( 
                                           length, height, thickness, E, Pzn, 
                                           Pyn, noElementsX, noElementsZn, 
                                           noElementsYn, elementSizeX, 
                                           elementSizeZn, elementSizeYn,
                                           amplificationFactor
                                          ):
    
    # Construct the deformed beam's center line
    deformedBeamXZn, deformedBeamXYn = functions.construct_deformed_beam_centerLine(
                                                                                      Pzn, Pyn, E, 
                                                                                      noElementsX,
                                                                                      thickness, height, 
                                                                                      length, elementSizeX,
                                                                                      amplificationFactor,
                                                                                      glCantileverCrossSection
                                                                                 )
    
    # Construct the normal vectors to the deformed beam's center line
    normalVecrtorsXYnUpperDef, normalVectorsXYnLowerDef = functions.construct_normal_vectors( deformedBeamXYn )
    
    # Construct mesh for the deformed and the deformed beams     
    listDeformedElementsXYn = functions.construct_deformed_elements(   
                                                                      deformedBeamXYn,
                                                                      elementSizeX,
                                                                      elementSizeYn,
                                                                      noElementsX,
                                                                      noElementsYn,
                                                                      normalVecrtorsXYnUpperDef,
                                                                      normalVectorsXYnLowerDef
                                                                  )
    
    # Determine the patches' X,Zn,Yn coordinates
    XCoordsDefXYn , YCoordsDefXYn = functions.create_coordinates_list( listDeformedElementsXYn)
    
    # Detemine the color of the elements
    biggestValue, smallestValue, listValuesUpperXZn, listValuesLowerXYn = functions.values_determiner( 
                                                                                                        Pzn, Pyn,
                                                                                                        length,
                                                                                                        height,
                                                                                                        thickness,
                                                                                                        E, elementSizeX,
                                                                                                        glCantileverCrossSection
                                                                                                   )
    
    # Coloring the deformed elements
    colorListDeformedXYn = functions.elements_color_determiner(
                                                                  True,
                                                                  'XY',
                                                                  listDeformedElementsXYn,
                                                                  noElementsX,
                                                                  noElementsYn,
                                                                  E, thickness, height,
                                                                  length, Pzn, Pyn, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXZn,
                                                                  glCantileverCrossSection
                                                             )

    return (
                listDeformedElementsXYn,
                XCoordsDefXYn,
                YCoordsDefXYn,
                listValuesLowerXYn,
                colorListDeformedXYn,
                biggestValue, smallestValue
           )


# Construct the deformed beam in XZn plane
(listDeformedElementsXZn, XCoordsDefXZn,
 YCoordsDefXZn, listValuesUpperXZn, colorListDeformedXZn,
 biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XZn( 
                               length, height, thickness, E, Pzn, Pyn,
                               noElementsX, noElementsYn, noElementsYn,
                               elementSizeX, elementSizeZn, elementSizeYn,
                               amplificationFactor
                           )

# Construct the deformed beam in XYn plane
(listDeformedElementsXYn, XCoordsDefXYn,
 YCoordsDefXYn, listValuesLowerXYn, colorListDeformedXYn,
 biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XYn( 
                               length, height, thickness, E, Pzn, Pyn,
                               noElementsX, noElementsYn, noElementsYn,
                               elementSizeX, elementSizeZn, elementSizeYn,
                               amplificationFactor
                           )

# Create alpha list for the transparency of the colored patches
alphaList = list()
for index in range(len(listDeformedElementsXZn)):
    alphaList.append(1)

# Update stresses along xzn-Element (sigma and tau)
def fun_update_xzn_element_stresses(length,height,thickness,glCantileverCrossSection,Pzn,Pyn):
    x_pos = 2.5
    zn_pos = height/2.0
    if(glCantileverCrossSection==3):
        zn_pos = height*2.0/3.0
    sigma_x_l,sigma_x_r,tau_xzn = functions.calculate_stresses_xzn_element(x_pos,zn_pos,length,height,thickness,glCantileverCrossSection,Pzn,Pyn)
    
    ## IF SIGMA BUTTON IS ACTIVATED:
    if (glCantileverStress==0):
        ## DELETE TAU PLOTS
        Tauplot_l_Source.data = dict(x = [], zn = [])
        Tauplot_r_Source.data = dict(x = [], zn = [])
        Tauplot_u_Source.data = dict(x = [], zn = [])   
        ## DELETE TAU LABELS
        Tauplot_Label_Source.data = dict(x=[], zn=[], names=[])
        ## DELETE TAU ARROWS
        TauArrowSource1.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        TauArrowSource2.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        TauArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        TauArrowSource4.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)

        ## SCALING AND POSITION OF SIGMA GLYPHS
        sigmascaling = 0.000003*50
        sigma_l_pos = 1.5
        sigma_r_pos = 3.5

        ## SIGMA_X LEFT END DATA SOURCE:
        sigma_x_l_scaled = np.linspace(0, 0, len(sigma_x_l))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_l)): 
            sigma_x_l_scaled[i]=sigma_x_l[len(sigma_x_l)-i-1]*sigmascaling
        SigmaPlot_l_x = np.hstack((np.linspace(sigma_l_pos, sigma_l_pos, len(sigma_x_l)), sigma_l_pos-abs(sigma_x_l_scaled)))
        if (glCantileverCrossSection==3):        
            SigmaPlot_l_zn = np.hstack((np.linspace(-0.525, 1.0/6.0, len(sigma_x_l)),np.linspace(1.0/6.0, -0.525, len(sigma_x_l))))
        else:
            SigmaPlot_l_zn = np.hstack((np.linspace(-0.525, 0, len(sigma_x_l)),np.linspace(0, -0.525, len(sigma_x_l))))
        Sigmaplot_l_Source.data = dict(x = SigmaPlot_l_x, zn = SigmaPlot_l_zn)

        ## SIGMA_X RIGHT END DATA SOURCE:
        sigma_x_r_scaled = np.linspace(0, 0, len(sigma_x_r))
        # Create scaled and reversed list 
        for i in range(len(sigma_x_r)): 
            sigma_x_r_scaled[i]=sigma_x_r[len(sigma_x_r)-i-1]*sigmascaling
        SigmaPlot_r_x = np.hstack((np.linspace(sigma_r_pos, sigma_r_pos, len(sigma_x_r)), sigma_r_pos+abs(sigma_x_r_scaled)))
        if (glCantileverCrossSection==3):
            SigmaPlot_r_zn = np.hstack((np.linspace(-0.525, 1.0/6.0, len(sigma_x_r)),np.linspace(1.0/6.0, -0.525, len(sigma_x_r))))
        else:
            SigmaPlot_r_zn = np.hstack((np.linspace(-0.525, 0, len(sigma_x_r)),np.linspace(0, -0.525, len(sigma_x_r))))
        Sigmaplot_r_Source.data = dict(x = SigmaPlot_r_x, zn = SigmaPlot_r_zn)

        # POSITION SIGMA LABELS
        if(glCantileverCrossSection==3):
            Sigmaplot_Label_Source.data = dict(
                x=[max(sigma_r_pos+abs(sigma_x_r_scaled))+0.1,min(sigma_l_pos-abs(sigma_x_l_scaled))-0.6], 
                zn=[-0.3, -0.3], names=["\\sigma_{xx}","\\sigma_{xx}"])            
        else:   
            Sigmaplot_Label_Source.data = dict(
                x=[max(sigma_r_pos+abs(sigma_x_r_scaled))+0.1,min(sigma_l_pos-abs(sigma_x_l_scaled))-0.6], 
                zn=[-0.4, -0.4], names=["\\sigma_{xx}","\\sigma_{xx}"])
        
        # SCALING AND POSITIONING OF SIGMA ARROWS
        arrow_scale = 0.7
        arrow_adjust_x = 0.05

        # Arrows left end 
        if (sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))] < -0.05): 
            SigmaArrowSource1.stream(dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], zns=[-0.4] , zne=[-0.4]),rollover=1)
            SigmaArrowSource2.stream(dict(xs=[sigma_l_pos-arrow_adjust_x] , xe= [sigma_l_pos+arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , zns=[-0.25] , zne=[-0.25] ),rollover=1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        elif (sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))] > 0.05): 
            SigmaArrowSource1.stream(dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*4.0/5.0))]], zns=[-0.4] , zne=[-0.4]),rollover=1)
            SigmaArrowSource2.stream(dict(xe=[sigma_l_pos-arrow_adjust_x] , xs= [sigma_l_pos-arrow_scale*sigma_x_l_scaled[int(round(len(sigma_x_l_scaled)*2.5/5.0))]] , zns=[-0.25] , zne=[-0.25] ),rollover=1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        else:
            SigmaArrowSource1.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
            SigmaArrowSource2.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
            SigmaArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)

        # Arrows right end
        if (sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))] < -0.05): 
            SigmaArrowSource4.stream(dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], zns=[-0.4] , zne=[-0.4]),rollover=1)
            SigmaArrowSource5.stream(dict(xs=[sigma_r_pos+arrow_adjust_x] , xe= [sigma_r_pos-arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , zns=[-0.25] , zne=[-0.25] ),rollover=1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        elif (sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))] > 0.05): 
            SigmaArrowSource4.stream(dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*4.0/5.0))]], zns=[-0.4] , zne=[-0.4]),rollover=1)
            SigmaArrowSource5.stream(dict(xe=[sigma_r_pos+arrow_adjust_x] , xs= [sigma_r_pos+arrow_scale*sigma_x_r_scaled[int(round(len(sigma_x_r_scaled)*2.5/5.0))]] , zns=[-0.25] , zne=[-0.25] ),rollover=1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        else:
            SigmaArrowSource4.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
            SigmaArrowSource5.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
            SigmaArrowSource6.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)

    ## IF TAU BUTTON IS ACTIVATED:
    if (glCantileverStress==1):    
        ## DELETE SIGMA PLOTS
        Sigmaplot_l_Source.data = dict(x = [], zn = [])
        Sigmaplot_r_Source.data = dict(x = [], zn = [])
        ## DELETE SIGMA LABELS
        Sigmaplot_Label_Source.data = dict(x=[], zn=[], names=[])
        ## DELETE SIGMA ARROWS
        SigmaArrowSource1.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        SigmaArrowSource2.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        SigmaArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        SigmaArrowSource4.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        SigmaArrowSource5.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        SigmaArrowSource6.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)

        ## SCALING AND POSITION OF TAU GLYPHS
        tau_xzn_scaling = 0.0020
        tau_xy_l_pos_x = 1.5
        tau_xzn_r_pos_x = 3.5
        tau_xy_u_pos_x = 2.5        

        ## TAU LEFT END DATA SOURCE:
        tau_xzn_l_scaled = np.linspace(0, 0, len(tau_xzn))
        # Create scaled and reversed list 
        for i in range(len(tau_xzn)): 
            tau_xzn_l_scaled[i]=tau_xzn[len(tau_xzn)-i-1]*tau_xzn_scaling
        TauPlot_l_x = np.hstack((np.linspace(tau_xy_l_pos_x, tau_xy_l_pos_x, len(tau_xzn)), tau_xy_l_pos_x-abs(tau_xzn_l_scaled)))
        if (glCantileverCrossSection==3):        
            TauPlot_l_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(tau_xzn)),np.linspace(1.0/6.0, -0.525, len(tau_xzn))))
        else:    
            TauPlot_l_y = np.hstack((np.linspace(-0.525, 0, len(tau_xzn)),np.linspace(0, -0.525, len(tau_xzn))))            
        Tauplot_l_Source.data = dict(x = TauPlot_l_x, zn = TauPlot_l_y)
        
        ## TAU RIGHT END DATA SOURCE:
        tau_xzn_r_scaled = np.linspace(0, 0, len(tau_xzn))
        # Create scaled and reversed list 
        for i in range(len(tau_xzn)): 
            tau_xzn_r_scaled[i]=tau_xzn[len(tau_xzn)-i-1]*tau_xzn_scaling
        TauPlot_r_x = np.hstack((np.linspace(tau_xzn_r_pos_x, tau_xzn_r_pos_x, len(tau_xzn)), tau_xzn_r_pos_x+abs(tau_xzn_r_scaled)))
        if (glCantileverCrossSection==3):       
            TauPlot_r_y = np.hstack((np.linspace(-0.525, 1.0/6.0, len(tau_xzn)),np.linspace(1.0/6.0, -0.525, len(tau_xzn))))
        else:
            TauPlot_r_y = np.hstack((np.linspace(-0.525, 0, len(tau_xzn)),np.linspace(0, -0.525, len(tau_xzn))))            
        Tauplot_r_Source.data = dict(x = TauPlot_r_x, zn = TauPlot_r_y)

        ## TAU UPPER BORDER DATA SOURCE
        tau_xzn_u_scaled = np.linspace(0, 0, len(tau_xzn))
        # Create scaled and reversed list consisting of tau_max value: 
        for i in range(len(tau_xzn)): 
            tau_xzn_u_scaled[i]=tau_xzn[len(tau_xzn)-1]*tau_xzn_scaling
        TauPlot_u_x = np.hstack((np.linspace(tau_xy_u_pos_x-1, tau_xy_u_pos_x+1, len(tau_xzn)), np.linspace(tau_xy_u_pos_x+1, tau_xy_u_pos_x-1, len(tau_xzn))))
        if (glCantileverCrossSection==3):              
            TauPlot_u_y = np.hstack((np.linspace(1.0/6.0, 1.0/6.0, len(tau_xzn)), abs(tau_xzn_u_scaled)+1.0/6.0)) 
        else:
            TauPlot_u_y = np.hstack((np.linspace(0, 0, len(tau_xzn)), abs(tau_xzn_u_scaled)))            
        Tauplot_u_Source.data = dict(x = TauPlot_u_x, zn = TauPlot_u_y)

        # POSITION TAU LABELS
        if(glCantileverCrossSection==3):
            Tauplot_Label_Source.data = dict(
                x=[max(tau_xzn_r_pos_x+abs(tau_xzn_r_scaled))+0.1, min(tau_xy_l_pos_x-abs(tau_xzn_l_scaled))-0.5, tau_xy_l_pos_x+0.7], 
                zn=[-0.3, -0.3, max(abs(tau_xzn_u_scaled))+0.3 ], names=['\\tau_{xz}','\\tau_{xz}','\\tau_{zx}'])
        else:    
            Tauplot_Label_Source.data = dict(
                x=[max(tau_xzn_r_pos_x+abs(tau_xzn_r_scaled))+0.1, min(tau_xy_l_pos_x-abs(tau_xzn_l_scaled))-0.5, tau_xy_l_pos_x+0.7], 
                zn=[-0.4, -0.4, max(abs(tau_xzn_u_scaled))+0.15 ], names=['\\tau_{xz}','\\tau_{xz}','\\tau_{zx}'])

        ### SCALING AND POSITIONING OF ARROWS:
        # Position arrows into tau glyph
        arrow_adjust_x = max(abs(tau_xzn_l_scaled))/4.0
        # Make arrow size grow with increasing tau stress, but restrict length of arrows to dimensions of tau glyph
        if (max(abs(tau_xzn_u_scaled))/2.0 >= 0.15):
            arrow_adjust_zn = 0.15
        else:
            arrow_adjust_zn = max(abs(tau_xzn_u_scaled))/2.0
        if (glCantileverCrossSection==3):
            arrow_move_zn = 0.04 + 1.0/12.0    
        else:
            arrow_move_zn = 0.04    
        
        ## ARROW LEFT END:
        tau_xzn_l_pos_zn = -0.25                 
        if (Pzn<0): 
            TauArrowSource1.stream(dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], zns=[tau_xzn_l_pos_zn+arrow_adjust_zn+arrow_move_zn] , zne=[tau_xzn_l_pos_zn-arrow_adjust_zn+arrow_move_zn]),rollover=1)
        elif (Pzn>0):
            TauArrowSource1.stream(dict(xs=[tau_xy_l_pos_x-arrow_adjust_x] , xe= [tau_xy_l_pos_x-arrow_adjust_x], zns=[tau_xzn_l_pos_zn-arrow_adjust_zn+arrow_move_zn] , zne=[tau_xzn_l_pos_zn+arrow_adjust_zn+arrow_move_zn]),rollover=1)
        else:            
            TauArrowSource1.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)
        
        ## ARROWS RIGHT END:             
        tau_xzn_r_pos_zn = -0.25           
        if (Pzn<-30):
            TauArrowSource2.stream(dict(xs=[tau_xzn_r_pos_x+arrow_adjust_x] , xe= [tau_xzn_r_pos_x+arrow_adjust_x], zns=[tau_xzn_r_pos_zn-arrow_adjust_zn+arrow_move_zn] , zne=[tau_xzn_r_pos_zn+arrow_adjust_zn+arrow_move_zn]),rollover=1)
        elif (Pzn>30):
            TauArrowSource2.stream(dict(xs=[tau_xzn_r_pos_x+arrow_adjust_x] , xe= [tau_xzn_r_pos_x+arrow_adjust_x], zns=[tau_xzn_r_pos_zn+arrow_adjust_zn+arrow_move_zn] , zne=[tau_xzn_r_pos_zn-arrow_adjust_zn+arrow_move_zn]),rollover=1)
        else:            
            TauArrowSource2.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)

        ## ARROWS UPPER BORDER:
        tau_xzn_u_pos_zn = 0.0            
        # New arrow scaling and positioning for upper tau stress
        if (max(abs(tau_xzn_u_scaled)) >= 0.3):
            arrow_adjust_x = 0.3
        else:
            arrow_adjust_x = max(abs(tau_xzn_u_scaled))
        if (glCantileverCrossSection==3):
            arrow_adjust_zn = max(abs(tau_xzn_u_scaled))/2.0 + 1.0/6.0
        else:            
            arrow_adjust_zn = max(abs(tau_xzn_u_scaled))/2.0
        if (Pzn<-30):
            TauArrowSource3.stream(dict(xs=[(tau_xy_u_pos_x-0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)+arrow_adjust_x], zns=[tau_xzn_u_pos_zn+arrow_adjust_zn] , zne=[tau_xzn_u_pos_zn+arrow_adjust_zn]),rollover=1)
            TauArrowSource4.stream(dict(xs=[(tau_xy_u_pos_x+0.5)-arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)+arrow_adjust_x], zns=[tau_xzn_u_pos_zn+arrow_adjust_zn] , zne=[tau_xzn_u_pos_zn+arrow_adjust_zn]),rollover=1)                     
        elif (Pzn>30):
            TauArrowSource3.stream(dict(xs=[(tau_xy_u_pos_x-0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x-0.5)-arrow_adjust_x], zns=[tau_xzn_u_pos_zn+arrow_adjust_zn] , zne=[tau_xzn_u_pos_zn+arrow_adjust_zn]),rollover=1)
            TauArrowSource4.stream(dict(xs=[(tau_xy_u_pos_x+0.5)+arrow_adjust_x] , xe= [(tau_xy_u_pos_x+0.5)-arrow_adjust_x], zns=[tau_xzn_u_pos_zn+arrow_adjust_zn] , zne=[tau_xzn_u_pos_zn+arrow_adjust_zn]),rollover=1)
        else:
            TauArrowSource3.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)        
            TauArrowSource4.stream(dict(xs=[] , xe= [], zns=[] , zne=[]),rollover=-1)


# The function to be excuted whenever the force in the zn direction changes
def fun_change_Pzn(attrname, old, new):
    global Pzn,Pyn, listDeformedElementsXZn
    
    # Change the value of the applied force according to the slider value
    Pzn = Znforce_slider.value*100.0

    # Recalculate the deformed beam's shape
    (listDeformedElementsXZn, XCoordsDefXZn,
     YCoordsDefXZn, listValuesUpperXZn, colorListDeformedXZn,
     biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XZn( 
                                   length, height, thickness, E, Pzn, Pyn,
                                   noElementsX, noElementsZn, noElementsYn,
                                   elementSizeX, elementSizeZn, elementSizeYn,
                                   amplificationFactor
                               )
    
    # Update the global variable the describes the deformed elements
    listDeformedElementsXZn = listDeformedElementsXZn
    
    # Determine the change of the color in the other view (XY plane)
    colorListDeformedXYn = functions.elements_color_determiner(
                                                                  True,
                                                                  'XY',
                                                                  listDeformedElementsXYn,
                                                                  noElementsX,
                                                                  noElementsYn,
                                                                  E, thickness, height,
                                                                  length, Pzn, Pyn, 
                                                                  biggestValue, smallestValue,
                                                                  listValuesUpperXZn,
                                                                  glCantileverCrossSection
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXYndef.data   = dict( x=sourceXYndef.data['x'], zn=sourceXYndef.data['zn'], c=colorListDeformedXYn, a=alphaList)
    sourceXZndef.data   = dict( x=XCoordsDefXZn,   zn=YCoordsDefXZn,   c =colorListDeformedXZn,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards

    if Pzn == 0:
        sourceArrowXZn.stream(dict(xs=[], zns=[],xe=[], zne=[]),rollover=-1)
        sourceFznLabel.data = dict(x= [], zn= [],f= [])                                 
    else:
        if sourceXZndef.data['zn'][0][3] <= 0:
            sourceArrowXZn.stream(dict(
                                      xs=[sourceXZndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                      zns=[sourceXZndef.data['zn'][len( sourceXYndef.data['zn'])-2][2]+1],
                                      xe=[sourceXZndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                      zne=[sourceXZndef.data['zn'][len( sourceXYndef.data['zn'])-2][2]],
                                 ),rollover=1)
            sourceFznLabel.stream(dict(
                                      x= [sourceArrowXZn.data['xs'][0] + 0.4],
                                      zn= [sourceArrowXZn.data['zns'][0]],
                                      f= ['Fzn']
                                 ),rollover=1)
        else:
            sourceArrowXZn.stream(dict(
                                      xs=[sourceXZndef.data['x'][len( sourceXYndef.data['x'])-1][2]], 
                                      zns=[sourceXZndef.data['zn'][len( sourceXYndef.data['zn'])-1][2]-1],
                                      xe=[sourceXZndef.data['x'][len( sourceXYndef.data['x'])-1][2]], 
                                      zne=[sourceXZndef.data['zn'][len( sourceXYndef.data['zn'])-1][2]],
                                 ),rollover=1)
            sourceFznLabel.stream(dict(
                                      x= [sourceArrowXZn.data['xs'][0] + 0.4],
                                      zn= [sourceArrowXZn.data['zns'][0]],
                                      f= ['Fzn']
                                 ),rollover=1)
        
    update_colorBar_extremas(smallestValue,biggestValue)
    fun_update_xzn_element_stresses(length,height,thickness,glCantileverCrossSection,Pzn,Pyn)
    

# The function to be excuted whenever the force in the z direction changes
def fun_change_Pyn(attrname, old, new):
    global Pzn,Pyn, listDeformedElementsXYn
    
    # Change the value of the applied force according to the slider value
    Pyn = Ynforce_slider.value*100.0

    # Recalculate the deformed beam's shape
    (listDeformedElementsXYn, XCoordsDefXYn, YCoordsDefXYn, 
     listValuesLowerXYn, colorListDeformedXYn, biggestValue, smallestValue) = deformed_cantilever_beam_determiner_XYn( 
                                   length, height, thickness, E, Pzn, Pyn,
                                   noElementsX, noElementsZn, noElementsYn,
                                   elementSizeX, elementSizeZn, elementSizeYn,
                                   amplificationFactor
                               )
    
    # Update the global variable the describes the deformed elements
    listDeformedElementsXYn = listDeformedElementsXYn
    
    # Determine the change of the color in the other view (XZ plane)
    colorListDeformedXZn = functions.elements_color_determiner(
                                                                  True,
                                                                  'XZ',
                                                                  listDeformedElementsXZn,
                                                                  noElementsX,
                                                                  noElementsZn,
                                                                  E, thickness, height,
                                                                  length, Pzn, Pyn,
                                                                  biggestValue, smallestValue,
                                                                  listValuesLowerXYn,
                                                                  glCantileverCrossSection
                                                             )
    
    # Update the source files of the deforemd beams
    sourceXZndef.data   = dict( x=sourceXZndef.data['x'], zn=sourceXZndef.data['zn'], c=colorListDeformedXZn, a=alphaList)
    sourceXYndef.data   = dict( x=XCoordsDefXYn,   zn=YCoordsDefXYn,   c =colorListDeformedXYn,   a=alphaList )
    
    # Update the source data file of the force arrow and the force label
    # The first part of the if-statement is excuted whenever the beam is 
    # deforming downwards

    if Pyn == 0:
        sourceArrowXYn.stream(dict(xs=[],zns=[],xe=[],zne=[]),rollover=-1)
        sourceFynLabel.data = dict(x=[],zn=[],f=[])
    else:
        if sourceXYndef.data['zn'][0][3] <= 0:
            sourceArrowXYn.stream(dict(
                                      xs=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                      zns=[sourceXYndef.data['zn'][len( sourceXYndef.data['zn'])-2][2]+1],
                                      xe=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                      zne=[sourceXYndef.data['zn'][len( sourceXYndef.data['zn'])-2][2]],
                                 ),rollover=1)
            sourceFynLabel.stream(dict(
                                      x= [sourceArrowXYn.data['xs'][0] + 0.4],
                                      zn= [sourceArrowXYn.data['zns'][0]],
                                      f= ['Fyn']
                                 ),rollover=1)
        else:
            sourceArrowXYn.stream(dict(
                                      xs=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-1][2]], 
                                      zns=[sourceXYndef.data['zn'][len( sourceXYndef.data['zn'])-1][2]-1],
                                      xe=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-1][2]], 
                                      zne=[sourceXYndef.data['zn'][len( sourceXYndef.data['zn'])-1][2]],
                                 ),rollover=1)
            sourceFynLabel.stream(dict(
                                      x= [sourceArrowXYn.data['xs'][0] + 0.4],
                                      zn= [sourceArrowXYn.data['zns'][0]],
                                      f= ['Fyn']
                                 ),rollover=1)
        
    update_colorBar_extremas(smallestValue,biggestValue)
    fun_update_xzn_element_stresses(length,height,thickness,glCantileverCrossSection,Pzn,Pyn)

# Function that is called, when change in selected cross section occurs
def fun_change_Cross_Section(attrname, old, new):
    if (radio_button_group.active == 0 ):
        (colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList) = update_colorBar(radio_button_group.active)
        colorDistributionNoteSource.data=dict(x=[5.9] , zn=[-2.8], note=['non-linear color distribution!'])
        CrossSectionSource1.data = dict(sp1=[CrossSection1], x = [0], zn = [0])
        CrossSectionSource2.data = dict(sp2=[], x = [], zn = [])
        CrossSectionSource3.data = dict(sp3=[], x = [], zn = [])
        CrossSectionSource4.data = dict(sp4=[], x = [], zn = [])
        CoordArrowXZnSource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)
        CoordArrowXYnSource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)
        CoordArrowXZnESource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)
        labelXZn.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])  
        labelXYn.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['yn','x'])      
        labelXZnElement.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])                          
        XZElementSource.data = dict(sp4=[XZElement], x = [0], zn = [0])   
        XZElement2Source.data = dict(sp4=[], x = [], zn = [])          
    elif (radio_button_group.active == 1):
        (colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList) = update_colorBar(radio_button_group.active)
        colorDistributionNoteSource.data=dict(x=[] , zn=[], note=[])
        CrossSectionSource1.data = dict(sp1=[], x = [], zn = [])
        CrossSectionSource2.data = dict(sp2=[CrossSection2], x = [0], zn = [0])
        CrossSectionSource3.data = dict(sp3=[], x = [], zn = [])
        CrossSectionSource4.data = dict(sp4=[], x = [], zn = [])        
        CoordArrowXZnSource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)   
        CoordArrowXZnESource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)  
        labelXZn.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])                           
        labelXZnElement.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])                                         
        XZElementSource.data = dict(sp4=[XZElement], x = [0], zn = [0])           
        XZElement2Source.data = dict(sp4=[], x = [], zn = [])        
    elif (radio_button_group.active == 2):
        (colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList) = update_colorBar(radio_button_group.active)
        colorDistributionNoteSource.data=dict(x=[] , zn=[], note=[])
        CrossSectionSource1.data = dict(sp1=[], x = [], zn = [])
        CrossSectionSource2.data = dict(sp2=[], x = [], zn = [])
        CrossSectionSource3.data = dict(sp3=[CrossSection3], x = [0], zn = [0])
        CrossSectionSource4.data = dict(sp4=[], x = [], zn = [])        
        CoordArrowXZnSource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)
        CoordArrowXZnESource.stream(dict( xs=[-0.5], zns=[0.0],xe=[5.9], zne=[0.0]),rollover=1)            
        labelXZn.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])                         
        labelXZnElement.data=dict(x=[-.3,5.8], zn=[-2.7,-.3], text=['zn','x'])    
        XZElementSource.data = dict(sp4=[XZElement], x = [0], zn = [0])   
        XZElement2Source.data = dict(sp4=[], x = [], zn = [])                                            
    elif (radio_button_group.active == 3):
        (colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList) = update_colorBar(radio_button_group.active)
        colorDistributionNoteSource.data=dict(x=[] , zn=[], note=[])
        CrossSectionSource1.data = dict(sp1=[], x = [], zn = [])
        CrossSectionSource2.data = dict(sp2=[], x = [], zn = [])
        CrossSectionSource3.data = dict(sp3=[], x = [], zn = [])       
        CrossSectionSource4.data = dict(sp4=[CrossSection4], x = [0], zn = [0]) 
        CoordArrowXZnSource.stream(dict( xs=[-0.5], zns=[1.0/6.0],xe=[5.9], zne=[1.0/6.0]),rollover=1)
        CoordArrowXZnESource.stream(dict( xs=[-0.5], zns=[1.0/6.0],xe=[5.9], zne=[1.0/6.0]),rollover=1)   
        labelXZn.data=dict(x=[-.3,5.8], zn=[-2.7,-.3+1.0/6.0], text=['zn','x'])
        labelXZnElement.data=dict(x=[-.3,5.8], zn=[-2.7,-.3+1.0/6.0], text=['zn','x'])    
        XZElementSource.data = dict(sp4=[], x =[], zn = []) 
        XZElement2Source.data = dict(sp4=[XZElement], x = [0], zn = [0])                                            

    # Update Color Bar
    colorBarSource.data = dict( x=colorBarXCoords, zn=colorBarYCoords, c=colorBarColorList, a=colorBarAlphaList )

    global glCantileverCrossSection
    glCantileverCrossSection = radio_button_group.active
    global glCantileverStress
    glCantileverStress = radio_button_group2.active



# Function to initialize data
def init_data():
    Znforce_slider.value = 0
    Ynforce_slider.value = 0
    radio_button_group.active = 0
    radio_button_group2.active = 0


    fun_change_Pzn(None,None, None)
    fun_change_Pyn(None,None, None)
    fun_change_Cross_Section(None,None,None)
    

# Construct the source file of all the beams
sourceXZndef   = ColumnDataSource(data=dict( x=XCoordsDefXZn,   zn=YCoordsDefXZn,   c =colorListDeformedXZn,   a=alphaList ))
sourceXYndef   = ColumnDataSource(data=dict( x=XCoordsDefXYn,   zn=YCoordsDefXYn,   c =colorListDeformedXYn,   a=alphaList ))

# Construct the source file of both the arrows
sourceArrowXZn = ColumnDataSource(
                                     data=dict( 
                                                   xs=[sourceXZndef.data['x'][len( sourceXZndef.data['x'])-2][2]], 
                                                   zns=[1.5],
                                                   xe=[sourceXZndef.data['x'][len( sourceXZndef.data['x'])-2][2]], 
                                                   zne=[sourceXZndef.data['zn'][len( sourceXZndef.data['zn'])-2][2]],                            
                                              )
                                )
sourceArrowXYn = ColumnDataSource(
                                     data=dict( 
                                                   xs=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                                   zns=[1.5],
                                                   xe=[sourceXYndef.data['x'][len( sourceXYndef.data['x'])-2][2]], 
                                                   zne=[sourceXYndef.data['zn'][len( sourceXYndef.data['zn'])-2][2]],                            
                                              )
                                )

# Construct the force sliders
Znforce_slider = LatexSlider(title= 'F_zn =   ', value=0.0, start=-1.0, end=1.0, step=0.25, value_unit='\cdot F_{zn,max}')
Ynforce_slider = LatexSlider(title= 'F_yn =  ', value=0.0, start=-1.0, end=1.0, step=0.25, value_unit='\cdot F_{yn,max}')

# Construct radio button to choose between geometries of cross section
radio_button_group = RadioButtonGroup(name="Geometry of cross section",labels=["Quadratic", "Double-T", "Circular","Triangular"], active=glCantileverCrossSection)

# Construct radio button to choose between plot of sigma(zn) or tau(zn)
radio_button_group2 = RadioButtonGroup(name="Plot of sigma or tau",labels=["Normal Stresses", "Shear Stresses"], active=glCantileverStress)

# Construct reset button
Reset_button = Button(label="Reset", button_type="success")



############ PLOT 1: ZYn Cross Section PLOT ###############
plotDefZY = Figure(    
                       plot_width=300    , 
                       plot_height=300   ,
                       x_range = ( -5,5 ) ,
                       y_range= ( -5,5 ) ,
                       title = 'Selected Cross Section',
                       tools = ''
                  )

plotDefZY.xaxis.major_tick_line_color=None
plotDefZY.xaxis.major_label_text_color=None
plotDefZY.xaxis.minor_tick_line_color=None
plotDefZY.xaxis.axis_line_color=None
plotDefZY.yaxis.major_tick_line_color=None
plotDefZY.yaxis.major_label_text_color=None
plotDefZY.yaxis.minor_tick_line_color=None
plotDefZY.yaxis.axis_line_color=None
plotDefZY.grid.visible = False
plotDefZY.toolbar.logo = None
plotDefZY.title.text_font_size="12.5pt"

plotDefZY.add_glyph(CrossSectionSource1,ImageURL(url="sp1", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefZY.add_glyph(CrossSectionSource2,ImageURL(url="sp2", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefZY.add_glyph(CrossSectionSource3,ImageURL(url="sp3", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))
plotDefZY.add_glyph(CrossSectionSource4,ImageURL(url="sp4", x=-3*5.0/3.0+0.05, y=3*5.0/3.0, w=3*10.0/3.0, h=3*10.0/3.0))

labelYZ = ColumnDataSource(data=dict(x=[0.5,-4.0],
                                     zn=[-4.0,-0.6],
                                     text=['zn','yn']))
plotDefZY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=4.5, 
                           x_end=0, 
                           y_end=-4.5, 
                           ))

plotDefZY.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_end=-4.5, 
                           y_start=0, 
                           x_start=4.5, 
                           y_end=0, 
                           ))
plotDefZY.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelYZ
                                )
                    )


############ PLOT 2: XZn PLOT ###############
plotDefXZn = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in XZ-View',
                       tools = ''
                  )
plotDefXZn.xaxis.major_tick_line_color=None
plotDefXZn.xaxis.major_label_text_color=None
plotDefXZn.xaxis.minor_tick_line_color=None
plotDefXZn.xaxis.axis_line_color=None
plotDefXZn.yaxis.major_tick_line_color=None
plotDefXZn.yaxis.major_label_text_color=None
plotDefXZn.yaxis.minor_tick_line_color=None
plotDefXZn.yaxis.axis_line_color=None
plotDefXZn.grid.visible = False
plotDefXZn.toolbar.logo = None
plotDefXZn.title.text_font_size="12.5pt"

plotDefXZn.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=3, 
                           x_end=0, 
                           y_end=-2.8, 
                           ))
plotDefXZn.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXZn
                                )
                    )

# Add color distribution note
plotDefXZn.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='note',
                                  text_color='grey',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="right",
                                  source=colorDistributionNoteSource
                                )
                    )

# Construct the arrows
plotDefXZn.add_layout( 
                     Arrow(end=NormalHead(line_color="black",line_width=3,size=10),
                           line_width=3,
                           x_start=['xs'][0],
                           y_start=['zns'][0],
                           x_end=['xe'][0], 
                           y_end=['zne'][0], 
                           source = sourceArrowXZn) 
                    )
plotDefXZn.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='zns',
                           x_end='xe', 
                           y_end='zne', 
                           source = CoordArrowXZnSource) 
                    )

# Construct the force labels
plotDefXZn.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='f',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFznLabel
                              )
                    )


############ PLOT 3: XYn PLOT ###############
plotDefXYn = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Deformation in XY-View',
                       tools = ''
                  )
plotDefXYn.xaxis.major_tick_line_color=None
plotDefXYn.xaxis.major_label_text_color=None
plotDefXYn.xaxis.minor_tick_line_color=None
plotDefXYn.xaxis.axis_line_color=None
plotDefXYn.yaxis.major_tick_line_color=None
plotDefXYn.yaxis.major_label_text_color=None
plotDefXYn.yaxis.minor_tick_line_color=None
plotDefXYn.yaxis.axis_line_color=None
plotDefXYn.grid.visible = False
plotDefXYn.toolbar.logo = None
plotDefXYn.title.text_font_size="12.5pt"

plotDefXYn.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=3, 
                           x_end=0, 
                           y_end=-2.8, 
                           ))

plotDefXYn.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXYn
                                )
                    )

# Add color distribution note
plotDefXYn.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='note',
                                  text_color='grey',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="right",
                                  source=colorDistributionNoteSource
                                )
                    )

# Construct the arrows
plotDefXYn.add_layout( 
                     Arrow(end=NormalHead(line_color="black",line_width=3,size=10),
                           line_width=3,
                           x_start=['xs'][0], 
                           y_start=['zns'][0], 
                           x_end=['xe'][0], 
                           y_end=['zne'][0], 
                           source = sourceArrowXYn)
                    )

plotDefXYn.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='zns',
                           x_end='xe', 
                           y_end='zne', 
                           source = CoordArrowXYnSource) 
                    )             

# Construct the force labels
plotDefXYn.add_layout(LabelSet(
                                  x='x', y='zn',
                                  text='f',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=sourceFynLabel
                              )
                    )


############ PLOT 4: XZn ELEMENT PLOT ###############
plotXZnElement = Figure(    
                       plot_width=400    , 
                       plot_height=400   ,
                       x_range = ( -.5,6 ) ,
                       y_range= ( -3,3 ) ,
                       title = 'Stresses along detached Element',
                       tools = ''
                  )
plotXZnElement.xaxis.major_tick_line_color=None
plotXZnElement.xaxis.major_label_text_color=None
plotXZnElement.xaxis.minor_tick_line_color=None
plotXZnElement.xaxis.axis_line_color=None
plotXZnElement.yaxis.major_tick_line_color=None
plotXZnElement.yaxis.major_label_text_color=None
plotXZnElement.yaxis.minor_tick_line_color=None
plotXZnElement.yaxis.axis_line_color=None
plotXZnElement.grid.visible = False
plotXZnElement.toolbar.logo = None
plotXZnElement.title.text_font_size="12.5pt"

plotXZnElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start=0, 
                           y_start=3, 
                           x_end=0, 
                           y_end=-2.8, 
                           ))

plotXZnElement.add_layout( 
                     Arrow(end=VeeHead(line_color="black",line_width=3,size=5),
                           x_start='xs',
                           y_start='zns',
                           x_end='xe', 
                           y_end='zne', 
                           source = CoordArrowXZnESource) 
                    )



plotXZnElement.add_layout(
                      LabelSet(
                                  x='x', y='zn',
                                  text='text',
                                  text_color='black',text_font_size="12pt",
                                  level='glyph',text_baseline="middle",text_align="center",
                                  source=labelXZnElement
                                )
                    )                    

                        
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource1))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource2))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource3))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource4))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource5))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = SigmaArrowSource6))

plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = TauArrowSource1))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = TauArrowSource2))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = TauArrowSource3))
plotXZnElement.add_layout( Arrow(end=NormalHead(line_color="black",line_width=1,size=2),
                           line_width=1,x_start=['xs'][0], y_start=['zns'][0], x_end=['xe'][0], y_end=['zne'][0], source = TauArrowSource4))

plotXZnElement.add_glyph(XZBeamSource,ImageURL(url="sp5", x=0, y=0.5, w=5, h=1.04))
plotXZnElement.add_glyph(XZElementSource,ImageURL(url="sp4", x=1.5, y=0, w=2, h=0.535))
plotXZnElement.add_glyph(XZElement2Source,ImageURL(url="sp4", x=1.5, y=1.0/6.0, w=2, h=0.535*(1+1.0/3.0)))

Sigmaplot_l_Glyph = Patch(x="x", y="zn", fill_color='#0065BD', fill_alpha=0.5)
plotXZnElement.add_glyph(Sigmaplot_l_Source, Sigmaplot_l_Glyph)

Sigmaplot_r_Glyph = Patch(x="x", y="zn", fill_color='#0065BD', fill_alpha=0.5)
plotXZnElement.add_glyph(Sigmaplot_r_Source, Sigmaplot_r_Glyph)

Tauplot_l_Glyph = Patch(x="x", y="zn", fill_color='#E37222', fill_alpha=0.5)
plotXZnElement.add_glyph(Tauplot_l_Source, Tauplot_l_Glyph)

Tauplot_r_Glyph = Patch(x="x", y="zn", fill_color='#E37222', fill_alpha=0.5)
plotXZnElement.add_glyph(Tauplot_r_Source, Tauplot_r_Glyph)

Tauplot_u_Glyph = Patch(x="x", y="zn", fill_color='#E37222', fill_alpha=0.5)
plotXZnElement.add_glyph(Tauplot_u_Source, Tauplot_u_Glyph)

Sigmaplot_Labels = LatexLabelSet(
    x='x', y='zn', text='names', source=Sigmaplot_Label_Source, 
    text_color ="#0065BD", level='glyph', x_offset=0, y_offset=0)

Tauplot_Labels = LatexLabelSet(
    x='x', y='zn', text='names', source=Tauplot_Label_Source, 
    text_color ="#E37222", level='glyph', x_offset=0, y_offset=0)    

plotXZnElement.add_layout(Sigmaplot_Labels)
plotXZnElement.add_layout(Tauplot_Labels)

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

def update_colorBar(glCantileverCrossSection):
    ## Create colorBar patches with node coords 
    colorBarXCoords = []
    colorBarYCoords = []
    for i in range(50):
        lowerLeft = [float(i)/10, -0.5]
        upperLeft = [float(i)/10, 0.5]
        lowerRight= [float(i)/10 + 1.0/10.0, -0.5]
        upperRight= [float(i)/10 + 1.0/10.0, 0.5]

        colorBarXCoords.append([lowerLeft[0], upperLeft[0], upperRight[0], lowerRight[0]])
        colorBarYCoords.append([lowerLeft[1], upperLeft[1], upperRight[1], lowerRight[1]])

    colorBarColorList = []
    colorBarAlphaList = []
    ## Determine the color distribution in the color bar
    smallestValue,biggestValue = -10.0,10.0
    valuesRange = []
    ## Create equidistant vector with 50 members between smallestValue and biggestValue:
    for i in range(50):
        valuesRange.append(smallestValue + (float(i)/49.0)*(biggestValue - smallestValue))
    ## Create vector with 50 colors corresponding to varluesRange-vector:
    for i in range(50):
        colorBarColorList.append(functions.color_determiner( smallestValue, biggestValue, valuesRange[i], glCantileverCrossSection ))
        colorBarAlphaList.append( 1 )

    return colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList

## Construct the source file for the color bar
(colorBarXCoords, colorBarYCoords , colorBarColorList, colorBarAlphaList) = update_colorBar(glCantileverCrossSection)
colorBarSource.data = dict( x=colorBarXCoords, zn=colorBarYCoords, c=colorBarColorList, a=colorBarAlphaList )

## Label colorbar min-max stess range
def update_colorBar_extremas(smallesValue, biggestValue):
    colorBar.title.text =  " "*15  + "-" + " "*55 + "Normal Stress" + " "*55 + "+"

# Construct the patches 
colorBar.patches( xs='x', ys='zn', source=colorBarSource, color = 'c', alpha = 'a' )
plotDefXZn.patches  (xs='x', ys='zn', source=sourceXZndef  , color = 'c', alpha = 'a')
plotDefXYn.patches  (xs='x', ys='zn', source=sourceXYndef  , color = 'c', alpha = 'a')

# Notify the corresponding functions to carry out the changes characterized by
# the sliders
Znforce_slider.on_change('value',fun_change_Pzn)
Ynforce_slider.on_change('value',fun_change_Pyn)
radio_button_group.on_change('active',fun_change_Cross_Section,fun_change_Pzn,fun_change_Pyn)
radio_button_group2.on_change('active',fun_change_Cross_Section,fun_change_Pzn,fun_change_Pyn)
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
    column(plotDefZY,widgetbox(radio_button_group),Znforce_slider,Ynforce_slider,Reset_button),
    column(row(column(plotXZnElement,row(Spacer(width=40),radio_button_group2)),column(row(plotDefXZn, plotDefXYn),colorBar))))))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '