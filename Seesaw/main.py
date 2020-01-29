"""
Python Bokeh app which visualizes a pair of forces acting on a seesaw
"""

from bokeh.plotting import figure 
from bokeh.layouts import column, row, Spacer
from bokeh.models import ColumnDataSource, Slider, Arrow, OpenHead, Line, TeeHead, Button, Toggle
from bokeh.models.glyphs import ImageURL
from bokeh.io import curdoc

import yaml

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
flags = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings = yaml.safe_load(open('Seesaw/static/strings.json', encoding='utf-8'))

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

def setValueText(F1, F2):
    value_plot.text = "$$\\begin{aligned} F_1&=" + "{:4.1f}".format(F1) + "\\,\\mathrm{N}\\\\ F_2&=" + "{:4.1f}".format(F2) + "\\,\\mathrm{N} \\end{aligned}$$"

def changeLength(attr, old, new):
    tmp = (l_beam-new)/new
    F1_new = (F_total*tmp) / (1+tmp)
    F2_new = F_total - F1_new
    F1_source.patch( {"yS":[(0,F1_new)]} )
    F2_source.patch( {"yS":[(0,F2_new)]} )
    dist_source.patch( {'xE':[(0,new)], 'xL':[(0,new/2.0-0.3)]} )
    support_source.patch( {'x':[(0,new)]} )
    if flags.data["show"][0] == 'on':
        setValueText(F1_new, F2_new)

def changeShow(active):
    a = show_button
    [lang] = flags.data["lang"]
    if active:
        flags.patch( {'show':[(0,'on')]} )
        [F1] = F1_source.data['yS']
        [F2] = F2_source.data['yS']
        setValueText(F1, F2)
        show_button.label = strings["show_button.label"]['on'][lang]
    else:
        flags.patch( {'show':[(0,'off')]} )
        value_plot.text= ""
        show_button.label = strings["show_button.label"]['off'][lang]

def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage('de')
    elif lang == "de":
        setDocumentLanguage('en')

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
     
# Slider to change location of Forces F1 and F2
F1F2Location_slider = LatexSlider(value=20, start=1, end=39, step=1, value_unit="\\text{m}")
F1F2Location_slider.on_change('value',changeLength)

# Toggle button to show forces
show_button = Toggle(button_type="success")
show_button.on_click(changeShow)

lang_button = Button(button_type="success")
lang_button.on_click(changeLanguage)

# Description from HTML file
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(render_as_text=False, width=880)

# Set language
setDocumentLanguage(std_lang)

curdoc().add_root(column(row(Spacer(width=600),lang_button),description,row(plot,column(F1F2Location_slider,show_button,value_plot))))
# curdoc().title = strings["curdoc().title"]["en"]
