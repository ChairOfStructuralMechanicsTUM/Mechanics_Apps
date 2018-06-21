from string import find, count, replace
from math import sqrt

acceptable_characters=u"1234567890.+-*/^()\u221A "
numbers=u"1234567890."
    
def isEquation(equation,x):
    global acceptable_characters, numbers
    # change , to . so 0,5 becomes 0.5, thus rendering European notation readable by python
    equation=replace(equation,',','.')
    #print (equation)
    # check there are as many opening brackets as closing brackets
    if (count(equation,'(')!=count(equation,')')):
        return False
    #print("Brakets in Balance")
    # set up while loop (for loop breaks at sqrt)
    n=len(equation)
    if (n==0):
        #print("Input empty")
        return False
    #print("Input not empty")
    i=0
    while (i<n):
        # if the input contains a non valid character return false
        if (find(acceptable_characters,equation[i])==-1 and equation[i]!=x):
            #print("invalid character used")
            return False
        #print("character valid")
        # if user has written 2(3+1) instead of 2*(3+1)
        # or 2sqrt(3) instead of 2*sqrt(3)
        # or 2s instead of 2*s
        # or s(1+3) etc
        # add missing *
        if (i!=n-1 and (find(numbers,equation[i])!=-1 or equation[i]==x)
            and (equation[i+1]=='(' or equation[i+1]==u'\u221A' or equation[i+1]==x)):
            sTemp=equation[i+1:]
            equation=equation[:i+1]+"*"+sTemp
            n+=1
        # if character is sqrt (u'\u221A') then replace with python readable "sqrt"
        if (equation[i]==u'\u221A'):
            sTemp=equation[i+1:]
            equation=equation[:i]+"sqrt"+sTemp
            # increase i so as not to check the letters in sqrt
            i+=4
            # increase n so that the whole string is still checked
            n+=3
            #print("sqrt detected:")
            #print(equation)
        elif (equation[i]=='^'):
            sTemp=equation[i+1:]
            equation=equation[:i]+"**"+sTemp
            # increase i so as not to check **
            i+=1
            # increase n so that the whole string is still checked
            n+=1
        i+=1

    # if false has not yet been returned then the equation should be valid and can be used in eval function
    try:
        # create a variable with the appropriate name and test function
        exec(x+"=1")
        eval(equation)
        # return it if everything works
        return equation
    except :
        # otherwise return False
        return False
