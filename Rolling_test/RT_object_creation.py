from __future__ import division # float division only, like in python 3
from RT_global_variables import (
        glob_SphereXLines, glob_SphereYLines,
        glob_time, g, fig_samples
        )


###############################################################################
###                            Sphere functions                             ###
###############################################################################
def createSphere(FIG,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    t_samples      = glob_time["t_samples"]                 # input/
    load_vals = ["SIN", "COS", "TX1", "TY1", "r"]
    SIN, COS, TX1, TY1, r = [values.get(val) for val in load_vals]
    
    
    fig_samples[FIG] = 5./14*g*SIN*t_samples*t_samples
    
    
    # find the centre, knowing that it touches the ramp at (TX1,TY1)
    newX = TX1+r*SIN
    newY = TY1+r*COS
    # draw the sphere in blue
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # use the reference lines to find the current position of the lines
    RCOS = r*COS
    RSIN = r*SIN
    X1 = SphereXLines[0]*RCOS+SphereYLines*RSIN+newX
    X2 = SphereXLines[1]*RCOS+SphereYLines*RSIN+newX
    Y1 = -SphereXLines[0]*RSIN+SphereYLines*RCOS+newY
    Y2 = -SphereXLines[1]*RSIN+SphereYLines*RCOS+newY
    # draw the lines
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])


def createHollowSphere(FIG,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    t_samples      = glob_time["t_samples"]                 # input/
    load_vals = ["SIN", "COS", "TX1", "TY1", "r", "ri"]
    SIN, COS, TX1, TY1, r, ri = [values.get(val) for val in load_vals]
    
    #print("DBUG: r", r)
    #print("DBUG: ri", ri)
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        sphere_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        sphere_lines_data.data = dict(x=[],y=[])
        #print("DBUG: hhhhhhhhhhhhhspehre")
    else:
        
        ratio = ri/r
        k = 1.0 + 0.4*(1.0 - ratio**5)/(1.0 - ratio**3)
        
        fig_samples[FIG] =  0.5*(g/k)*SIN*t_samples*t_samples
        
        # find the centre, knowing that it touches the ramp at (TX1,TY1)
        newX = TX1+r*SIN
        newY = TY1+r*COS
        # draw the sphere in semi-transparent blue
        sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1-ri/r])
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
def createCylinder(FIG,cylinder_data, cylinder_lines_data,values):
    t_samples = glob_time["t_samples"] # input/
    load_vals = ["SIN", "COS", "TX1", "TY1", "r"]
    SIN, COS, TX1, TY1, r = [values.get(val) for val in load_vals]
    
    fig_samples[FIG] =  (g/3.0)*SIN*t_samples*t_samples
    
    # draw the cylinder around the centre, knowing that it touches the ramp at (TX1,TY1)
    cylinder_data.data=dict(x=[TX1+r*SIN],y=[TY1+r*COS],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[TX1,TX1+2*r*SIN],
        [TX1+r*(SIN-COS),TX1+r*(SIN+COS)]],
        y=[[TY1,TY1+2*r*COS],[TY1+r*(COS+SIN),TY1+r*(COS-SIN)]])


def createHollowCylinder(FIG,hollowCylinder_data, hollowCylinder_lines_data,values):
    t_samples = glob_time["t_samples"] # input/
    load_vals = ["SIN", "COS", "TX1", "TY1", "r", "ri"]
    SIN, COS, TX1, TY1, r, ri = [values.get(val) for val in load_vals]
    
    if (abs(r-ri)<1e-5):
        # empty data if radius == inner radius (numerically)
        hollowCylinder_data.data       = dict(x=[],y=[],w=[],c=[],a=[])
        hollowCylinder_lines_data.data = dict(x=[],y=[])
    else:
        
        ratio = ri/r
        z = 3.0 + ratio*ratio
        fig_samples[FIG] =  (g/z)*SIN*t_samples*t_samples
        
        # draw the cylinder around the centre, knowing that it touches the ramp at (TX1,TY1)
        hollowCylinder_data.data=dict(x=[TX1+r*SIN,TX1+r*SIN],
            y=[TY1+r*COS,TY1+r*COS],w=[2*r,2*ri],c=["#0065BD","#FFFFFF"],a=[1,1])
        hollowCylinder_lines_data.data=dict(x=[[TX1,TX1+(r-ri)*SIN],
            [TX1+(r+ri)*SIN,TX1+2*r*SIN],
            [TX1+r*(SIN-COS),TX1+r*SIN-ri*COS],
            [TX1+r*(SIN+COS),TX1+r*SIN+ri*COS]],
            y=[[TY1,TY1+(r-ri)*COS],[TY1+(r+ri)*COS,TY1+2*r*COS],
            [TY1+r*(COS+SIN),TY1+r*COS+ri*SIN],
            [TY1+r*(COS-SIN),TY1+r*COS-ri*SIN]])
