# general imports
from math import sqrt

# bokeh imports

# internal imports
from SD_Constants import acceptable_characters, numbers
from SD_InputChecker import validate_function

# latex integration

#---------------------------------------------------------------------#



def eval_fct(fct, x='s', val=0):
    # returns either the value of the given function for x=val or throws an exception

    # check if the given function is valid
    [valid, fct] = validate_function(fct,x)
    if not valid:
        print("Not a valid function!")
        exception_str =  "in eval_fct:  Input function should be valid at this point but is not. Revisit input checks!\n"
        exception_str += "given function: " + " >>>>>>  " + fct + "  <<<<<< "
        raise Exception(exception_str)
    else:
        # if false has not yet been returned then fct should be valid and can be used in eval function
        try:
            # create a variable with the appropriate name and test function
            exec(x+"="+str(val))
            # return it if everything works
            return eval(fct)
        except:
            # might be the case for example for zero division or negative roots
            exception_str =  "in eval_fct:  Error evaluating the function.\n"
            exception_str += "given function: " + " >>>>>>  " + fct + "  <<<<<< " + "for " + str(x) + " = " + str(val)
            exception_str += "\nMost likely a negative root or zero division."
            #raise Exception(exception_str)
            print(exception_str)

            # return zero to proceed
            return 0



