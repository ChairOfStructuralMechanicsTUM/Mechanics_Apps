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

###################################
#         beam properties         #
###################################

F = 80                  # maximum force of the dynamic load
L = 5.0                 # length of the beam
EI = 10000.0*(1+0.1j)            # Youngs Modulus * area moment of inertia
mue = 1.0               # mue

###################################
#       plotting properties       #
###################################

n = 401                         # value of fragmentation of the beam
max_omega = 501                 # maximum of displayable frequency


##################################
#        external images         #
##################################

# images/graphics from external sources
pinned_support_img = "Beam_Modes/static/images/pinned_support.svg"
fixed_support_left_img = "Beam_Modes/static/images/fixed_support_left.svg"
fixed_support_right_img = "Beam_Modes/static/images/fixed_support_right.svg"

# height support images
img_h = 1.0
img_w_pinned = 0.4
img_w_fixed = 0.1
y_fixed = 0.45
