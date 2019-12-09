from bokeh.models import ColumnDataSource

from MC_helper_functions import calculate_radius_and_center, clear_rect_source, clear_arrow_source

from math import pi,sqrt,pow,sin,cos,atan 


# define the sources for each figure here to avoid blasting the main code


class fig1():
    # initialize ColumnDataSources
    def __init__(self):
        # Arrows
        self.NxP_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NzP_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NxN_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NzN_arrow_source  = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nxz1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nxz2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nxz3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nxz4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

        # Rectangles
        self.NxP_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NzP_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NxN_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NzN_rect_source  = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nxz1_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nxz2_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nxz3_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nxz4_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))


        ### Labels
        self.Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))


    def plot_normal_forces_x(self, MohrNx):
        MohrNx = MohrNx*0.75
        if(MohrNx<0):
            self.NxP_arrow_source.stream(dict(xS=[12.5-MohrNx],  xE=[12.5],  yS=[0], yE=[0], lW = [2]),rollover=1)
            self.NxN_arrow_source.stream(dict(xS=[-12.5+MohrNx], xE=[-12.5], yS=[0], yE=[0], lW = [2]),rollover=1)
     
            self.NxP_rect_source.data  = dict(x=[(25-MohrNx)/2],  y=[0], w=[MohrNx-1.5], h = [13], angle=[0])
            self.NxN_rect_source.data  = dict(x=[(-25+MohrNx)/2], y=[0], w=[MohrNx-1.5], h = [13], angle=[0]) 
        elif(MohrNx==0):
            clear_arrow_source( [self.NxP_arrow_source, self.NxN_arrow_source] )
            clear_rect_source( [self.NxP_rect_source, self.NxN_rect_source] )
        else:
            self.NxP_arrow_source.stream(dict(xS=[12.5],  xE=[12.5+MohrNx],  yS=[0], yE=[0], lW = [2]),rollover=1)
            self.NxN_arrow_source.stream(dict(xS=[-12.5], xE=[-12.5-MohrNx], yS=[0], yE=[0], lW = [2]),rollover=1)
 
            self.NxP_rect_source.data   = dict(x=[(25+MohrNx)/2],  y=[0], w=[MohrNx+1.5], h = [13], angle=[0])        
            self.NxN_rect_source.data   = dict(x=[(-25-MohrNx)/2], y=[0], w=[MohrNx+1.5], h = [13], angle=[0]) 


    def plot_normal_forces_z(self, MohrNz):
        MohrNz=MohrNz*0.75
        if(MohrNz<0):
            self.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5-MohrNz],  yE=[12.5],  lW = [2]),rollover=1)
            self.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5+MohrNz], yE=[-12.5], lW = [2]),rollover=1)
            self.NzP_rect_source.data  = dict(x=[0], y=[(25-MohrNz)/2],  w=[13], h = [MohrNz-1.5], angle=[0])
            self.NzN_rect_source.data  = dict(x=[0], y=[(-25+MohrNz)/2], w=[13], h = [MohrNz-1.5], angle=[0])   
        elif (MohrNz==0):
            clear_arrow_source( [self.NzP_arrow_source, self.NzN_arrow_source] )
            clear_rect_source( [self.NzP_rect_source, self.NzN_rect_source] )
        else:
            self.NzP_arrow_source.stream(dict(xS=[0], xE=[0], yS=[12.5],  yE=[12.5+MohrNz],  lW = [2]),rollover=1)
            self.NzN_arrow_source.stream(dict(xS=[0], xE=[0], yS=[-12.5], yE=[-12.5-MohrNz], lW = [2]),rollover=1)
            self.NzP_rect_source.data  = dict(x=[0], y=[(25+MohrNz)/2],  w=[13], h = [MohrNz+1.5], angle=[0])
            self.NzN_rect_source.data  = dict(x=[0], y=[(-25-MohrNz)/2], w=[13], h = [MohrNz+1.5], angle=[0])  


    def plot_shear_forces(self, MohrNxz):
        MohrNxz=MohrNxz*0.75
        if(MohrNxz==0):
            clear_arrow_source( [self.Nxz1_arrow_source, self.Nxz2_arrow_source, self.Nxz3_arrow_source, self.Nxz4_arrow_source] )    
            clear_rect_source( [self.Nxz1_rect_source, self.Nxz2_rect_source, self.Nxz3_rect_source, self.Nxz4_rect_source] )
        else:     
            self.Nxz1_arrow_source.stream(dict(xS=[9],       xE=[9],        yS=[0-(MohrNxz/2)], yE=[0+(MohrNxz/2)], lW = [2]),rollover=1)
            self.Nxz2_arrow_source.stream(dict(xS=[-9],      xE=[-9],       yS=[0+(MohrNxz/2)], yE=[0-(MohrNxz/2)], lW = [2]),rollover=1)
            self.Nxz3_arrow_source.stream(dict(xS=[-MohrNxz/2],  xE=[MohrNxz/2],    yS=[9],         yE=[9],         lW = [2]),rollover=1)
            self.Nxz4_arrow_source.stream(dict(xS=[(MohrNxz/2)], xE=[-(MohrNxz/2)], yS=[-9],        yE=[-9],        lW = [2]),rollover=1)
            self.Nxz1_rect_source.data  = dict(x=[9],  y=[0],  w=[0.3*MohrNxz+0.5], h=[13],          angle=[0])
            self.Nxz2_rect_source.data  = dict(x=[-9], y=[0],  w=[0.3*MohrNxz+0.5], h=[13],          angle=[0])
            self.Nxz3_rect_source.data  = dict(x=[0],  y=[9],  w=[13],          h=[0.3*MohrNxz+0.5], angle=[0])
            self.Nxz4_rect_source.data  = dict(x=[0],  y=[-9], w=[13],          h=[0.3*MohrNxz+0.5], angle=[0]) 




class fig2():
    # initialize ColumnDataSources
    def __init__(self):
        self.Mohr_Circle_source = ColumnDataSource(data=dict(x=[], y=[], radius=[]))
        self.Wedge_source       = ColumnDataSource(data=dict(x=[], y=[],radius=[], sA=[], eA=[]))
        self.Newplane_line_source      = ColumnDataSource(data=dict(x=[],y=[]))
        self.OriginalPlane_line_source = ColumnDataSource(data=dict(x=[],y=[]))

        ### Labels
        self.Perm_Label_source   = ColumnDataSource(data=dict(x=[23.5,1.5], y=[-2.5, 23], names=["\\sigma", "\\tau"]))
        self.Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names=[]))
        self.Show_Label_source   = ColumnDataSource(data=dict(x=[], y=[], names=[]))


    def ChangeMohrCircle(self,input_vars):
        MohrNx  = input_vars["MohrNx"]
        MohrNz  = input_vars["MohrNz"]
        MohrNxz = input_vars["MohrNxz"]
        MohrP_Angle = input_vars["MohrP_Angle"]

        [radius, centreX, rleft_x] = calculate_radius_and_center(input_vars)
        rleft_z = 0
        
        self.Mohr_Circle_source.data        = dict(x=[centreX], y=[0], radius=[radius])   
        self.OriginalPlane_line_source.data = dict(x=[rleft_x,MohrNz,MohrNz], y=[rleft_z,MohrNxz,0])
    
        ## Calculate forces in rotated element
        Nzeta     = float(((MohrNx+MohrNz)/2)+(((MohrNx-MohrNz)/2)*cos(2*MohrP_Angle))+MohrNxz*sin(2*MohrP_Angle))
        Neta      = float(((MohrNx+MohrNz)/2)-(((MohrNx-MohrNz)/2)*cos(2*MohrP_Angle))-MohrNxz*sin(2*MohrP_Angle))
        Nzetaeta  = float((-(((MohrNx-MohrNz)/2)*sin(2*MohrP_Angle)))+MohrNxz*cos(2*MohrP_Angle))

        if MohrP_Angle == 0:
            Nzeta    = MohrNx
            Neta     = MohrNz
            Nzetaeta = MohrNxz
        if MohrP_Angle == (pi/2):
            Nzeta    = MohrNz
            Neta     = MohrNx
            Nzetaeta = -MohrNxz

        self.Newplane_line_source.data       = dict(x=[rleft_x,Neta], y=[rleft_z,Nzetaeta])

        self.Moving_Label_source.data = dict(x=[MohrNx,MohrNz,0.0, 0.0, Neta,Nzeta,MohrNz,Neta],
                                                y=[0.0,0.0,MohrNxz, Nzetaeta,0.0,0.0,MohrNxz,Nzetaeta],
                                                names=['\\sigma_x','\\sigma_z','\\tau_{xz}','\\tau_{\\overline{xz}}','\\sigma_{\\overline{z}}','\\sigma_{\\overline{x}}',"A","B"])
        
        # self.Moving_Label_source.data = dict(x=[(25+2.5)*cos(-MohrP_Angle)-1,(-25-2.5)*sin(MohrP_Angle)-1],y=[(25+2.5)*sin(-MohrP_Angle)-1,(-25-2.5)*cos(MohrP_Angle)-1], 
        #                                     names = ['\\overline{x}', '\\overline{z}'])

        # print("in sources:",f2.Newplane_line_source)
        # print("in sources:",f2.Newplane_line_source)



    def reset_circle(self, centreX, radius, angle_label):
        self.Mohr_Circle_source.data          = dict(x=[centreX], y=[0], radius=[radius])
        self.Newplane_line_source.data        = dict(x=[], y=[])
        self.OriginalPlane_line_source.data   = dict(x=[], y=[])
        self.Moving_Label_source.data  = dict(x=[],y=[],names =[])
        self.Show_Label_source.data    = dict(x=[],y=[],names =[])
        self.Wedge_source.data                = dict(x=[], y=[],radius=[], sA=[], eA=[])
        angle_label.text = ''




class fig3():
    # initialize ColumnDataSources
    def __init__(self):
        ## Rotating plane: 
        self.Rotating_Plane_source     = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
        self.Rotating_Plane_red_source = ColumnDataSource(data=dict(x=[], y=[],angle = [],size =[]))
        ### Rotating Coordinate-System:
        self.Rotating_Axis_X_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
        self.Rotating_Axis_Y_source = ColumnDataSource(data=dict(xS=[], yS=[], xE=[], yE=[]))
        ## Arrows:
        self.NzetaP_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NzetaN_arrow_source    = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NetaP_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.NetaN_arrow_source     = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nzetaeta1_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nzetaeta2_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nzetaeta3_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.Nzetaeta4_arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        ## Rectangles:
        self.NzetaP_rect_source    = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NzetaN_rect_source    = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NetaP_rect_source     = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.NetaN_rect_source     = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nzetaeta1_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nzetaeta2_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nzetaeta3_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))
        self.Nzetaeta4_rect_source = ColumnDataSource(data=dict(x=[], y=[], w=[], h=[], angle=[]))

        ### Labels
        self.Perm_Label_source   = ColumnDataSource(data=dict(x=[22,1], y=[-5, -27], names=['x', 'z']))
        self.Moving_Label_source = ColumnDataSource(data=dict(x=[], y=[], names =[]))

    def reset_rotating_plane(self):
        self.Rotating_Axis_X_source.stream(dict(xS=[], yS=[], xE=[], yE=[]), rollover=-1) # arrow glyph
        self.Rotating_Axis_Y_source.stream(dict(xS=[], yS=[], xE=[], yE=[]), rollover=-1) # arrow glyph
        self.Moving_Label_source.data=dict(x=[], y=[], names =[])

        self.Rotating_Plane_source.data     = dict(x=[], y=[],angle =[],size = [])
        self.Rotating_Plane_red_source.data = dict(x=[], y=[],angle =[],size = [])


    def move_labels(self, MohrP_Angle):
        self.Moving_Label_source.data = dict(x=[(25+2.5)*cos(-MohrP_Angle)-1,(-25-2.5)*sin(MohrP_Angle)-1],y=[(25+2.5)*sin(-MohrP_Angle)-1,(-25-2.5)*cos(MohrP_Angle)-1], 
                                            names = ['\\overline{x}', '\\overline{z}'])


    def ChangeRotatingPlane_Forces(self, input_vars):
        MohrNx  = input_vars["MohrNx"]
        MohrNz  = input_vars["MohrNz"]
        MohrNxz = input_vars["MohrNxz"]
        MohrP_Angle = input_vars["MohrP_Angle"]

        Nzeta    = float(float((MohrNx+MohrNz)/2)+(float((MohrNx-MohrNz)/2)*cos(2*MohrP_Angle))+float(MohrNxz*sin(2*MohrP_Angle)))
        Neta     = float(float((MohrNx+MohrNz)/2)-(float((MohrNx-MohrNz)/2)*cos(2*MohrP_Angle))-float(MohrNxz*sin(2*MohrP_Angle)))
        Nzetaeta = float((-(((MohrNx-MohrNz)/2)*sin(2*MohrP_Angle)))+MohrNxz*cos(2*MohrP_Angle))
    
        MohrP_Angle = -MohrP_Angle

        ## Set Nzetaeta=0 if angle-slider is set to principal direction
        [radius, centreX, rleft_x] = calculate_radius_and_center(input_vars)

        alpha_0 = 180*atan(MohrNxz/(MohrNz+(-rleft_x+0.00001)))/(pi)
        alpha_0 = int(alpha_0+0.5)

        alpharepetitions = [-90, -180, 0, 90, 180]
        for n in alpharepetitions:
            if input_vars["alpha"] == alpha_0+n:
                Nzetaeta=0         
                break
        ## Set Nzeta = 0 if alpha equals value in list MohrNzeta_zero_angles
        for m in input_vars["MohrNzeta_zero_angles"]: 
            if input_vars["alpha"] == m:
                Nzeta = 0
                break
        ## Set Neta = 0 if alpha equals value in list MohrNeta_zero_angles
        for m in input_vars["MohrNeta_zero_angles"]: 
            if input_vars["alpha"] == m:
                Neta = 0
                break

        Nzeta = 0.75*Nzeta
        if Nzeta>0:
            self.NzetaP_arrow_source.stream(dict(xS=[12.5*cos(MohrP_Angle)],  xE=[(12.5+Nzeta)*cos(MohrP_Angle)],  yS=[(12.5*sin(MohrP_Angle))],   yE=[(((12.5+Nzeta)*sin(MohrP_Angle)))],   lW = [2]),rollover=1)
            self.NzetaN_arrow_source.stream(dict(xS=[-12.5*cos(MohrP_Angle)], xE=[(-12.5-Nzeta)*cos(MohrP_Angle)], yS=[0-(12.5*sin(MohrP_Angle))], yE=[(0-((12.5+Nzeta)*sin(MohrP_Angle)))], lW = [2]),rollover=1)
            self.NzetaP_rect_source.data  = dict(x=[(12.5*cos(MohrP_Angle)+(12.5+Nzeta)*cos(MohrP_Angle))/2],   y=[((12.5*sin(MohrP_Angle))+(((12.5+Nzeta)*sin(MohrP_Angle))))/2],   w=[Nzeta+1.5], h = [13], angle=[MohrP_Angle])
            self.NzetaN_rect_source.data  = dict(x=[(-12.5*cos(MohrP_Angle)+(-12.5-Nzeta)*cos(MohrP_Angle))/2], y=[((-12.5*sin(MohrP_Angle))+(-((12.5+Nzeta)*sin(MohrP_Angle))))/2], w=[Nzeta+1.5], h = [13], angle=[MohrP_Angle])

        elif Nzeta==0:
            clear_arrow_source( [self.NzetaP_arrow_source, self.NzetaN_arrow_source] )
            clear_rect_source( [self.NzetaP_rect_source, self.NzetaN_rect_source] )
        else:
            self.NzetaP_arrow_source.stream(dict(xS=[(12.5-Nzeta)*cos(MohrP_Angle)],  xE=[12.5*cos(MohrP_Angle)],   yS=[0+((12.5-Nzeta)*sin(MohrP_Angle))],   yE=[0+(12.5*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.NzetaN_arrow_source.stream(dict(xS=[(-12.5+Nzeta)*cos(MohrP_Angle)], xE=[-12.5 *cos(MohrP_Angle)], yS=[(0-((12.5-Nzeta)*sin(MohrP_Angle)))], yE=[0-(12.5*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.NzetaP_rect_source.data  = dict(x=[(12.5*cos(MohrP_Angle)+(12.5-Nzeta)*cos(MohrP_Angle))/2],   y=[((12.5*sin(MohrP_Angle))+(((12.5-Nzeta)*sin(MohrP_Angle))))/2],   w=[Nzeta-1.5], h = [13], angle=[MohrP_Angle])
            self.NzetaN_rect_source.data  = dict(x=[(-12.5*cos(MohrP_Angle)+(-12.5+Nzeta)*cos(MohrP_Angle))/2], y=[((-12.5*sin(MohrP_Angle))+(-((12.5-Nzeta)*sin(MohrP_Angle))))/2], w=[Nzeta-1.5], h = [13], angle=[MohrP_Angle])

        Neta = 0.75*Neta
        if Neta>0:
            self.NetaP_arrow_source.stream(dict(xS=[12.5*cos((pi/2)+MohrP_Angle)], xE=[(12.5+Neta)*cos((pi/2)+MohrP_Angle)], yS=[(12.5*sin((pi/2)+MohrP_Angle))], yE=[((12.5+Neta)*sin((pi/2)+MohrP_Angle))], lW = [2]),rollover=1)
            self.NetaN_arrow_source.stream(dict(xS=[12.5*sin(MohrP_Angle)],        xE=[(12.5+Neta)*sin(MohrP_Angle)],        yS=[-(12.5*cos(MohrP_Angle))],       yE=[-((12.5+Neta)*cos(MohrP_Angle))],       lW = [2]),rollover=1)
            self.NetaP_rect_source.data  = dict(x=[(12.5*cos((pi/2)+MohrP_Angle)+(12.5+Neta)*cos((pi/2)+MohrP_Angle))/2], y=[((12.5*sin((pi/2)+MohrP_Angle))+((12.5+Neta)*sin((pi/2)+MohrP_Angle)))/2], h=[Neta+1.5], w = [13], angle=[MohrP_Angle])
            self.NetaN_rect_source.data  = dict(x=[(12.5*sin(MohrP_Angle)+(12.5+Neta)*sin(MohrP_Angle))/2],               y=[(-(12.5*cos(MohrP_Angle))+-((12.5+Neta)*cos(MohrP_Angle)))/2],             h=[Neta+1.5], w = [13], angle=[MohrP_Angle])

        elif Neta==0:
            clear_arrow_source( [self.NetaP_arrow_source, self.NetaN_arrow_source] )
            clear_rect_source( [self.NetaP_rect_source, self.NetaN_rect_source] )
        else:
            self.NetaP_arrow_source.stream(dict(xS=[(12.5-Neta)*cos((pi/2)+MohrP_Angle)],xE=[12.5*cos((pi/2)+MohrP_Angle)], yS=[((12.5-Neta)*sin((pi/2)+MohrP_Angle))], yE=[0+(12.5*sin((pi/2)+MohrP_Angle))],  lW = [2]),rollover=1)
            self.NetaN_arrow_source.stream(dict(xS=[(12.5-Neta)*sin(MohrP_Angle)],xE=[12.5*sin(MohrP_Angle)],               yS=[-(12.5-Neta)*cos(MohrP_Angle)],         yE=[-12.5*cos(MohrP_Angle)],            lW = [2]),rollover=1)
            self.NetaP_rect_source.data  = dict(x=[((12.5-Neta)*cos((pi/2)+MohrP_Angle)+12.5*cos((pi/2)+MohrP_Angle))/2], y=[(((12.5-Neta)*sin((pi/2)+MohrP_Angle))+0+(12.5*sin((pi/2)+MohrP_Angle)))/2], h=[Neta-1.5], w = [13], angle=[MohrP_Angle])
            self.NetaN_rect_source.data  = dict(x=[((12.5-Neta)*sin(MohrP_Angle)+12.5*sin(MohrP_Angle))/2],               y=[(-(12.5-Neta)*cos(MohrP_Angle)+-12.5*cos(MohrP_Angle))/2],                   h=[Neta-1.5], w = [13], angle=[MohrP_Angle])

        Nzetaeta=0.75*Nzetaeta
        if Nzetaeta>0:
            self.Nzetaeta1_arrow_source.stream(dict(xS=[9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))],  xE=[9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))],  yS=[(0+9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))], yE=[(0+9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta2_arrow_source.stream(dict(xS=[-9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))], xE=[-9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))], yS=[(0+9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))], yE=[(0+9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta3_arrow_source.stream(dict(xS=[-9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))], xE=[-9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))], yS=[(0-9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))], yE=[(0-9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta4_arrow_source.stream(dict(xS=[9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))],  xE=[9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))],  yS=[(0-9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))], yE=[(0-9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta1_rect_source.data  = dict(x=[(9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))+9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle)))/2],   y=[((0+9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))+(0+9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[MohrP_Angle])
            self.Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))+-9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle)))/2], y=[((0+9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))+(0+9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[MohrP_Angle])
            self.Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))-9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle)))/2],  y=[((0-9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))+(0-9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle)))/2], w=[0.3*Nzetaeta+.5], h = [13], angle=[MohrP_Angle])
            self.Nzetaeta4_rect_source.data  = dict(x=[(9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))+9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle)))/2],   y=[((0-9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))+(0-9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle)))/2], h=[0.3*Nzetaeta+.5], w = [13], angle=[MohrP_Angle])
        elif Nzetaeta==0:
            clear_arrow_source( [self.Nzetaeta1_arrow_source, self.Nzetaeta2_arrow_source, self.Nzetaeta3_arrow_source, self.Nzetaeta4_arrow_source] )
            clear_rect_source( [self.Nzetaeta1_rect_source, self.Nzetaeta2_rect_source, self.Nzetaeta3_rect_source, self.Nzetaeta4_rect_source] )
        else:
            self.Nzetaeta1_arrow_source.stream(dict(xS=[9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))],  xE=[9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))],  yS=[(0+9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))], yE=[(0+9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta2_arrow_source.stream(dict(xS=[-9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))], xE=[-9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))], yS=[(0+9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))], yE=[(0+9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta3_arrow_source.stream(dict(xS=[-9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))], xE=[-9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))], yS=[(0-9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))], yE=[(0-9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta4_arrow_source.stream(dict(xS=[9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))],  xE=[9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))],  yS=[(0-9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))], yE=[(0-9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))], lW = [2]),rollover=1)
            self.Nzetaeta1_rect_source.data  = dict(x=[(9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle))+9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle)))/2],   y=[((0+9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle))+(0+9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[MohrP_Angle])
            self.Nzetaeta2_rect_source.data  = dict(x=[(-9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle))+-9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle)))/2], y=[((0+9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle))+(0+9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[MohrP_Angle])
            self.Nzetaeta3_rect_source.data  = dict(x=[(-9*cos(MohrP_Angle)-((Nzetaeta/2)*sin(MohrP_Angle))-9*cos(MohrP_Angle)+((Nzetaeta/2)*sin(MohrP_Angle)))/2],  y=[((0-9*sin(MohrP_Angle))+((Nzetaeta/2)*cos(MohrP_Angle))+(0-9*sin(MohrP_Angle))-((Nzetaeta/2)*cos(MohrP_Angle)))/2], w=[0.3*Nzetaeta-.5], h = [13], angle=[MohrP_Angle])
            self.Nzetaeta4_rect_source.data  = dict(x=[(9*sin(MohrP_Angle)+((Nzetaeta/2)*cos(MohrP_Angle))+9*sin(MohrP_Angle)-((Nzetaeta/2)*cos(MohrP_Angle)))/2],   y=[((0-9*cos(MohrP_Angle))+((Nzetaeta/2)*sin(MohrP_Angle))+(0-9*cos(MohrP_Angle))-((Nzetaeta/2)*sin(MohrP_Angle)))/2], h=[0.3*Nzetaeta-.5], w = [13], angle=[MohrP_Angle])

        input_vars["MohrP_Angle"] = -MohrP_Angle #      /output 
