
from math import pi,sqrt,pow,sin,cos,atan 




def calculate_radius_and_center(input_vars):
    radius_temp  = float(sqrt(pow(((input_vars["MohrNx"]-input_vars["MohrNz"])/2),2)+pow(input_vars["MohrNxz"],2)))
    centreX_temp = float((input_vars["MohrNx"]+input_vars["MohrNz"])/2)
    rleft_x_temp = centreX_temp - radius_temp # not always needed
    return [radius_temp, centreX_temp, rleft_x_temp]