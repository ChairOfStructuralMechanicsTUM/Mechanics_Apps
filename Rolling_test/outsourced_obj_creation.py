from __future__ import division # float devision only, like in python 3
from outsourced_glob_var import glob_SphereXLines, glob_SphereYLines, glob_values


###############################################################################
###                            Sphere functions                             ###
###############################################################################
def createSphere(r,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # find the centre, knowing that it touches the ramp at (offset,H)
    newX = offset+r*SIN
    newY = H+r*COS
    # draw the sphere in blue
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # use the referece lines to find the current position of the lines
    RCOS = r*COS
    RSIN = r*SIN
    X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
    X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
    Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
    Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
    # draw the lines
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])


def createHollowSphere(r,ri,sphere_data,sphere_lines_data):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        sphere_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        sphere_lines_data.data = dict(x=[],y=[])
    else:    
        # find the centre, knowing that it touches the ramp at (offset,H)
        newX = offset+r*SIN
        newY = H+r*COS
        # draw the sphere in semi-transparent blue
        sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1-ri/r]) # a=[0.4]
        # use the referece lines to find the current position of the lines
        RCOS = r*COS
        RSIN = r*SIN
        X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
        X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
        Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
        Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
        # draw the lines
        sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])



###############################################################################
###                           Cylinder functions                            ###
###############################################################################
def createCylinder(r, cylinder_data, cylinder_lines_data):
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    # draw the cylinder around the centre, knowing that it touches the ramp at (offset,H)
    cylinder_data.data=dict(x=[offset+r*SIN],y=[H+r*COS],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[offset,offset+2*r*SIN],
        [offset+r*(SIN-COS),offset+r*(SIN+COS)]],
        y=[[H,H+2*r*COS],[H+r*(COS+SIN),H+r*(COS-SIN)]])


def createHollowCylinder(r,ri, hollowCylinder_data, hollowCylinder_lines_data):
    load_vals = ["SIN", "COS", "offset", "H"]
    SIN, COS, offset, H = [glob_values.get(val) for val in load_vals]
    
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        hollowCylinder_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        hollowCylinder_lines_data.data = dict(x=[],y=[])
    else:
        # draw the cylinder around the centre, knowing that it touches the ramp at (offset,H)
        hollowCylinder_data.data=dict(x=[offset+r*SIN,offset+r*SIN],
            y=[H+r*COS,H+r*COS],w=[2*r,2*ri],c=["#0065BD","#FFFFFF"],a=[1,1])
        hollowCylinder_lines_data.data=dict(x=[[offset,offset+(r-ri)*SIN],
            [offset+(r+ri)*SIN,offset+2*r*SIN],
            [offset+r*(SIN-COS),offset+r*SIN-ri*COS],
            [offset+r*(SIN+COS),offset+r*SIN+ri*COS]],
            y=[[H,H+(r-ri)*COS],[H+(r+ri)*COS,H+2*r*COS],
            [H+r*(COS+SIN),H+r*COS+ri*SIN],
            [H+r*(COS-SIN),H+r*COS-ri*SIN]])
