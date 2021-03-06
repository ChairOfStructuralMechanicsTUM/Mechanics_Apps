"""
Mohr Circle - explains how Mohr's Circle can be used to identify different stresses
"""
###################################
# Imports
###################################

# general imports
from math import pi, sin, cos, atan
import yaml

# bokeh imports
from bokeh.io                   import curdoc
from bokeh.plotting             import figure
from bokeh.layouts              import column, row, layout
from bokeh.models               import ColumnDataSource, Slider, Arrow, OpenHead, NormalHead, Button
from bokeh.models.markers       import Square, Circle
from bokeh.models.glyphs        import Wedge, Rect
from bokeh.models.layouts       import Spacer

# internal imports
from MC_figure_sources import fig1, fig2, fig3
from MC_helper_functions import (
    calculate_radius_and_center, 
    clear_arrow_source, clear_rect_source, 
    add_layouts_from_list, add_glyphs_from_list
)
from MC_constants import (
    initial_MohrNx, initial_MohrNxz, initial_MohrNz, initial_MohrP_Angle,
    initial_Neta, initial_Nzeta, initial_Nzetaeta,
    initial_centreX, initial_radius, initial_rleft_z,
    c_blue, c_orange, c_green
)

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend



###################################
# DataSources
###################################

std_lang = 'en'
flags    = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings  = yaml.safe_load(open('Mohr_Circle/static/strings.json', encoding='utf-8'))

figure_texts = ColumnDataSource(data=dict(text=["\\text{Normal Stresses}\\ \\sigma_x, \\sigma_z",
                                                "\\text{Shear Stresses}\\ \\tau_{xz}",
                                                "\\text{Normal Stresses}\\ \\sigma_{\overline{x}}, \\sigma_{\overline{z}}",
                                                "\\text{Shear Stresses}\\ \\tau_{\overline{xz}}",
                                                "Stress State A",
                                                "Mohr's Circle",
                                                "Stress State B",
                                                ]))

### Initial Values
radius   = initial_radius
centreX  = initial_centreX
Neta     = initial_Neta 
Nzeta    = initial_Nzeta
Nzetaeta = initial_Nzetaeta
rleft_x  = centreX-radius
rleft_z  = initial_rleft_z

# global variables
global_vars = dict(MohrNx=initial_MohrNx, MohrNz=initial_MohrNz, MohrNxz=initial_MohrNxz,
                   MohrP_Angle=0, MohrNzeta_zero_angles=[], MohrNeta_zero_angles=[],
                   alpha=0, MohrChangeShow=-1)

### Initializing variables
f1 = fig1()
f2 = fig2()
f3 = fig3()



###################################
# Callback Functions
###################################

def reset():
    Normal_X_slider.disabled      = False
    Normal_Z_slider.disabled      = False
    Tangential_XZ_slider.disabled = False
    Plane_Angle_slider.disabled   = True
    draw_button.disabled          = False
    show_button.disabled          = True

    global_vars["MohrChangeShow"] = -1
    global_vars["alpha"]          = 0
    global_vars["MohrP_Angle"]    = initial_MohrP_Angle
    global_vars["MohrNx"]         = initial_MohrNx
    global_vars["MohrNz"]         = initial_MohrNz
    global_vars["MohrNxz"]        = initial_MohrNxz
        
    radius  = initial_radius
    centreX = initial_centreX
    
    ### Calculations
    [radius, centreX, _]       = calculate_radius_and_center(global_vars)
    Normal_X_slider.value      = 0
    Normal_Z_slider.value      = 0
    Tangential_XZ_slider.value = 0
    Plane_Angle_slider.value   = 0

    ### Figure 1, Reset values for arrows:
    sources_to_reset = [f1.NxP_arrow_source,  f1.NxN_arrow_source,  f1.NzP_arrow_source,  f1.NzN_arrow_source,
                        f1.Nxz1_arrow_source, f1.Nxz2_arrow_source, f1.Nxz3_arrow_source, f1.Nxz4_arrow_source]
    clear_arrow_source(sources_to_reset)
    ## Figure 1, Reset Rectangles:
    sources_to_reset = [f1.NxP_rect_source,  f1.NxN_rect_source,  f1.NzP_rect_source,  f1.NzN_rect_source, 
                        f1.Nxz1_rect_source, f1.Nxz2_rect_source, f1.Nxz3_rect_source, f1.Nxz4_rect_source]
    clear_rect_source(sources_to_reset)
    
    ### Figure 2, Reset Circle:
    f2.reset_circle(centreX, radius, glMohrFigure2_angle_label)

    ## Figure 3, Reset arrows:
    sources_to_reset = [f3.NzetaP_arrow_source,    f3.NzetaN_arrow_source,    f3.NetaP_arrow_source,     f3.NetaN_arrow_source,
                        f3.Nzetaeta1_arrow_source, f3.Nzetaeta2_arrow_source, f3.Nzetaeta3_arrow_source, f3.Nzetaeta4_arrow_source]
    clear_arrow_source(sources_to_reset)
    ## Figure 3, Reset rectangles:
    sources_to_reset = [f3.NzetaP_rect_source,    f3.NzetaN_rect_source,    f3.NetaP_rect_source,     f3.NetaN_rect_source,
                        f3.Nzetaeta1_rect_source, f3.Nzetaeta2_rect_source, f3.Nzetaeta3_rect_source, f3.Nzetaeta4_rect_source]
    clear_rect_source(sources_to_reset)    
    ## Figure 3, Reset rotating plane and axis:
    f3.reset_rotating_plane()

def show():
    MohrNx         = global_vars["MohrNx"]
    MohrNz         = global_vars["MohrNz"]
    MohrNxz        = global_vars["MohrNxz"]
    MohrChangeShow = global_vars["MohrChangeShow"]
    
    if MohrChangeShow == 1:
        [radius, centreX, rleft_x] = calculate_radius_and_center(global_vars)
        rright_x = centreX+radius

        ## Print Labels for principal stress and direction
        alpha = 180*atan(MohrNxz/(MohrNz+(-rleft_x+0.00001)))/(pi)
        alpha = int(alpha+0.5)
        f2.Show_Label_source.data = dict(x=[rleft_x,rright_x,centreX],
                                                y=[0,0,0],
                                                names=['\\sigma_{II}','\\sigma_{I}','\\sigma_{M}'])
        f2.Wedge_source.data = dict(x=[rleft_x], y=[0],radius=[radius/2], sA=[atan(MohrNxz/(MohrNz+(-rleft_x+0.00001)))], eA=[0])
        glMohrFigure2_angle_label.text = '\\alpha_0=' + str(alpha)
        global_vars["MohrChangeShow"]  = MohrChangeShow*-1

    elif MohrChangeShow == -1:
        f2.Wedge_source.data           = dict(x=[], y=[],radius=[], sA=[], eA=[])
        f2.Show_Label_source.data      = dict(x=[], y=[], names =[])
        glMohrFigure2_angle_label.text = ''
        global_vars["MohrChangeShow"]  = MohrChangeShow*-1

def draw():
    MohrNx      = global_vars["MohrNx"]
    MohrNz      = global_vars["MohrNz"]
    MohrNxz     = global_vars["MohrNxz"]
    MohrP_Angle = global_vars["MohrP_Angle"]

    Normal_X_slider.disabled       = True
    Normal_Z_slider.disabled       = True
    Tangential_XZ_slider.disabled  = True
    Plane_Angle_slider.disabled    = False
    show_button.disabled           = False
    draw_button.disabled           = True

    global_vars["MohrChangeShow"]  = 1

    ## Calculations
    [radius, centreX, _] = calculate_radius_and_center(global_vars)
    Neta                 = float(((MohrNx+MohrNz)/2)-(((MohrNx-MohrNz)/2)*cos(2*MohrP_Angle))-MohrNxz*sin(2*MohrP_Angle))
    Nzetaeta             = float((-(((MohrNx-MohrNz)/2)*sin(2*MohrP_Angle)))+MohrNxz*cos(2*MohrP_Angle))

    ## Calculate Angle for which Nzeta or Neta will be zero (sign-change-method):
    NZeta_List0 = [181]*360
    NZeta_List1 = [181]*360
    global_vars["MohrNzeta_zero_angles"] = [181]*360
    Neta_List0  = [181]*360
    Neta_List1  = [181]*360
    global_vars["MohrNeta_zero_angles"]  = [181]*360

    ## Nzeta:
    for n in range(-180,180):
        NZeta_List0[n+180] = float(((MohrNx+MohrNz)/2)+(((MohrNx-MohrNz)/2)*cos(2*-n*pi/180))+MohrNxz*sin(2*-n*pi/180))
        NZeta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if NZeta_List0[m+180]*NZeta_List0[m+181]<0:
            global_vars["MohrNzeta_zero_angles"][count]=NZeta_List1[m+180]
            count = count+1
    ## Neta:
    for n in range(-180,180):
        Neta_List0[n+180] = float(((MohrNx+MohrNz)/2)-(((MohrNx-MohrNz)/2)*cos(2*-n*pi/180))-MohrNxz*sin(2*-n*pi/180))
        Neta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if Neta_List0[m+180]*Neta_List0[m+181]<0:
            global_vars["MohrNeta_zero_angles"][count]=Neta_List1[m+180]
            count = count+1

    ##Figure 1, Draw MohrNx and keep it until reset() ist called:
    
    if(MohrNx*0.75<0):
        f1.NxP_arrow_source.data = dict(xS=[12.5-MohrNx*0.75],  xE=[12.5],  yS=[0], yE=[0], lW = [2])
        f1.NxN_arrow_source.data = dict(xS=[-12.5+MohrNx*0.75], xE=[-12.5], yS=[0], yE=[0], lW = [2]) 
        f1.NxP_rect_source.data  = dict(x=[(25-MohrNx*0.75)/2],  y=[0], w=[MohrNx*0.75-1.5], h = [13], angle=[0])
        f1.NxN_rect_source.data  = dict(x=[(-25+MohrNx*0.75)/2], y=[0], w=[MohrNx*0.75-1.5], h = [13], angle=[0])
    elif(MohrNx*0.75==0):
        clear_arrow_source( [f1.NxP_arrow_source, f1.NxN_arrow_source] )
        clear_rect_source ( [f1.NxP_rect_source,  f1.NxN_rect_source ] )
    else:
        f1.NxP_arrow_source.data  = dict(xS=[12.5],  xE=[12.5+MohrNx*0.75],  yS=[0], yE=[0], lW = [2])
        f1.NxN_arrow_source.data  = dict(xS=[-12.5], xE=[-12.5-MohrNx*0.75], yS=[0], yE=[0], lW = [2])
        f1.NxP_rect_source.data   = dict(x=[(25+MohrNx*0.75)/2],  y=[0], w=[MohrNx*0.75+1.5], h = [13], angle=[0])        
        f1.NxN_rect_source.data   = dict(x=[(-25-MohrNx*0.75)/2], y=[0], w=[MohrNx*0.75+1.5], h = [13], angle=[0])  

    ##Figure 1, Draw MohrNz and keep it until reset() ist called:
    new = MohrNz
    new = new*0.75
    if(new<0):
        f1.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2])
        f1.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2])
        f1.NzP_rect_source.data  = dict(x=[0], y=[(25-new)/2],  w=[13], h = [new-1.5], angle=[0])
        f1.NzN_rect_source.data  = dict(x=[0], y=[(-25+new)/2], w=[13], h = [new-1.5], angle=[0])   
    elif (new==0):
        clear_arrow_source( [f1.NzP_arrow_source, f1.NzN_arrow_source] )
        clear_rect_source ( [f1.NzP_rect_source,  f1.NzN_rect_source ] )
    else:
        f1.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new], lW = [2])
        f1.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2])
        f1.NzP_rect_source.data  = dict(x=[0], y=[(25+new)/2],  w=[13], h = [new+1.5], angle=[0])
        f1.NzN_rect_source.data  = dict(x=[0], y=[(-25-new)/2], w=[13], h = [new+1.5], angle=[0])   
         
    new = MohrNxz
    new=new*0.75        
    if(new==0):
        clear_arrow_source( [f1.Nxz1_arrow_source, f1.Nxz2_arrow_source, f1.Nxz3_arrow_source, f1.Nxz4_arrow_source] )
        clear_rect_source ( [f1.Nxz1_rect_source,  f1.Nxz2_rect_source,  f1.Nxz3_rect_source,  f1.Nxz4_rect_source ] )
    else:     
        f1.Nxz1_arrow_source.data = dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2])
        f1.Nxz2_arrow_source.data = dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2])
        f1.Nxz3_arrow_source.data = dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2])
        f1.Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]) 
 
        f1.Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        f1.Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        f1.Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*new+0.5], angle=[0])
        f1.Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*new+0.5], angle=[0])

    ## Figure 2, draw Mohr-Circle:
    f2.Mohr_Circle_source.data         = dict(x=[centreX], y=[0], radius=[radius])
    f2.Wedge_source.data               = dict(x=[], y=[],radius=[], sA=[], eA=[])
    f2.Newplane_line_source.data       = dict(x=[rleft_x,Neta,Neta],     y=[rleft_z,Nzetaeta,0])
    f2.OriginalPlane_line_source.data  = dict(x=[rleft_x,MohrNz,MohrNz], y=[rleft_z,MohrNxz,0])
    f2.Show_Label_source.data          = dict(x=[], y=[], names =[])

    ## Figure 3, initializing:
    f3.Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-MohrP_Angle],size = [75])

    f3.ChangeRotatingPlane_Forces(global_vars)
    f2.ChangeMohrCircle(global_vars)
    f3.move_labels(MohrP_Angle)

def NormalForceX_init(attr,old,new):
   ## Figure 1, Present the Normal Forces while Draw-Button wasn't yet activated:  
        global_vars["MohrNx"] = new 
        f1.plot_normal_forces_x(new)

def NormalForceZ_init(attr,old,new):
    ## Figure 1, Present the Normal Forces while draw() hasn't been called yet:
        global_vars["MohrNz"] = new
        f1.plot_normal_forces_z(new)

def TangentialXZ_init(attr,old,new):
    ## Figure 1, Present the Shear Forces while draw() hasn't yet been called: 
        global_vars["MohrNxz"] = new
        f1.plot_shear_forces(global_vars["MohrNxz"])


def changePlaneAngle(attr,old,new):
        MohrNx  = global_vars["MohrNx"]
        MohrNz  = global_vars["MohrNz"]
        MohrNxz = global_vars["MohrNxz"]

        global_vars["alpha"] = new
        MohrP_Angle = -new*(pi/180)

        ## Paint Rotating Plane red if angle=alpha_0
        [radius, centreX, rleft_x] = calculate_radius_and_center(global_vars)
        alpha_0 = 180*atan(MohrNxz/(MohrNz+(-rleft_x+0.00001)))/(pi)
        alpha_0 = int(alpha_0+0.5)
        
        alpharepetitions = [-90, -180, 0, 90, 180]
        for n in alpharepetitions:
            if new == alpha_0+n:
                f3.Rotating_Plane_red_source.data = dict(x=[0], y=[0], angle =[-MohrP_Angle], size = [75])
                f3.Rotating_Plane_source.data     = dict(x=[],  y=[],  angle =[],             size = []  )
                break
        else:
            f3.Rotating_Plane_source.data     = dict(x=[0], y=[0], angle =[-MohrP_Angle], size = [75])
            f3.Rotating_Plane_red_source.data = dict(x=[],  y=[],  angle =[],             size = []  )

        # Figure 3, Rotate Axis:  
        MohrP_Angle = -MohrP_Angle
        f3.Rotating_Axis_X_source.stream(dict(xS=[0], yS=[0], xE=[25*cos(MohrP_Angle)],    yE=[25*sin(MohrP_Angle)  ]),rollover=1)
        f3.Rotating_Axis_Y_source.stream(dict(xS=[0], yS=[0], xE=[-25*sin(-MohrP_Angle)],  yE=[-25*cos(-MohrP_Angle)]),rollover=1)
        
        global_vars["MohrP_Angle"] = -MohrP_Angle   #      /output
        f2.ChangeMohrCircle(global_vars)
        f3.move_labels(-MohrP_Angle)
        f3.ChangeRotatingPlane_Forces(global_vars)



###################################
# Change language
###################################

def update_figures():
    legend1.items = [(figure_texts.data['text'][0], [dummy_normal_1]),
                     (figure_texts.data['text'][1], [dummy_shear_1 ])]
    legend3.items = [(figure_texts.data['text'][2], [dummy_normal_3]),
                     (figure_texts.data['text'][3], [dummy_shear_3 ])]
    figure1.title.text = figure_texts.data['text'][4]
    figure2.title.text = figure_texts.data['text'][5]
    figure3.title.text = figure_texts.data['text'][6]

def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage('de')
    elif lang == "de":
        setDocumentLanguage('en')
    update_figures()

def setDocumentLanguage(lang):
    flags.patch( {'lang':[(0,lang)]} )
    for s in strings:
        if 'checkFlag' in strings[s]:
            flag = flags.data[strings[s]['checkFlag']][0]
            exec( (s + '=\"' + strings[s][flag][lang] + '\"').encode(encoding='utf-8') )
        elif 'isCode' in strings[s] and strings[s]['isCode']:
            exec( (s + '=' + strings[s][lang]).encode(encoding='utf-8') )
        else:
            exec( (s + '=\"' + strings[s][lang] + '\"').encode(encoding='utf-8') )



###################################
# Figures
###################################

### Figure 1, Define Geometry:
NxP_arrow_glyph = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.NxP_arrow_source,line_color=c_orange)
NxN_arrow_glyph = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.NxN_arrow_source,line_color=c_orange)
NzP_arrow_glyph = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.NzP_arrow_source,line_color=c_orange)
NzN_arrow_glyph = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.NzN_arrow_source,line_color=c_orange)
Nxz1_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.Nxz1_arrow_source,line_color=c_blue)
Nxz2_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.Nxz2_arrow_source,line_color=c_blue)
Nxz3_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.Nxz3_arrow_source,line_color=c_blue)
Nxz4_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.Nxz4_arrow_source,line_color=c_blue)
### Figure 1, Rectangle glyphs:
NNP_rect_glphys = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color=c_orange, fill_alpha=0.5)
Nxz_rect_glyphs = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color=c_blue, fill_alpha=0.5)

### Figure 1, Define Figure and add Geometry:
figure1 = figure(title=figure_texts.data['text'][4], tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400)
figure1.square([0], [0], size=75, color="black", alpha=0.5)
figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure1.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))

glyphs_to_add = [NxP_arrow_glyph, NxN_arrow_glyph, NzP_arrow_glyph, NzN_arrow_glyph, Nxz1_arrow_glyph, Nxz2_arrow_glyph, Nxz3_arrow_glyph, Nxz4_arrow_glyph]
add_layouts_from_list(figure1, glyphs_to_add)

glyphs_to_add = [NNP_rect_glphys, NNP_rect_glphys, NNP_rect_glphys, NNP_rect_glphys, Nxz_rect_glyphs, Nxz_rect_glyphs, Nxz_rect_glyphs, Nxz_rect_glyphs]
glyph_sources = [f1.NxP_rect_source, f1.NxN_rect_source, f1.NzP_rect_source, f1.NzN_rect_source, f1.Nxz1_rect_source, f1.Nxz2_rect_source, f1.Nxz3_rect_source, f1.Nxz4_rect_source]
add_glyphs_from_list(figure1, glyphs_to_add, glyph_sources)

# dummy glyphs for the legend entries
dummy_normal_1 = figure1.square([0.0],[0.0],size=0,fill_color=c_orange,fill_alpha=0.5)
dummy_shear_1  = figure1.square([0.0],[0.0],size=0,fill_color=c_blue,fill_alpha=0.5)

legend1 = LatexLegend(items=[
    (figure_texts.data['text'][0], [dummy_normal_1]),
    (figure_texts.data['text'][1], [dummy_shear_1 ]),
], location='top_left', max_label_width = 220)
figure1.add_layout(legend1)

# LatexLabelSet has to be added to the layout after LatexLegend! Otherwise the labels won't show.
figure1_labels = LatexLabelSet(x='x', y='y', text='names', level='glyph',
                                x_offset=0, y_offset=0, source=f1.Perm_Label_source)

figure1.add_layout(figure1_labels)


### Figure 2: Define Geometry
Mohr_Circle_glyph = Circle(x='x',y='y',radius='radius', radius_dimension='y', fill_color='#c3c3c3', fill_alpha=0.5)
Wedge_glyph       = Wedge(x="x", y="y", radius="radius", start_angle="sA", end_angle="eA", fill_color="firebrick", fill_alpha=0.6, direction="clock")
### Figure 2: Define Figure and add Geometry
figure2 = figure(title=figure_texts.data['text'][5], tools="pan,save,wheel_zoom,reset", x_range=(-25.5,25.5), y_range=(-25.5,25.5),width=400,height=400, toolbar_location="right")
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=-23, y_start=0, x_end=23, y_end=0))
figure2.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=-23, x_end=0, y_end=23))
figure2.add_glyph(f2.Mohr_Circle_source,Mohr_Circle_glyph)
figure2.add_glyph(f2.Wedge_source,Wedge_glyph)
# Modified line
figure2.line  (x='x', y='y', source= f2.Newplane_line_source,         color=c_green, line_width=3, line_join = 'bevel')
figure2.circle(x='x', y='y', source= f2.Newplane_line_source, size=4, color="black", alpha=0.4)
figure2.circle(x='x', y='y', source= f2.Moving_Label_source,  size=5, color="black")
figure2.circle(x='x', y='y', source= f2.Show_Label_source,    size=5, color="firebrick")
figure2_labels1 = LatexLabelSet(x='x', y='y', text='names', level='glyph', x_offset=0, y_offset=0, source=f2.Perm_Label_source)
figure2_labels2 = LatexLabelSet(x='x', y='y', text='names', source=f2.Moving_Label_source, text_color = 'black', level='glyph', x_offset=3, y_offset=3)
figure2_labels3 = LatexLabelSet(x='x', y='y', text='names', source=f2.Show_Label_source, text_color = 'firebrick', level='glyph', x_offset=3, y_offset=-15)
figure2.add_layout(figure2_labels1)
figure2.add_layout(figure2_labels2)
figure2.add_layout(figure2_labels3)
# Original line
figure2.line(x='x',y='y',source= f2.OriginalPlane_line_source, color="black", alpha=0.5, line_width=3, line_join = 'bevel')
figure2.circle(x='x',y='y',source= f2.OriginalPlane_line_source, size=4, color="black", alpha=0.4)
glMohrFigure2_angle_label = LatexLabel(text="",x=20,y=330,render_mode='css',text_color='firebrick', x_units='screen', y_units='screen')
figure2.add_layout(glMohrFigure2_angle_label)

### Figure 3: Define Geometry
Rotating_Plane_glyph     = Square(x='x', y='y', angle='angle', size='size', fill_color=c_green,     fill_alpha=0.5)
Rotating_Plane_red_glyph = Square(x='x', y='y', angle='angle', size='size', fill_color='firebrick', fill_alpha=0.5)

Rotating_Axis_X_glyph = Arrow(end=NormalHead(fill_color=c_green, size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f3.Rotating_Axis_X_source )
Rotating_Axis_Y_glyph = Arrow(end=NormalHead(fill_color=c_green, size=15), x_start='xS', y_start='yS', x_end='xE', y_end='yE', source=f3.Rotating_Axis_Y_source )

NzetaP_arrow_glyph    = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.NzetaP_arrow_source,line_color=c_orange)
NzetaN_arrow_glyph    = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.NzetaN_arrow_source,line_color=c_orange)
NetaP_arrow_glyph     = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.NetaP_arrow_source,line_color=c_orange)
NetaN_arrow_glyph     = Arrow(end=OpenHead(line_color=c_orange,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.NetaN_arrow_source,line_color=c_orange)
Nzetaeta1_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.Nzetaeta1_arrow_source,line_color=c_blue)
Nzetaeta2_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.Nzetaeta2_arrow_source,line_color=c_blue)
Nzetaeta3_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.Nzetaeta3_arrow_source,line_color=c_blue)
Nzetaeta4_arrow_glyph = Arrow(end=OpenHead(line_color=c_blue,line_width= 2, size=5),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f3.Nzetaeta4_arrow_source,line_color=c_blue)
### Figure 3, Rectangle glyphs:
Neta_rect_glyphs   = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color=c_orange, fill_alpha=0.5)
Ntaeta_rect_glyphs = Rect(x="x", y="y", width="w", height="h", angle="angle", fill_color=c_blue, fill_alpha=0.5)
### Figure 3, Define Figure and add Geometry:
figure3 = figure(title=figure_texts.data['text'][6], tools="save", x_range=(-30,30), y_range=(-30,30),width=400,height=400,)
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=25, y_end=0))
figure3.add_layout(Arrow(end=NormalHead(fill_color="black", size=15),
                   x_start=0, y_start=0, x_end=0, y_end=-25))
figure3_labels  = LatexLabelSet(x='x', y='y', text='names', level='glyph', x_offset=5, y_offset=5, source=f1.Perm_Label_source)
figure3_labels2 = LatexLabelSet(x='x', y='y', text='names', source=f3.Moving_Label_source)


glyphs_to_add = [NzetaP_arrow_glyph, NzetaN_arrow_glyph, NetaP_arrow_glyph, NetaN_arrow_glyph,
                 Nzetaeta1_arrow_glyph, Nzetaeta2_arrow_glyph, Nzetaeta3_arrow_glyph, Nzetaeta4_arrow_glyph, Rotating_Axis_X_glyph, Rotating_Axis_Y_glyph]
add_layouts_from_list(figure3, glyphs_to_add)

glyphs_to_add = [Rotating_Plane_glyph, Rotating_Plane_red_glyph, Neta_rect_glyphs, Neta_rect_glyphs, Neta_rect_glyphs, Neta_rect_glyphs,
                 Ntaeta_rect_glyphs, Ntaeta_rect_glyphs, Ntaeta_rect_glyphs, Ntaeta_rect_glyphs]
glyph_sources = [f3.Rotating_Plane_source, f3.Rotating_Plane_red_source, f3.NzetaP_rect_source, f3.NzetaN_rect_source, f3.NetaP_rect_source, f3.NetaN_rect_source,
                 f3.Nzetaeta1_rect_source, f3.Nzetaeta2_rect_source, f3.Nzetaeta3_rect_source, f3.Nzetaeta4_rect_source]
add_glyphs_from_list(figure3, glyphs_to_add, glyph_sources)


# dummy glyphs for the legend entries
dummy_normal_3 = figure3.square([0.0],[0.0],size=0,fill_color=c_orange,fill_alpha=0.5)
dummy_shear_3  = figure3.square([0.0],[0.0],size=0,fill_color=c_blue,fill_alpha=0.5)

legend3 = LatexLegend(items=[
    (figure_texts.data['text'][2], [dummy_normal_3]),
    (figure_texts.data['text'][3], [dummy_shear_3 ]),
], location='top_left', max_label_width = 220)
figure3.add_layout(legend3)

# LatexLabelSet has to be added to the layout after LatexLegend! Otherwise the labels won't show.
figure3.add_layout(figure3_labels)
figure3.add_layout(figure3_labels2)


### All figures, Turn off grids: 
def turn_off_grid(fig):
    fig.xaxis.major_tick_line_color  = None
    fig.xaxis.major_label_text_color = None
    fig.xaxis.minor_tick_line_color  = None
    fig.xaxis.axis_line_color        = None
    fig.yaxis.major_tick_line_color  = None
    fig.yaxis.major_label_text_color = None
    fig.yaxis.minor_tick_line_color  = None
    fig.yaxis.axis_line_color        = None
    fig.xgrid.visible                = False
    fig.ygrid.visible                = False
    fig.toolbar.logo                 = None

turn_off_grid(figure1)
turn_off_grid(figure2)
turn_off_grid(figure3)



###################################
# Buttons and Sliders
###################################

### Create  sliders to change Normal and Tangential Forces
Normal_X_slider= LatexSlider(title="\\sigma_x=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value = 0, start = -10, end = 10, step = 0.5)
Normal_X_slider.on_change('value',NormalForceX_init)
    
Normal_Z_slider= LatexSlider(title="\\sigma_z=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value = 0, start = -10, end = 10, step = 0.5)
Normal_Z_slider.on_change('value',NormalForceZ_init)
   
Tangential_XZ_slider= LatexSlider(title="\\tau_{xz}=",value_unit='\\frac{\\mathrm{N}}{\\mathrm{mm}^2}',value = 0, start = 0, end = 10, step = 0.5)
Tangential_XZ_slider.on_change('value',TangentialXZ_init)
    
Plane_Angle_slider= LatexSlider(title= "\\alpha=",value_unit='^{\\circ}',value= 0,start = -180, end = 180, step = 1)
Plane_Angle_slider.on_change('value',changePlaneAngle)
Plane_Angle_slider.disabled = True


###Create Reset Button:
reset_button = Button(label="Reset", button_type="success")
reset_button.on_click(reset)

###Create Draw Button:
draw_button  = Button(label="Draw", button_type="success")
draw_button.on_click(draw)

###Create Show Button:
show_button  = Button(label="Show/Hide principal stress + direction", button_type="success", disabled=True)
show_button.on_click(show)

lang_button = Button(label='Zu Deutsch wechseln', button_type="success")
lang_button.on_click(changeLanguage)



###################################
# Page Layout
###################################

### Add description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1140)

### Arrange layout
doc_layout = layout(children=[column(
    row(Spacer(width=860),lang_button),
    row(description),
    row(Spacer(height=30)),
    row(column(figure1,row(Spacer(height=10,width=50),column(Normal_X_slider,Normal_Z_slider,Tangential_XZ_slider))),column(figure2,row(Spacer(height=10,width=50),column(draw_button,show_button,reset_button))),column(figure3, row(Spacer(height=10,width=50),Plane_Angle_slider))))])
curdoc().add_root(doc_layout)
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '

