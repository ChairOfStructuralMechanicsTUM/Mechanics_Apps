from bokeh import document
from bokeh.plotting import figure
from bokeh.layouts import row

from Classes.ColumnDataSources import ColumnDataSources
from Classes.ElementSupportEnum import ElSupEnum
from Classes.OutputData import OutputVisu


class CurrentDoc:
    def __init__(self, curr_doc: document):
        self.curr_doc = curr_doc
        self.curr_doc.template_variables['DocElement'] = ColumnDataSources()
        self.curr_doc.template_variables['Buttons'] = {}
        self.curr_doc.template_variables['ButtonActivated'] = -1
        self.curr_doc.template_variables['DivInput'] = 0
        self.curr_doc.template_variables['DivMsg'] = 0
        self.curr_doc.template_variables['Msg2User'] = ""
        self.curr_doc.template_variables['ElinfoCurrentElement'] = (False, False, False)
        self.curr_doc.template_variables['ElinfoInputBlocked'] = False
        self.curr_doc.template_variables['CatchRadius'] = 0
        self.curr_doc.template_variables['ObjectID'] = 0
        self.curr_doc.template_variables['PlottingTestCase'] = False
        self.curr_doc.template_variables['TestCaseAngle'] = []
        self.curr_doc.template_variables['TestCaseCountIndep'] = 0
        self.curr_doc.template_variables['PlotData'] = OutputVisu()
        self.curr_doc.template_variables['PlotInput'] = figure()
        self.curr_doc.template_variables['PlotList'] = []
        self.curr_doc.template_variables['PlotNormalF'] = figure()
        self.curr_doc.template_variables['PlotNormalDisp'] = figure()
        self.curr_doc.template_variables['PlotShearF'] = figure()
        self.curr_doc.template_variables['PlotMoment'] = figure()
        self.curr_doc.template_variables['PlotShearDisp'] = figure()
        self.curr_doc.template_variables['PlotShearAngle'] = figure()
        self.curr_doc.template_variables['DivElementInfo'] = {}
        self.curr_doc.template_variables['InputElementInfo'] = {}
        self.curr_doc.template_variables['GroupElementInfo'] = {}
        self.curr_doc.template_variables['ChildrenElementInfo'] = {}
        self.curr_doc.template_variables['LayoutElementInfo'] = row()
        self.curr_doc.template_variables['LenDsInput'] = 0
        self.curr_doc.template_variables['NodedepElVals'] = [ElSupEnum.SPRING_SUPPORT.value,
                                                             ElSupEnum.SPRING_MOMENT_SUPPORT.value,
                                                             ElSupEnum.SPRING.value, ElSupEnum.BEAM.value,
                                                             ElSupEnum.LOAD_POINT.value, ElSupEnum.LOAD_MOMENT.value,
                                                             ElSupEnum.LOAD_LINE.value, ElSupEnum.LOAD_TEMP.value]


    @property
    def data_sources(self):
        return self.curr_doc.template_variables['DocElement']

    # dict containing all element bokeh buttons and their corresponding ElementSupportEnum as key
    @property
    def buttons(self):
        return self.curr_doc.template_variables['Buttons']

    @property
    def button_activated(self):
        return self.curr_doc.template_variables['ButtonActivated']

    @button_activated.setter
    def button_activated(self, value):
        self.curr_doc.template_variables['ButtonActivated'] = value

    @property
    def div_input(self):
        return self.curr_doc.template_variables['DivInput']

    @div_input.setter
    def div_input(self, value):
        self.curr_doc.template_variables['DivInput'] = value

    @property
    def div_msg(self):
        return self.curr_doc.template_variables['DivMsg']

    @div_msg.setter
    def div_msg(self, value):
        self.curr_doc.template_variables['DivMsg'] = value

    @property
    def msg2user(self):
        return self.curr_doc.template_variables['Msg2User']

    @msg2user.setter
    def msg2user(self, value):
        self.curr_doc.template_variables['Msg2User'] = value

    @property
    def elinfo_current_element(self):
        return self.curr_doc.template_variables['ElinfoCurrentElement']

    @elinfo_current_element.setter
    def elinfo_current_element(self, value):
        self.curr_doc.template_variables['ElinfoCurrentElement'] = value

    @property
    def elinfo_input_blocked(self):
        return self.curr_doc.template_variables['ElinfoInputBlocked']

    @elinfo_input_blocked.setter
    def elinfo_input_blocked(self, value):
        self.curr_doc.template_variables['ElinfoInputBlocked'] = value

    @property
    def object_id(self):
        return self.curr_doc.template_variables['ObjectID']

    @object_id.setter
    def object_id(self, value):
        self.curr_doc.template_variables['ObjectID'] = value

    @property
    def catch_radius(self):
        return self.curr_doc.template_variables['CatchRadius']

    @catch_radius.setter
    def catch_radius(self, value):
        self.curr_doc.template_variables['CatchRadius'] = value

    @property
    def plotting_test_case(self):
        return self.curr_doc.template_variables['PlottingTestCase']

    @plotting_test_case.setter
    def plotting_test_case(self, value):
        self.curr_doc.template_variables['PlottingTestCase'] = value

    @property
    def test_case_angle(self):
        return self.curr_doc.template_variables['TestCaseAngle']

    @test_case_angle.setter
    def test_case_angle(self, value):
        self.curr_doc.template_variables['TestCaseAngle'] = value

    @property
    def test_case_count_indep(self):
        return self.curr_doc.template_variables['TestCaseCountIndep']

    @test_case_count_indep.setter
    def test_case_count_indep(self, value):
        self.curr_doc.template_variables['TestCaseCountIndep'] = value

    @property
    def plot_data(self):
        return self.curr_doc.template_variables['PlotData']

    @property
    def plot_input(self):
        return self.curr_doc.template_variables['PlotInput']

    @plot_input.setter
    def plot_input(self, value):
        self.curr_doc.template_variables['PlotInput'] = value

    @property
    def plot_list(self):
        return self.curr_doc.template_variables['PlotList']

    @plot_list.setter
    def plot_list(self, value):
        self.curr_doc.template_variables['PlotList'] = value

    @property
    def plot_normal_f(self):
        return self.curr_doc.template_variables['PlotNormalF']

    @plot_normal_f.setter
    def plot_normal_f(self, value):
        self.curr_doc.template_variables['PlotNormalF'] = value

    @property
    def plot_normal_disp(self):
        return self.curr_doc.template_variables['PlotNormalDisp']

    @plot_normal_disp.setter
    def plot_normal_disp(self, value):
        self.curr_doc.template_variables['PlotNormalDisp'] = value

    @property
    def plot_shear_f(self):
        return self.curr_doc.template_variables['PlotShearF']

    @plot_shear_f.setter
    def plot_shear_f(self, value):
        self.curr_doc.template_variables['PlotShearF'] = value

    @property
    def plot_moment(self):
        return self.curr_doc.template_variables['PlotMoment']

    @plot_moment.setter
    def plot_moment(self, value):
        self.curr_doc.template_variables['PlotMoment'] = value

    @property
    def plot_shear_disp(self):
        return self.curr_doc.template_variables['PlotShearDisp']

    @plot_shear_disp.setter
    def plot_shear_disp(self, value):
        self.curr_doc.template_variables['PlotShearDisp'] = value

    @property
    def plot_shear_angle(self):
        return self.curr_doc.template_variables['PlotShearAngle']

    @plot_shear_angle.setter
    def plot_shear_angle(self, value):
        self.curr_doc.template_variables['PlotShearAngle'] = value

    @property
    def div_element_info(self):
        return self.curr_doc.template_variables['DivElementInfo']

    @div_element_info.setter
    def div_element_info(self, value):
        self.curr_doc.template_variables['DivElementInfo'] = value

    @property
    def input_element_info(self):
        return self.curr_doc.template_variables['InputElementInfo']

    @input_element_info.setter
    def input_element_info(self, value):
        self.curr_doc.template_variables['InputElementInfo'] = value

    @property
    def group_element_info(self):
        return self.curr_doc.template_variables['GroupElementInfo']

    @group_element_info.setter
    def group_element_info(self, value):
        self.curr_doc.template_variables['GroupElementInfo'] = value

    @property
    def children_element_info(self):
        return self.curr_doc.template_variables['ChildrenElementInfo']

    @children_element_info.setter
    def children_element_info(self, value):
        self.curr_doc.template_variables['ChildrenElementInfo'] = value

    @property
    def layout_element_info(self):
        return self.curr_doc.template_variables['LayoutElementInfo']

    @layout_element_info.setter
    def layout_element_info(self, value):
        self.curr_doc.template_variables['LayoutElementInfo'] = value

    @property
    def len_ds_input(self):
        return self.curr_doc.template_variables['LenDsInput']

    @len_ds_input.setter
    def len_ds_input(self, value):
        self.curr_doc.template_variables['LenDsInput'] = value

    @property
    def nodedep_element_values(self):
        return self.curr_doc.template_variables['NodedepElVals']
