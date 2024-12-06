from __future__ import division # float division only, like in python 3
from math import sin, cos

from RT_global_variables import glob_SphereXLines, glob_SphereYLines, fig_samples


###############################################################################
###                            Sphere functions                             ###
###############################################################################
def moveSphere(FIG,t,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1", "r"]
    alpha, SIN, COS, TX1, TY1, r = [values.get(val) for val in load_vals]
    
    # find the displacement of the point touching the ramp
    displacement = fig_samples[FIG][t]
    # find the rotation of the sphere
    rotation     = -displacement/r
    # find the new centre of the sphere
    newX = TX1 + displacement*COS + r*SIN
    newY = TY1 - displacement*SIN + r*COS
    
    # update the drawing
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    # find the new positions of the guidelines from the reference sphere
    cosAngle = r*cos(alpha-rotation)
    sinAngle = r*sin(alpha-rotation)
    X1 = SphereXLines[0]*cosAngle+SphereYLines*sinAngle+newX
    X2 = SphereXLines[1]*cosAngle+SphereYLines*sinAngle+newX
    Y1 = -SphereXLines[0]*sinAngle+SphereYLines*cosAngle+newY
    Y2 = -SphereXLines[1]*sinAngle+SphereYLines*cosAngle+newY
    
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)


def moveHollowSphere(FIG,t,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1", "r", "ri"]
    alpha, SIN, COS, TX1, TY1, r, ri = [values.get(val) for val in load_vals]
    
    # find the displacement of the point touching the ramp
    displacement = fig_samples[FIG][t]
    # find the rotation of the sphere
    rotation     = -displacement/r
    
    # find the new centre of the sphere
    newX = TX1 + displacement*COS + r*SIN
    newY = TY1 - displacement*SIN + r*COS
    # update the drawing
    sphere_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1-ri/r])
    # find the new positions of the guidelines from the reference sphere
    cosAngle = r*cos(alpha-rotation)
    sinAngle = r*sin(alpha-rotation)
    X1 = SphereXLines[0]*cosAngle+SphereYLines*sinAngle+newX
    X2 = SphereXLines[1]*cosAngle+SphereYLines*sinAngle+newX
    Y1 = -SphereXLines[0]*sinAngle+SphereYLines*cosAngle+newY
    Y2 = -SphereXLines[1]*sinAngle+SphereYLines*cosAngle+newY
    sphere_lines_data.data=dict(x=[X1, X2],y=[Y1,Y2])
    return (newX,newY)


###############################################################################
###                           Cylinder functions                            ###
###############################################################################
def moveCylinder(FIG,t,cylinder_data, cylinder_lines_data,values):
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1", "r"]
    alpha, SIN, COS, TX1, TY1, r = [values.get(val) for val in load_vals]
    
    # find the displacement of the point touching the ramp
    displacement = fig_samples[FIG][t]
    # find the rotation of the cylinder
    rotation     = -displacement/r
    
    # find the new centre of the cylinder
    newX      = TX1 + displacement*COS + r*SIN
    newY      = TY1 - displacement*SIN + r*COS
    cosRAngle = r*cos(alpha-rotation)
    sinRAngle = r*sin(alpha-rotation)
    # update the drawing
    cylinder_data.data=dict(x=[newX],y=[newY],w=[2*r],c=["#0065BD"],a=[1])
    cylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX-cosRAngle],
        [newX+sinRAngle,newX-sinRAngle]],
        y=[[newY-sinRAngle,newY+sinRAngle],
        [newY+cosRAngle,newY-cosRAngle]])
    return (newX,newY)


def moveHollowCylinder(FIG,t,hollowCylinder_data,hollowCylinder_lines_data,values):
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1", "r", "ri"]
    alpha, SIN, COS, TX1, TY1, r, ri = [values.get(val) for val in load_vals]
    
    # find the displacement of the point touching the ramp
    displacement = fig_samples[FIG][t]
    # find the rotation of the cylinder
    rotation     = -displacement/r
    
    # constants used multiple times calculated in advance to reduce computation time
    cosAR      = cos(alpha-rotation)
    sinAR      = sin(alpha-rotation)
    cosRAngle  = r*cosAR
    cosRIAngle = ri*cosAR
    sinRAngle  = r*sinAR
    sinRIAngle = ri*sinAR
    # find the new centre of the cylinder
    newX = TX1 + displacement*COS + r*SIN
    newY = TY1 - displacement*SIN + r*COS
    # update the drawing
    hollowCylinder_data.data=dict(x=[newX,newX],
        y=[newY,newY],w=[2*r,2*ri],c=["#0065BD","#FFFFFF"],a=[1,1])
    hollowCylinder_lines_data.data=dict(x=[[newX+cosRAngle,newX+cosRIAngle],
        [newX-cosRAngle,newX-cosRIAngle],
        [newX+sinRAngle,newX+sinRIAngle],
        [newX-sinRAngle,newX-sinRIAngle]],
        y=[[newY-sinRAngle,newY-sinRIAngle],
        [newY+sinRAngle,newY+sinRIAngle],
        [newY+cosRAngle,newY+cosRIAngle],
        [newY-cosRAngle,newY-cosRIAngle]])
    return (newX,newY)