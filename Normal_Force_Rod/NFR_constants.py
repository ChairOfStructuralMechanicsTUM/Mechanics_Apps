


### default values (for setup)

## coordinates

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
ysl      = -0.1
ysr      = -0.1 

# load bounds (coordinates)
lb       = 0.2   # lower boundary
ub       = 0.7   # upper boundary


## constants used for the functions
F        = 1.0
L        = xr_end-xr_start
E        = 1.0
A        = 1.0
p0       = 1.0
T        = 1.0
alpha_T  = 1.0
sigma    = 0.0

### global constants  (they really never change)

## figure settings
fig_width  = 630
fig_height = 300

x_range = (xr_start-1.5,xr_end+1.5)

#TODO: define default arrow color here!
# also initial load position etc.
color_rod   = "#0065BD"
color_arrow = "#0065BD"


# initial slider settings:
initial_load = 0
initial_load_position = 0.5*(xr_end - xr_start)




### images/graphics from external sources
slide_support_img = "Normal_Force_Rod/static/images/auflager01.svg"
fixed_support_img = "Normal_Force_Rod/static/images/auflager02.svg"








