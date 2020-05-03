

class ColumnDataSources_storage:
    def __init__(self):
        # vis_callbacks
        self.ds_input                        = None
        self.ds_glyph_images                 = None
        self.ds_glyph_beam                   = None
        self.ds_glyph_lineload               = None
        self.ds_arrow_lineload               = None
        self.ds_glyph_springsPointMomentTemp = None
        self.ds_input_selected               = None
        self.ds_active_button                = None
        self.ds_element_count                = None
        self.ds_chosen_node                  = None
        self.ds_1st_chosen                   = None
        self.ds_element_info                 = None
        self.ds_indep_elements               = None
        self.ds_nodedep_elements             = None
        # vis_elementToPlot
        self.ds_images = None
        # vis_initalization
        self.ds_x_axis                       = None
        self.ds_y_axis                       = None


ColumnDataSources = ColumnDataSources_storage()
