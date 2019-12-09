
from math import pi,sqrt,pow,sin,cos,atan 


def clear_arrow_source(source_list):
    empty_dict = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
    for cds in source_list:
        ro = len(cds.data["xS"])
        cds.stream(empty_dict, rollover=-ro)

def clear_rect_source(source_list):
    empty_dict = dict(x=[], y=[], w=[], h=[], angle=[])
    for cds in source_list:
        ro = len(cds.data["x"])
        cds.stream(empty_dict, rollover=-ro)
       


def calculate_radius_and_center(input_vars):
    radius_temp  = float(sqrt(pow(((input_vars["MohrNx"]-input_vars["MohrNz"])/2),2)+pow(input_vars["MohrNxz"],2)))
    centreX_temp = float((input_vars["MohrNx"]+input_vars["MohrNz"])/2)
    rleft_x_temp = centreX_temp - radius_temp # not always needed
    return [radius_temp, centreX_temp, rleft_x_temp]




def add_layouts_from_list(fig, layout_list):
    for tmp_layout in layout_list:
        fig.add_layout(tmp_layout)

def add_glyphs_from_list(fig, glyph_list, source_list):
    assert len(glyph_list) == len(source_list), "Lists must have same length!"
    for i in range(0,len(glyph_list)):
        fig.add_glyph(source_list[i], glyph_list[i])