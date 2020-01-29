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
    xr_start, xr_end,           # beam start/end coordinate
    color_rod, color_arrow,     # beam color, force arrow color
    xsl, ysl, xsr, ysr,         # coordinates for the supports
    slide_support_img,          # support image (slide) 
    fixed_support_img,          # support image (fixed)
    lb, ub,                     # lower and upper bound for patch labels
    y_offset,                   # offset of the beam in y direction
    initial_load, initial_load_position,  # inital load values
    color_rod_hot, color_rod_cold # colors for temperature load
    )

# latex integration

#---------------------------------------------------------------------#


class NFR_beam():
    def __init__(self, cross="constant"):
        ## inputs:
        #   cross       cross-section (constant or tapered)
        
        # beam structure
        self.color = color_rod
        #self.shape = ColumnDataSource(data=dict(x=[xr_start, xr_end],y=[y_offset, y_offset],color=[self.color]))
        self.shape = ColumnDataSource(data=dict(x=[xr_start, xr_end],y=[y_offset, y_offset]))
        self.support_left  = ColumnDataSource(data=dict(sp_img=[fixed_support_img], x=[xsl] , y=[ysl]))
        self.support_right = ColumnDataSource(data=dict(sp_img=[slide_support_img], x=[xsr] , y=[ysr]))


        # possible loads as dictionary mapping
        self.load = {
            0:  ["point",             self._set_point_load],
            1:  ["constant",       self._set_constant_load],
            2:  ["triangular",   self._set_triangular_load],
            3:  ["temperature", self._set_temperature_load]
        }
        self.load_key = initial_load
        self.load_position = initial_load_position
        self.load_direction = "ltr" # left to right


        # define load sources
        self.point_load_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[]))
        self.constant_load_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.triangular_load_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.temperature_load_source = ColumnDataSource(data=dict(x=[], y=[]))

        # define label source
        # one cds in enough, since the label structure is always the same
        self.load_labels = ColumnDataSource(data=dict(x=[], y=[], name=[]))

        # arrow labels for constant and triangular load graphics
        self.arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[]))

        # set initial load which should be displayed at the start
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
        # call the function matching to the load
        self.load_key = new_load

        try:
            self.load[new_load][1]() # updates the load sources for display
        except KeyError as k_error:
            print("KeyError! - undefined key "+str(k_error))
            print("The available keys are ")
            for k, v in self.load.items():
                print(str(k) + ": " + v[0])

        # problem: arrows showing to the right are visible for a short period of time when rtl!
        # # # # self._update_load_direction()
        # solution: put the call in the specific set functions themselves


    def _update_load_direction(self):
        # if arrows should show from right to left
        # swap start and end coordinates of the arrows

        ### leave this in case the bug https://github.com/bokeh/bokeh/issues/9436 is solved
        # # if self.load_direction == "rtl":
        # #     self.arrow_source.data['xS'], self.arrow_source.data['xE'] = \
        # #     self.arrow_source.data['xE'], self.arrow_source.data['xS']

        # #     self.point_load_source.data['xS'], self.point_load_source.data['xE'] = \
        # #     self.point_load_source.data['xE'], self.point_load_source.data['xS']

        if self.load_direction == "rtl":
            new_source = self.arrow_source.data
            new_source['xS'], new_source['xE'] = new_source['xE'], new_source['xS']
            self.arrow_source.stream(new_source, rollover=len(new_source['xS'])) # len=rollover can be 2 for triangular or 3 for constant laod

            new_source = self.point_load_source.data
            new_source['xS'], new_source['xE'] = new_source['xE'], new_source['xS']
            self.point_load_source.stream(new_source, rollover=1) # len=rollover=1 for point source


    def set_load_direction(self, new_dir):
        if new_dir == 0:
            self.load_direction = "rtl" # right to left
        elif new_dir == 1:
            self.load_direction = "ltr" # left to right
        else:
            raise Exception("Error changing the load. No supported direction!")

        self.set_load(self.load_key) # update sources


    def set_load_position(self, new_pos):
        self.load_position = new_pos
        self.set_load(self.load_key) # update sources


    # update the point load source and clear the rest
    def _set_point_load(self):
        LP = self.load_position

        #self.point_load_source.data=dict(xS=[xr_start-0.5+LP], xE=[xr_start+0.5+LP], yS=[y_offset+0.3], yE=[y_offset+0.3], lW=[2], lC=[color_arrow])
        self.point_load_source.stream(dict(xS=[xr_start-0.5+LP], xE=[xr_start+0.5+LP], yS=[y_offset+0.3], yE=[y_offset+0.3], lW=[2], lC=[color_arrow]), rollover=1)

        self.load_labels.data=dict(x=[xr_start-0.1+LP, xr_start-0.05+LP], y=[y_offset+0.4, y_offset+0.1], name=['F','|'])

        self._update_load_direction()

        self._clear_source(self.constant_load_source)
        self._clear_source(self.triangular_load_source)
        self._clear_source(self.temperature_load_source)
        self._clear_source(self.arrow_source)


    # update the constant load source and clear the rest    
    def _set_constant_load(self):
        LP = self.load_position

        # don't show if the load position is only applied to the first point
        if LP < 1e-5: #close to zero
            self._clear_source(self.constant_load_source)
            self._clear_source(self.arrow_source)
            self._clear_source(self.point_load_source) # since for point loads 0 is allowed
            self._clear_source(self.load_labels)
        else:

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


    # update the triangular load source and clear the rest
    def _set_triangular_load(self):
        LP = self.load_position

        # don't show if the load position is only applied to the first point
        if LP < 1e-5: #close to zero
            self._clear_source(self.triangular_load_source)
            self._clear_source(self.arrow_source)
            self._clear_source(self.point_load_source) # since for point loads 0 is allowed
            self._clear_source(self.load_labels)
        else:

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


    # update the temperature load source and clear the rest
    def _set_temperature_load(self):

        LP = self.load_position

        # don't show if the load position is only applied to the first point
        if LP < 1e-5: #close to zero
            self._clear_source(self.temperature_load_source)
            self._clear_source(self.point_load_source) # since for point loads 0 is allowed
            self._clear_source(self.load_labels)
        else:

            self.temperature_load_source.data=dict(x=[xr_start, xr_start, LP, LP], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb])

            self.load_labels.data = dict(x=[LP+0.1], y=[y_offset+0.2], name=['T'])

            # # change the color and pictures based on amplitude
            # if self.load_direction == "ltr":
            #     self.color = color_rod_hot

        
            self._clear_source(self.point_load_source)
            self._clear_source(self.constant_load_source)
            self._clear_source(self.triangular_load_source)
            self._clear_source(self.arrow_source)


    # clears ColumnDataSources in such a way, that all keys will stay but only contain empty lists
    def _clear_source(self, cds):
        # exploit the inner rollover definition data = data[-rollover:]
        cds.stream(cds.data, -2*len(list(cds.data.values())[0])) # get the length of the first column of the CDS


    # move the load to position x (or extend it from 0 to x)
    def move_load(self, x=None):
        if x is not None:
            self.set_load_position(x)
        else:
            self.set_load(self.load_key)


    # change support pictures
    def set_left_support(self, support_type):
        if support_type == 0: # fixed
            self.support_left.data["sp_img"] = [fixed_support_img]
        elif support_type == 1: # slide
            self.support_left.data["sp_img"] = [slide_support_img]
        else:
            raise Exception("Error changing the left support. No supported type!")


    def set_right_support(self, support_type):
        if support_type == 0: # fixed
            self.support_right.data["sp_img"] = [fixed_support_img]
        elif support_type == 1: # slide
            self.support_right.data["sp_img"] = [slide_support_img]
        else:
            raise Exception("Error changing the right support. No supported type!")


    # change support coordinates
    def set_ls_coords(self, x, y):
        self.support_left.data['x'] = [x]
        self.support_left.data['y'] = [y]

    def set_rs_coords(self, x, y):
        self.support_right.data['x'] = [x]
        self.support_right.data['y'] = [y]


    
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
        # only plot once!
        # use ColumnDataSource updates to change the plot
        # no re-plotting necessary!


        # plot point load
        point_load_glyph = Arrow(end=OpenHead(line_color=color_arrow,line_width=2, size=5), 
                        x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                        line_width='lW', line_color='lC', source=self.point_load_source)
        fig.add_layout(point_load_glyph)

        # plot loads that use patches
        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.constant_load_source)
        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.triangular_load_source)
        fig.patch(x='x', y='y', fill_alpha=0.5, source=self.temperature_load_source)

        # plot the labels for the corresponding load
        labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=self.load_labels)
        fig.add_layout(labels)

        # add force arrows into the patches
        arrow_glyphs = Arrow(end=OpenHead(line_color=color_arrow,line_width=2, size=5), 
                x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                line_width='lW', line_color='lC', source=self.arrow_source)
        fig.add_layout(arrow_glyphs)
