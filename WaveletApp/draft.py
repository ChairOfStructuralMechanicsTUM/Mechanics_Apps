# import numpy as np
# from scipy.optimize import minimize_scalar
# import math
# from scipy.optimize import root

# n=200
# a=np.linspace(0.1,5,n)
# b=np.linspace(0.1,5,n)

# # for i, a_i in enumerate(a):
# #         for j, b_j in enumerate(b):
# #             return  (t-b[j])/a[i] * exp(-( (t-b[j])/a[i] )**2.0)


# a = 3
# b = 2
# c = 1

# def func(x):
#     # return (math.exp(x * a) - math.exp(x * b) - c)**2
#     return math.exp(-x**2)*x


# res= root(func,x0=1,)

# print(res)

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Div

output_file("div.html")

div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
are <i>200</i> and <i>100</i> respectively.""",
width=200, height=100)
show(widgetbox(div))