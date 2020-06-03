

class OutputVisu:
    """
    Contains all necessary information about the elements being plotted in the output plots
    """
    def __init__(self, doc):
        self.doc = doc
        self.init_dictionaries()
        self.init_plot_el_list()

    def init_dictionaries(self):
        self.char_vals_dict = dict()  # Makes sure, that every characteristic value gets only plotted once
        self.bound_vals_dict = dict()
        self.extreme_vals_dict = dict()
        self.extreme_vals_cross_dict = dict()
        self.zero_cross_dict = dict()
        self.zero_cross_cross_dict = dict()
        self.dict_list = [self.char_vals_dict, self.bound_vals_dict, self.extreme_vals_dict, self.extreme_vals_cross_dict,
                          self.zero_cross_dict, self.zero_cross_cross_dict]

    def init_plot_el_list(self):
        self.plot_el_lists = [[], [], [], [], [], []]

    def reset_data_sources(self):
        self.init_dictionaries()
        self.init_plot_el_list()

    def reset_plot(self, plot, list_of_els):
        # reset dictionaries
        for dict_el in self.dict_list:
            if plot in dict_el:
                searched_list = dict_el[plot]
                searched_list.clear()

        # reset structures
        if not list_of_els:
            return
        for el in list_of_els:
            print("el: " + str(el))
            glyph = plot.select(name=el)
            plot.renderers.remove(glyph[0])
        list_of_els.clear()
