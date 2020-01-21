"""Differentiation example
Demonstrates some differentiation operations.
"""
import re
from sympy import Symbol, pprint
import math

from Libs import symbolictoolbox as symbbox
from Libs import geometriccalc as gc
from Element_Initialising import integrate_function_with_constant


# TODO Find out how to do a properly error handling in Python, so that errors can be writtenc oorrectly to the user (Flags usw.)
#   raise ValueErrors
def check_float_input(inp):
    """
    :param inp: string to check if float
    :return: float if possible to cast, else nan; return message if something wrong
    """
    # check for regular expressions: https://regex101.com/
    message = ''
    # Check if Point and comma are inside, then error
    if re.search("((\..*,)|(,.*\.))", inp): # Richtige Methode hierfuer?
        message = "number cannot be transferred, because point and comma inside the string."
        print(message)
        return float('nan'), message

    # If more than one seperator of same type, then error
    if re.search("((\..*){2,})|((,.*){2,})", inp):
        message = "Only one seperator allowed in the number"
        print(message)
        return float('nan'), message

    # If only comma inside, change comma to Point and give once a warning (not more often)
    if re.search("(,){1}", inp):
        inp = inp.replace(',', '.')
        message = "comma changed to point"

    try:
        float(inp)
        return float(inp), message
    except:
        message = "Input cannot be written as a number"
        return float('nan'), message


def get_func_from_user(knot1, knot2, func_type=""):
    test_str = "(a + 2*s)**5"
    s = Symbol('s')
    if func_type == "":
        func_type = input("Choose between function of type: constant [c], linear [l], arbitrary [a]")
    if func_type.lower() == "c":
        # TODO function needs to be set correctly to the knots
        c_0 = input("Height of function: ")
        res, mes = check_float_input(c_0)
        if math.isnan(res):
            func = symbbox.get_symbol_from_string(str(c_0))
            return func
        else:
            func = (res + s*0)
            return func
    if func_type.lower() == "l":
        if knot1 == knot2:
            print("Knot1 & Knot2 are the same. No line load created.")
            return 0
        y0 = check_float_input(input("Start force: "))
        y1 = check_float_input(input("End force: "))
        # TODO check if y0 and y1 are symbols or number values. Get it correctly
        x0 = 0
        x1 = gc.knot_dist(knot1, knot2)



def main():
    a = Symbol('a')
    b = Symbol('b')
    e = (a + 2*b)**5

    print("\nExpression : ")
    print()
    pprint(e)
    print("\n\nDifferentiating w.r.t. a:")
    print()
    pprint(e.diff(a))
    print("\n\nDifferentiating w.r.t. b:")
    print()
    pprint(e.diff(b))
    print("\n\nSecond derivative of the above result w.r.t. a:")
    print()
    pprint(e.diff(b).diff(a, 2))
    print("\n\nExpanding the above result:")
    print()
    pprint(e.expand().diff(b).diff(a, 2))
    print()


def show_symbolic_functionality():
    '''
    function not needed for final program
    It only shows the functionality of the symbolic tool function
    Was used for 2nd presentation of software lab
    '''
    # print('Please add your function to integrate: ', end='')
    func_str = input('Please add your function to integrate: ')
    func = symbbox.get_func_from_string(func_str)
    print('Your function is: ')
    pprint(func)
    i = 0
    while True:
        decision = input('Do you want to integrate this function? [y, n]').lower()
        if decision == 'y':
            int_val_str = input('Which value do you want to integrate over?')
            int_val = symbbox.get_func_from_string(int_val_str)
            int_const = Symbol('c' + str(i))
            if int_val in func.free_symbols:
                func = integrate_function_with_constant(func, int_val, int_const)
                print('Your integrated function is:')
                pprint(func)
            else:
                func += int_const
            i += 1
        elif decision == 'n':
            print('Integration process stopped.')
            return


if __name__ == "__main__":
    show_symbolic_functionality()
    # knot1 = Knot(0, 0)
    # knot2 = Knot(1, 0)
    # #func = get_func_from_user(knot1, knot2, "c")
    # #pprint(func)
    # a0 = get_func_from_string('a0')
    #
    #
    # inp = "a0+2*a+3*b1"
    # func = get_func_from_string(inp)
    #
    #
    # free_symbs = func.free_symbols
    # for symb in free_symbs:
    #     print(symb)
    # el_list = []
    # for el in el_list:
    #     print(el)