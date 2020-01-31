"""
Normal Force Rod - force and deformation equations

"""
# general imports
from __future__ import division # float division only, like in python 3
import numpy as np

# bokeh imports

# internal imports
from NFR_constants import(
        F, L, E, A, sigma, p0, T, alpha_T,
        xr_end, sol_reso, xr_start
        )

# latex integration

#---------------------------------------------------------------------#

# write sample data in this dict
local_samples = dict(x1=[], x2=[], nsx1=0, nsx2=0)



########################
##     point_load     ##
########################    
# left support fixed, right support fixed
def calcN_p_ff(L1, ampl):
    load_vals = ["nsx1", "nsx2"]
    num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 =  ampl*F*(1.0-L1/L) * np.ones(num_samples_x1)
    y2 = -ampl*F*(L1/L)     * np.ones(num_samples_x2)
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
##   constant load   ##
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
    load_vals = ["x1", "x2"]
    x1, x2 = [local_samples.get(val) for val in load_vals]
    y1 = ampl*p0/(E*A) * (-0.5*x1*x1 + L1*(L - 0.5*L1))
    y2 = ampl*p0*L1/(E*A) * ((L-L1) - x2)
    return (y1,y2)




#######################
##  triangular load  ##
#######################

# decorators @np.errstate(divide='ignore',invalid='ignore') ignore the
# zero div warning message, since the zero div errors are all handled in try-except-blocks here

# left support fixed, right support fixed
@np.errstate(divide='ignore',invalid='ignore')
def calcN_tri_ff(L1, ampl):
    load_vals = ["x1", "nsx1", "nsx2"]
    x1, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    try:
        y1 = ampl*p0*L1*0.5*(1.0 - L1/(3.0*L)) - ampl*p0*x1*(1.0 - x1/(2*L1))
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = -ampl*p0*L1*L1/(6.0*L) * np.ones(num_samples_x2)
    return (y1,y2)

@np.errstate(divide='ignore',invalid='ignore')
def calcU_tri_ff(L1, ampl):
    load_vals = ["x1", "x2", "nsx1"]
    x1, x2, num_samples_x1 = [local_samples.get(val) for val in load_vals]
    try:
        y1 = ampl*p0*x1*0.5*( 1.0/(3.0*L1)*x1*x1 - x1 + L1 - L1*L1/(3.0*L))/(E*A)
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = ampl*p0*L1*(L1/(6.0*E*A*L)) * ((L-L1) - x2)
    return (y1,y2)


# left support fixed, right support slides
@np.errstate(divide='ignore',invalid='ignore')
def calcN_tri_fs(L1, ampl):
    load_vals = ["x1", "nsx1", "nsx2"]
    x1, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    try:
        y1 = ampl*p0*(x1*x1/(2.0*L1) - x1 + 0.5*L1)
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)

@np.errstate(divide='ignore',invalid='ignore')
def calcU_tri_fs(L1, ampl):
    load_vals = ["x1", "nsx1", "nsx2"]
    x1, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    try:
        y1 = ampl*p0*0.5*x1*(x1*x1/(3.0*L1) - x1 + L1)/(E*A)
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = ampl*p0*L1*(L1/(6.0*E*A)) * np.ones(num_samples_x2)
    return (y1,y2)


# left support slides, right support fixed
@np.errstate(divide='ignore',invalid='ignore')
def calcN_tri_sf(L1, ampl):
    load_vals = ["x1", "nsx1", "nsx2"]
    x1, num_samples_x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    try:
        y1 =  ampl*(p0/L1)*x1*(0.5*x1 - L1)
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = -ampl*p0*L1*0.5 * np.ones(num_samples_x2)
    return (y1,y2)

@np.errstate(divide='ignore',invalid='ignore')
def calcU_tri_sf(L1, ampl):
    load_vals = ["x1", "x2", "nsx1"]
    x1, x2, num_samples_x1 = [local_samples.get(val) for val in load_vals]
    #y1 = p0/(E*A) * (0.5*L*L1 - L1*L1/3.0 - x1*p0/(sigma*L1)*x1*x1)
    try:
        y1 = -ampl*p0*x1*x1/(2.0*E*A) + ampl*p0*x1*x1*x1/(6.0*E*A*L1) + ampl*p0*L1/(2.0*E*A)*(L-L1/3.0)
    except ZeroDivisionError:
        y1 = np.zeros(num_samples_x1)
    y2 = ampl*p0*L1/(2.0*E*A)*(L-L1-x2)
    return (y1,y2)


#######################
##    temperature    ##
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
    load_vals = ["x1", "nsx2"]
    x1, num_samples_x2 = [local_samples.get(val) for val in load_vals]
    y1 = alpha_T*ampl*T*(x1-L1)
    y2 = sigma * np.ones(num_samples_x2)
    return (y1,y2)


# ------------------------------------------------------#
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
# ------------------------------------------------------#


# empty sources for invalid cases (no plot)
def invalid_config(L1, ampl):
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
    ## -- preparation -- ##
    x_samples = np.linspace(xr_start,xr_end,sol_reso)
    
    # set them here to avoid repeated evaluations
    x1 = x_samples[x_samples<=L1]
    x2 = x_samples[x_samples>L1]
    # output for file-global function variables
    local_samples['x1'] = x1 # samples from [0,L1]
    local_samples['x2'] = x2 # samples from [L1,L]
    local_samples['x2'] = np.linspace(0,xr_end-L1,sol_reso-len(x1))
    local_samples['nsx1'] = len(x1) # number of samples in x1 array
    local_samples['nsx2'] = len(x2) # number of samples in x2 array
    

    ## -- building the function sring -- ##
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

    ## -- calling the functions -- ##
    
    funN = fun_handle[fun_str_N]
    funU = fun_handle[fun_str_U]
        
    (N1,N2) = funN(L1,ampl)
    (U1,U2) = funU(L1,ampl)
    
    ## -- combining and storing the results -- ##
    samples_total = dict(x=None, yN=None, yU=None)
    samples_total['yN'] = np.concatenate((N1,N2))
    samples_total['yU'] = np.concatenate((U1,U2))
    
    if samples_total['yN'].size==0 or samples_total['yU'].size==0:
        samples_total['x'] = []
    else:
        samples_total['x'] = x_samples
    

    return samples_total
