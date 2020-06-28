###################################
# Imports
###################################
# general imports
from math                 import pi

# bokeh imports
from bokeh.io             import curdoc
from bokeh.plotting       import figure
from bokeh.models         import ColumnDataSource, Arrow, OpenHead, Patch, Ellipse
from bokeh.models.widgets import Button, RadioGroup
from bokeh.layouts        import column, row, Spacer

# latex integration
from os.path              import dirname, join, split, abspath
import sys, inspect

# local imports
from DeformableObject     import DeformableObject

currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir)

from latex_support        import LatexDiv, LatexLabelSet, LatexSlider


###################################
# Constants
###################################
# colors
c_black  = "#333333"
c_blue   = "#3070b3"
c_green  = "#a2ad00 "
c_orange = "#e37222"
c_gray   = "#b3b3b3"

# default values
material_parameters = dict(
    steel       = [210000,0.28] ,
    aluminium   = [70000,0.35]  ,
    lead        = [19000,0.44]  ,
    rubber      = [1000,0.5]    )
E_start_value  = material_parameters['rubber'][0]
nu_start_value = material_parameters['rubber'][1]
a = 0.75



###################################
# DataSources
###################################
deformable_object = DeformableObject(10,5,0,0, E_start_value, nu_start_value)
# symbols on object
deformable_object.add_child(-2.5,0,False,[[-1.5,1.5,1.5,-1.5,-1.5],[1,1,-1,-1,1]])
deformable_object.add_child(1.5,0,False,[[-a,0,a,0,-a],[0,a,0,-a,0]])
deformable_object.add_child(3.5,0,True,[2*a,2*a])
# force symbols
deformable_object.add_force_symbol(0,2.5,10,1,0,'R_y')
deformable_object.add_force_symbol(-5,0,5,1,pi/2,'R_x')
deformable_object.add_force_symbol(0,-2.5,10,1,pi,'R_y')
deformable_object.add_force_symbol(5,0,5,1,3/2*pi,'R_x')
deformable_object.deform_object(0,0)



###################################
# Helper Functions
###################################
def update_F_slider(slider_root, new_step, new_start, new_end):
    slider_root.step = new_step
    slider_root.start, slider_root.end = new_start, new_end
    if slider_root.value < new_start: slider_root.value = new_start
    elif slider_root.value > new_end: slider_root.value = new_end



###################################
# Callback Functions
###################################
def cb_change_material(attr, old, new):
    if materials.active == 4:
        E_slider.disabled  = False
        nu_slider.disabled = False
        if E_slider.value < 60000: E_slider.value = 60000
        update_F_slider(Fx_slider, 10, -50, 50)
        update_F_slider(Fy_slider, 10, -50, 50)
        E, nu = E_slider.value, nu_slider.value
    else:
        # disable sliders and set values to material parameters
        if materials.active == 0:
            update_F_slider(Fx_slider, 0.10, -0.5, 0.5)
            update_F_slider(Fy_slider, 0.10, -0.5, 0.5)
            E, nu = material_parameters['rubber'][0], material_parameters['rubber'][1]
        elif materials.active == 1:
            update_F_slider(Fx_slider, 2, -10, 10)
            update_F_slider(Fy_slider, 2, -10, 10)
            E, nu = material_parameters['lead'][0], material_parameters['lead'][1]
        elif materials.active == 2:
            update_F_slider(Fx_slider, 10, -50, 50)
            update_F_slider(Fy_slider, 10, -50, 50)
            E, nu = material_parameters['aluminium'][0], material_parameters['aluminium'][1]
        elif materials.active == 3:
            update_F_slider(Fx_slider, 10, -50, 50)
            update_F_slider(Fy_slider, 10, -50, 50)
            E, nu = material_parameters['steel'][0], material_parameters['steel'][1]
        E_slider.value     = E
        nu_slider.value    = nu
        E_slider.disabled  = True
        nu_slider.disabled = True
    # Update data and calculate deformed object
    deformable_object.E  = E
    deformable_object.nu = nu
    deformable_object.deform_object(Fx_slider.value*1000, Fy_slider.value*1000) # * 1000 (kN -> N)

def cb_change_load(attr, old, new):
    deformable_object.deform_object(Fx_slider.value*1000, Fy_slider.value*1000) # * 1000 (kN -> N)

def cb_show_hide_symbols(event):
    deformable_object.children_vis *= -1
    if deformable_object.children_vis == 1:
        width, fill = 1, c_black
        # state = True (not supported for Patch in bokeh 1.4.0)
        button.label = 'hide symbols'
    else:
        width, fill = 0, None
        # state = False (not supported for Patch in bokeh 1.4.0)
        button.label = 'show symbols'
    for child in children_visual:
        child.line_width, child.fill_color = width, fill
        # child.visible = state (not supported for Patch in bokeh 1.4.0)



###################################
# Figures
###################################
figure = figure(x_range=(-15,15), y_range=(-10,10), height=400, width=600, tools='', toolbar_location=None, 
    outline_line_color=c_black, outline_line_width=1)
figure.axis.visible = False

# plot undeformed object
source                   = deformable_object.data_source['undeformed']
undeformed_visual        = Patch(x='x', y='y', line_color=c_black, fill_color=None, line_dash=(10,10))
figure.                    add_glyph(source,undeformed_visual)

# plot deformed object
source                   = deformable_object.data_source['deformed']
deformed_visual          = Patch(x='x', y='y', line_color=c_black, fill_color=c_gray, fill_alpha=0.5 )
figure.                    add_glyph(source,deformed_visual)

# plot symbols on object
children_visual = []
for child in deformable_object.children:
    if not child.ellipse:
        source           = child.data_source
        visual           = Patch(x='x', y='y', line_color=c_black, line_width=0, fill_color=None, fill_alpha=0.5 )
    else:
        source           = child.data_source
        visual           = Ellipse(x='x', y='y', width='w', height='h', line_color=c_black, line_width=0, fill_color=None, fill_alpha=0.5)
    figure.                add_glyph(source,visual)
    children_visual.       append(visual)

# plot force symbols
for force_symbol in deformable_object.force_symbols:
    # sigma
    source           = force_symbol.data_source['sigma']
    visual           = Patch(x='x', y='y', line_color=c_black, line_width=1, fill_color=c_orange, fill_alpha=0.75 )
    figure.            add_glyph(source,visual)
    # sigma arrows
    source           = force_symbol.data_source['sigma_arrows']
    visual           = Arrow(end=OpenHead(line_color=c_black,line_width=1,size=5),
        x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_black, line_width=1,
        source=source)
    figure.            add_layout(visual)
    # R arrows
    source           = force_symbol.data_source['R_arrow']
    visual           = Arrow(end=OpenHead(line_color=c_black,line_width=2,size=10),
        x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_color=c_black, line_width=2,
        source=source)
    figure.            add_layout(visual)
    # plot labels
    source           = force_symbol.data_source['R_label']
    visual           = LatexLabelSet(x='x', y='y', text='label_text', source=source, level='glyph', x_offset=-10, y_offset=-10)
    figure.            add_layout(visual)



###################################
# Buttons and Sliders
###################################

# sliders to choose force applied to x- and y-axis
Fx_slider = LatexSlider(title='R_x=', value_unit='{kN}', value=0, start=-0.5, end=0.5, step=0.10, width=300)
Fy_slider = LatexSlider(title='R_y=', value_unit='{kN}', value=0, start=-0.5, end=0.5, step=0.10, width=300)
Fx_slider.  on_change('value', cb_change_load)
Fy_slider.  on_change('value', cb_change_load)

# sliders to choose material parameters
E_slider  = LatexSlider(title='E=', value_unit='{N/mm}^{2}', value=E_start_value, start=60000, end=260000, step=20000, width=250, disabled=True)
nu_slider = LatexSlider(title='\\nu=', value_unit='', value=nu_start_value, start=0, end=0.5, step=0.05, width=250, disabled=True)
E_slider.   on_change('value', cb_change_material)
nu_slider.  on_change('value', cb_change_material)

# button to show/hide symbols on object
button    = Button(label='show symbols', button_type='success', width=200)
button.     on_click(cb_show_hide_symbols)

# radio button to choose material
materials = RadioGroup(name='Material parameters:',labels=['rubber', 'lead', 'aluminium', 'steel', 'custom'], active=0)
materials.  on_change('active', cb_change_material)



###################################
# Page Layout
###################################

description_filename = join(dirname(__file__), "description.html")
description          = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1000)

material_caption_filename = join(dirname(__file__), "caption.html")
material_caption          = LatexDiv(text=open(material_caption_filename).read(), render_as_text=False, width=300)

widget_box = column(Fx_slider,Fy_slider, row(Spacer(width=50), button), Spacer(height=10), material_caption,materials, 
    row(Spacer(width=25),E_slider), row(Spacer(width=25),nu_slider) )

curdoc().add_root(column(
    description, Spacer(height=10), row(Spacer(width=10), widget_box,Spacer(width=10), column(Spacer(height=5),figure)), Spacer(height=20)
))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')
