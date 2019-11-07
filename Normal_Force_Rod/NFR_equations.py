from __future__ import division # float division only, like in python 3
import numpy as np

from NFR_constants import(
        F, L, E, A, sigma, p0, T, alpha_T,
        xr_end, sol_reso, xr_start
        )
#from NFR_data_sources import (
#        x_samples ,samplesF, samplesU, global_variables
#        )

# equations for all cases used in the app
# used to compute the y-coordinates for the plots

# y1 are the y-coordinates for x in [0,L1]
# y2 are the y-coordinates for x in [L1,L] # attention!: local x from [0,L-L1]

    
## file-global variables
# set them here to avoid repeated evaluations
# does not work that way :(
# because only the first initial value stays, no change afterwards

# current load position
#L1 = load_position_slide.value

local_samples = dict(x1=[], x2=[], nsx1=0, nsx2=0)
#TODO: maybe even dict for all variables? (x1,x2,L1,E,A,...)
#TODO: would be better in case of FLEA being non-constant
#TODO: if not needed/wanted, also change global_variables to be called in 
#      compute_new_scenario and add the input ampl for calcNU -> shorter
#x1 = x_samples[x_samples<=L1]
#x2 = x_samples[x_samples>L1]
#
#num_samples_x1 = len(x1)
#num_samples_x2 = len(x2)




#######################
## point_load
#######################    
# left support fixed, right support fixed
def calcN_p_ff(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  ampl*F*(1.0-L1/L) * np.ones(num_samples_x1)
    y2 = -ampl*F*(L1/L)     * np.ones(num_samples_x2)
    #print("DEBUG: N_p_ff, y2",y2)
    return (y1,y2)
    
def calcU_p_ff(L1, ampl):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*F/(E*A)*(1.0-L1/L) * x1
    y2 = ampl*F/(E*A)*(L1/L) * ((L-L1) - x2)
    return (y1,y2)
    
# left support fixed, right support slides
def calcN_p_fs(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*F * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    #print("DEBUG: N_p_fs, y2",y2)
    return (y1,y2)

def calcU_p_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*F/(E*A) * x1
    y2 = ampl*F/(E*A) * L1 * np.ones(num_samples_x2)
    return (y1,y2)
    
# left support slides, right support fixed
def calcN_p_sf(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = -ampl*F * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_p_sf(L1, ampl):
    load_vals = ["x2","nsx1"]
    x2, num_samples_x1 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*F/(E*A) * (L-L1) * np.ones(num_samples_x1)
    y2 = ampl*F/(E*A) * ((L-L1) - x2)
    return (y1,y2)



#######################
## constant load
#######################    

# left support fixed, right support fixed
def calcN_c_ff(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*(L1 -0.5*L1*L1/L - x1)
    y2 = -0.5*ampl*p0*L1*(L1/L) * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_ff(L1, ampl):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    #y1 =  (1./(E*A))*(ampl*p0*L1*(1.0-0.5*L1/L)*x1 - 0.5*ampl*p0*x1*x1)
    y1 =  -ampl*p0*x1*x1/(2.0*E*A) + ampl*p0*L1/(E*A)*(1.0-L1/(2.0*L))*x1
    y2 = ampl*p0*L1*0.5*(L1/(L*E*A)) * ((L-L1) - x2)
    return (y1,y2)


# left support fixed, right support slides
def calcN_c_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*(L1 - x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*x1 * (-0.5*x1 + L1)/(E*A)
    y2 = (1./(2.0*E*A))*ampl*p0*L1*L1 * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_c_sf(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = -ampl*p0*x1
    y2 = -ampl*p0*L1 * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_c_sf(L1, ampl):
    load_vals = ["x1", "x2","nsx1", "nsx2"]
    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0/(E*A) * (-0.5*x1*x1 + L1*(L - 0.5*L1))
    y2 = ampl*p0*L1/(E*A) * ((L-L1) - x2)
    return (y1,y2)




#######################
## triangular load
#######################    

# left support fixed, right support fixed
def calcN_tri_ff(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  ampl*p0*L1*0.5*(1.0 - L1/(3.0*L)) - ampl*p0*x1*(1.0 - x1/(2*L1))
    y2 = -ampl*p0*L1*L1/(6.0*L) * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_ff(L1, ampl):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*x1*0.5*( 1.0/(3.0*L1)*x1*x1 - x1 + L1 - L1*L1/(3.0*L))/(E*A)
    y2 = ampl*p0*L1*(L1/(6.0*E*A*L)) * ((L-L1) - x2)
    return (y1,y2)


# left support fixed, right support slides
def calcN_tri_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*(x1*x1/(2.0*L1) - x1 + 0.5*L1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0*0.5*x1*(x1*x1/(3.0*L1) - x1 + L1)/(E*A)
    y2 = ampl*p0*L1*(L1/(6.0*E*A)) * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_tri_sf(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  ampl*(p0/L1)*x1*(0.5*x1 - L1)
    y2 = -ampl*p0*L1*0.5 * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_tri_sf(L1, ampl):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    #y1 = p0/(E*A) * (0.5*L*L1 - L1*L1/3.0 - x1*p0/(sigma*L1)*x1*x1)
    
    y1 = -ampl*p0*x1*x1/(2.0*E*A) + ampl*p0*x1*x1*x1/(6.0*E*A*L1) + ampl*p0*L1/(2.0*E*A)*(L-L1/3.0)
    y2 = ampl*p0*L1/(2.0*E*A)*(L-L1-x2)
    
    #y1 = ampl*p0/(E*A*6.0*L1) * (x1*x1*x1 - 3.0*x1*x1*L1 + 3.0*L - L1)
    #y2 = ampl*p0*0.5*L1/(E*A) * ((L-L1) - x2)
    # # # print("DBUG: comp grenze")
    # # # print(-ampl*p0*L1*L1/(2.0*E*A) + ampl*p0*L1*L1*L1/(6.0*E*A*L1) + ampl*p0*L1/(2.0*E*A)*(L-L1/3.0))
    # # # print( ampl*p0*L1/(2.0*E*A)*(L-L1-0.0))
    # # # print("--------")
    return (y1,y2)




#######################
## temperature
#######################    

# left support fixed, right support fixed
def calcN_temp_ff(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = -alpha_T*ampl*T*(L1/L)*E*A * np.ones(num_samples_x1)
    y2 = -alpha_T*ampl*T*(L1/L)*E*A * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_ff(L1, ampl):
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*ampl*T*x1 * (1.0 - (L1/L)) 
    y2 = alpha_T*ampl*T*(L1/L) * ((L-L1) - x2)
    #y2 = alpha_T*ampl*T*L1 * (1.0 - L1/L - x2/L)
    return (y1,y2)


# left support fixed, right support slides
def calcN_temp_fs(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_fs(L1, ampl):
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*ampl*T*x1
    y2 = alpha_T*ampl*T*L1 * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
def calcN_temp_sf(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = sigma * np.ones(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

def calcU_temp_sf(L1, ampl):
    load_vals = ["x1", "x2", "nsx1", "nsx2"]
    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*ampl*T*(x1-L1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)




# template:

#def calcN_p_sf(L1, ampl):
#    load_vals = ["x1", "x2", "nsx1", "nsx2"]
#    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
#    y1 = 1
#    y2 = 1
#    return (y1,y2)
#
#def calcU_p_sf(L1, ampl):
#    load_vals = ["x1", "x2", "nsx1", "nsx2"]
#    x1, x2, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
#    y1 = 1
#    y2 = 1
#    return (y1,y2)    
    
# empty sources for invalid cases (no plot)
def invalid_config(L1, ampl):
    #samplesF.data = dict(x=[], y=[])
    #samplesU.data = dict(x=[], y=[])
    return ([],[])
    
    





# dictionary for function handles to avoid large if/else-construct
# needs to be defined after the functions
fun_handle = {'Npff': calcN_p_ff, 'Npfs': calcN_p_fs, 'Npsf': calcN_p_sf, 'Npss': invalid_config,
              'Upff': calcU_p_ff, 'Upfs': calcU_p_fs, 'Upsf': calcU_p_sf, 'Upss': invalid_config,
              'Ncff': calcN_c_ff, 'Ncfs': calcN_c_fs, 'Ncsf': calcN_c_sf, 'Ncss': invalid_config,
              'Ucff': calcU_c_ff, 'Ucfs': calcU_c_fs, 'Ucsf': calcU_c_sf, 'Ucss': invalid_config,
              'Ntriff': calcN_tri_ff, 'Ntrifs': calcN_tri_fs, 'Ntrisf': calcN_tri_sf, 'Ntriss': invalid_config,
              'Utriff': calcU_tri_ff, 'Utrifs': calcU_tri_fs, 'Utrisf': calcU_tri_sf, 'Utriss': invalid_config,
              'Ntempff': calcN_temp_ff, 'Ntempfs': calcN_temp_fs, 'Ntempsf': calcN_temp_sf, 'Ntempss': invalid_config,
              'Utempff': calcU_temp_ff, 'Utempfs': calcU_temp_fs, 'Utempsf': calcU_temp_sf, 'Utempss': invalid_config
              }



# delegates to specific cases
def calcNU(ls_type, rs_type, load_type, L1, ampl):    
    ## preparation
    #samples_total = dict(x=x_samples, yN=None, yU=None)
    x_samples = np.linspace(xr_start,xr_end,sol_reso)
    
    # set them here to avoid repeated evaluations
    x1 = x_samples[x_samples<=L1]
    x2 = x_samples[x_samples>L1]
    # TODO: build in check for None-type to avoid error message
    #num_samples_x1 = len(x1)
    #num_samples_x2 = len(x2)
    # output for file-global function variables
    local_samples['x1'] = x1 # samples from [0,L1]
    local_samples['x2'] = x2 # samples from [L1,L]
    #print("DEBUG: first x2:",x2)
    local_samples['x2'] = np.linspace(0,xr_end-L1,sol_reso-len(x1))
    #print("DEBUG: second x2:",x2)
    local_samples['nsx1'] = len(x1) # number of samples in x1 array
    local_samples['nsx2'] = len(x2) # number of samples in x2 array
    #print("DBUG: len x1, x2", len(x1), len(x2))
    
    fun_str = ""
    
    # abbreviations for the load types
    if load_type==0:    # point load
        fun_str += "p"
    elif load_type==1:  # constant load
        fun_str += "c"
    elif load_type==2:  # triangular load
        fun_str += "tri"
    elif load_type==3:  # temperature load
        fun_str += "temp"
    
    # abbreviations for the left support types
    if ls_type==0:      # fixed left support
        fun_str += "f"
    elif ls_type==1:    # sliding left support
        fun_str += "s"
    
    # abbreviations for the right support types
    if rs_type==0:      # fixed right support
        fun_str += "f"
    elif rs_type==1:    # sliding left support
        fun_str += "s"
        
    
    fun_str_N = "N"+fun_str
    fun_str_U = "U"+fun_str
    
    funN = fun_handle[fun_str_N]
    funU = fun_handle[fun_str_U]
    
    
#    # TODO: outsource, no need to store the samples every time, only when L1 has changed
#    funN = None # function handle
#    funU = None # function handle
#    
#    ## selecting the correct functions
#    if load_type==0: # point load
#        if ls_type==0: # fixed left support
#            if rs_type==0: # fixed right support
#                funN = calcN_p_ff
#                funU = calcU_p_ff
#            else:          # sliding right support
#                funN = calcN_p_fs
#                funU = calcU_p_fs
#        else:           # sliding left support
#            if rs_type==0: # fixed right support
#                funN = calcN_p_sf
#                funU = calcU_p_sf
#            else:
#                invalid_config()
#                return
#    elif load_type==1: # constant load
#        if ls_type==0: # fixed left support
#            if rs_type==0: # fixed right support
#                funN = calcN_c_ff
#                funU = calcU_c_ff
#            else:          # sliding right support
#                funN = calcN_c_fs
#                funU = calcU_c_fs
#        else:           # sliding left support
#            if rs_type==0: # fixed right support
#                funN = calcN_c_sf
#                funU = calcU_c_sf
#            else:
#                invalid_config()
#                return
#    elif load_type==2: # triangular load
#        if ls_type==0: # fixed left support
#            if rs_type==0: # fixed right support
#                funN = calcN_tri_ff
#                funU = calcU_tri_ff
#            else:          # sliding right support
#                funN = calcN_tri_fs
#                funU = calcU_tri_fs
#        else:           # sliding left support
#            if rs_type==0: # fixed right support
#                funN = calcN_tri_sf
#                funU = calcU_tri_sf
#            else:
#                invalid_config()
#                return
#    elif load_type==3: # temperature
#        if ls_type==0: # fixed left support
#            if rs_type==0: # fixed right support
#                funN = calcN_temp_ff
#                funU = calcU_temp_ff
#            else:          # sliding right support
#                funN = calcN_temp_fs
#                funU = calcU_temp_fs
#        else:           # sliding left support
#            if rs_type==0: # fixed right support
#                funN = calcN_temp_sf
#                funU = calcU_temp_sf
#            else:
#                invalid_config()
#                return
#            
#    #TODO: or at least, if lambda functions won't work, make a list and only
#          # compare the values [1,0,1] or strings
#            
    (N1,N2) = funN(L1,ampl)
    (U1,U2) = funU(L1,ampl)
    
    ## combining and storing the results
#    samplesF.data['x'] = x_samples
#    samplesU.data['x'] = x_samples
#    samplesF.data['y'] = np.concatenate((N1,N2))
#    samplesU.data['y'] = np.concatenate((U1,U2))
    
    #samples_total['x']  = x_samples
    samples_total = dict(x=None, yN=None, yU=None)
    samples_total['yN'] = np.concatenate((N1,N2))
    samples_total['yU'] = np.concatenate((U1,U2))
    
    # # # print("DBUG: funN=",funN)
    # # # print("DBUG: funU=",funU)
    # # # print("DBUG: yN=",samples_total['yN'])
    # # # print("DBUG: yU=",samples_total['yU'])
    if samples_total['yN'].size==0 or samples_total['yU'].size==0:
        samples_total['x'] = []
    else:
        samples_total['x']  = x_samples
    
    #samplesN = np.concatenate((N1,N2))
    #samplesU = np.concatenate((U1,U2))
    
    return samples_total
    
    
#TODO: check if switching to lambda functions reduces code and/or time
    # or in other words: find a better selection process
    # need to put the sub-functions in another file most likely
