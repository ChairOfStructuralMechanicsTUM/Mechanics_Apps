"""
This file contains all geometric functions needed during different calculations
"""
import math
import numpy as np
from Classes import Knot
from sympy import solveset, S, EmptySet, FiniteSet, ConditionSet, nsimplify

# from System_of_Beams import vis_initialization as vis_init


def knot_dist(knot1, knot2):
    """
    Calculates the distance between two knots
    """
    return math.sqrt(math.pow(knot1.x_-knot2.x_, 2) + math.pow(knot1.y_ - knot2.y_, 2))


def get_angle(knot1, knot2):
    """
    Calculates the global angle between the x-axis and a line being defined by the knots
    :param knot1: start knot of the line
    :param knot2: end knot of the line
    :return: angle in radian
    """
    dx = knot2.x_-knot1.x_
    dy = knot2.y_-knot1.y_
    return math.atan2(dy, dx)


def is_close_list(comp_val, comp_list, rel_tol=1e-9, abs_tol=0.0):
    """
    Checks, if a value exists in a list. All values in a user defined range will be
    taken into account. Returns true or false
    :param comp_val: value being searched for in the list
    :param comp_list: list of existing values
    :param rel_tol: relative tolerance
    :param abs_tol: absolute tolerance
    :return: boolean, if exists or not
    """
    for el in comp_list:
        if math.isclose(float(comp_val), float(el), rel_tol=rel_tol, abs_tol=abs_tol):
            return True
    return False


def rotate_x_y_values(x_vals, y_vals, start_knot, end_knot, tol=1e-15):
    """
    Rotates x and y values around the given structure. Can handle single x_vals or lists
    :param x_vals: single value or list of x_vals
    :param y_vals: single value or list of y_vals
    :param tol: solving floating point round errors
    :return: single value or list of values, depends on the input: x_vals_rot, y_vals_rot
    """
    rot_ang = get_angle(start_knot, end_knot)
    if rot_ang != 0:
        x_rot = []
        y_rot = []
        rot_mat = np.array(([np.cos(rot_ang), -np.sin(rot_ang)], [np.sin(rot_ang), np.cos(rot_ang)]))
        rot_mat[np.abs(rot_mat) < tol] = 0
        if isinstance(x_vals, list) or isinstance(x_vals, np.ndarray):
            for x_val, y_val in zip(x_vals, y_vals):
                pos_vec = np.array([[x_val - start_knot.x_], [y_val - start_knot.y_]])
                res = rot_mat.dot(pos_vec)
                x_rot.append(res.item(0) + start_knot.x_)
                y_rot.append(res.item(1) + start_knot.y_)
        else:
            pos_vec = np.array([[x_vals - start_knot.x_], [y_vals - start_knot.y_]])
            res = rot_mat.dot(pos_vec)
            x_rot = (res.item(0) + start_knot.x_)
            y_rot = (res.item(1) + start_knot.y_)
        x_vals = x_rot
        y_vals = y_rot
    return x_vals, y_vals


def is_close_position(x_val, y_val, list_of_vals, rel_tol=1e-9, abs_tol=0.0):
    """
    Searches in a list of values if the chosen position (x, y) already exists
    :param x_val: x position to search for
    :param y_val: y position to search for
    :param list_of_vals: [PointCol1, PointCol2, ..., PointCol_n]
    :return:
    """
    # if len(list_of_vals) <= 1:
    #     if math.isclose(float(x_val), float(list_of_vals.x_val), rel_tol=rel_tol, abs_tol=abs_tol) and math.isclose(float(y_val), float(list_of_vals.y_val), rel_tol=rel_tol, abs_tol=abs_tol):
    #         return True
    for el in list_of_vals:
        if math.isclose(float(x_val), float(el.x_val), rel_tol=rel_tol, abs_tol=abs_tol) and math.isclose(float(y_val), float(el.y_val), rel_tol=rel_tol, abs_tol=abs_tol):
            return True
    return False


def get_real_roots(func, root_symb, round_pos=2):
    """
    Calculates all real roots of a symbolic function. Returns floats
    :param func: function find the roots in
    :param root_symb: the symbol the function runs over. eg: f(x)=2*x, then root_symb=x
    :param round_pos: defines the accuracy of rounding
    :return: list of all real roots [root1, root2, ... , root_n]
    """
    root_vec = []
    func = nsimplify(func)
    roots = solveset(func, root_symb, S.Reals)
    if roots.is_empty:
        return root_vec
    if isinstance(roots, FiniteSet):
        for root in roots:
            try:
                root_vec.append(round(float(root), round_pos))
            except:
                continue  # necessary, to handle complex roots
        return root_vec
    elif isinstance(roots, ConditionSet):
        '''
        TODO 
        If sin, cos function is used, a condition set will be created.
        This needs to be handeled differently, but is not implemented yet
        '''
        # vis_init.expand_msg2user("Due to the complex input function, characteristic values cannot be successfully calculated")
    return root_vec


def find_nearest(array, value):
    """
    Searches a list and finds the indexes of the elements, being nearest to the value
    :param array: list to search in
    :param value: value to search for
    :return: returns a list of indexes of the values being close to the value
    """
    array = np.asarray(array)
    x = np.abs(array - value)
    idx = np.where(x == x.min())[0]
    return idx


if __name__ == '__main__':
    knot0 = Knot.Knot(0, 0, 0, 1)
    knot1 = Knot.Knot(1, 1, 0, 1)
    knot2 = Knot.Knot(2, -1, 1, 1)
    knot3 = Knot.Knot(3, -1, -1, 1)
    knot4 = Knot.Knot(4, 1, -1, 1)
    knot5 = Knot.Knot(5, 0, -1, 1)

    # ANGLE TESTS
    # print(get_angle(knot0, knot1) * 180 / math.pi)
    # print(get_angle(knot0, knot2) * 180 / math.pi)
    # print(get_angle(knot3, knot1) * 180 / math.pi)
    # print(get_angle(knot0, knot4) * 180 / math.pi)
    # print(get_angle(knot0, knot5) * 180 / math.pi)

    # ROTATION MATRIX TESTS
    x = 1
    y = 0
    x, y = rotate_x_y_values(x, y, knot0, knot1)
    print("x: {}\t y: {}".format(x, y))
