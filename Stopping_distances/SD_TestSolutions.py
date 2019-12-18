#from string import find, count#, replace
from math import sqrt

acceptable_characters=u"1234567890.+-*/^()\u221A "
numbers=u"1234567890."
    
def validate_function(fct,x):
    #global acceptable_characters, numbers
    # change , to . so 0,5 becomes 0.5, thus rendering European notation readable by python
    fct= fct.replace(',','.')
    #print (fct)
    # check there are as many opening brackets as closing brackets
    if (fct.count('(')!=fct.count(')')):
        return False
    #print("Brakets in Balance")
    # set up while loop (for loop breaks at sqrt)
    n=len(fct)
    if (n==0):
        #print("Input empty")
        return False
    #print("Input not empty")
    i=0
    while (i<n):
        # if the input contains a non valid character return false
        if (acceptable_characters.find(fct[i])==-1 and fct[i]!=x):
            #print("invalid character used")
            return False
        #print("character valid")
        # if user has written 2(3+1) instead of 2*(3+1)
        # or 2sqrt(3) instead of 2*sqrt(3)
        # or 2s instead of 2*s
        # or s(1+3) etc
        # add missing *
        # # # print("--DEBUG: i,n = ", i,n)
        # # # print("--DEBUG: fct[i] = ", fct[i])
        # # # print("--DEBUG: fct = ", fct)# if fct[i]=='5' else pass
        if (i!=n-1 and (numbers.find(fct[i])!=-1 or fct[i]==x)
            and (fct[i+1]=='(' or fct[i+1]==u'\u221A' or fct[i+1]==x)):
            sTemp=fct[i+1:]
            fct=fct[:i+1]+"*"+sTemp
            n+=1
        # # # print("--DEBUG: fct = ", fct)# if fct[i]=='5' else pass
        # if character is sqrt (u'\u221A') then replace with python readable "sqrt"
        if (fct[i]==u'\u221A'):
            sTemp=fct[i+1:]
            fct=fct[:i]+"sqrt"+sTemp
            # increase i so as not to check the letters in sqrt
            i+=4
            # increase n so that the whole string is still checked
            n+=3
            # print("sqrt detected:")
            # print(fct)
        elif (fct[i]=='^'):
            sTemp=fct[i+1:]
            fct=fct[:i]+"**"+sTemp
            # increase i so as not to check **
            i+=1
            # increase n so that the whole string is still checked
            n+=1
        i+=1

    return fct


def eval_fct(fct, x='s', val=0):
    # returns either "not valid" or the value of the given function

    # check if the given function is valid
    fct = validate_function(fct,x)
    if fct == False:
        print("Not a valid function!")
        return "not valid"
    else:
        # if false has not yet been returned then fct should be valid and can be used in eval function
        try:
            # create a variable with the appropriate name and test function
            # # # print("val = ", val)
            # # # print("fct = ", fct)
            exec(x+"="+str(val))
            # # # # print("x = ", x)
            #print("s = ", s)
            #print(eval(fct))
            #eval(fct)
            # return it if everything works
            return eval(fct)
        except :
            # otherwise return False
            # no, do not return False, since it can be confused with zero
            #return False
            return "not valid"


