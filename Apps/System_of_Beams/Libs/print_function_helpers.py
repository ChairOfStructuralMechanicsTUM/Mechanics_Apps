import copy

# Class to colourise print statements
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_arr(arr_to_print):
    for el in arr_to_print:
        print(el)


def print_results(result, variables):
    for v in variables:
        print(result[v])


def print_knot_and_element_list(knot_list, ele_list):
    print("\nKNOTS:")
    print_arr(knot_list)
    print("\nELEMENTS:")
    print_arr(ele_list)
    print("\n")


def list_with_every_knot_only_once(knot_inp_list):
    """
    The file normally gets a knot_list of the style [[start_knot1, end_knot1], ... [start_knot_n, end_knot_n]]
    This functions takes this list and converts it to a list with ever knot just once
    :param knot_inp_list:
    :return: sorted list of knots (by id)
    """
    knot_set = set()
    nodeindep_to_plot = copy.deepcopy(knot_inp_list)
    if len(nodeindep_to_plot) >= 1 and isinstance(nodeindep_to_plot[0], list):
        for el in nodeindep_to_plot:
            knot_set.update(el)
        nodeindep_to_plot = list(knot_set)
    nodeindep_to_plot.sort(key=lambda knot: knot.id)
    return nodeindep_to_plot


def get_id_from_knots(knot1, knot2):
    """
    creates unique identifier for every beam that can be used to find the related forces
    :return: string
    """
    return str(knot1.id) + str(knot2.id)
    # return str(knot1.y_) + str(knot1.y_) + str(knot2.x_) + str(knot2.y_)


if __name__ == '__main__':
    # example:
    print(bcolors.HEADER + 'test' + bcolors.ENDC)

    # suppress new line in the end of print statement
    print('Test', end='')
    print('Test goes on in the same line')