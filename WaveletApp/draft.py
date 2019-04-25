import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos, pi, exp
from scipy.integrate import quad

import mpld3
from mpld3 import plugins
from bokeh.io import output_file, show
from bokeh.models.widgets import Div
from os.path import dirname, split, join, abspath

wavelet_plot_filename = join(dirname(__file__), "lines.html")

Resolut=100
amp=1
T0=2
a = np.linspace(1, 5, Resolut)
b = np.linspace(0.1, 10, Resolut)
W = np.zeros((Resolut, Resolut))

for i in range (0,Resolut):
    for j in range (0,Resolut):
        def integrand1(t):
            output = a[i]**-0.5 * amp * (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)
            return output
        W[i][j]=quad(integrand1, 1, 3)[0]

fig, ax = plt.subplots()
im = ax.pcolormesh(a,b,W)
#plt.show()


fig.colorbar(im, ax=ax)
ax.set_title('An Image', size=20)


mpld3.fig_to_html(fig)
mpld3.show()
mpld3.save_html(fig, "Wavelet.html")

# print(mpld3.fig_to_html(fig))
# out_fname = os.path.join(options.outdir, 'plots', 'gene_overview_%s%s%s.html' % (gene.name, event_tag, log_tag))
# plugins.clear(fig)
# mpld3.save_html(fig, "Wavelet.html")
# wavelet_plot = Div (text=open(wavelet_plot_filename).read(), render_as_text=False, width=650, height=100)
# show(wavelet_plot)