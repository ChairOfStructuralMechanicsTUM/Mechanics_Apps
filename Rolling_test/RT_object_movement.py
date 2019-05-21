from __future__ import division # float division only, like in python 3
from math import sin, cos

from RT_global_variables import glob_SphereXLines, glob_SphereYLines, g


###############################################################################
###                            Sphere functions                             ###
###############################################################################
def moveSphere(t,r,m,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1"]
    alpha, SIN, COS, TX1, TY1 = [values.get(val) for val in load_vals]
    # find the displacement of the point touching the ramp
    displacement = g*SIN*t*t*1.25
    # actual formula (?): # displacement = g*SIN*t*t*5/14   ## 5/14 --> 5/4 --> 1.25
    #displacement = g*SIN*t*t*5./14 #- r   # -r due to its extension
    # find the rotation of the sphere
    rotation = -displacement/r
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


def moveHollowSphere(t,r,m,ri,sphere_data,sphere_lines_data,values):
    [SphereXLines] = glob_SphereXLines.data["SphereXLines"] # input/
    [SphereYLines] = glob_SphereYLines.data["SphereYLines"] # input/
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1"]
    alpha, SIN, COS, TX1, TY1 = [values.get(val) for val in load_vals]
    
    temp = r*g*SIN*t*t*1.25*(r**3-ri**3)/(r**5-ri**5)
    # actual formula (?): # temp = 5/14*r*g*SIN*t*t*(r**3-ri**3)/(r**5-ri**5)   ## 5/14 --> 5/4 --> 1.25
    #temp = 5./14*r*g*SIN*t*t*(r**3-ri**3)/(r**5-ri**5)
    # find the rotation of the sphere
    rotation = -temp
    # find the displacement of the point touching the ramp
    displacement = temp*r #- r   # -r due to its extension
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
def moveCylinder(t,r,m, cylinder_data, cylinder_lines_data,values):
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1"]
    alpha, SIN, COS, TX1, TY1 = [values.get(val) for val in load_vals]
    # find the displacement of the point touching the ramp
    displacement = g*SIN*t*t
    # actual formula (?): # displacement = g*SIN*t*t*1/3
    #displacement = (g*SIN*t*t)/3. #- r   # -r due to its extension
    # find the rotation of the cylinder
    rotation = -displacement/r
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


def moveHollowCylinder(t,r,m,ri,hollowCylinder_data,hollowCylinder_lines_data,values):
    load_vals = ["alpha", "SIN", "COS", "TX1", "TY1"]
    alpha, SIN, COS, TX1, TY1 = [values.get(val) for val in load_vals]
    
    temp = r*g*SIN*t*t/(r*r+ri*ri)
    # actual formula (?): # temp = 1*r*g*SIN*t*t/(3*r*r+ri*ri)
    #temp = r*g*SIN*t*t/(3.0*r*r+ri*ri)

    # find the rotation of the cylinder
    rotation = -temp
    # find the displacement of the point touching the ramp
    displacement = r*temp #- r   # -r due to its extension
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