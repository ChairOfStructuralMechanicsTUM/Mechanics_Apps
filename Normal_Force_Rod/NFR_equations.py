from __future__ import division # float division only, like in python 3
import numpy as np

from NFR_constants import(
        F, L, E, A, sigma, p0, T, alpha_T
        )
from NFR_data_sources import (
        x_samples ,samplesF, samplesU
        )
from NFR_buttons import (
        load_position_slide
        )


# equations for all cases used in the app
# used to compute the y-coordinates for the plots

# y1 are the y-coordinates for x in [0,L1]
# y2 are the y-coordinates for x in [L1,L] # attention!: local x from [0,L-L1]


## file-global variables
# set them here to avoid repeated evaluations
# does not work that way :(

# current load position
#L1 = load_position_slide.value

local_samples = dict(x1=[], x2=[], nsx1=0, nsx2=0)
#TODO: maybe even dict for all variables? (x1,x2,L1,E,A,...)
#TODO: would be better in case of FLEA being non-constant
#x1 = x_samples[x_samples<=L1]
#x2 = x_samples[x_samples>L1]
#
#num_samples_x1 = len(x1)
#num_samples_x2 = len(x2)



# delegates to specific cases
def calcN(ls_type, rs_type, load_type, L1):    
    ## preparation
    # set them here to avoid repeated evaluations
    x1 = x_samples[x_samples<=L1]
    x2 = x_samples[x_samples>L1]
    #num_samples_x1 = len(x1)
    #num_samples_x2 = len(x2)
    # output for file-global function variables
    local_samples['x1'] = x1 # samples from [0,L1]
    local_samples['x2'] = x2 # samples from [L1,L]
    local_samples['nsx1'] = len(x1) # number of samples in x1 array
    local_samples['nsx2'] = len(x2) # number of samples in x2 array
    # TODO: outsource, no need to store the samples every time, only when L1 has changed
    funN = None # function handle
    funU = None # function handle
    
    ## selecting the correct functions
    if load_type==0: # point load
        if ls_type==0: # fixed left support
            if rs_type==0: # fixed right support
                funN = calcN_p_ff
                funU = calcU_p_ff
            else:          # sliding right support
                funN = calcN_p_fs
                funU = calcU_p_fs
        else:           # sliding left support
            if rs_type==0: # fixed right support
                funN = calcN_p_sf
                funU = calcU_p_sf
            else:
                invalid_config()
                return
    elif load_type==1: # constant load
        if ls_type==0: # fixed left support
            if rs_type==0: # fixed right support
                funN = calcN_c_ff
                funU = calcU_c_ff
            else:          # sliding right support
                funN = calcN_c_fs
                funU = calcU_c_fs
        else:           # sliding left support
            if rs_type==0: # fixed right support
                funN = calcN_c_sf
                funU = calcU_c_sf
            else:
                invalid_config()
                return
    elif load_type==2: # triangular load
        if ls_type==0: # fixed left support
            if rs_type==0: # fixed right support
                funN = calcN_tri_ff
                funU = calcU_tri_ff
            else:          # sliding right support
                funN = calcN_tri_fs
                funU = calcU_tri_fs
        else:           # sliding left support
            if rs_type==0: # fixed right support
                funN = calcN_tri_sf
                funU = calcU_tri_sf
            else:
                invalid_config()
                return
    elif load_type==3: # temperature
        if ls_type==0: # fixed left support
            if rs_type==0: # fixed right support
                funN = calcN_temp_ff
                funU = calcU_temp_ff
            else:          # sliding right support
                funN = calcN_temp_fs
                funU = calcU_temp_fs
        else:           # sliding left support
            if rs_type==0: # fixed right support
                funN = calcN_temp_sf
                funU = calcU_temp_sf
            else:
                invalid_config()
                return
            
    #TODO: or at least, if lambda functions won't work, make a list and only
          # compare the values [1,0,1]
            
    (N1,N2) = funN(L1)
    (U1,U2) = funU(L1)
    
    ## combining and storing the results
    samplesF.data['x'] = x_samples
    samplesU.data['x'] = x_samples
    samplesF.data['y'] = np.concatenate((N1,N2))
    samplesU.data['y'] = np.concatenate((U1,U2))
    
#TODO: check if switching to lambda functions reduces code and/or time
    # or in other words: find a better selection process
    # need to put the sub-functions in another file most likely

#######################
## point_load
#######################    
# left support fixed, right support fixed
def calcN_p_ff(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  F*(1.0-L1/L) * np.ones(num_samples_x1)
    y2 = -F*(L1/L)     * np.ones(num_samples_x2)
    #print("DEBUG: N_p_ff, y2",y2)
    return (y1,y2)
    
def calcU_p_ff(L1):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 =  F/(E*A)*(1.0-L1/L) * x1
    y2 = -F/(E*A)*(L1/L) * x2
    return (y1,y2)
    
# left support fixed, right support slides
def calcN_p_fs(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = F * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x1)
    #print("DEBUG: N_p_fs, y2",y2)
    return (y1,y2)

def calcU_p_fs(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = F/(E*A) * x1
    y2 = F/(E*A) * L1 * np.ones(num_samples_x2)
    return (y1,y2)
    
# left support slides, right support fixed
def calcN_p_sf(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = -F    * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_p_sf(L1):
    load_vals = ["x2","nsx1"]
    x2, num_samples_x1 = [local_samples.get(val) for val in load_vals]
    y1 =  F/(E*A) * (L-L1) * np.ones(num_samples_x1)
    y2 = -F/(E*A) * (x2 + (L-L1))
    return (y1,y2)



#######################
## constant load
#######################    

# left support fixed, right support fixed
def calcN_c_ff(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = L1*p0*(1.0-0.5*L1/L) - p0*x1
    y2 = -0.5*p0*L1*(L1/L) * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_ff(L1):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = p0*L1*(1.0-0.5*L1/L)*x1 - 0.5*p0*x1*x1
    y2 = -p0*L1*0.5*(L1/L) * (x2 - (L-L1))
    return (y1,y2)


# left support fixed, right support slides
def calcN_c_fs(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = p0*L1 * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_fs(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = p0*x1 * (-0.5*x1 + L1)
    y2 = 0.5*p0*L1*L1 * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_c_sf(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = -p0*x1
    y2 = -p0*L1 * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_sf(L1):
    load_vals = ["x1", "x2","nsx1", "nsx2"]
    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  p0/(E*A) * (-0.5*x1*x1 + L1*L)
    y2 = -p0*L1/(E*A) * (x2 - (L-L1))
    return (y1,y2)




#######################
## triangular load
#######################    

# left support fixed, right support fixed
def calcN_tri_ff(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = p0*L1*(0.5-L1/(3.0*L)) -(0.5*p0/L1)*x1*x1
    y2 = -p0*L1*L1/(3*L) * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_ff(L1):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 =  p0*x1*( -1.0/(6.0*L1)*x1*x1 + 0.5*L1 - L1*L1/(3*L))
    y2 = -p0*L1*(L1/3.0) * ((1.0/L)*x2 -1.0 + L1/L )
    return (y1,y2)


# left support fixed, right support slides
def calcN_tri_fs(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = 0.5*p0*L1 * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_fs(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = 0.5*p0*x1*(L1 - 1.0/(3*L1)*x1*x1 )
    y2 = L1*p0*L1/3.0 * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_tri_sf(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = -0.5*(p0/L1)*x1*x1
    y2 = -0.5*p0*L1 * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_sf(L1):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = p0/(E*A) * (0.5*L*L1 - L1*L1/3.0 - x1*p0/(sigma*L1)*x1*x1)
    y2 = 0.5*L1*p0/(E*A) * (-1.0*x2 + (L-L1))
    return (y1,y2)




#######################
## temperature
#######################    

# left support fixed, right support fixed
def calcN_temp_ff(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = -alpha_T*T*(L1/L)*E*A * np.ones(num_samples_x1)
    y2 = -alpha_T*T*(L1/L)*E*A * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_ff(L1):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*T*x1 * (1.0 - E*A*(L1/L))
    y2 = alpha_T*T*(L1/L) * ((L-L1) - E*A*x2)
    return (y1,y2)


# left support fixed, right support slides
def calcN_temp_fs(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_fs(L1):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*T*x1
    y2 = alpha_T*T*L1 * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_temp_sf(L1):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_sf(L1):
    load_vals = ["x1", "x2", "nsx1", "nsx2"]
    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*T*(x1-L1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)




# template:

#def calcN_p_sf(L1):
#    load_vals = ["x1", "x2", "nsx1", "nsx2"]
#    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
#    y1 = 1
#    y2 = 1
#    return (y1,y2)
#
#def calcU_p_sf(L1):
#    load_vals = ["x1", "x2", "nsx1", "nsx2"]
#    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
#    y1 = 1
#    y2 = 1
#    return (y1,y2)    
    
# empty sources for invalid cases (no plot)
def invalid_config():
    samplesF.data = dict(x=[], y=[])
    samplesU.data = dict(x=[], y=[])
    
    