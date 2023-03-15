# time for periodic update of plot in milliseconds
update_time = 100

# settings for the iteration slider
iter_init = 50
iter_max = 1000
iter_step = 50

# settings for the frequency slider
freq_init = 1
freq_min = 1
freq_max = 10
freq_step = 1

# resolution in pixels
x_res = 400
y_res = 400

# initial set
x0 = -2
y0 = -1.5
xw = 3.0
yw = 3.0
x1 = x0 + xw
y1 = y0 + yw

# if a the result of an iteration in the computation of the mandelbrot set is bigger than the divergence_radius,
# iteration is stopped and we assume, that the this point diverges after N iterations
iteration_bound = 10
