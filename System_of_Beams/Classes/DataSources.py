from Classes import ElementSupportEnum as eLnum
from ColumnDataSources import ColumnDataSources


class DataSources:
    def __init__(self, doc):
        self.doc = doc
        self.ds_input = ColumnDataSources.ds_input
        self.ds_glyph_images = ColumnDataSources.ds_glyph_images
        self.ds_glyph_beam = ColumnDataSources.ds_glyph_beam
        self.ds_glyph_lineload = ColumnDataSources.ds_glyph_lineload
        self.ds_arrow_lineload = ColumnDataSources.ds_arrow_lineload
        self.ds_glyph_springsPointMomentTemp = ColumnDataSources.ds_glyph_springsPointMomentTemp
        self.ds_input_selected = ColumnDataSources.ds_input_selected
        self.ds_active_button = ColumnDataSources.ds_active_button
        self.ds_element_count = ColumnDataSources.ds_element_count
        self.ds_chosen_node = ColumnDataSources.ds_chosen_node
        self.ds_1st_chosen = ColumnDataSources.ds_1st_chosen
        self.ds_element_info = ColumnDataSources.ds_element_info
        self.ds_indep_elements = ColumnDataSources.ds_indep_elements
        self.ds_nodedep_elements = ColumnDataSources.ds_nodedep_elements

        # variable for the currently activated element button for the input plot
        self.button_activated = -1

        # radius to select specific element in input plot
        self.catch_radius = 0.15

        # used for automatic naming of the elements in the plot using a consecutive number
        self.object_id = 0

        # current element in the element info box, used to be able to delte the single element - Tupel(name, indep, index)
        self.elinfo_current_element = (False, False, False)
        # whether user input of element info box is blocked
        self.elinfo_input_blocked = False

        # whether currently a test case is plotted - independent element should get angle and elinfo shouldn't react
        self.plotting_test_case = False
        self.test_case_angle = []
        self.test_case_count_indep = 0

        # used to adapt plot elements when entries in ds_input were deleted
        self.len_ds_input = 0

        # node dependent enum element values of the plot to distinguish in the java script callback cb_plot_tap()
        self.nodedep_element_values = [eLnum.ElSupEnum.SPRING_SUPPORT.value, eLnum.ElSupEnum.SPRING_MOMENT_SUPPORT.value,
                                       eLnum.ElSupEnum.SPRING.value, eLnum.ElSupEnum.BEAM.value,
                                       eLnum.ElSupEnum.LOAD_POINT.value,
                                       eLnum.ElSupEnum.LOAD_MOMENT.value, eLnum.ElSupEnum.LOAD_LINE.value,
                                       eLnum.ElSupEnum.LOAD_TEMP.value]
