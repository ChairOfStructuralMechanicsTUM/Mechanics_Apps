from testing_collection import visualisation_tests as visu_tests
from Classes.CurrentDocument import CurrentDoc


def run_tests(curr_doc: CurrentDoc):
    """
    1.) write test case and add it to file test_cases.py
    2.) Call it in this function (run_tests() will be called in 'System_of_Beams\main.py'
    3.) make sure, the variable 'run_tests' in the file main.py is set to true
    4.) Only the latest run test can be plotted (no opportunities up to now to run one after another)
    5.) Results will be visualized at the bokeh server
    """

    """
    VISUALISATION TESTS
    """

    # print("Single beam lineload test")
    # visu_tests.single_beam_lineload_visu(curr_doc)

    # print("Final Software lab structure")
    # visu_tests.final_structure_software_lab(curr_doc)

    print('Test example Quirin')                                                  #19.11
    visu_tests.example_unterlagen_visu(curr_doc)

    # print("Visualise all possible nodedep elements")
    # visu_tests.vis_all_possible_nodedep_ele(curr_doc)

    """
    CALCULATION TESTS
    """

    # print("Single beam lineload test")                                            #24.11
    # test_cases.single_beam_lineload_test(curr_doc)

    # print('normal line load')                                                     #24.11
    # test_cases.single_beam_normal_lineload_test(curr_doc)

    # print("Single beam clamping test")                                            #24.11
    # test_cases.single_clamping_left_side(curr_doc)

    # print("Two beam lineload test")                                               #17.11
    # test_cases.two_beam_lineload_test(curr_doc)

    # print("Two beam lineload overdefined test")                                   #17.11
    # test_cases.single_beam_lineload_test_overdefined(curr_doc)

    # print("Single beam lineload test underdefined")                               #24.11
    # test_cases.single_beam_lineload_test_underdefined(curr_doc)

    # print('Big beam out of free elements')                                        #17.11
    # test_cases.two_beam_combined_to_one_complete_lineload_test(curr_doc)

    # print('Big beam out of free elements 2 l')                                    #17.11
    # test_cases.two_beam_combined_to_one_complete_lineload_test_2l(curr_doc)

    # print('Single load in the middle')                                            #17.11
    # test_cases.two_beam_combined_to_one_single_load_middle(curr_doc)

    # print('Seperated elements')                                                   #17.11
    # test_cases.single_beam_lineload_test_seperated_elements(curr_doc)

    # print('Joint test)                                                            #18.11
    # test_cases.two_beam_combined_to_one_single_load_middle_joint(curr_doc)
    #
    # print('Clamping with single load test')                                       #17.11
    # test_cases.single_clamping_left_side_single_load(curr_doc)

    # print('TM example')                                                           #17.11
    # test_cases.example_from_sheet_2_4(curr_doc)

    # print('Trapezlast')                                                           #17.11
    # test_cases.single_beam_trapezload_test(curr_doc)

    # print('Temperature test')                                                     #17.11
    # test_cases.single_beam_temperature_test(curr_doc)

    # print('Triangle test')                                                        #17.11
    # test_cases.two_beam_triangle_load_middle(curr_doc)

    # print('Temperature clamping')                                                 #18.11
    # test_cases.single_clamping_left_side_temperature(curr_doc)

    # print('ss13')                                                                 #17.11
    # test_cases.example_ss13(curr_doc)

    # print('ss12')                                                                 #17.11
    # test_cases.example_ss12(curr_doc)
    #
    # print('ss12_vereinfacht')                                                     #17.11
    # test_cases.example_ss12_vereinfacht(curr_doc)

    # print('ss11')                                                                 #17.11
    # test_cases.example_ss11(curr_doc)

    # print('ss14')                                                                 #19.11
    # test_cases.example_ss14(curr_doc)

    # print('schraeg')                                                              #17.11
    # test_cases.single_beam_schraeg(curr_doc)

    # print('vertical')                                                             #17.11
    # test_cases.single_beam_lineload_vertical_test(curr_doc)

    # print('vertical single load')                                                 #17.11
    # test_cases.single_beam_single_load_vertical_test(curr_doc)

    # print('Test Ecke')                                                            #17.11
    # test_cases.two_beam_corner_line_load(curr_doc)

    # print('triangle_not_symmetric')                                               #17.11
    # test_cases.two_beam_triangle_load_middle_not_symmetrical(curr_doc)

    # print('Test example Quirin')                                                  #19.11
    # test_cases.example_unterlagen_test(curr_doc)

    # print('Test Quirin vereinfacht')                                              #19.11
    # test_cases.example_unterlagen_test_vereinfacht(curr_doc)

    # print('test cos')                                                             #18.11
    # test_cases.single_beam_cos_test(curr_doc)

    # print('test multiple elements')                                               #19.11
    # test_cases.multiple_elements(curr_doc)

    # print('test case spring')                                                      #24.11
    # test_cases.example_2_3_neu(curr_doc)

    # print('Test case ss 15')                                                      #24.11
    # test_cases.example_ss15(curr_doc)

    # print('Test case ss 16')                                                      #24.11
    # test_cases.example_SS_16(curr_doc)

    # test_cases.single_beam_lineload_test_infinity(curr_doc)

    # test_cases.final_structure_software_lab(curr_doc)
    # test_cases.final_structure_software_lab(curr_doc)

