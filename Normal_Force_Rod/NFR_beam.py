"""
Normal Force Rod - beam class, for visualization purposes

"""
# general imports
from __future__ import division

# bokeh imports
from bokeh.models import ColumnDataSource, Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import ImageURL

# internal imports
from NFR_constants import (
    xr_start, xr_end,
    color_rod, color_arrow,
    lb, ub,  # lower and upper bound for patches
    y_offset,
    initial_load, initial_load_position
    )

# latex integration

#---------------------------------------------------------------------#


class NFR_beam():
    def __init__(self, xr_start, xr_end, y_offset, cross="constant"):
        ## inputs:
        #   xr_start     start coordinate of beam
        #   xr_end       end coordinate of beam
        #   y_offset    displacement in y-direction
        #   cross       cross-section (constant or tapered)
        
        self.shape = ColumnDataSource(data=dict(x=[xr_start, xr_end],y=[y_offset, y_offset]))
        self.color = color_rod
        self.support_left  = ColumnDataSource(data=dict(sp_img=["Normal_Force_Rod/static/images/fixed_support.svg"], x=[xr_start - 0.35] , y=[-0.05]))
        self.support_right = ColumnDataSource(data=dict(sp_img=["Normal_Force_Rod/static/images/slide_support.svg"], x=[xr_end - 0.33] , y=[-0.08]))
        # self.support_left  = "Normal_Force_Rod/static/images/fixed_support.svg"
        # self.support_right = "Normal_Force_Rod/static/images/slide_support.svg"


        # loads as dictionary mapping
        self.load = {
            0:  ["point", self._set_point_load],
            1:  ["constant", self._set_constant_load],
            2:  ["triangular", self._set_triangular_load],
            3:  ["temperature", self._set_temperature_load]
        }
        self.load_key = initial_load
        #self.load = "point"
        self.load_position = initial_load_position
        self.load_direction = "ltr" # left to right


        # define load and label sources
        self.point_load_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[]))
        #self.point_load_labels = ColumnDataSource(data=dict(x=[], y=[], name=[]))
        # x_half = (xr_end - xr_start)*0.5
        # self.point_load_source = ColumnDataSource(data=dict(xS=[x_half-0.5], xE=[x_half+0.5], yS=[y_offset+0.3], yE=[y_offset+0.3], lW=[2], lC=[color_arrow]))
        # self.point_load_labels = ColumnDataSource(data=dict(x=[x_half-0.05, x_half-0.05], y=[y_offset+0.4, y_offset+0.1], name=['F','|']))

        self.constant_load_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.triangular_load_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.temperature_load_source = ColumnDataSource(data=dict(x=[], y=[]))

        #self.constant_load_labels = ColumnDataSource(data=dict(x=[], y=[], name=[]))
        #self.constant_load_source = ColumnDataSource(data=dict(x=[xr_start, xr_start, x_half, x_half], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb]))
        # force arrow labels own cds  (constant + triang load)
        self.arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[]))

        # since the label structure is always the same, keep one cds for all loads
        # also saves one clear function each
        self.load_labels = ColumnDataSource(data=dict(x=[], y=[], name=[]))


        # set initial load which should be displayed at the start
        #self._set_point_load()
        self.set_load(initial_load)

    # print information to console
    def __str__(self):
        tmp_str = "Beam:\n"
        tmp_str += "  length: " + str(abs(xr_end - xr_start)) + "\n"
        tmp_str += "  color:  " + self.color + "\n"
        tmp_str += "  load:   " + self.load[self.load_key][0] + " at x=" + str(self.load_position) + "\n"
        return tmp_str

    
    def set_color(self, new_color):
        self.color = new_color
    
    def set_load(self, new_load):
        # if new_load == 0:
        #     self.load = "point"
        #     self._set_point_load()
        # elif new_load == 1:
        #     self.load = "constant"
        #     self._set_constant_load()
        #     #self._clear_point_load_source()
        #     #self.point_load_labels.data = dict(x=[0.1], y=[0.2], name=['p'])
        # elif new_load == 2:
        #     self.load = "triangular"
        #     self._set_triangular_load()
        # elif new_load == 3:
        #     self.load = "temperature"
        #     self._set_temperature_load()
        # else:
        #     raise Exception("Error changing the load. No supported type!")

        # call the function matching to the load
        self.load_key = new_load

        try:
            self.load[new_load][1]()
        except KeyError as k_error:
            print("KeyError! - undefined key "+str(k_error))
            print("The available keys are ")
            for k, v in self.load.items():
                print(str(k) + ": " + v[0])


        # problem: arrows showing to the right are visible for a short period of time when rtl!
        # # # # self._update_load_direction()
        # solution: put the call in the specific set functions themselves

    #def change_load_direction(self):
    def _update_load_direction(self):
        # swap start and end coordinates of the arrows
        #xS = self.arrow_source.data['xS']

        # if arrows should show from right to left
        if self.load_direction == "rtl":
            self.arrow_source.data['xS'], self.arrow_source.data['xE'] = \
            self.arrow_source.data['xE'], self.arrow_source.data['xS']

            self.point_load_source.data['xS'], self.point_load_source.data['xE'] = \
            self.point_load_source.data['xE'], self.point_load_source.data['xS']

    def set_load_direction(self, new_dir):
        if new_dir == 0:
            self.load_direction = "rtl"
        elif new_dir == 1:
            self.load_direction = "ltr"
        else:
            raise Exception("Error changing the load. No supported direction!")

        self.set_load(self.load_key)


    def set_load_position(self, new_pos):
        self.load_position = new_pos
        self.set_load(self.load_key)


    # update the ColumnDataSources based on the applied load
    # def _update_sources(self):
    #     if self.load == "point":
    #         self._set_constant_load()

    # def _clear_point_load_source(self):
    #     return dict(xS=[], xE=[], yS=[], yE=[])

    def _set_point_load(self):
        LP = self.load_position

        self.point_load_source.data=dict(xS=[xr_start-0.5+LP], xE=[xr_start+0.5+LP], yS=[y_offset+0.3], yE=[y_offset+0.3], lW=[2], lC=[color_arrow])

        self.load_labels.data=dict(x=[xr_start-0.1+LP, xr_start-0.05+LP], y=[y_offset+0.4, y_offset+0.1], name=['F','|'])

        self._update_load_direction()

        self._clear_source(self.constant_load_source)
        self._clear_source(self.triangular_load_source)
        self._clear_source(self.temperature_load_source)
        self._clear_source(self.arrow_source)

    
    def _set_constant_load(self):

        LP = self.load_position

        self.constant_load_source.data=dict(x=[xr_start, xr_start, LP, LP], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])


        self.load_labels.data = dict(x=[LP+0.1], y=[y_offset+0.2], name=['p'])

        xS = []
        xE = []
        # calculate the coordinats for the arrows and labels
        num_arrows = 3 # amount of arrows
        part = (LP-xr_start)/(num_arrows*2+1)
        local_index = list(range(1,num_arrows*2+1))
        # arrow start positions (odd)
        for i in local_index[::2]:
            xS.append(part*i)
            #xM.append(part*(i+0.5))
        # arrow end positions (even)
        for i in local_index[1:][::2]:
            xE.append(part*i)

        yS = [y_offset+0.45]*num_arrows
        yE = [y_offset+0.45]*num_arrows

        tmp_update_dict = dict(xS=xS, xE=xE, yS=yS, yE=yE, lW=[2]*num_arrows, lC=[color_arrow]*num_arrows)

        self.arrow_source.stream(tmp_update_dict,num_arrows)
        self._update_load_direction()

        self._clear_source(self.point_load_source)
        self._clear_source(self.triangular_load_source)
        self._clear_source(self.temperature_load_source)

    def _set_triangular_load(self):

        LP = self.load_position

        self.triangular_load_source.data=dict(x=[xr_start, xr_start, LP], y=[y_offset+lb, y_offset+ub, y_offset+lb])


        self.load_labels.data = dict(x=[LP+0.1], y=[y_offset+0.2], name=['p'])

        xS = []
        xE = []
        # calculate the coordinats for the arrows and labels
        num_arrows = 2 # amount of arrows
        part = 0.5*(LP-xr_start)/(num_arrows*2+1)
        local_index = list(range(1,num_arrows*2+1))
        # arrow start positions (odd)
        for i in local_index[::2]:
            xS.append(part*i)
            #xM.append(part*(i+0.5))
        # arrow end positions (even)
        for i in local_index[1:][::2]:
            xE.append(part*i)

        yS = [y_offset+0.45]*num_arrows
        yE = [y_offset+0.45]*num_arrows

        tmp_update_dict = dict(xS=xS, xE=xE, yS=yS, yE=yE, lW=[2]*num_arrows, lC=[color_arrow]*num_arrows)

        self.arrow_source.stream(tmp_update_dict,num_arrows)
        self._update_load_direction()

        self._clear_source(self.point_load_source)
        self._clear_source(self.constant_load_source)
        self._clear_source(self.temperature_load_source)


    def _set_temperature_load(self):

        LP = self.load_position

        self.temperature_load_source.data=dict(x=[xr_start, xr_start, LP, LP], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])


        self.load_labels.data = dict(x=[LP+0.1], y=[y_offset+0.2], name=['T'])

       
        self._clear_source(self.point_load_source)
        self._clear_source(self.constant_load_source)
        self._clear_source(self.triangular_load_source)
        self._clear_source(self.arrow_source)



    def _clear_source(self, cds):
        # exploit the inner rollover definition data = data[-rollover:]
        cds.stream(cds.data, -2*len(cds.data.values()[0]))


    # #def _update_constant_load_source():
    # # 

    # def _clear_point_load_source(self):
    #     # test differnt clear functions

    #     # full clear
    #     self.point_load_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[])

    #     # only make line invisible
    #     # nope, does not work
    #     #self.point_load_source.data['lW'] = [None]

    #     # bokeh/python intern?
    #     # only .clear() for dicts and .remove() for cds



    def set_left_support(self, support_type):
        if support_type == 0: # fixed
            self.support_left.data["sp_img"] = ["Normal_Force_Rod/static/images/fixed_support.svg"]
        elif support_type == 1: # slide
            self.support_left.data["sp_img"] = ["Normal_Force_Rod/static/images/slide_support.svg"]
        else:
            raise Exception("Error changing the left support. No supported type!")


    def set_right_support(self, support_type):
        if support_type == 0: # fixed
            self.support_right.data["sp_img"] = ["Normal_Force_Rod/static/images/fixed_support.svg"]
        elif support_type == 1: # slide
            self.support_right.data["sp_img"] = ["Normal_Force_Rod/static/images/slide_support.svg"]
        else:
            raise Exception("Error changing the right support. No supported type!")



    # change support coordinates
    def set_ls_coords(self, x, y):
        self.support_left.data['x'] = [x]
        self.support_left.data['y'] = [y]

    def set_rs_coords(self, x, y):
        self.support_right.data['x'] = [x]
        self.support_right.data['y'] = [y]

    def move_load(self, x=None):

        if x is not None:
            self.set_load_position(x)
        else:
            self.set_load(self.load_key)
        # self.point_load_source.data['xS'] = [x - 0.5]
        # self.point_load_source.data['xE'] = [x + 0.5]

        # self.point_load_labels.data['x'] = [x - 0.05, x - 0.05]

        # or update all sources at once? 
      
        #self.load[self.load_key][1]()
        #self.set_load(self.load_key)

        # if self.load == "point":
        #     self._set_point_load()
        # elif self.load == "constant":
        #     self._set_constant_load()
        # elif self.load == "triangular":
        #     self._set_triangular_load()
        # elif self.load == "temperature":
        #     self._set_temperature_load()

    
    
    def plot_all(self, fig):
        self.plot_beam(fig)
        self.plot_supports(fig)
        self.plot_label(fig)

    def plot_beam(self, fig, width=15):
        fig.patch(x='x', y='y', color=self.color, source=self.shape, line_width=width)

    def plot_beam_shadow(self, fig, color="black", alpha=0.8, width=2):
        fig.patch(x='x', y='y', color=color, source=self.shape, line_width=width, line_alpha=alpha, fill_alpha=alpha)

    def plot_supports(self, fig):
        fig.add_glyph(self.support_left, ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))
        fig.add_glyph(self.support_right,ImageURL(url="sp_img", x='x', y='y', w=0.66, h=0.4))

    def plot_label(self, fig):
        # better to plot each time (may be slow) AND: other labels stay! and alpha becomes worse
        # or better to set the other sources to zero?  (in _update_loads)

        # better to plot all at once and then delete cds we dont need


        # if self.load == "point":
        point_load_glyph = Arrow(end=OpenHead(line_color=color_arrow,line_width=2, size=5), 
                        x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                        line_width='lW', line_color='lC', source=self.point_load_source)
        
        labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=self.load_labels)

#        const_load_glyph = 

        fig.add_layout(point_load_glyph)
        fig.add_layout(labels)

        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.constant_load_source)
        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.triangular_load_source)
        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.temperature_load_source)



        arrow_glyphs = Arrow(end=OpenHead(line_color=color_arrow,line_width=2, size=5), 
                        x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                        line_width='lW', line_color='lC', source=self.arrow_source)


        fig.add_layout(arrow_glyphs)

        # elif self.load == "constant":
        #     fig.patch(x='x', y='y', fill_alpha=0.5, source=self.constant_load_source)