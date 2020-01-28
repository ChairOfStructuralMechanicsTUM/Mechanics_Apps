import Mohr_Variables as Mvar
from math import sqrt, sin, cos, pi, atan



def changePlaneAngle(attr,old,new):
        
        [glMohrNx]               = Mvar.glob_MohrNx.data["val"]         # input/
        [glMohrNz]               = Mvar.glob_MohrNz.data["val"]         # input/
        [glMohrNxz]              = Mvar.glob_MohrNxz.data["val"]        # input/

        alpha = new
        glMohrP_Angle = -new*(pi/180)


        ## Paint Rotating Plane red if angle=alpha_0
        radius  = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
        centreX = float((glMohrNx+glMohrNz)/2)
        Mvar.rleft_x=centreX-radius
        alpha_0=180*atan(glMohrNxz/(glMohrNz+(-Mvar.rleft_x+0.00001)))/(pi)
        alpha_0=int(alpha_0+0.5)
        
        alpharepetitions = [-90, -180, 0, 90, 180]
        for n in alpharepetitions:
            if alpha == alpha_0+n:
                Mvar.Rotating_Plane_red_source.data = dict(x=[0], y=[0], angle =[-glMohrP_Angle], size = [75])
                Mvar.Rotating_Plane_source.data     = dict(x=[],  y=[],  angle =[],         size = []  )
                break
        else:
            Mvar.Rotating_Plane_source.data     = dict(x=[0], y=[0], angle =[-glMohrP_Angle], size = [75])
            Mvar.Rotating_Plane_red_source.data = dict(x=[],  y=[],  angle =[],         size = []  )

        # Figure 3, Rotate Axis:  
        glMohrP_Angle = -glMohrP_Angle
        Mvar.Rotating_Axis_X_source.data = dict(xS=[0], yS=[0], xE=[25*cos(glMohrP_Angle)],    yE=[25*sin(glMohrP_Angle)  ])
        Mvar.Rotating_Axis_Y_source.data = dict(xS=[0], yS=[0], xE=[-25*sin(-glMohrP_Angle)],  yE=[-25*cos(-glMohrP_Angle)])
        
        glMohrP_Angle = -glMohrP_Angle
        
        Mvar.glob_alpha.data       = dict(val=[alpha])         #      /output
        Mvar.glob_MohrP_Angle.data = dict(val=[glMohrP_Angle]) #      /output
        
        ChangeMohrCircle()
        ChangeRotatingPlane_Forces()


                 
def ChangeMohrCircle():
    
    [glMohrNx]      = Mvar.glob_MohrNx.data["val"]      # input/
    [glMohrNz]      = Mvar.glob_MohrNz.data["val"]      # input/
    [glMohrNxz]     = Mvar.glob_MohrNxz.data["val"]     # input/
    [glMohrP_Angle] = Mvar.glob_MohrP_Angle.data["val"] # input/
    
    radius       = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX      = float((glMohrNx+glMohrNz)/2)
    Mvar.rleft_z = 0
    Mvar.rleft_x = centreX-radius
    
    Mvar.Mohr_Circle_source.data        = dict(x=[centreX], y=[0], radius=[radius])   
    Mvar.OriginalPlane_line_source.data = dict(x=[Mvar.rleft_x,glMohrNz,glMohrNz], y=[Mvar.rleft_z,glMohrNxz,0])
  
    ## Calculate forces in rotated element
    Mvar.Nzeta     = float(((glMohrNx+glMohrNz)/2)+(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))+glMohrNxz*sin(2*glMohrP_Angle))
    Mvar.Neta      = float(((glMohrNx+glMohrNz)/2)-(((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-glMohrNxz*sin(2*glMohrP_Angle))
    Mvar.Nzetaeta  = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))

    if glMohrP_Angle == 0:
        Mvar.Nzeta    = glMohrNx
        Mvar.Neta     = glMohrNz
        Mvar.Nzetaeta = glMohrNxz
    if glMohrP_Angle == (pi/2):
        Mvar.Nzeta    = glMohrNz
        Mvar.Neta     = glMohrNx
        Mvar.Nzetaeta = -glMohrNxz


    Mvar.Newplane_line_source.data       = dict(x=[Mvar.rleft_x,Mvar.Neta], y=[Mvar.rleft_z,Mvar.Nzetaeta])

    Mvar.Figure2Moving_Label_source.data = dict(x=[glMohrNx,glMohrNz,0.0, 0.0, Mvar.Neta,Mvar.Nzeta,glMohrNz,Mvar.Neta],
                                            y=[0.0,0.0,glMohrNxz, Mvar.Nzetaeta,0.0,0.0,glMohrNxz,Mvar.Nzetaeta],
                                            names=['\\sigma_x','\\sigma_z','\\tau_{xz}','\\tau_{\\overline{xz}}','\\sigma_{\\overline{z}}','\\sigma_{\\overline{x}}',"A","B"])
    
    Mvar.Figure3Moving_Label_source.data = dict(x=[(25+2.5)*cos(-glMohrP_Angle)-1,(-25-2.5)*sin(glMohrP_Angle)-1],y=[(25+2.5)*sin(-glMohrP_Angle)-1,(-25-2.5)*cos(glMohrP_Angle)-1], 
                                        names = ['\\overline{x}', '\\overline{z}'])


    
def ChangeRotatingPlane_Forces():
    
    [alpha]                   = Mvar.glob_alpha.data["val"]                 # input/
    [glMohrNx]                = Mvar.glob_MohrNx.data["val"]                # input/
    [glMohrNz]                = Mvar.glob_MohrNz.data["val"]                # input/
    [glMohrNxz]               = Mvar.glob_MohrNxz.data["val"]               # input/
    [glMohrP_Angle]           = Mvar.glob_MohrP_Angle.data["val"]           # input/output
    [glMohrNzeta_zero_angles] = Mvar.glob_MohrNzeta_zero_angles.data["val"] # input/
    [glMohrNeta_zero_angles]  = Mvar.glob_MohrNeta_zero_angles.data["val"]  # input/
    Mvar.Nzeta    = float(float((glMohrNx+glMohrNz)/2)+(float((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))+float(glMohrNxz*sin(2*glMohrP_Angle)))
    Mvar.Neta     = float(float((glMohrNx+glMohrNz)/2)-(float((glMohrNx-glMohrNz)/2)*cos(2*glMohrP_Angle))-float(glMohrNxz*sin(2*glMohrP_Angle)))
    Mvar.Nzetaeta = float((-(((glMohrNx-glMohrNz)/2)*sin(2*glMohrP_Angle)))+glMohrNxz*cos(2*glMohrP_Angle))
   
    glMohrP_Angle = -glMohrP_Angle

    ## Set Mvar.Nzetaeta=0 if angle-slider is set to principal direction
    radius       = float(sqrt(pow(((glMohrNx-glMohrNz)/2),2)+pow(glMohrNxz,2)))
    centreX      = float((glMohrNx+glMohrNz)/2)
    Mvar.rleft_x = centreX-radius

    alpha_0 = 180*atan(glMohrNxz/(glMohrNz+(-Mvar.rleft_x+0.00001)))/(pi)
    alpha_0 = int(alpha_0+0.5)

    alpharepetitions = [-90, -180, 0, 90, 180]
    for n in alpharepetitions:
        if alpha == alpha_0+n:
            Mvar.Nzetaeta=0         
            break
    ## Set Mvar.Nzeta = 0 if alpha equals value in list glMohrNzeta_zero_angles
    for m in glMohrNzeta_zero_angles: 
        if alpha == m:
            Mvar.Nzeta = 0
            break
    ## Set Mvar.Neta = 0 if alpha equals value in list glMohrNeta_zero_angles
    for m in glMohrNeta_zero_angles: 
        if alpha == m:
            Mvar.Neta = 0
            break


    Mvar.Nzeta = 0.75*Mvar.Nzeta
    if Mvar.Nzeta>0:
        #Mvar.NzetaP_arrow_source.data = dict(xS=[12.5*cos(glMohrP_Angle)],  xE=[(12.5+Mvar.Nzeta)*cos(glMohrP_Angle)],  yS=[(12.5*sin(glMohrP_Angle))],   yE=[(((12.5+Mvar.Nzeta)*sin(glMohrP_Angle)))],   lW = [2])
        #Mvar.NzetaN_arrow_source.data = dict(xS=[-12.5*cos(glMohrP_Angle)], xE=[(-12.5-Mvar.Nzeta)*cos(glMohrP_Angle)], yS=[0-(12.5*sin(glMohrP_Angle))], yE=[(0-((12.5+Mvar.Nzeta)*sin(glMohrP_Angle)))], lW = [2])

        Mvar.NzetaP_arrow_source.stream(dict(xS=[12.5*cos(glMohrP_Angle)],  xE=[(12.5+Mvar.Nzeta)*cos(glMohrP_Angle)],  yS=[(12.5*sin(glMohrP_Angle))],   yE=[(((12.5+Mvar.Nzeta)*sin(glMohrP_Angle)))],   lW = [2]), rollover=-1)
        Mvar.NzetaN_arrow_source.stream(dict(xS=[-12.5*cos(glMohrP_Angle)], xE=[(-12.5-Mvar.Nzeta)*cos(glMohrP_Angle)], yS=[0-(12.5*sin(glMohrP_Angle))], yE=[(0-((12.5+Mvar.Nzeta)*sin(glMohrP_Angle)))], lW = [2]), rollover=-1)    
        
        Mvar.NzetaP_rect_source.data  = dict(x=[(12.5*cos(glMohrP_Angle)+(12.5+Mvar.Nzeta)*cos(glMohrP_Angle))/2],   y=[((12.5*sin(glMohrP_Angle))+(((12.5+Mvar.Nzeta)*sin(glMohrP_Angle))))/2],   w=[Mvar.Nzeta+1.5], h = [13], angle=[glMohrP_Angle])
        Mvar.NzetaN_rect_source.data  = dict(x=[(-12.5*cos(glMohrP_Angle)+(-12.5-Mvar.Nzeta)*cos(glMohrP_Angle))/2], y=[((-12.5*sin(glMohrP_Angle))+(-((12.5+Mvar.Nzeta)*sin(glMohrP_Angle))))/2], w=[Mvar.Nzeta+1.5], h = [13], angle=[glMohrP_Angle])
       

        

    elif Mvar.Nzeta==0:
        #Mvar.NzetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.NzetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        Mvar.NzetaP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
        Mvar.NzetaN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)       
        Mvar.NzetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.NzetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        #Mvar.NzetaP_arrow_source.data = dict(xS=[(12.5-Mvar.Nzeta)*cos(glMohrP_Angle)],  xE=[12.5*cos(glMohrP_Angle)],   yS=[0+((12.5-Mvar.Nzeta)*sin(glMohrP_Angle))],   yE=[0+(12.5*sin(glMohrP_Angle))], lW = [2])
        #Mvar.NzetaN_arrow_source.data = dict(xS=[(-12.5+Mvar.Nzeta)*cos(glMohrP_Angle)], xE=[-12.5 *cos(glMohrP_Angle)], yS=[(0-((12.5-Mvar.Nzeta)*sin(glMohrP_Angle)))], yE=[0-(12.5*sin(glMohrP_Angle))], lW = [2])
        
        Mvar.NzetaP_arrow_source.stream(dict(xS=[(12.5-Mvar.Nzeta)*cos(glMohrP_Angle)],  xE=[12.5*cos(glMohrP_Angle)],   yS=[0+((12.5-Mvar.Nzeta)*sin(glMohrP_Angle))],   yE=[0+(12.5*sin(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.NzetaN_arrow_source.stream(dict(xS=[(-12.5+Mvar.Nzeta)*cos(glMohrP_Angle)], xE=[-12.5 *cos(glMohrP_Angle)], yS=[(0-((12.5-Mvar.Nzeta)*sin(glMohrP_Angle)))], yE=[0-(12.5*sin(glMohrP_Angle))], lW = [2]), rollover=-1)
        
        Mvar.NzetaP_rect_source.data  = dict(x=[(12.5*cos(glMohrP_Angle)+(12.5-Mvar.Nzeta)*cos(glMohrP_Angle))/2],   y=[((12.5*sin(glMohrP_Angle))+(((12.5-Mvar.Nzeta)*sin(glMohrP_Angle))))/2],   w=[Mvar.Nzeta-1.5], h = [13], angle=[glMohrP_Angle])
        Mvar.NzetaN_rect_source.data  = dict(x=[(-12.5*cos(glMohrP_Angle)+(-12.5+Mvar.Nzeta)*cos(glMohrP_Angle))/2], y=[((-12.5*sin(glMohrP_Angle))+(-((12.5-Mvar.Nzeta)*sin(glMohrP_Angle))))/2], w=[Mvar.Nzeta-1.5], h = [13], angle=[glMohrP_Angle])

    Mvar.Neta = 0.75*Mvar.Neta
    if Mvar.Neta>0:
        #Mvar.NetaP_arrow_source.data = dict(xS=[12.5*cos((pi/2)+glMohrP_Angle)], xE=[(12.5+Mvar.Neta)*cos((pi/2)+glMohrP_Angle)], yS=[(12.5*sin((pi/2)+glMohrP_Angle))], yE=[((12.5+Mvar.Neta)*sin((pi/2)+glMohrP_Angle))], lW = [2])
        #Mvar.NetaN_arrow_source.data = dict(xS=[12.5*sin(glMohrP_Angle)],        xE=[(12.5+Mvar.Neta)*sin(glMohrP_Angle)],        yS=[-(12.5*cos(glMohrP_Angle))],       yE=[-((12.5+Mvar.Neta)*cos(glMohrP_Angle))],       lW = [2]) 

        Mvar.NetaP_arrow_source.stream(dict(xS=[12.5*cos((pi/2)+glMohrP_Angle)], xE=[(12.5+Mvar.Neta)*cos((pi/2)+glMohrP_Angle)], yS=[(12.5*sin((pi/2)+glMohrP_Angle))], yE=[((12.5+Mvar.Neta)*sin((pi/2)+glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.NetaN_arrow_source.stream(dict(xS=[12.5*sin(glMohrP_Angle)],        xE=[(12.5+Mvar.Neta)*sin(glMohrP_Angle)],        yS=[-(12.5*cos(glMohrP_Angle))],       yE=[-((12.5+Mvar.Neta)*cos(glMohrP_Angle))],       lW = [2]), rollover=-1)        
       
        Mvar.NetaP_rect_source.data  = dict(x=[(12.5*cos((pi/2)+glMohrP_Angle)+(12.5+Mvar.Neta)*cos((pi/2)+glMohrP_Angle))/2], y=[((12.5*sin((pi/2)+glMohrP_Angle))+((12.5+Mvar.Neta)*sin((pi/2)+glMohrP_Angle)))/2], h=[Mvar.Neta+1.5], w = [13], angle=[glMohrP_Angle])
        Mvar.NetaN_rect_source.data  = dict(x=[(12.5*sin(glMohrP_Angle)+(12.5+Mvar.Neta)*sin(glMohrP_Angle))/2],               y=[(-(12.5*cos(glMohrP_Angle))+-((12.5+Mvar.Neta)*cos(glMohrP_Angle)))/2],             h=[Mvar.Neta+1.5], w = [13], angle=[glMohrP_Angle])

    elif Mvar.Neta==0:
        #Mvar.NetaP_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.NetaN_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])

        Mvar.NetaP_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []), rollover=-1)
        Mvar.NetaN_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []), rollover=-1)

        Mvar.NetaP_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.NetaN_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])

    else:
        Mvar.NetaP_arrow_source.stream(dict(xS=[(12.5-Mvar.Neta)*cos((pi/2)+glMohrP_Angle)],xE=[12.5*cos((pi/2)+glMohrP_Angle)], yS=[((12.5-Mvar.Neta)*sin((pi/2)+glMohrP_Angle))], yE=[0+(12.5*sin((pi/2)+glMohrP_Angle))],  lW = [2]), rollover=-1)
        Mvar.NetaN_arrow_source.stream(dict(xS=[(12.5-Mvar.Neta)*sin(glMohrP_Angle)],xE=[12.5*sin(glMohrP_Angle)],               yS=[-(12.5-Mvar.Neta)*cos(glMohrP_Angle)],         yE=[-12.5*cos(glMohrP_Angle)],            lW = [2]), rollover=-1)      
        
        Mvar.NetaP_rect_source.data  = dict(x=[((12.5-Mvar.Neta)*cos((pi/2)+glMohrP_Angle)+12.5*cos((pi/2)+glMohrP_Angle))/2], y=[(((12.5-Mvar.Neta)*sin((pi/2)+glMohrP_Angle))+0+(12.5*sin((pi/2)+glMohrP_Angle)))/2], h=[Mvar.Neta-1.5], w = [13], angle=[glMohrP_Angle])
        Mvar.NetaN_rect_source.data  = dict(x=[((12.5-Mvar.Neta)*sin(glMohrP_Angle)+12.5*sin(glMohrP_Angle))/2],               y=[(-(12.5-Mvar.Neta)*cos(glMohrP_Angle)+-12.5*cos(glMohrP_Angle))/2],                   h=[Mvar.Neta-1.5], w = [13], angle=[glMohrP_Angle])


    Mvar.Nzetaeta=0.75*Mvar.Nzetaeta
    if Mvar.Nzetaeta>0:
        Mvar.Nzetaeta1_arrow_source.stream(dict(xS=[9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))],  xE=[9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))],  yS=[(0+9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0+9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta2_arrow_source.stream(dict(xS=[-9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], xE=[-9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yS=[(0+9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0+9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta3_arrow_source.stream(dict(xS=[-9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], xE=[-9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yS=[(0-9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0-9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta4_arrow_source.stream(dict(xS=[9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))],  xE=[9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))],  yS=[(0-9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0-9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2]), rollover=-1)
        
        
        Mvar.Nzetaeta1_rect_source.data  = dict(x=[(9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2],   y=[((0+9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+(0+9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Mvar.Nzetaeta+.5], h = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+-9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], y=[((0+9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+(0+9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Mvar.Nzetaeta+.5], w = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))-9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2],  y=[((0-9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+(0-9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Mvar.Nzetaeta+.5], h = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta4_rect_source.data  = dict(x=[(9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2],   y=[((0-9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+(0-9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Mvar.Nzetaeta+.5], w = [13], angle=[glMohrP_Angle])

    elif Mvar.Nzetaeta==0:
        #Mvar.Nzetaeta1_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nzetaeta2_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nzetaeta3_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])
        #Mvar.Nzetaeta4_arrow_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW = [])

        Mvar.Nzetaeta1_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
        Mvar.Nzetaeta2_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
        Mvar.Nzetaeta3_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)
        Mvar.Nzetaeta4_arrow_source.stream(dict(xS=[], xE=[], yS=[], yE=[], lW = []),rollover=-1)

        Mvar.Nzetaeta1_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.Nzetaeta2_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.Nzetaeta3_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
        Mvar.Nzetaeta4_rect_source.data  = dict(x=[], y=[], w=[], h = [], angle=[])
       

    else:
        Mvar.Nzetaeta1_arrow_source.stream(dict(xS=[9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))],  xE=[9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))],  yS=[(0+9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0+9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta2_arrow_source.stream(dict(xS=[-9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], xE=[-9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yS=[(0+9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0+9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta3_arrow_source.stream(dict(xS=[-9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], xE=[-9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yS=[(0-9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], yE=[(0-9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))], lW = [2]), rollover=-1)
        Mvar.Nzetaeta4_arrow_source.stream(dict(xS=[9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))],  xE=[9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))],  yS=[(0-9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], yE=[(0-9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))], lW = [2]), rollover=-1)

        Mvar.Nzetaeta1_rect_source.data  = dict(x=[(9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2],   y=[((0+9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+(0+9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Mvar.Nzetaeta-.5], h = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+-9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], y=[((0+9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+(0+9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Mvar.Nzetaeta-.5], w = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(glMohrP_Angle)-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))-9*cos(glMohrP_Angle)+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2],  y=[((0-9*sin(glMohrP_Angle))+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+(0-9*sin(glMohrP_Angle))-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2], w=[0.3*Mvar.Nzetaeta-.5], h = [13], angle=[glMohrP_Angle])
        Mvar.Nzetaeta4_rect_source.data  = dict(x=[(9*sin(glMohrP_Angle)+((Mvar.Nzetaeta/2)*cos(glMohrP_Angle))+9*sin(glMohrP_Angle)-((Mvar.Nzetaeta/2)*cos(glMohrP_Angle)))/2],   y=[((0-9*cos(glMohrP_Angle))+((Mvar.Nzetaeta/2)*sin(glMohrP_Angle))+(0-9*cos(glMohrP_Angle))-((Mvar.Nzetaeta/2)*sin(glMohrP_Angle)))/2], h=[0.3*Mvar.Nzetaeta-.5], w = [13], angle=[glMohrP_Angle])

    glMohrP_Angle = -glMohrP_Angle
    Mvar.glob_MohrP_Angle.data = dict(val=[glMohrP_Angle])