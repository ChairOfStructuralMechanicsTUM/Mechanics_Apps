from bokeh.models import ColumnDataSource

from MC_helper_functions import calculate_radius_and_center

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


    #      f3.Rotating_Axis_X_source.data=dict(xS=[], yS=[], xE=[], yE=[])
    # f3.Rotating_Axis_Y_source.data=dict(xS=[], yS=[], xE=[], yE=[])
    # f3.Moving_Label_source.data=dict(x=[], y=[], names =[])
    
