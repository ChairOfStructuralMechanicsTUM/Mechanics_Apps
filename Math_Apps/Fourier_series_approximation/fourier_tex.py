#==============================================================================
# Returns the correct leading sign, depending on coeff, the sign is encoded as
# a html request, since the TeX string will be sent via request (important for
# plus sign!). Additionaly the coeff is rounded to 2 digits.
#==============================================================================
def selective_str(coeff):
    if(round(coeff,3)==0):
        return ""
    elif(round(coeff,3)==1):
        return "%2B" # encoding for a plus sign in html request
    elif(round(coeff,3)==-1):
        return ""
    elif(coeff < 0):
        return ""+format(coeff,'.2f')
    else:
        return "%2B"+format(coeff,'.2f')
        
#==============================================================================
# Returns the value of k as a string. If k is equal to 1 an empty string is
# returned. This is particularly useful for expressions like k*something, where
# one does not want to show factors equal to 1.        
#==============================================================================
def k_str(k):
    if(k==1):
        return ""
    else:
        return str(k)            

#==============================================================================
# Returns a string of the format coeff*cos(k*x), if k is equal to 1 this factor
# is not displayed. The same holds for the coefficient. If the coefficient is
# small, then we omit its contribution and return an empty string.
#==============================================================================
def selective_str_cos(coeff,T,k):
    if(abs(coeff)<.01):
        return ""
    else:
        return selective_str(coeff)+"\\cos\\left("+k_str(k)+"x "+"\\frac{2\\pi}{"+str(round(T,3))+'}\\right)'        

#==============================================================================
# Returns a string of the format coeff*sin(k*x), if k is equal to 1 this factor
# is not displayed. The same holds for the coefficient. If the coefficient is
# small, then we omit its contribution and return an empty string.
#==============================================================================
def selective_str_sin(coeff,T,k):
    if(abs(coeff)<.01):
        return ""
    else:
        return selective_str(coeff)+"\sin\\left("+k_str(k)+"x "+"\\frac{2\\pi}{"+str(round(T,3))+'}\\right)'              

#==============================================================================
# Uses the functions from above to generate a TeX string of the fourier series
# representation with given coefficients a and b and the periodicity T.    
#==============================================================================
def generate_tex(a,b,T):
    TeX_string = ""
    N = len(a)-1
    print "generating TeX string for N = "+str(N)
    
    for k in range(0,N+1):
        if(k == 0):
            if(round(a[k],3) != 0):
                TeX_string += str(a[k])
        else:
            TeX_string += selective_str_cos(a[k],T,k)+selective_str_sin(b[k],T,k)                    
    
    if(TeX_string[0:3]=='%2B'):
        TeX_string = TeX_string[3:len(TeX_string)] #remove leading plus if there is one
        
    if(TeX_string==""):
        TeX_string="0"
        
    TeX_string = "   f(x)="+TeX_string+"   "
        
    print "sending the following TeX string: "+TeX_string
    return TeX_string