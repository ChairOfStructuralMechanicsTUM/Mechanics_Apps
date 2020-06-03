from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row


class DocElement:
    def __init__(self, doc):
        self.doc = doc
        # input plot, the user can add elements to it and combine them to a mechanical system
        self.plot_input = figure()

        # dict containing all element bokeh buttons and their corresponding ElementSupportEnum as key
        self.buttons = {}

        # dict containing all element-info-box inputs
        self.input_element_info = {}
        # dict containing some element-info-box Divs
        self.div_element_info = {}
        # dict containing some element-info-box radio- or checkbox-groups
        self.group_element_info = {}
        # dict containing children of layout_element_info
        self.children_element_info = {}
        # layout of the element-info-box
        self.layout_element_info = row()

        # bokeh Div for showing messages to the user like warnings and errors and initial text string that gets expanded
        self.div_msg = 0
        self.msg2user = ""

        # bokeh Div for showing messages concerning the input plot to the user
        self.div_input = 0

        # output plots used after calculations
        self.plot_list = []
        self.plot_normal_f = figure()
        self.plot_normal_disp = figure()
        self.plot_shear_f = figure()
        self.plot_moment = figure()
        self.plot_shear_disp = figure()
        self.plot_shear_angle = figure()
