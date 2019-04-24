"""
Python Bokeh app which visualizes a pair of forces acting on a seesaw
"""

from bokeh.plotting import figure 
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead, Line, TeeHead, Button
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc

import json

from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv, LatexSlider, LatexLabelSet

h_beam = 1.0
l_beam = 40.0
F_total = 40.0
std_lang = 'en'
flags = ColumnDataSource(data=dict(show=[False], lang=[std_lang]))
strings = json.load(open('Seesaw/static/strings.json'))

# Force vectors and labels
F1_source = ColumnDataSource(dict(xS=[0], xE=[0], yS=[F_total/2], yE=[0], xL=[1], yL=[5], name=["F_1"]))
F2_source = ColumnDataSource(dict(xS=[l_beam], xE=[l_beam], yS=[F_total/2], yE=[0], xL=[l_beam-3], yL=[5], name=["F_2"]))
# Support source
support_source = ColumnDataSource(dict(x = [20], y = [-2.0*h_beam], src = ["Seesaw/static/images/simple_support.svg"]))

# Plot
plot = figure(title="", tools="", x_range=(-2,42), y_range=(-50,50))
plot.toolbar.logo = None
plot.axis.axis_label_text_font_style="normal"
plot.axis.axis_label_text_font_size="14pt"
plot.xaxis.axis_label=strings["plot_x_label"][std_lang]
plot.yaxis.axis_label=strings["plot_y_label"][std_lang]

# plot bar and support
plot.line([0, l_beam], [-h_beam, -h_beam], line_width=10, color='#3070B3')
plot.add_glyph(support_source,ImageURL(url="src", x='x', y='y', w=5, h=5, anchor="top_center"))

# plot distance
dist_source = ColumnDataSource(dict(xS=[0], xE=[20], yS=[-15], yE=[-15], xL=[20.0/2.0-0.3], yL=[-13.5], text=["a"]))
dist = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
    start=TeeHead(line_color="#808080",line_width=1, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=1, line_color="#808080", source=dist_source)
dist_label = LatexLabelSet(x='xL', y='yL', text='text', source=dist_source)
length = Arrow(end=TeeHead(line_color="#808080", line_width=1, size=10),
    start=TeeHead(line_color="#808080",line_width=1, size=10),
    x_start=0, y_start=-25, x_end=40, y_end=-25, line_width=1, line_color="#808080")
length_label = LatexLabelSet(x='x', y='y', text='text', source=ColumnDataSource(dict(x=[19.7], y=[-23.5], text=["l"])))

#plotting Vectors as arrows
F1_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222", line_width=4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=4, source=F1_source,line_color="#E37222")
F2_arrow_glyph = Arrow(end=OpenHead(line_color="#E37222", line_width=4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width=4, source=F2_source,line_color="#E37222")

F1_label_glyph=LatexLabelSet(x='xL', y='yL', text='name', text_font_size="15pt", level='glyph', source=F1_source)
F2_label_glyph=LatexLabelSet(x='xL', y='yL', text='name', text_font_size="15pt", level='glyph', source=F2_source)

plot.add_layout(F1_arrow_glyph)
plot.add_layout(F2_arrow_glyph)
plot.add_layout(F1_label_glyph)
plot.add_layout(F2_label_glyph)
plot.add_layout(dist)
plot.add_layout(dist_label)
plot.add_layout(length)
plot.add_layout(length_label)

# Div to show force and distance values
value_plot = LatexDiv(text="", render_as_text=False, width=300)

def changeLength(attr, old, new):
    tmp = (l_beam-new)/new
    F1_new = (F_total*tmp) / (1+tmp)
    F2_new = F_total - F1_new
    F1_source.patch( {"yS":[(0,F1_new)]} )
    F2_source.patch( {"yS":[(0,F2_new)]} )
    dist_source.patch( {'xE':[(0,new)], 'xL':[(0,new/2.0-0.3)]} )
    support_source.patch( {'x':[(0,new)]} )
    [show] = flags.data["show"]
    if show:
        value_plot.text = "$$\\begin{aligned} F_1&=" + str(F1_new) + "\\,\\mathrm{N}\\\\ F_2&=" + str(F2_new) + "\\,\\mathrm{N} \\end{aligned}$$"

def changeShow():
    [show] = flags.data["show"]
    [lang] = flags.data["lang"]
    flags.patch( {'show':[(0,not show)]} )
    if not show:
        [F1] = F1_source.data['yS']
        [F2] = F2_source.data['yS']
        value_plot.text = "$$\\begin{aligned} F_1&=" + str(F1) + "\\,\\mathrm{N}\\\\ F_2&=" + str(F2) + "\\,\\mathrm{N} \\end{aligned}$$"
        show_button.label = strings["show_button_label"]['off'][lang]
    else:
        value_plot.text= ""
        show_button.label = strings["show_button_label"]['on'][lang]

def changeLang():
    [lang] = flags.data["lang"]
    if lang == "en":
        lang = "de"
        # lang_button.label = "Switch to English"
        flags.patch( {'lang':[(0,lang)]} )
    elif lang == "de":
        lang = "en"
        # lang_button.label = "Zu Deutsch wechseln"
        flags.patch( {'lang':[(0,lang)]} )

    show = 'off' if flags.data["show"][0] else 'on'

    description.text = open(strings["description_text"][lang]).read()
    curdoc().title = strings["app_name"][lang]
    lang_button.label = strings["lang_button"][lang]
    F1F2Location_slider.title = strings["slider_label"][lang]
    plot.xaxis.axis_label=strings["plot_x_label"][lang]
    plot.yaxis.axis_label=strings["plot_y_label"][lang]
    show_button.label=strings["show_button_label"][show][lang]
     
# Slider to change location of Forces F1 and F2
F1F2Location_slider = LatexSlider(title=strings["slider_label"][std_lang], value=20, start=1, end=39, step=1, value_unit="\\text{m}")
F1F2Location_slider.on_change('value',changeLength)

# Button to show forces
show_button = Button(label=strings["show_button_label"]['on'][std_lang], button_type="success")
show_button.on_click(changeShow)

lang_button = Button(label=strings["lang_button"][std_lang], button_type="success")
lang_button.on_click(changeLang)

#adding description from HTML file
description = LatexDiv(text=open(strings["description_text"][std_lang]).read(), render_as_text=False, width=880)

curdoc().add_root(column(row(Spacer(width=600),lang_button),description,row(plot,column(F1F2Location_slider,show_button,value_plot))))
curdoc().title = strings["app_name"][std_lang]
