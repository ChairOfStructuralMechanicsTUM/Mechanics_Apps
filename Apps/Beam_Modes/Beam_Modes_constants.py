"""
Template App - constants used throughout all files
"""
import numpy as np
import pathlib
app_base_path = pathlib.Path(__file__).resolve().parents[0]
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
mue = 1.0               # mue
EI_real = 10000.0

###################################
#       plotting properties       #
###################################

n_beam = 401                    # value of fragmentation of the beam
n_r = 499                       # value of fragmentation of the excitation frequency ratio
max_r = 10                      # maximum of displayable excitation frequency ratio

##################################
#        external images         #
##################################

# images/graphics from external sources
pinned_support_img = str(app_base_path / "static/images/pinned_support.svg")
fixed_support_left_img = str(app_base_path / "static/images/fixed_support_left.svg")
fixed_support_right_img = str(app_base_path / "static/images/fixed_support_right.svg")

# height support images
img_h = 1.0
img_w_pinned = 0.4
img_w_fixed = 0.1
y_fixed = 0.45
