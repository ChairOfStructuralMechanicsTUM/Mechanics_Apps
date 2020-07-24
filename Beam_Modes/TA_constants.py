"""
Template App - constants used throughout all files
"""
import numpy as np
# ----------------------------------------------------------------- #

###################################
#             colors              #
###################################


# basic colors
c_black = "#333333"
c_blue  = "#3070b3"
c_white = "#ffffff"

# arrows / objects
c_green  = "#a2ad00"
c_orange = "#e37222"

# auxiliary lines / objects
c_gray        = "#b3b3b3"
c_gray_text   = "#8a8a8a"
c_gray_light1 = "#e6e6e6"
c_gray_light2 = "#f7f7f7"
c_gray_warm   = "#8f8f8f"

###################################
#      fixed beam properties      #
###################################

F = 80                  # maximum force of the dynamic load
L = 5.0                 # length of the beam
EI = 10000.0            # Youngs Modulus * area moment of inertia 
mue = 1.0               # mue

###################################
#  fixed calculation properties   #
#         for the plots           #
###################################

n = 401                         # value of fragmentation of the beam
max_omega = 500                 # maximum of displayable frequency
max_amp_plot = 5000.0           # highest displayable deflection

###################################
#           coordinates           #
###################################

# start coordinates of the beam 
X = np.linspace(0,L,n)
Y = np.zeros(n)

# start coordinates of the amplitude display
X_Amp =                 np.linspace(0,max_omega,max_omega+1)
Y_Amp =                 np.zeros(max_omega+1)

# start coordinates for the indicator of the displayed amplitude location
X_NAF =                 [0.0,0.0]
Y_NAF =                 [-L,L]

# start coordinates for the current frequency pointer
X_freq =                [0.0,0.0]
Y_freq =                [0.001,max_amp_plot]


##################################
#        external images         #
##################################

# images/graphics from external sources
pinned_support_img = "Beam_Oscillations/static/images/pinned_support.svg"
fixed_support_left_img = "Beam_Oscillations/static/images/fixed_support_left.svg"
fixed_support_right_img = "Beam_Oscillations/static/images/fixed_support_right.svg"

# height support images
img_h = 1.0
img_w_pinned = 0.4
img_w_fixed = 0.1
y_fixed = 0.45
