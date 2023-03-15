from bokeh.models import ColumnDataSource


#Class frame: This creates an object of type Frame. The frame contains variables
#that are pertaining to the frame. For this app, 2 frames are created (F1 and F2)
#F1 is the initial frame, and F2 is the new frame once  F1 has been frozen.
class Maxwell_Frame(object):
    def __init__(self,name,n):
        self.pts            = ColumnDataSource(data=dict(x = [], y = [] ))
        self.p_mag          = 0
        self.boundary       = 0
        self.x0             = 0.1
        self.xf             = 0.8
        self.y0             = 0.1
        self.yf             = 0.6
        self.name           = name
        self.p_loc          = 0
        self.mag_start      = -100
        self.mag_end        = 100
        self.mag_val        = 0
        self.loc_start      = 0
        self.loc_end        = 100
        self.loc_val        = 50
        self.n              = n
        self.arrow_source   = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.e_s            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

        #EDIT Start
        self.e_s12          = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))
        self.e_s21          = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

        self.tri            = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.seg            = ColumnDataSource(data=dict(x0=[], x1=[], y0=[], y1=[]))
        self.t_line         = ColumnDataSource(data=dict(x=[], y=[]))
        self.label          = ColumnDataSource(data=dict(x=[] , y=[], name = []))
        self.dline          = ColumnDataSource(data=dict(x=[], y=[]))
        self.dlabel         = ColumnDataSource(data=dict(x=[] , y=[], name = []))
        self.w1             = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], name = []))
        
        
        self.w12            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], name = []))
        self.w12_11         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.w12_12         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.w21            = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], name = []))
        self.w21_11         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[] ))
        self.w21_12         = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[] ))
        
        self.w2             = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[]))
        self.wdline         = ColumnDataSource(data=dict(x1=[], x2 =[], y1 = [], y2=[]))
        
        
        self.wdline12       = ColumnDataSource(data=dict(x1=[], x2 =[], y1 = [], y2=[]))
        self.wdline21       = ColumnDataSource(data=dict(x1=[], x2 =[], y1 = [], y2=[]))
        #EDIT End

    def set_mag(self, a):
        '''Sets the magnitude of the load on frame (p_mag) equal to a'''
        self.p_mag = a
    def set_param(self, a):
        '''sets the location of load on frame (p_loc) equal to a'''
        self.p_loc = a
    def get_mag(self):
        '''Function returns load magnitude value'''
        return self.p_mag
    def get_param(self):
        '''Function returns load position value'''
        return self.p_loc