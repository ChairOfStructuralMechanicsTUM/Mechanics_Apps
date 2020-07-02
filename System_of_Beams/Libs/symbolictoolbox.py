from sympy import pprint, Symbol, sympify, Number, solveset, S, pretty
import re

CALC_SYMBOLS = ['+', '-', '*', '/', '**', '(', ')', '[', ']']
GREEK_ALPHABET = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'my',
                  'ny', 'xi', 'omikron', 'pi', 'rho', 'sigma', 'tau', 'ypsilon', 'phi', 'chi', 'psi', 'omega']
FUNCTION_WORDS = ['sin', 'cos', 'tan', 'cot', 'sinh', 'cosh', 'tanh', 'coth']
EXCLUDE_WORDS = GREEK_ALPHABET + FUNCTION_WORDS


def remove_free_symbols(func, symb_to_remain):
    """
    Replaces all free symbols in a symbolic function with ones.
    Only the symbol to remain stays in the function
    :param func: func to be refactored
    :param symb_to_remain: symbol hat needs to stay. If None all symbols are replaced
    :return: refactored function
    """
    if isinstance(func, int) or isinstance(func, float):
        return func
    func = replace_temp_loads(func)
    free_symbols = func.free_symbols
    if symb_to_remain in free_symbols:
        free_symbols.remove(symb_to_remain)

    val_to_assign = [1] * len(free_symbols)
    set_to_one = dict(zip(free_symbols, val_to_assign))
    return func.subs(set_to_one)

def replace_temp_loads(func, value=1/3):
    """
    Replaces temperature symbols in a symbolic function with param value. This prevents irritating output plots.
    :param func: func to be refactored
    :return: refactored function
    """
    temperature_symbols = {'dT', 'T'}

    val_to_assign = [value] * len(temperature_symbols)
    set_to_value = dict(zip(temperature_symbols, val_to_assign))
    return func.subs(set_to_value)

def get_free_symbols(func, symbs_to_ignore=None):
    """
    Returns all free elements of a function, by ignoring symbs_to_ignore
    :param func: function to check
    :param symbs_to_ignore: values to ignore in result
    :return: list of all free symbols
    """
    if isinstance(func, int) or isinstance(func, float):
        return [func]
    if not isinstance(symbs_to_ignore, list):
        symbs_to_ignore = [symbs_to_ignore]
    free_symbs = []
    all_free_symbs = func.free_symbols
    for el in all_free_symbs:
        if el not in symbs_to_ignore:
            free_symbs.append(el)
    return free_symbs


def round_expr(expr, num_digits):
    """
    Round function that can be used for symbolic expressions
    """
    if isinstance(expr, float) or isinstance(expr, int):
        return round(expr, 2)
    return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})


def get_symbol_from_string(inp):
    """
    Takes one string and converts it to a symbol
    :param inp: short string (best case just one char)
    :return: returns this string as a symbol
    Example: inp=2a => return=2a
    """
    if isinstance(inp, str):
        test = Symbol(inp)
        return Symbol(inp)
    else:
        raise Exception('Symbol cannot be created')


def get_str_from_func(func, round_prec=1):
    """
    Converts a function to a string and refactors the string to make it more readable
    """
    # Can be used to write it to the pprint format
    # return pretty(func)

    # round function
    func = round_expr(func, round_prec)

    func_str = str(func)
    # replace ** with ^
    str_to_search = re.compile("\*\*")
    func_str = re.sub(str_to_search, "^", func_str)

    # delete useless zeros at the end
    str_to_search = re.compile("(?:(\.\d*?[1-9]+)|\.)0*")
    func_str = re.sub(str_to_search, r"\1", func_str)

    # Change * to middle dots
    str_to_search = re.compile("\*")
    func_str = re.sub(str_to_search, u"\u00B7", func_str)

    return func_str


def validate_input_string(inp_str):
    # TODO do the validation for user defined input here
    return inp_str


# TODO Warning this function uses eval, and thus shouldn’t be used on unsanitized input.
def get_func_from_string(inp):
    """
    Gets a complete string from a user and converts it into a symbolic expression
    :param inp: string that needs to be converted
    """
    # Change 2a to 2*a
    pat_mis_mult = re.compile("\d{1}[a-zA-Z]{1}")
    missed_mult_signs = re.findall(pat_mis_mult, inp)
    for el in missed_mult_signs:
        pos = re.search(pat_mis_mult, inp)
        start_pos = pos.start()
        end_pos = pos.end()
        inp = inp[:start_pos + 1] + '*' + inp[end_pos - 1:]

    # set all strings with more than two chars to lower characters
    pat_mult_chars = re.compile("[a-zA-Z]{2,}")
    mult_chars = re.findall(pat_mult_chars, inp)
    for el in mult_chars:
        start_pos = inp.find(el)
        end_pos = start_pos + len(el)
        if inp[start_pos:end_pos].lower() in EXCLUDE_WORDS:
            if not inp[start_pos:end_pos].lower() == inp[start_pos:end_pos]:
                inp = inp[:start_pos] + inp[start_pos:end_pos].lower() + inp[end_pos:]

    return sympify(inp)


if __name__ == "__main__":
    x = Symbol('x')
    q = Symbol('q')
    y = x**2-2+5*q
    res = solveset(y, x, S.Reals)
    # print(res)
    a = 1
