#main file:
from bokeh.plotting import Figure, output_file , show
from bokeh.models import ColumnDataSource, Slider, LabelSet, OpenHead, Arrow
from bokeh.layouts import column, row, widgetbox
from bokeh.io import curdoc
from bokeh.models.widgets import Button, CheckboxGroup
import numpy as np
from class_force import Force, Beam

#initialization of objects
beam = Beam()                               #creation of beam object. this holds the actual beam
fa = Force("A",1)                           #creation of support a.
fb = Force("B",2)                           #creation of support b
print fb.loc
fb.loc = beam.xf
number = 2
flist = []
for count in range(0,number):
    force = Force("F" +str(count))
    flist.append(force)
    print force.name

#Cantilever rectangle source:
quad_source = ColumnDataSource(data=dict(top= [], bottom= [],left = [], right =[]))
segment_source = ColumnDataSource(data=dict(x0= [], y0= [],x1 = [], y1 =[]))
labels_source = ColumnDataSource(data=dict(x=[] , y=[],name = []))


move_tri = 0.25
triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))

def Fun_Cantilever():
    triangle_source.data = dict(x = [], y = [], size = [])
    fa.arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    fb.arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
    top = 2
    bottom  = -top
    left = -1
    right = 0
    clines = 40
    quad_source.data = dict(top = [top], bottom = [bottom], left = [left] , right = [right])
    xseg = np.ones(clines) * left
    yseg = np.linspace(bottom,top-0.2,clines)
    x1seg = np.ones(clines) * right
    y1seg = np.linspace(bottom+0.2,top,clines)
    segment_source.data = dict(x0= xseg, y0= yseg,x1 = x1seg, y1 =y1seg)



def Fun_F(p_mag,k,l):
    f1_mag = -1.0 * (p_mag *k) / l
    return f1_mag

def Fun_Update(attr,old,new):
    names = []
    rmag = 0
    rloc = 0
    rdy  = np.ones(beam.resol) * 0
    for i in range(0,number):
        flist[i].update_arrow(fb.loc_slider.value)         #update the concentrated loads
        rmag += flist[i].mag
        rloc += flist[i].loc
        rdy  = np.add(rdy,flist[i].dy)
        #names.append(flist[i].name)
    rloc = rloc / number
    a = rloc - beam.x0
    b = fb.loc - rloc
    beam.source.data['y'] = rdy

    if fb.loc_slider.value == 0: #cantilever
        Fun_Cantilever()
    else:
    #Update the support forces
        fa.mag = Fun_F(rmag,b,fb.loc_slider.value)
        fb.mag = Fun_F(rmag,a,fb.loc_slider.value)
        fa.update_arrow(fb.loc_slider.value)
        fb.update_arrow(fb.loc_slider.value)
        triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])
        #names = names + fa.name + fb.name




#triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])

plot = Figure(title="Doppeltgelagerter Balken und Einzellast", x_range=(beam.x0-.5,beam.xf+.5), y_range=(-2.5,2.5))
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
