from bokeh.plotting import Figure, show
import numpy as np
from math import exp
from scipy.integrate import quad
from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.palettes import Viridis, Spectral
import colorcet as cc

Image = Figure(x_range=(0, 5), y_range=(0, 5),
                            x_axis_label='b', y_axis_label='a',
                            title="An Image",  width=400, height=400)
Image_source = ColumnDataSource(data={'a': [],'b':[],'W':[]})
color_mapper = LinearColorMapper(palette="Spectral11")

Resolut=120
amp=1
T0=2
a = np.linspace(0.1, 5, Resolut)
b = np.linspace(0.1, 5, Resolut)
W = np.zeros((Resolut, Resolut))

for i in range (0,Resolut):
    for j in range (0,Resolut):
        def integrand1(t):
            output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
            return output
        W[i][j]=quad(integrand1, 1, 3)[0]

Image_source.data = {'a': [a],'b':[b],'W':[W]}
Image.image(image="W", source=Image_source, palette=cc.palette.CET_R3, x=0, y=0, dw=5, dh=5)   
show(Image)
# CET_D1A
# CET_R2