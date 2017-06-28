#main file:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np
from classes import *

#initialization of objects
canti       = Cantilever()
norm        = Beam()
fa          = Support("A",0.0,0.0)                                                    #creation of support a.
fb          = Support("B",0.0,norm.xf)                                                    #creation of support b
f1          = Load("F1")                                                            #1st load
f2          = Load("F2")                                                            #2nd load
f3          = Load("F3")                                                            #3rd load
f4          = Load("F4")                                                            #4th load
f5          = Load("F5")                                                            #5th load on frame
resultant   = Force("Resultant",0.0,0.0)                                                           #creation of (theoretical) resultant load

#sliders:


#Cantilever rectangle source:


#move_tri = 0.25

def fun_f(p_mag,k,l):
    f_mag = -1.0 * (p_mag *k) / l
    return f_mag

def calc_resultant(f1,f2,f3,f4,f5):
    resultant.mag           = (f1.mag + f2.mag + f3.mag + f4.mag + f5.mag) / 5.0
    resultant.loc           = (f1.loc + f2.loc + f3.loc + f4.loc + f5.loc) / 5.0
    resultant.deflection    = (f1.deflection + f2.deflection + f3.deflection + f4.deflection + f5.deflection)

def update_supports():
    a = resultant.loc
    b = fb.loc - a
    fa.mag = fun_f(resultant.mag,b,fb.loc)
    fb.mag = fun_f(resultant.mag,a,fb.loc)
    fa.update_arrow()
    fb.update_arrow()

def fun_update(attr,old,new):
    f1.update_arrow()
    f2.update_arrow()
    f3.update_arrow()
    f4.update_arrow()
    f5.update_arrow()

    if fb.loc == 0:
        fun_cantilever()
    elif fb.loc != 0:
        fun_normal()

    update_supports()

def fun_normal():
    canti.clear_beam()
    canti.clear_box()
    f1.deflection = norm.fun_deflection(f1.loc, fb.loc, f1.mag)
    f2.deflection = norm.fun_deflection(f2.loc, fb.loc, f2.mag)
    f3.deflection = norm.fun_deflection(f3.loc, fb.loc, f3.mag)
    f4.deflection = norm.fun_deflection(f4.loc, fb.loc, f4.mag)
    f5.deflection = norm.fun_deflection(f5.loc, fb.loc, f5.mag)
    calc_resultant(f1,f2,f3,f4,f5)
    norm.source.data['y'] = resultant.deflection


def fun_cantilever():
    norm.clear_beam()
    fa.fun_clear()
    fb.fun_clear()
    canti.create_box()
    f1.deflection = canti.fun_deflection(f1.loc, f1.mag)
    f2.deflection = canti.fun_deflection(f2.loc, f2.mag)
    f3.deflection = canti.fun_deflection(f3.loc, f3.mag)
    f4.deflection = canti.fun_deflection(f4.loc, f4.mag)
    f5.deflection = canti.fun_deflection(f5.loc, f5.mag)
    calc_resultant(f1,f2,f3,f4,f5)
    canti.source.data['y'] = resultant.deflection

print "hi"

###Main Plot:
plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(0-.5,1+.5), y_range=(-2.5,2.5))
#plot.line(x='x', y='y', source=norm.source, color='#0065BD',line_width=20)
#plot.line(x='x', y='y', source=norm.source, color='#0065BD',line_width=20)
#plot.triangle(x='x', y='y', size = 'size', source= triangle_source,color="#E37222", line_width=2)
plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = canti.quad_source, color="#808080", fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = canti.segment_source, color="#F4A582", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
#labels = LabelSet(x='x', y='y', text='name', level='glyph',
#              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')
###Plot with moment and shear:
'''
y_range0 = -600
y_range1 = -y_range0
plot1 = Figure(title="Biegemoment, Querkraft", x_range=(x0,xf), y_range=(y_range0,y_range1), width = 400, height = 200)
plot1.line(x='x', y='y', source=mom_source, color='blue',line_width=5)
plot1.line(x='x', y='y', source=shear_source, color='red',line_width=5)
plot1.line(x= [x0-1,xf+1], y = [0, 0 ], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.line(x= [xf/2,xf/2], y = [y_range0,y_range1], color = 'black', line_width =2 ,line_alpha = 0.4, line_dash=[1])
plot1.axis.visible = False
'''
###arrow plotting:
#P arrow:'''
f1_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f1.arrow_source,line_color="#A2AD00")

f2_arrow_glyph = Arrow(end=OpenHead(line_color="#A2AD00",line_width= 4, size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width= "lW", source=f2.arrow_source,line_color="#A2AD00")

#Position 2 arrow:
fb_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE', line_width = "lW", source=fa.arrow_source,line_color="#003359")
#Position 1 arrow:
fa_arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
    x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=fb.arrow_source,line_color="#003359" )

###add layouts:
#plot.add_layout(labels)
plot.add_layout(fb_arrow_glyph)
plot.add_layout(f2_arrow_glyph)
plot.add_layout(f1_arrow_glyph)
plot.add_layout(fa_arrow_glyph)

###Reset Button
#button = Button(label="Reset", button_type="success")

###CheckboxGroup
#Biegelinie Checkbox
#checkbox = CheckboxGroup(
#        labels=["Biegelinie", "Mit Schub (Biegelinie muss auch markiert sein!)"], active=[])


###on_change:
f1.loc_slider.on_change('value', fun_update)
f2.loc_slider.on_change('value', fun_update)
f2.mag_slider.on_change('value', fun_update)
f1.mag_slider.on_change('value', fun_update)

#p_mag_slide.on_change('value', Fun_Update)
fb.loc_slider.on_change('value', fun_update)
fb.mag_slider.on_change('value', fun_update)

#lth_slide.on_change('value',Fun_Update)
#checkbox.on_change('active',Fun_Update)
#button.on_click(initial)

#main:
#initial()
'''
#triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])

plot = Figure(title="", x_range=(beam.x0-.5,beam.xf+.5), y_range=(-2.5,2.5))
my_line=plot.line(x='x', y='y', source=beam.source, color='#0065BD',line_width=20)
plot.triangle(x='x', y='y', size = 'size', source= triangle_source,color="#E37222", line_width=2)
plot.quad(top='top', bottom='bottom', left='left',
    right='right', source = quad_source, color="#808080", fill_alpha = 0.5)
plot.segment(x0='x0', y0='y0', x1='x1',
          y1='y1', source = segment_source, color="#F4A582", line_width=2)
plot.axis.visible = False
plot.outline_line_width = 7
plot.outline_line_alpha = 0.3
plot.outline_line_color = "Black"
labels = LabelSet(x='x', y='y', text='name', level='glyph',
              x_offset=5, y_offset=-30, source=labels_source, render_mode='canvas')

for i in range(0,number):
    plot.add_layout(flist[i].arrow_glyph)
plot.add_layout(fa.arrow_glyph)
plot.add_layout(fb.arrow_glyph)

force.loc_slider.on_change('value', Fun_Update)
force.mag_slider.on_change('value', Fun_Update)
fb.loc_slider.on_change('value', Fun_Update)
#f2_loc_slide.on_change('value',Fun_Update)
#lth_slide.on_change('value',Fun_Update)





vals1 = []
vals2 = []
vals3 = []
for i in range(0,number):
    vals1 = flist[i].loc_slider
    vals2 = flist[i].mag_slider
    vals3.append(vals1)

column1 = [flist[0].loc_slider,flist[0].mag_slider,flist[1].loc_slider,flist[1].mag_slider,
    fb.loc_slider]

curdoc().add_root( row( column(column1),  column(plot) ) )
'''
#curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '



#f1.mag_slider,f2.mag_slider,fb.mag_slider,f1.loc_slider,f2.loc_slider,fb.loc_slider),

curdoc().add_root( plot)
