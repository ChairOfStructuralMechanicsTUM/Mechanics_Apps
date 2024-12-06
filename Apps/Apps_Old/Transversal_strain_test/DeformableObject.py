###################################
# Imports
###################################
# general imports
from math               import pi, cos, sin

# bokeh imports
from bokeh.models       import ColumnDataSource



##################################
# Costum Objects
##################################

class DeformableObject():
    def __init__(self, width, height, origin_x, origin_y, E, nu):
        # material parameters
        self.E              = E     # [N/mm²]
        self.nu             = nu
        
        # undeformed size
        self.width          = width
        self.height         = height

        # origin (centre) coordinates 
        self.origin_x       = origin_x
        self.origin_y       = origin_y

        # current size (deformed size)
        self.scale          = 5
        self.eps_x          = 0
        self.eps_y          = 0
        self.current_width  = width
        self.current_height = height

        self.children       = []
        self.children_vis   = -1
        self.force_symbols  = []

        # data source for plot
        self.data_source = dict(
            undeformed = ColumnDataSource(data=dict()) ,
            deformed   = ColumnDataSource(data=dict()) )

        # set size of undeformed object
        self.data_source_undeformed()

    def add_child(self, x_pos, y_pos, ellipse, shape_data):
        child = Child_of_DeformableObject(x_pos, y_pos, ellipse, shape_data)
        self.children.append(child)
    
    def add_force_symbol(self,x_pos,y_pos,width,height,angle,force_text):
        force_symbol = ForceSymbol(x_pos,y_pos,width,height,angle,force_text)
        self.force_symbols.append(force_symbol)
        
    def data_source_undeformed(self):
        x, y = self.origin_x , self.origin_y
        w, h = self.width    , self.height
        self.data_source['undeformed'].data['x'] = [x-w/2, x+w/2, x+w/2, x-w/2]
        self.data_source['undeformed'].data['y'] = [y+h/2, y+h/2, y-h/2, y-h/2]

    def deform_object(self, Fx, Fy):
        '''
        Fx and Fy in [N]
        '''
        sigma_x , sigma_y = Fx/self.height , Fy/self.width
        self.eps_x = ( sigma_x/self.E - sigma_y/self.E * self.nu ) * self.scale
        self.eps_y = ( sigma_y/self.E - sigma_x/self.E * self.nu ) * self.scale

        # calculate new geometry and update data source
        self.current_width  = (1+self.eps_x) * self.width
        self.current_height = (1+self.eps_y) * self.height
        x, y = self.origin_x      , self.origin_y
        w, h = self.current_width , self.current_height
        self.data_source['deformed'].data['x'] = [x-w/2, x+w/2, x+w/2, x-w/2]
        self.data_source['deformed'].data['y'] = [y+h/2, y+h/2, y-h/2, y-h/2]

        # calculate new geometry of symbols and update data source
        for child in self.children:
            child.update_data(self.eps_x, self.eps_y)

        # calculate new geometry of force-symbols and update data source
        for force_symbol in self.force_symbols:
            angle = force_symbol.angle
            if angle == 0 or angle == pi:
                w, sigma, eps = self.current_width, sigma_y, self.eps_y
            else:
                w, sigma, eps = self.current_height, sigma_x, self.eps_x 
            force_symbol.update_data(w, sigma, eps)

    def deform_coords(self,delta,eps):
        return delta*(1+eps)
    

class Child_of_DeformableObject(DeformableObject):
    def __init__(self, x_pos, y_pos, ellipse, shape_data):
        # position of the center of the object relative to the parents center
        self.x_pos              = x_pos
        self.y_pos              = y_pos
        # if ellipse: True or False
        self.ellipse            = ellipse 
        # coordinates of the undeformed object [[x0,x1,...],[y0,y1,...]]
        # if ellipse: width and height of the undeformed ellipse [width, height]
        self.shape_data         = shape_data
        # data source for plot
        self.data_source        = ColumnDataSource(data=dict())

    def update_data(self, eps_x, eps_y):
        # calculate new geometry of children and update data source
        x0, y0 = self.x_pos, self.y_pos
        if not self.ellipse:
            x_vec, y_vec = [], []
            for i in range(len(self.shape_data[0])):
                x, y         = self.shape_data[0][i], self.shape_data[1][i]
                dx, dy       = x0+x, y0+y
                x_def, y_def = self.deform_coords(dx, eps_x), self.deform_coords(dy, eps_y)
                x_vec.append(x_def)
                y_vec.append(y_def)
            self.data_source.data['x'] = x_vec
            self.data_source.data['y'] = y_vec
        else:
            x0_def, y0_def = self.deform_coords(x0, eps_x), self.deform_coords(y0, eps_y)
            w, h           = self.shape_data[0], self.shape_data[1]
            w0, w1, h0, h1 = x0-w/2, x0+w/2, y0-h/2, y0+h/2
            w_def = self.deform_coords(w1, eps_x) - self.deform_coords(w0, eps_x)
            h_def = self.deform_coords(h1, eps_y) - self.deform_coords(h0, eps_y)
            self.data_source.data['x'] = [x0_def]
            self.data_source.data['y'] = [y0_def]
            self.data_source.data['w'] = [w_def ]
            self.data_source.data['h'] = [h_def ]
    
class ForceSymbol(DeformableObject):
    def __init__(self, x_pos, y_pos, width, height, angle, force_text):
        self.x_pos       = x_pos
        self.y_pos       = y_pos
        self.width       = width
        self.height      = height
        self.angle       = angle
        self.force_text  = force_text
        # data source for plot
        self.data_source = dict(
            sigma        = ColumnDataSource(data=dict()) ,
            sigma_arrows = ColumnDataSource(data=dict()) ,
            R_arrow      = ColumnDataSource(data=dict()) ,
            R_label      = ColumnDataSource(data=dict()) )
    
    def update_data(self, width, sigma, eps):
        # calculate new geometry of force-symbols and update data source
        self.width = width
        w, h = self.width, self.height
        if sigma != 0:
            if sigma > 0: h0, h1 = 0, h
            else:         h0, h1 = h, 0
            # sigma in local coordinates
            x = [-w/2,-w/2,w/2,w/2,-w/2]
            y = [0   ,h   ,h  ,0  ,0   ]
            # Arrows for sigma in local coordinates
            xS= [-w/2,0,w/2]
            yS= [h0 ,h0,h0]
            xE= [-w/2,0 ,w/2]
            yE= [h1  ,h1,h1]
            # R arrow in local coordinates
            RxS, RyS = [0], [h+1+h0*2]
            RxE, RyE = [0], [h+1+h1*2]
            # R label in local coordinates
            R_text = [self.force_text]
            if   self.angle == 0:       Rlx, Rly = [1], [h+1+h1+h0]
            elif self.angle == 1/2*pi:  Rlx, Rly = [1.3], [h+1+h1+h0]
            elif self.angle == pi:      Rlx, Rly = [-1], [h+1+h1+h0]
            elif self.angle == 3/2*pi:  Rlx, Rly = [-1.3], [h+1+h1+h0]
            # calculate global coordinates
            all_xy = [[x,y],[xS,yS],[xE,yE],[RxS, RyS],[RxE, RyE],[Rlx, Rly]]
            for xy in all_xy:
                for i in range(len(xy[0])):
                    if   self.angle == 0:      add = 0.5 + eps * self.y_pos
                    elif self.angle == 1/2*pi: add = 0.5 - eps * self.x_pos
                    elif self.angle == pi:     add = 0.5 - eps * self.y_pos
                    elif self.angle == 3/2*pi: add = 0.5 + eps * self.x_pos
                    xy[1][i] += add
                    x = xy[0][i]*cos(self.angle) - xy[1][i]*sin(self.angle)
                    y = xy[0][i]*sin(self.angle) + xy[1][i]*cos(self.angle)
                    x += self.x_pos
                    y += self.y_pos
                    xy[0][i], xy[1][i] = x, y
        else: 
            all_xy = [[[],[]],[[],[]],[[],[]],[[],[]],[[],[]],[[],[]]]
            R_text = []
        # update data source
        self.data_source['sigma'].data  = dict(x=all_xy[0][0], y=all_xy[0][1])
        self.data_source['sigma_arrows'].data = dict(xS=all_xy[1][0], yS=all_xy[1][1], xE=all_xy[2][0], yE=all_xy[2][1])
        self.data_source['sigma_arrows'].stream(self.data_source['sigma_arrows'].data,rollover=-1)
        self.data_source['R_arrow'].data = dict(xS=all_xy[3][0], yS=all_xy[3][1], xE=all_xy[4][0], yE=all_xy[4][1])
        self.data_source['R_arrow'].stream(self.data_source['R_arrow'].data,rollover=-1)
        self.data_source['R_label'].data = dict(x=all_xy[5][0], y=all_xy[5][1], label_text=R_text)

    
