###############################
# IMPORTS
###############################

# import local files
import vis_initialization as vis_init
from testing_collection import test_runner as test_lib


###############################
# INITIALIZATION
###############################

vis_init.initialize(max_indep_elements=20, catch_radius=0.15)

run_tests = False  # run tests or not
if run_tests:
    test_lib.run_tests()
