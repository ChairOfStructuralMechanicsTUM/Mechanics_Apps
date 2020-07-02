'''###############################
IMPORTS
###############################'''
# general imports
import numpy                       as np

# import bokeh module
from bokeh.models              import ColumnDataSource
from bokeh.io                  import curdoc
from bokeh.models.callbacks    import CustomJS

# import local file
from Classes.ColumnDataSources import ColumnDataSources
from Classes.CurrentDocument   import CurrentDoc
from testing_collection        import test_runner as test_lib
import vis_initialization          as vis_init


'''###############################
# INITIALIZATION MAIN
###############################'''

curr_doc = CurrentDoc(curdoc())
vis_init.initialize(curr_doc, max_indep_elements=20, catch_radius=0.15)
# curdoc().add_root(doc_layout)

run_tests = False  # run tests or not
if run_tests:
    test_lib.run_tests(curr_doc)
