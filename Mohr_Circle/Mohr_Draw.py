import Mohr_Variables as Mvar
from math import sqrt, sin, cos, pi
from Mohr_ChangeFunctions import ChangeRotatingPlane_Forces, ChangeMohrCircle


def draw():

    Mvar.glob_MohrChangeShow.data = dict(val=[1])                   #      /output
    [glMohrNx]               = Mvar.glob_MohrNx.data["val"]         # input/
    [glMohrNz]               = Mvar.glob_MohrNz.data["val"]         # input/
    [glMohrNxz]              = Mvar.glob_MohrNxz.data["val"]        # input/
    [glMohrP_Angle]          = Mvar.glob_MohrP_Angle.data["val"]    # input/

    ## Calculations
    radius         = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX        = float((glMohrNx+glMohrNz)/2)
    Mvar.Neta      = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-glMohrNxz*sin(2*glMohrP_Angle))
    Mvar.Nzetaeta  = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))

    ## Calculate Angle for which Mvar.Nzeta or Mvar.Neta will be zero (sign-change-method):
    Mvar.Nzeta_List0 = [181]*360
    Mvar.Nzeta_List1 = [181]*360
    glMohrNzeta_zero_angles = [181]*360
    Mvar.glob_MohrNzeta_zero_angles.data = dict(val=[glMohrNzeta_zero_angles]) #      /output
    Mvar.Neta_List0 = [181]*360
    Mvar.Neta_List1 = [181]*360
    glMohrNeta_zero_angles = [181]*360
    Mvar.glob_MohrNeta_zero_angles.data = dict(val=[glMohrNeta_zero_angles]) #      /output

    ## Mvar.Nzeta:
    for n in range(-180,180):
        Mvar.Nzeta_List0[n+180] = float(((glMohrNx+glMohrNz)/2)+(((glMohrNx-glMohrNz)/2)*cos(2*-n*pi/180))+glMohrNxz*sin(2*-n*pi/180))
        Mvar.Nzeta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if Mvar.Nzeta_List0[m+180]*Mvar.Nzeta_List0[m+181]<0:
            glMohrNzeta_zero_angles[count] = Mvar.Nzeta_List1[m+180]
            count = count+1
    ## Mvar.Neta:
    for n in range(-180,180):
        Mvar.Neta_List0[n+180] = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*-n*pi/180))-glMohrNxz*sin(2*-n*pi/180))
        Mvar.Neta_List1[n+180] = n
    count = 0
    for m in range(-180,179):
        if Mvar.Neta_List0[m+180]*Mvar.Neta_List0[m+181]<0:
            glMohrNeta_zero_angles[count] = Mvar.Neta_List1[m+180]
            count = count+1


    ##Figure 1, Draw glMohrNx and keep it until reset() ist called:
    
    if(glMohrNx*0.75<0):
        #Mvar.NxP_arrow_source.data = dict(xS=[12.5-glMohrNx*0.75],  xE=[12.5],  yS=[0], yE=[0], lW = [2])
        #Mvar.NxN_arrow_source.data = dict(xS=[-12.5+glMohrNx*0.75], xE=[-12.5], yS=[0], yE=[0], lW = [2]) 
        Mvar.NxP_arrow_source.stream(dict(xS=[12.5-glMohrNx*0.75],  xE=[12.5],  yS=[0], yE=[0], lW = [2]),rollover=1)
        Mvar.NxN_arrow_source.stream(dict(xS=[-12.5+glMohrNx*0.75], xE=[-12.5], yS=[0], yE=[0], lW = [2]),rollover=1)

        Mvar.NxP_rect_source.data  = dict(x=[(25-glMohrNx*0.75)/2],  y=[0], w=[glMohrNx*0.75-1.5], h = [13], angle=[0])
        Mvar.NxN_rect_source.data  = dict(x=[(-25+glMohrNx*0.75)/2], y=[0], w=[glMohrNx*0.75-1.5], h = [13], angle=[0])
        
    elif(glMohrNx*0.75==0):
        #Mvar.NxP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.NxN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Mvar.NxP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.NxN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)

        Mvar.NxP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.NxN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        #Mvar.NxP_arrow_source.data = dict(xS=[12.5],  xE=[12.5+glMohrNx*0.75],  yS=[0], yE=[0], lW = [2])
        #Mvar.NxN_arrow_source.data = dict(xS=[-12.5], xE=[-12.5-glMohrNx*0.75], yS=[0], yE=[0], lW = [2])
        Mvar.NxP_arrow_source.stream(dict(xS=[12.5],  xE=[12.5+glMohrNx*0.75],  yS=[0], yE=[0], lW = [2]),rollover=1)
        Mvar.NxN_arrow_source.stream(dict(xS=[-12.5], xE=[-12.5-glMohrNx*0.75], yS=[0], yE=[0], lW = [2]),rollover=1)
        Mvar.NxP_rect_source.data  = dict(x=[(25+glMohrNx*0.75)/2],  y=[0], w=[glMohrNx*0.75+1.5], h = [13], angle=[0])        
        Mvar.NxN_rect_source.data  = dict(x=[(-25-glMohrNx*0.75)/2], y=[0], w=[glMohrNx*0.75+1.5], h = [13], angle=[0])  
    

    ##Figure 1, Draw glMohrNz and keep it until reset() ist called:
    new = glMohrNz
    new = new*0.75
    if(new<0):
        #Mvar.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2])
        #Mvar.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2])
        Mvar.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5-new],  yE=[12.5],  lW = [2]),rollover=1)
        Mvar.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5+new], yE=[-12.5], lW = [2]),rollover=1)
        Mvar.NzP_rect_source.data  = dict(x=[0], y=[(25-new)/2],  w=[13], h = [new-1.5], angle=[0])
        Mvar.NzN_rect_source.data  = dict(x=[0], y=[(-25+new)/2], w=[13], h = [new-1.5], angle=[0])   
    elif (new==0):
        #Mvar.NzP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.NzN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Mvar.NzP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.NzN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.NzP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.NzN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
    else:
        #Mvar.NzP_arrow_source.data = dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new], lW = [2])
        #Mvar.NzN_arrow_source.data = dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2])
        Mvar.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+new], lW = [2]),rollover=1)
        Mvar.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-new], lW = [2]),rollover=1)
        Mvar.NzP_rect_source.data  = dict(x=[0], y=[(25+new)/2],  w=[13], h = [new+1.5], angle=[0])
        Mvar.NzN_rect_source.data  = dict(x=[0], y=[(-25-new)/2], w=[13], h = [new+1.5], angle=[0])   
         
          
    new = glMohrNxz
    new = new*0.75        
    if(new==0):
        #Mvar.Nxz1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nxz2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nxz3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nxz4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = []) 
        Mvar.Nxz1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.Nxz2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.Nxz3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)
        Mvar.Nxz4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=1)   
         
        Mvar.Nxz1_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Mvar.Nxz2_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Mvar.Nxz3_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
        Mvar.Nxz4_rect_source.data  = dict(x=[], y=[], w=[], h=[], angle=[])
    else:     
        #Mvar.Nxz1_arrow_source.data = dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2])
        #Mvar.Nxz2_arrow_source.data = dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2])
        #Mvar.Nxz3_arrow_source.data = dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2])
        #Mvar.Nxz4_arrow_source.data = dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]) 

        Mvar.Nxz1_arrow_source.stream(dict(xS=[9],       xE=[9],        yS=[0-(new/2)], yE=[0+(new/2)], lW = [2]),rollover=1)
        Mvar.Nxz2_arrow_source.stream(dict(xS=[-9],      xE=[-9],       yS=[0+(new/2)], yE=[0-(new/2)], lW = [2]),rollover=1)
        Mvar.Nxz3_arrow_source.stream(dict(xS=[-new/2],  xE=[new/2],    yS=[9],         yE=[9],         lW = [2]),rollover=1)
        Mvar.Nxz4_arrow_source.stream(dict(xS=[(new/2)], xE=[-(new/2)], yS=[-9],        yE=[-9],        lW = [2]),rollover=1)         
        Mvar.Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        Mvar.Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*new+0.5], h=[13],          angle=[0])
        Mvar.Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*new+0.5], angle=[0])
        Mvar.Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*new+0.5], angle=[0])


    ## Figure 2, draw Mohr-Circle:
    Mvar.Mohr_Circle_source.data = dict(x=[centreX], y=[0], radius=[radius])
    Mvar.Wedge_source.data       = dict(x=[], y=[],radius=[], sA=[], eA=[])

    Mvar.Newplane_line_source.data       = dict(x=[Mvar.rleft_x,Mvar.Neta,Mvar.Neta], y=[Mvar.rleft_z,Mvar.Nzetaeta,0])
    Mvar.OriginalPlane_line_source.data  = dict(x=[Mvar.rleft_x,glMohrNz,glMohrNz], y=[Mvar.rleft_z,glMohrNxz,0])
    Mvar.Figure2Show_Label_source.data   = dict(x=[],y=[], names =[])

    ## Figure 3, initializing:
    Mvar.Rotating_Plane_source.data = dict(x=[0], y=[0],angle =[-glMohrP_Angle],size = [75])

    Mvar.glob_MohrNeta_zero_angles.data  = dict(val=[glMohrNeta_zero_angles])  #       /output
    Mvar.glob_MohrNzeta_zero_angles.data = dict(val=[glMohrNzeta_zero_angles]) #       /output
    ChangeRotatingPlane_Forces()
    ChangeMohrCircle()

