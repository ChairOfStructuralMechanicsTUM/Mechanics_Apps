from math import sqrt

from SD_Constants import acceptable_characters, numbers

from SD_InputChecker import validate_function




# TODO?: add a function to derive the exact formulas



def eval_fct(fct, x='s', val=0):
    # returns either "not valid" or the value of the given function

    # check if the given function is valid
    [valid, fct] = validate_function(fct,x)
    if not valid:
        print("Not a valid function!")
        exception_str =  "in eval_fct:  Input function should be valid at this point but is not. Revisit input checks!\n"
        exception_str += "given function: " + ">>>>>>" + fct + "<<<<<<"
        raise Exception(exception_str)
        #return "not valid"
    else:
        # if false has not yet been returned then fct should be valid and can be used in eval function
        try:
            # create a variable with the appropriate name and test function
            exec(x+"="+str(val))
            # return it if everything works
            return eval(fct)
        except :
            # otherwise return False
            # no, do not return False, since it can be confused with zero
            #return False
            #return "not valid"
            exception_str =  "in eval_fct:  Error evaluating the function.\n"
            exception_str += "given function: " + ">>>>>>" + fct + "<<<<<<"
            raise Exception(exception_str)



