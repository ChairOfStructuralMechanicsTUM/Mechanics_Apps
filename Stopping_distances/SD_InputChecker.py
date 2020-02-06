from math import sqrt
import re

from SD_Constants import acceptable_characters, numbers



def squeeze_string(s):
    # omit spaces
    return s.replace(" ","")

# check if input is empty
def isempty(input_string):
    input_string = squeeze_string(input_string)
    return True if len(input_string)==0 else False



def validate_value(v_input, old_val):
    # Input:   v_input      string
    #          old_val      float
    # Output:  isValid      bool
    #          new_val      float
    # True  if input value is valid, new input value will be returned
    # False if input value is invalid, old value will be returned
    #TODO:? restriction to a meaningful range

    isValid = False

    # replace , with . i.e. change 0,5 to 0.5
    v = squeeze_string(v_input).replace(',','.')
    try:
        # convert input to float, if this is not possible then a ValueError is thrown
        new_val = float(v)
        isValid = True
    except ValueError:
        # if conversion was unsuccesful then return old value
        new_val = old_val
        isValid = False
    
    return [isValid, new_val]


    
def validate_function(fct,x):
    # Input:    fct         string      representing the function under consideration
    #           x           character   the independent variable
    # Output:   isValid     bool
    #           fct         string      evaluateable function
    # If fct is invalid, it returns as an empty string.

    invalid_return = [False, ""]

    if isempty(fct):
        return invalid_return

    # change , to . so 0,5 becomes 0.5, thus rendering European notation readable by python
    fct = squeeze_string(fct).replace(',','.')

    # test if the input contains a non valid character
    if not all(characters in acceptable_characters + x for characters in fct):
        return invalid_return

    # check if there are as many opening brackets as closing brackets
    if (fct.count('(')!=fct.count(')')):
        return invalid_return

    # check if there are repeating mathematical operators  (only one operator next to a number or parenthesis allowed!)
    # replace all operators by "?"
    test_op_str = re.sub('[\+\-\*\/\^]','?',fct)
    # find repeating operators
    list_rep_op = re.findall(r"\?{2,}",test_op_str)
    # if there are any reps, not valid
    if len(list_rep_op)>0:
        return invalid_return

    # check if the function starts with * or / or ^
    if fct[0]=='*' or fct[0]=='/' or fct[0]=='^':
        return invalid_return

    # check for empty parentheses
    list_empty_p = re.findall("\( {0,}\)",fct)
    if len(list_empty_p)>0:
        return invalid_return

    # check whether an opening paranthesis is followed by *, / or ^
    list_op_after_oppar = re.findall("\([\^\*\/]",fct)
    if len(list_op_after_oppar)>0:
        return invalid_return


    # add missing * between closing and opening parantheses
    # i.e. (...)(...) becomes (...)*(...)
    fct = fct.replace(")(", ")*(")

    # add missing * between ) and s
    # i.e. if user has written (3+1)s instead of (3+1)*s
    fct = fct.replace(")"+x, ")*"+x)
    # same with s and (
    # ie. if user has written s(3+1) instead of s*(3+1)
    fct = fct.replace(x+"(", x+"*(")
    
    # more complex, but covers more cases:
    # also accepts spaces but the string should already be squeezed at this point anyway, so the easy way above should also work
    # # # # tmp = re.findall(r"\) {0,}x",fct)
    # # # # for i in range(0,len(tmp)):
    # # # #     fct = fct.replace(tmp[i],tmp[i].replace('x','*x'))

    # add missing * between ) and sqrt
    fct = fct.replace(u")\u221A", u")*\u221A")

    # add missing * between the following cases: 
    # if user has written 2(3+1) instead of 2*(3+1)
    # or 2sqrt(3) instead of 2*sqrt(3)
    # or 2s instead of 2*s
    fct = re.sub(r"([0-9"+x+r"])([\u221A\("+x+r"])",r"\1*\2",fct)
    fct = re.sub(r"([0-9"+x+r"])([\u221A\("+x+r"])",r"\1*\2",fct)
    # needs repetition to cover cases like  2s√(3) or ssss... 

    # replace Matlab ^ with Python **
    fct = fct.replace("^", "**")

    # replace unicode square root with python readable "sqrt"
    fct = fct.replace(u"\u221A", "sqrt")


    # do not allow numbers after parentheses like   sqrt(s)5
    # and also no numbers after the variable like   s5 
    list_num_after_p = re.findall("[\)"+x+"][0-9]",fct)
    if len(list_num_after_p)>0:
        return invalid_return


    # if everything is fine
    return [True, fct]





