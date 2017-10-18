from __future__ import division

import mandel
import mandel_colormap
from scipy.ndimage.filters import gaussian_filter, median_filter
import scipy.misc as smp

# this script generates a nice looking static picture of the mandelbrot set.
# target resolution
x_res = 200
y_res = 200

# in the following you find some sample setups.
# Spiral
name = 'mandel_spiral.png'
cx = -0.74364085
cy = 0.13182733
d = 0.000120168
frequency = 32
max_iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0

#Lightning
name = 'mandel_lightning.png'
cx = 0.37144264
cy = 0.64935303
d = 0.00005
frequency = 256
max_iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0

#Tail
name = 'mandel_tail.png'
cx = -0.7435669
cy = 0.1314023
d = 0.0022878
frequency = 64
max_iterations = 10 * frequency
iteration_bound = 10
median_filtering_size = x_res / 100
gauss_filtering_sigma = 1

#ganz
name = 'mandel_ganz.png'
cx = -0.5
cy = 0
d = 3
frequency = 16
max_iterations = 10000
iteration_bound = 100
median_filtering_size = 0
gauss_filtering_sigma = 0.1

x0 = cx-d*.5
y0 = cy-d*.5
xw = d
yw = d

### main process starts here. ###

# calculate mandelbrot set
it_count = mandel.mandel(x0, y0, xw, yw, x_res, y_res, max_iterations, iteration_bound)

# apply some filters
if median_filtering_size is not 0:
    it_count = median_filter(it_count, size=median_filtering_size)
if gauss_filtering_sigma is not 0:
    it_count = gaussian_filter(it_count, sigma=gauss_filtering_sigma)

color = mandel_colormap.iteration_count_to_rgb_color(it_count, frequency, max_iterations)
print color.shape

# plot and save picture
img = smp.toimage(color) # Create a PIL image
img.save(name)
img.show()


