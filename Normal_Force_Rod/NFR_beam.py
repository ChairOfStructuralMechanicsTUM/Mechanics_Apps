from bokeh.models import ColumnDataSource, Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import ImageURL


from NFR_constants import lb, ub # lower and upper bound for patches



class NFR_beam():
    def __init__(self, x_start, x_end, y_offset, cross="constant"):
        ## inputs:
        #   x_start     start coordinate of beam
        #   x_end       end coordinate of beam
        #   y_offset    displacement in y-direction
        #   cross       cross-section (constant or tapered)
        
        self.shape = ColumnDataSource(data=dict(x=[x_start, x_end],y=[y_offset, y_offset]))
        self.color = "#0065BD"
        self.support_left  = ColumnDataSource(data=dict(sp_img=["Normal_Force_Rod/static/images/fixed_support.svg"], x=[x_start - 0.35] , y=[-0.05]))
        self.support_right = ColumnDataSource(data=dict(sp_img=["Normal_Force_Rod/static/images/slide_support.svg"], x=[x_end - 0.33] , y=[-0.08]))
        # self.support_left  = "Normal_Force_Rod/static/images/fixed_support.svg"
        # self.support_right = "Normal_Force_Rod/static/images/slide_support.svg"

        self.load = "point"

        x_half = (x_end - x_start)*0.5
        self.point_load_source = ColumnDataSource(data=dict(xS=[x_half-0.5], xE=[x_half+0.5], yS=[y_offset+0.3], yE=[y_offset+0.3], lW=[2], lC=["#0065BD"]))
        self.point_load_labels = ColumnDataSource(data=dict(x=[x_half-0.05, x_half-0.05], y=[y_offset+0.4, y_offset+0.1], name=['F','|']))

        self.constant_load_source = ColumnDataSource(data=dict(x=[x_start, x_start, x_half, x_half], y=[y_offset+lb, y_offset+ub, y_offset+ub, y_offset+lb]))
        # force arrow labels own cds

    
    def set_color(self, new_color):
        self.color = new_color
    
    def set_load(self, new_load):
        if new_load == 0:
            self.load = "point"
        elif new_load == 1:
            self.load = "constant"
        elif new_load == 2:
            self.load = "triangular"
        elif new_load == 3:
            self.load = "temperature"
        else:
            raise Exception("Error changing the load. No supported type!")

    
    #def _update_constant_load_source():
    # 

    def _clear_point_load_source():
        # test differnt clear functions

        # full clear
        self.point_load_source.data = dict(xS=[], xE=[], yS=[], yE=[], lW=[], lC=[])

        # only make line invisible
        self.point_load_source.data['lW'] = [0]

        # bokeh intern?




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

    def move_load(self, x):
        self.point_load_source.data['xS'] = [x - 0.5]
        self.point_load_source.data['xE'] = [x + 0.5]

        self.point_load_labels.data['x'] = [x - 0.05, x - 0.05]

    
    
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
        print(self.load)
        # better to plot each time (may be slow) AND: other labels stay! and alpha becomes worse
        # or better to set the other sources to zero?  (in _update_loads)
        if self.load == "point":
            arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width=2, size=5), 
                            x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                            line_width='lW', line_color='lC', source=self.point_load_source)
            
            labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=self.point_load_labels)

            fig.add_layout(arrow_glyph)
            fig.add_layout(labels)
        elif self.load == "constant":
            fig.patch(x='x', y='y', fill_alpha=0.5, source=self.constant_load_source)