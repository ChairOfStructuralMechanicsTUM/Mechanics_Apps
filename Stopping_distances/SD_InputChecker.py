from math import sqrt

from SD_Constants import acceptable_characters, numbers



def squeeze_string(s):
    # omit spaces
    return s.replace(" ","")

# check if input is empty
def isempty(input_string):
    input_string = squeeze_string(input_string)
    return True if len(input_string)==0 else False



def value_validation(v_input, old_val):
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


    
# # # # def validate_function(fct,x):
# # # #     #global acceptable_characters, numbers
# # # #     # change , to . so 0,5 becomes 0.5, thus rendering European notation readable by python
# # # #     fct= fct.replace(',','.')
# # # #     # check there are as many opening brackets as closing brackets
# # # #     if (fct.count('(')!=fct.count(')')):
# # # #         return False
# # # #     # set up while loop (for loop breaks at sqrt)
# # # #     n=len(fct)
# # # #     if (n==0):
# # # #         return False

# # # #     i=0
# # # #     while (i<n):
# # # #         # if the input contains a non valid character return false
# # # #         if (acceptable_characters.find(fct[i])==-1 and fct[i]!=x):
# # # #             return False
# # # #         # if user has written 2(3+1) instead of 2*(3+1)
# # # #         # or 2sqrt(3) instead of 2*sqrt(3)
# # # #         # or 2s instead of 2*s
# # # #         # or s(1+3) etc
# # # #         # add missing *
# # # #         if (i!=n-1 and (numbers.find(fct[i])!=-1 or fct[i]==x)
# # # #             and (fct[i+1]=='(' or fct[i+1]==u'\u221A' or fct[i+1]==x)):
# # # #             sTemp=fct[i+1:]
# # # #             fct=fct[:i+1]+"*"+sTemp
# # # #             n+=1
# # # #         # if character is sqrt (u'\u221A') then replace with python readable "sqrt"
# # # #         if (fct[i]==u'\u221A'):
# # # #             sTemp=fct[i+1:]
# # # #             fct=fct[:i]+"sqrt"+sTemp
# # # #             # increase i so as not to check the letters in sqrt
# # # #             i+=4
# # # #             # increase n so that the whole string is still checked
# # # #             n+=3
# # # #         elif (fct[i]=='^'):
# # # #             sTemp=fct[i+1:]
# # # #             fct=fct[:i]+"**"+sTemp
# # # #             # increase i so as not to check **
# # # #             i+=1
# # # #             # increase n so that the whole string is still checked
# # # #             n+=1
# # # #         i+=1

# # # #     return fct


# # # # def eval_fct(fct, x='s', val=0):
# # # #     # returns either "not valid" or the value of the given function

# # # #     # check if the given function is valid
# # # #     fct = validate_function(fct,x)
# # # #     if fct == False:
# # # #         print("Not a valid function!")
# # # #         return "not valid"
# # # #     else:
# # # #         # if false has not yet been returned then fct should be valid and can be used in eval function
# # # #         try:
# # # #             # create a variable with the appropriate name and test function
# # # #             exec(x+"="+str(val))
# # # #             # return it if everything works
# # # #             return eval(fct)
# # # #         except :
# # # #             # otherwise return False
# # # #             # no, do not return False, since it can be confused with zero
# # # #             #return False
# # # #             return "not valid"


