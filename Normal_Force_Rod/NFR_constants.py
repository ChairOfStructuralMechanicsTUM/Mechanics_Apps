"""
Normal Force Rod - constants used throughout different files

"""

# ----------------------------------------------------------------- #


###################################
#           coordinates           #
###################################

# rod/beam
xr_start = 0.0
xr_end   = 10.0
y_offset = 0.0
#y_cross  = 0.5 # offset for the labels etc. in case of tapared cross-section mode
r_reso   = 100  # resolution, i.e. number of points to draw the rod
sol_reso = 1000 # resolution/samples for the N and U functions

# supports
xsl      = xr_start - 0.325
xsr      = xr_end - 0.33
ysl      = -0.05
ysr      = -0.08

# load patch bounds
lb       = 0.2   # lower boundary
ub       = 0.7   # upper boundary


## constants used for the functions/equations
F        = 1.0
L        = xr_end-xr_start
E        = 1.0
A        = 1.0
p0       = 1.0
T        = 1.0
alpha_T  = 1.0
sigma    = 0.0   # actually no sigma in formulas, missread; could be replaced by hard coded zeros




###################################
#         figure settings         #
###################################

# scale
fig_width  = 600
fig_height = 300
x_range    = (xr_start-1.5,xr_end+1.5)

# color
color_rod   = "#0065BD" # beam color
color_arrow = "#0065BD" # force arrow color

color_rod_cold = "#3070b3"
color_rod_hot  = "#e37222"





###################################
#     slider/button settings      #
###################################

# initial settings
initial_load = 0 # for the load buttons
initial_load_position = 0.5*(xr_end - xr_start) # for th slider



##################################
#        external images         #
##################################

# images/graphics from external sources
slide_support_img = "Normal_Force_Rod/static/images/slide_support.svg"
fixed_support_img = "Normal_Force_Rod/static/images/fixed_support.svg"








