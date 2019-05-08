from __future__ import division
import numpy as np
from numpy import cos, sin, sqrt, pi, exp
from numpy.fft import fft, fftshift, ifft, ifftshift
from bokeh.layouts import column, row, widgetbox, layout
from bokeh.models.widgets import Div, RadioButtonGroup, DataTable, TableColumn
from bokeh.models.annotations import Title
from bokeh.models import ColumnDataSource, Button, Slider, Range1d, Plot, Label
from bokeh.models import LinearAxis, Grid, PanTool, WheelZoomTool, SaveTool
from bokeh.models import BoxZoomTool, Arrow, NormalHead, ResetTool, RangeSlider
from bokeh.models.layouts import Spacer
from bokeh.io import curdoc
from bokeh.models.glyphs import Line, Annulus
from bokeh.plotting import figure, show
# latex support
from os.path import dirname, join, split, abspath
import sys, inspect
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), 'shared/')
sys.path.insert(0,parentdir)
from latex_support import LatexDiv, LatexLabel, LatexLabelSet
from latex_support import LatexSlider, LatexLegend





###############################################################################
###############################################################################
# WAVE PROPAGATION APP
# 
# Bachelor thesis Nr.71
# date: 07. Mai 2019
# author: Simon Pleyer (simon.pleyer_at_tum.de)
# Python 2.7.15
# bokeh 1.0.2
# numpy 1.14.2
###############################################################################
# SHORT DESCRIPTION
# 
# This App visualizes the basic wave propagation phenomena in the ground. The
# soil is modelled as a homogeneous, isotropic, linear-elastic half-space with
# a vertical harmonically pulsating load on the surface.
# The plot on the left shows the total displacement of several particles in the
# soil.
# The plot on the right shows the displacement components of the potentials for 
# one specific soil particle. 
###############################################################################
# POTENTIAL IMPROVEMENTS AND OPEN ISSUES  
# 
# 1. The interval for the calculation in x-dircetion (B=16m) and the distance
#    between the particles (dx=0.0625m) is fixed. This leads to superposition
#    of waves and large displacementa at the borders of the interval. The
#    displacement should be close to zero.
#    -> chose B and the dx according to Omega und the wavelength of the
#       Rayleigh wave
# 2. Three-dimensional wave propagation
# 3. Excitaion from the ground
# 4. Multiple soil layers
# 5. Horizontal excitation
# 6. Non-harmonic excitations
# 7. Resize axis ranges of potentials plot automatically
# 8. Disable RadioButtonGroup (p0 on/off) when play is active
# 9. Reset RadioButtonGroup (p0 on/off) to p0=1 when reset-button was pressed
###############################################################################
###############################################################################





###############################################################################
# define global variables #####################################################
###############################################################################
# input values
initial_zeta = 0.3
initial_ny = 0.3
initial_Omega = 100
initial_b = 3
initial_p0 = 1
global_zeta = ColumnDataSource(data = dict(zeta = [initial_zeta]))
global_ny = ColumnDataSource(data = dict(ny = [initial_ny]))
global_Omega = ColumnDataSource(data = dict(Omega = [initial_Omega]))
global_b = ColumnDataSource(data = dict(b = [initial_b]))
global_p0 = ColumnDataSource(data = dict(p0 = [initial_p0]))

# change z-range with Slider or automatically with Omega
initial_zrange = (0,50)
initial_slider_zrange = (0,50)
initial_lamb_zrange = (0,50)
global_zrange = ColumnDataSource(data = dict(zrange = [initial_zrange]))
global_slider_zrange = ColumnDataSource(data =
 dict(slider_zrange = [initial_slider_zrange]))
global_lamb_zrange = ColumnDataSource(data =
 dict(lamb_zrange = [initial_lamb_zrange]))

# change x-range with Slider
initial_x_range = (-5,5)
global_x_range = ColumnDataSource(data = dict(x_range = [initial_x_range]))

# select particle for potential displacements
initial_chosen_x = -3
initial_chosen_z = 2
global_chosen_x = ColumnDataSource(data = dict(chosen_x = [initial_chosen_x]))
global_chosen_z = ColumnDataSource(data = dict(chosen_z = [initial_chosen_z]))
initial_chosen_x_value = -2.1875
initial_chosen_z_value = 1.9
global_chosen_x_value = ColumnDataSource(data = 
                            dict(chosen_x_value = [initial_chosen_x_value]))
global_chosen_z_value = ColumnDataSource(data = 
                            dict(chosen_z_value = [initial_chosen_z_value]))

# general parameters
global_E = ColumnDataSource(data = dict(E = []))
global_rho = ColumnDataSource(data = dict(rho = []))
global_my = ColumnDataSource(data = dict(my = []))
global_lamb = ColumnDataSource(data = dict(lamb = []))
global_c_p = ColumnDataSource(data = dict(c_p = []))
global_lamb_p = ColumnDataSource(data = dict(lamb_p = []))
global_k_p = ColumnDataSource(data = dict(k_p = []))
global_c_s = ColumnDataSource(data = dict(c_s = []))
global_lamb_s = ColumnDataSource(data = dict(lamb_s = []))
global_k_s = ColumnDataSource(data = dict(k_s = []))
global_c_r = ColumnDataSource(data = dict(c_r = []))
global_lamb_r = ColumnDataSource(data = dict(lamb_r = []))
global_k_r = ColumnDataSource(data = dict(k_r = []))

# load parameters
global_P = ColumnDataSource(data = dict(P = []))
global_x = ColumnDataSource(data = dict(x = []))
global_B = ColumnDataSource(data = dict(B = []))
global_kx = ColumnDataSource(data = dict(kx = []))
global_z = ColumnDataSource(data = dict(z = []))

# reducing number of particles
initial_select_z = np.array([
                    [ 0], [4], [8], [13], [19], [25], [31], [37], [43], 
                    [49], [55], [61], [67], [73], [79]
                    ])
initial_select_x = [0, 20, 40, 60, 80, 100, 116, 128, 139, 155, 175, 195, 215,
                   235, 255]                   
global_select_z = ColumnDataSource(data =dict(select_z = [initial_select_z]))
global_select_x = ColumnDataSource(data = dict(select_x = [initial_select_x]))
global_x_short = ColumnDataSource(data = dict(x_short = []))
global_z_short = ColumnDataSource(data = dict(z_short = []))

# solve halfspace parameters
# _f ... Fourier domain (kx)
# _o ... IFT in (kx - x)
global_A_2_f = ColumnDataSource(data = dict(A_2_f = []))
global_B_x2_f = ColumnDataSource(data = dict(B_x2_f = []))
global_B_y2_f = ColumnDataSource(data = dict(B_y2_f = []))
global_Phi_f = ColumnDataSource(data = dict(Phi_f = []))
global_Psi_x_f = ColumnDataSource(data = dict(Psi_x_f = []))
global_Psi_y_f = ColumnDataSource(data = dict(Psi_y_f = []))
global_u_f = ColumnDataSource(data = dict(u_f = []))
global_w_f = ColumnDataSource(data = dict(w_f = []))
global_lamb1_f = ColumnDataSource(data = dict(lamb1_f = []))
global_lamb2_f = ColumnDataSource(data = dict(lamb2_f = []))
global_u_o = ColumnDataSource(data = dict(u_o = []))
global_w_o = ColumnDataSource(data = dict(w_o = []))
global_u_o_short = ColumnDataSource(data = dict(u_o_short = []))
global_w_o_short = ColumnDataSource(data = dict(w_o_short = []))

# solve potentials parameters
global_dPhi_f_dx = ColumnDataSource(data = dict(dPhi_f_dx = []))
global_dPhi_f_dz = ColumnDataSource(data = dict(dPhi_f_dz = []))
global_dPsi_y_f_dx = ColumnDataSource(data = dict(dPsi_y_f_dx = []))
global_dPsi_y_f_dz = ColumnDataSource(data = dict(dPsi_y_f_dz = []))
global_dPhi_o_dx = ColumnDataSource(data = dict(dPhi_o_dx = []))
global_dPhi_o_dz = ColumnDataSource(data = dict(dPhi_o_dz = []))
global_dPsi_y_o_dx = ColumnDataSource(data = dict(dPsi_y_o_dx = []))
global_dPsi_y_o_dz = ColumnDataSource(data = dict(dPsi_y_o_dz = []))
global_dPhi_o_dx_short = ColumnDataSource(data = dict(dPhi_o_dx_short = []))
global_dPhi_o_dz_short = ColumnDataSource(data = dict(dPhi_o_dz_short = []))
global_dPsi_y_o_dx_short = ColumnDataSource(data =
 dict(dPsi_y_o_dx_short = []))
global_dPsi_y_o_dz_short = ColumnDataSource(data =
 dict(dPsi_y_o_dz_short = []))
global_dPhi_dx = ColumnDataSource(data = 
 dict(dPhi_dx = [np.zeros((len(initial_select_z),len(initial_select_z)),
                          dtype = complex)]))
global_dPhi_dz = ColumnDataSource(data = 
 dict(dPhi_dz = [np.zeros((len(initial_select_z),len(initial_select_z)),
                          dtype = complex)]))
global_dPsi_y_dx = ColumnDataSource(data = 
 dict(dPsi_y_dx = [np.zeros((len(initial_select_z),len(initial_select_z)),
                            dtype = complex)]))
global_dPsi_y_dz = ColumnDataSource(data = 
 dict(dPsi_y_dz = [np.zeros((len(initial_select_z),len(initial_select_z)),
                            dtype = complex)]))

# rayleigh parameters
global_c_r_c_s = ColumnDataSource(data = dict(c_r_c_s = []))
global_c_p_c_s = ColumnDataSource(data = dict(c_p_c_s = []))
global_beta_1 = ColumnDataSource(data = dict(beta_1 = []))
global_beta_2 = ColumnDataSource(data = dict(beta_2 = []))
global_C_2_C_1 = ColumnDataSource(data = dict(C_2_C_1 = []))
rayleigh_data_table = ColumnDataSource(data = {
                              'ny' : 
                              [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30,
                              0.35, 0.40, 0.45, 0.50],
                              'c_r_c_s' : 
                              [0.874032, 0.883695, 0.893106, 0.902220,
                              0.910996, 0.919402,0.927413, 0.935013, 0.942195,
                              0.948960, 0.955313],
                              'c_p_c_s' : 
                              [1.414214, 1.452966, 1.500000, 1.558387,
                              1.632993, 1.732051,1.870829, 2.081667, 2.449490,
                              3.316625, 10**25],
                              'beta_1' : 
                              [0.786151, 0.793783, 0.803426, 0.815367,
                              0.829929, 0.847487,0.868481, 0.893448, 0.923063,
                              0.958193, 1.000000],
                              'beta_2' : 
                              [0.485868, 0.468064, 0.449846, 0.431277,
                              0.412415, 0.393320,0.374040, 0.354613, 0.335064,
                              0.315397, 0.295598],
                              'C_2_C_1' : 
                              [-1.272020, -1.302263, -1.336414, -1.374987,
                              -1.418577, -1.467890,-1.523776, -1.587294,
                              -1.659785, -1.743000, -1.839287]
                                      })





###############################################################################
# output variables ############################################################
###############################################################################
# displacements in particles plot
global_u = ColumnDataSource(data = 
 dict(u = [np.zeros((len(initial_select_z),len(initial_select_z)),
                    dtype = complex)]))
global_w = ColumnDataSource(data =
 dict(w = [np.zeros((len(initial_select_z),len(initial_select_z)),
                    dtype = complex)]))

# displacements plot
source_line = ColumnDataSource(data = dict( x =[-8,8], y = [0,0]))
surface_source = ColumnDataSource(data = dict(x = [-8,8], y = [0,0]))
initial_global_particle_source = ColumnDataSource(data = dict(x_coord = [],
                                                            z_coord = []))
global_particle_source = ColumnDataSource(data = 
                                          dict(x_coord = [],z_coord = []))
selected_Annulus_source = ColumnDataSource(data = 
                                           dict(x_coord = [],z_coord = []))

# data table containing wavespeed and wavelength and G
global_parameters_data_table_source = ColumnDataSource(data = 
 dict(lamb_p = [],c_p = [],lamb_s = [],c_s = [],lamb_r = [],c_r = [],my = []))

# data table containing coordinates of chosen x- and z-particle
global_chosen_particle_data_table_source = ColumnDataSource(data = 
 dict( chosen_x_value = [initial_chosen_x_value],
      chosen_z_value = [initial_chosen_z_value]))

# displacement components of potentials
global_dPhi_dx_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                            xE = [],zE = []))
global_dPhi_dz_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                            xE = [],zE = []))
global_dPsi_y_dx_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                              xE = [],zE = []))
global_dPsi_y_dz_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                              xE = [],zE = []))
total_potential_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                             xE = [],zE = []))
global_u_rayleigh_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                        xE = [],zE = []))
global_w_rayleigh_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                        xE = [],zE = []))
global_rayleigh_vector_source = ColumnDataSource(data = dict(xS = [],zS = [],
                                                             xE = [],zE = []))

# callback 
t = 0
global_slider_zrange_active = ColumnDataSource(data =
 dict(slider_zrange_active = [False]))
global_lamb_zrange_active = ColumnDataSource(data =
 dict(lamb_zrange_active = [False]))
global_t = ColumnDataSource(data=dict(t=[t]))
global_active = ColumnDataSource(data = dict(active = [False]))
global_callback_id = ColumnDataSource(dict(callback_id = [None]))





###############################################################################
# evaluate displacement and potentials with external load #####################
###############################################################################
def evolve1():
  [t] = global_t.data['t']
  [Omega] = global_Omega.data['Omega']
  [x_short] = global_x_short.data['x_short']
  [z_short] = global_z_short.data['z_short']
  [chosen_x] = global_chosen_x.data['chosen_x']
  [chosen_z] = global_chosen_z.data['chosen_z']
  [chosen_x_value] = global_chosen_x_value.data['chosen_x_value']
  [chosen_z_value] = global_chosen_z_value.data['chosen_z_value']   
  # displacements
  [u_o_short] = global_u_o_short.data['u_o_short']
  [w_o_short] = global_w_o_short.data['w_o_short']
  [u] = global_u.data['u']
  [w] = global_w.data['w']
  # potentials
  [dPhi_dx] = global_dPhi_dx.data['dPhi_dx']
  [dPhi_dz] = global_dPhi_dz.data['dPhi_dz']
  [dPsi_y_dx] = global_dPsi_y_dx.data['dPsi_y_dx']
  [dPsi_y_dz] = global_dPsi_y_dz.data['dPsi_y_dz']
  [dPhi_o_dx_short] = global_dPhi_o_dx_short.data['dPhi_o_dx_short']
  [dPhi_o_dz_short] = global_dPhi_o_dz_short.data['dPhi_o_dz_short']
  [dPsi_y_o_dx_short] = global_dPsi_y_o_dx_short.data['dPsi_y_o_dx_short']
  [dPsi_y_o_dz_short] = global_dPsi_y_o_dz_short.data['dPsi_y_o_dz_short']
  omega = -Omega

  # total displacements IFT (omega - t)
  for nzz in range(0,len(z_short)):
      for nxx in range(0,len(x_short)):
          u[nzz,nxx] = (u_o_short[nzz,nxx]*exp(-1j*omega*t)
                        + np.conjugate(u_o_short[nzz,nxx])*exp(1j*omega*t))
          w[nzz,nxx] = (w_o_short[nzz,nxx]*exp(-1j*omega*t) 
                        + np.conjugate(w_o_short[nzz,nxx])*exp(1j*omega*t))
          global_u.data = dict(u = [u])
          global_w.data = dict(w = [w])

  # scaling displacements
  delta_x = x_short[1]-x_short[0]
  delta_z = z_short[1]-z_short[0]
  scaling_factor_u = 10**6 * abs(delta_x) * Omega
  scaling_factor_w = 10**6 * abs(delta_z) * Omega
  u = scaling_factor_u * u.real
  w = scaling_factor_w * w.real

  # displacements list of lists to list
  u_flat = u.flatten()
  w_flat = w.flatten()
  # string together x- and z-coordinates for Annulus plot
  x_multiline = np.tile(x_short,len(x_short))
  z_multiline = - np.repeat(z_short,len(z_short))
  # add displacement to each particle
  x_u_multiline = x_multiline + u_flat
  z_w_multiline = z_multiline - w_flat

  # select particle to be highlighted
  shift = int((len(x_short)-1)/2)  
  x_annulus = x_short[chosen_x+shift] + u[chosen_z,chosen_x+shift]
  z_annulus = - z_short[chosen_z] - w[chosen_z,chosen_x+shift]
  
  chosen_x_value = x_short[chosen_x+shift]
  chosen_z_value = z_short[chosen_z]

  # output total displacements plot
  global_particle_source.data = dict(x_coord = x_u_multiline.tolist(),
                                   z_coord = z_w_multiline.tolist())     
  selected_Annulus_source.data= dict(x_coord = [x_annulus],
                                   z_coord = [z_annulus])
  if z_short[0] == 0:
    surface_source.data = dict(x = x_u_multiline[0:len(x_short)],
                                 y = z_w_multiline[0:len(x_short)])
  else:
    surface_source.data = dict(x = [],
                               y = [])

  # potentials IFT (omega - t)
  for nzz in range(0,len(z_short)):
      for nxx in range(0,len(x_short)):
          dPhi_dx[nzz,nxx] = dPhi_o_dx_short[nzz,nxx]*exp(-1j*omega*t) 
          + np.conjugate(dPhi_o_dx_short[nzz,nxx])*exp(1j*omega*t)
          dPhi_dz[nzz,nxx] = dPhi_o_dz_short[nzz,nxx]*exp(-1j*omega*t)
          + np.conjugate(dPhi_o_dz_short[nzz,nxx])*exp(1j*omega*t)
          dPsi_y_dx[nzz,nxx] = dPsi_y_o_dx_short[nzz,nxx]*exp(-1j*omega*t)
          + np.conjugate(dPsi_y_o_dx_short[nzz,nxx])*exp(1j*omega*t)
          dPsi_y_dz[nzz,nxx] = dPsi_y_o_dz_short[nzz,nxx]*exp(-1j*omega*t) 
          + np.conjugate(dPsi_y_o_dz_short[nzz,nxx])*exp(1j*omega*t)
          
          global_dPhi_dx.data = dict(dPhi_dx = [dPhi_dx])
          global_dPhi_dz.data = dict(dPhi_dz = [dPhi_dz])
          global_dPsi_y_dx.data = dict(dPsi_y_dx = [dPsi_y_dx])
          global_dPsi_y_dz.data = dict(dPsi_y_dz = [dPsi_y_dz])

  dPhi_dx = scaling_factor_u*dPhi_dx.real
  dPsi_y_dz = scaling_factor_u*dPsi_y_dz.real
  dPhi_dz = scaling_factor_w*dPhi_dz.real
  dPsi_y_dx = scaling_factor_w*dPsi_y_dx.real
  # chose selected particle
  dPhi_dx = dPhi_dx[chosen_z,chosen_x+shift]
  dPsi_y_dz = dPsi_y_dz[chosen_z,chosen_x+shift]
  dPhi_dz = dPhi_dz[chosen_z,chosen_x+shift]
  dPsi_y_dx = dPsi_y_dx[chosen_z,chosen_x+shift]
  u_ueberlager_ende = dPhi_dx - dPsi_y_dz
  w_ueberlager_ende = - dPhi_dz - dPsi_y_dx
  
  global_chosen_particle_data_table_source.data = dict(chosen_x_value=
                                                       [chosen_x_value],
                                                       chosen_z_value=
                                                       [chosen_z_value])

  # output potentials plot
  global_dPhi_dx_vector_source.data = dict(xS=[0],zS=[0],xE=[dPhi_dx],zE=[0])
  global_dPsi_y_dz_vector_source.data = dict(xS=[dPhi_dx],zS=[0],
                                            xE=[u_ueberlager_ende],zE=[0])
  global_dPhi_dz_vector_source.data = dict(xS=[0],zS=[0],xE=[0],
                                           zE=[dPhi_dz])
  global_dPsi_y_dx_vector_source.data = dict(xS=[0],zS=[dPhi_dz],
                                            xE=[0],zE=[w_ueberlager_ende])
  total_potential_vector_source.data = dict(xS=[0],zS=[0],
                                            xE=[u_ueberlager_ende],
                                            zE=[w_ueberlager_ende])





###############################################################################
# evaluate displacement and potentials without external load - Rayleigh only ##
###############################################################################
def evolve2():
  [t] = global_t.data['t']
  [Omega] = global_Omega.data['Omega']
  [x_short] = global_x_short.data['x_short']
  [z_short] = global_z_short.data['z_short']
  [chosen_x] = global_chosen_x.data['chosen_x']
  [chosen_z] = global_chosen_z.data['chosen_z']
  [chosen_x_value] = global_chosen_x_value.data['chosen_x_value']
  [chosen_z_value] = global_chosen_z_value.data['chosen_z_value']   
  # rayleigh parameters
  [k_r] = global_k_r.data['k_r']
  [beta_1] = global_beta_1.data['beta_1']
  [beta_2] = global_beta_2.data['beta_2']
  [c_r] = global_c_r.data['c_r']
  [C_2_C_1] = global_C_2_C_1.data['C_2_C_1']
  # displacements
  [u] = global_u.data['u']
  [w] = global_w.data['w']
  # potentials
  [dPhi_dx] = global_dPhi_dx.data['dPhi_dx']
  [dPhi_dz] = global_dPhi_dz.data['dPhi_dz']
  [dPsi_y_dx] = global_dPsi_y_dx.data['dPsi_y_dx']
  [dPsi_y_dz] = global_dPsi_y_dz.data['dPsi_y_dz']
  [dPhi_o_dx_short] = global_dPhi_o_dx_short.data['dPhi_o_dx_short']
  [dPhi_o_dz_short] = global_dPhi_o_dz_short.data['dPhi_o_dz_short']
  [dPsi_y_o_dx_short] = global_dPsi_y_o_dx_short.data['dPsi_y_o_dx_short']
  [dPsi_y_o_dz_short] = global_dPsi_y_o_dz_short.data['dPsi_y_o_dz_short']
  omega = -Omega
  
  # total displacements rayleigh equations
  for nzz in range(0,len(z_short)):
    for nxx in range(0,len(x_short)):
        u[nzz,nxx] = k_r*1*(exp(-beta_1*k_r*z_short[nzz])-0.5*(1+beta_2**2)
                            *exp(-beta_2*k_r*z_short[nzz]))*sin(k_r*
                            (x_short[nxx]-c_r*t))
        w[nzz,nxx] = k_r*C_2_C_1*(exp(-beta_2*k_r*z_short[nzz])
                                  -0.5*(1+beta_2**2)
                                  *exp(-beta_1*k_r*z_short[nzz]))*cos(k_r*
                                  (x_short[nxx]-c_r*t))
        global_u.data = dict(u = [u])
        global_w.data = dict(w = [w])

  # scaling displacements
  delta_x = x_short[1]-x_short[0]
  delta_z = z_short[1]-z_short[0]
  scaling_factor_u = 10**2 * abs(delta_x) / (Omega) 
  scaling_factor_w = 10**2 * abs(delta_z) / (Omega)
  u = scaling_factor_u * u.real
  w = scaling_factor_w * w.real
  
  # displacements list of lists to list
  u_flat = u.flatten()
  w_flat = w.flatten()
  # string together x- and z-coordinates for Annulus plot
  x_multiline = np.tile(x_short,len(x_short))
  z_multiline = - np.repeat(z_short,len(z_short))
  # add displacement to each particle
  x_u_multiline = x_multiline + u_flat
  z_w_multiline = z_multiline - w_flat

  # select particle to be highlighted
  shift = int((len(x_short)-1)/2)
  x_annulus = x_short[chosen_x+shift] + u[chosen_z,chosen_x+shift]
  z_annulus = - z_short[chosen_z] - w[chosen_z,chosen_x+shift]

  chosen_x_value = x_short[chosen_x+shift]
  chosen_z_value = z_short[chosen_z]

  global_chosen_particle_data_table_source.data = dict(chosen_x_value=
                                                       [chosen_x_value],
                                                       chosen_z_value=
                                                       [chosen_z_value])

  # output total displacements plot
  global_particle_source.data = dict(x_coord = x_u_multiline.tolist(),
                                   z_coord = z_w_multiline.tolist())     
  selected_Annulus_source.data= dict(x_coord = [x_annulus],
                                   z_coord = [z_annulus])
  if z_short[0] == 0:
    surface_source.data = dict(x = x_u_multiline[0:len(x_short)],
                               y = z_w_multiline[0:len(x_short)])
  else:
    surface_source.data = dict(x = [],
                               y = [])

  # potentials rayleigh equation
  chosen_u_rayleigh = u[chosen_z,chosen_x+shift]
  chosen_w_rayleigh = -w[chosen_z,chosen_x+shift]
  # output potentials plot

  global_u_rayleigh_source.data = dict(xS=[0],zS=[0],
                                       xE=[chosen_u_rayleigh],zE=[0])
  global_w_rayleigh_source.data = dict(xS=[0],zS=[0],
                                       xE=[0],zE=[chosen_w_rayleigh])
  global_rayleigh_vector_source.data = dict(xS=[0],zS=[0],
                                            xE=[chosen_u_rayleigh],
                                            zE=[chosen_w_rayleigh])





###############################################################################
# combine evole1() and evolve2() ##############################################
###############################################################################
def evolve():
  [t] = global_t.data['t']
  dt = 0.01
  [p0] = global_p0.data['p0']
  [x_short] = global_x_short.data['x_short']
  [z_short] = global_z_short.data['z_short']

  # initial particles in total displacements plot
  x_multiline = np.tile(x_short,len(x_short))
  z_multiline = - np.repeat(z_short,len(z_short))
  initial_global_particle_source.data = dict(x_coord = x_multiline.tolist(),
                                             z_coord = z_multiline.tolist())
  # do not show anything in potentials plot if t = 0
  if t == 0:
    global_particle_source.data = dict(x_coord = x_multiline.tolist(),
                                       z_coord = z_multiline.tolist())
    dPhi_dx_vector_glyph.visible = False
    dPsi_y_dz_vector_glyph.visible = False
    dPhi_dz_vector_glyph.visible = False
    dPsi_y_dx_vector_glyph.visible = False
    total_potential_vector_glyph.visible = False
    u_rayleigh_vector_glyph.visible = False
    w_rayleigh_vector_glyph.visible = False
    total_rayleigh_vector_glyph.visible = False
  # show only rayleigh potentials as vectors in potentials plot
  else:
    if p0 == 0:
        dPhi_dx_vector_glyph.visible = False
        dPsi_y_dz_vector_glyph.visible = False
        dPhi_dz_vector_glyph.visible = False
        dPsi_y_dx_vector_glyph.visible = False
        total_potential_vector_glyph.visible = False
        u_rayleigh_vector_glyph.visible = True
        w_rayleigh_vector_glyph.visible = True
        total_rayleigh_vector_glyph.visible = True
        evolve2()
  # do not show rayleigh ptentials as vectors in potentials plot
    else:
        dPhi_dx_vector_glyph.visible = True
        dPsi_y_dz_vector_glyph.visible = True
        dPhi_dz_vector_glyph.visible = True
        dPsi_y_dx_vector_glyph.visible = True
        total_potential_vector_glyph.visible = True
        u_rayleigh_vector_glyph.visible = False
        w_rayleigh_vector_glyph.visible = False
        total_rayleigh_vector_glyph.visible = False
        evolve1()
  t+=dt
  global_t.data = dict(t=[t])





###############################################################################
# Fourier Transform of load ###################################################
###############################################################################
def load_fft():
  update_parameters()
  [b] = global_b.data['b']
  [p0] = global_p0.data['p0']
  [B] = global_B.data['B']
  [x] = global_x.data['x']
  # number of evaluation points
  N = 2**8
  # kx vector in Fourier domain
  dkx = (1*pi)/B
  kx = np.arange(-(N/2)*dkx, ((N/2))*dkx, dkx)
  kx[abs(kx) < 10 ** -10] = 0
  
  # set up load vector in time domain
  if b == B:
    p = np.ones(len(x))*p0
    notzero = N
  else:  
    p = np.zeros(len(x))
    for i in range(0,len(p)):
      if abs(x[i]) < b/2:
        p[i]  = p0
      elif abs(x[i]) == b/2:
        p[i]  = p0/2
    if b == 0:
      p = 2*p
      notzero = 1
    else:
      notzero = 0
      for i in range(0,len(p)):
        if p[i] != 0:
          notzero = notzero + 1
      notzero = notzero - 1
  
  # Fourier Transform of load (kx, z, omega) regardless of b
  P = 4*pi**2 * fftshift(fft(p))/(notzero)
  
  # output
  global_P.data = dict(P = [P])
  global_kx.data = dict(kx = [kx])





###############################################################################
# solve displacements #########################################################
###############################################################################
def solve_halfspace():
  [c_s] = global_c_s.data['c_s']
  [c_p] = global_c_p.data['c_p']
  [k_p] = global_k_p.data['k_p']
  [k_s] = global_k_s.data['k_s']
  [Omega] = global_Omega.data['Omega']
  [z] = global_z.data['z']
  [x] = global_x.data['x']
  [kx] = global_kx.data['kx']
  [P] = global_P.data['P']
  [my] = global_my.data['my']
  [select_z] = global_select_z.data['select_z']
  [select_x] = global_select_x.data['select_x']
  # pre-definde vectors with zeros
  global_u_f.data = dict(u_f = [np.zeros((len(z),len(kx)),
                                         dtype = complex)])
  global_w_f.data = dict(w_f = [np.zeros((len(z),len(kx)),
                                         dtype = complex)]) 
  global_A_2_f.data = dict(A_2_f = [np.zeros(len(kx),dtype = complex)])
  global_B_x2_f.data = dict(B_x2_f = [np.zeros(len(kx),dtype = complex)])
  global_B_y2_f.data = dict(B_y2_f = [np.zeros(len(kx),dtype = complex)])
  global_Phi_f.data = dict(Phi_f = [np.zeros((len(z),len(kx)),
                                                 dtype = complex)])
  global_Psi_x_f.data = dict(Psi_x_f = [np.zeros((len(z),len(kx)),
                                                 dtype = complex)])
  global_Psi_y_f.data = dict(Psi_y_f = [np.zeros((len(z),len(kx)),
                                                 dtype = complex)])
  global_lamb1_f.data = dict(lamb1_f = [np.zeros(len(kx),dtype = complex)])
  global_lamb2_f.data = dict(lamb2_f = [np.zeros(len(kx),dtype = complex)])
  [u_f] = global_u_f.data['u_f']
  [w_f] = global_w_f.data['w_f']
  [A_2_f] = global_A_2_f.data['A_2_f']
  [B_x2_f] = global_B_x2_f.data['B_x2_f']
  [B_y2_f] = global_B_y2_f.data['B_y2_f']
  [Phi_f] = global_Phi_f.data['Phi_f']
  [Psi_x_f] = global_Psi_x_f.data['Psi_x_f']
  [Psi_y_f] = global_Psi_y_f.data['Psi_y_f']
  [lamb1_f] = global_lamb1_f.data['lamb1_f']
  [lamb2_f] = global_lamb2_f.data['lamb2_f']
  omega = -Omega
  
  # solve for unknown parameters A2, Bx2, By2
  for i in range(0,len(kx)):
      kx_i = kx[i]
      P_i = P[i]
      ky = 0
      k_r = sqrt(kx_i**2+ky**2)
      lamb1_i = -1j * sqrt(k_p**2-kx_i**2-ky**2)
      lamb2_i = -1j * sqrt(k_s**2-kx_i**2-ky**2)

      stress = np.array([[-P_i], [0], [0]])
      
      K = my * np.array([
                        [2*(kx_i**2+ky**2)-k_s**2, 2*1j*ky*lamb2_i,
                        -2*1j*kx_i*lamb2_i], 
                        [-2*1j*ky*lamb1_i, lamb2_i**2+ky**2, -kx_i*ky], 
                        [-2*1j*kx_i*lamb1_i, kx_i*ky, -(lamb2_i**2+kx_i**2)]
                        ])

      K_inv = np.linalg.inv(K)

      unknowns = np.dot(K_inv,stress)

      A_2_f_i = unknowns[0]
      B_x2_f_i = unknowns[1]
      B_y2_f_i = unknowns[2]
      # place solution in pre-defined vectors
      lamb1_f[i] = lamb1_i
      lamb2_f[i] = lamb2_i
      A_2_f[i] = A_2_f_i
      B_x2_f[i] = B_x2_f_i
      B_y2_f[i] = B_y2_f_i

  # solve for displacements and potentials in Fourier domain
  for m in range(0,len(z)):
      z_m = z[m]
      for i in range(0,len(kx)):
          lamb1_i = lamb1_f[i]
          lamb2_i = lamb2_f[i]
          A_2_f_i = A_2_f[i]
          B_x2_f_i = B_x2_f[i]
          B_y2_f_i = B_y2_f[i]
          kx_i = kx[i]
          ky = 0

          Phi_f_i = A_2_f_i * exp(-lamb1_i*z_m)
          Psi_x_f_i = B_x2_f_i * exp(-lamb2_i*z_m)
          Psi_y_f_i = B_y2_f_i * exp(-lamb2_i*z_m)
          Psi_z_f_i = 0 

          KK = np.array([
                        [1j*kx_i, 0, lamb2_i],
                        [1j*ky, -lamb2_i, 0],
                        [-lamb1_i, -1j*ky, 1j*kx_i]
                        ])

          knowns = np.array([
                            [A_2_f_i*exp(-lamb1_i*z_m)], 
                            [B_x2_f_i*exp(-lamb2_i*z_m)], 
                            [B_y2_f_i*exp(-lamb2_i*z_m)]
                            ])

          u_f_i,v_f_i,w_f_i = np.matmul(KK,knowns)

          # place solution in pre-defined vectors
          u_f[m,i] = u_f_i
          w_f[m,i] = w_f_i
          Phi_f[m,i] = Phi_f_i
          Psi_x_f[m,i] = Psi_x_f_i
          Psi_y_f[m,i] = Psi_y_f_i

  # output in Fourier domain (kx,z,omega)
  global_u_f.data = dict(u_f = [u_f])
  global_w_f.data = dict(w_f = [w_f]) 
  global_Phi_f.data = dict(Phi_f = [Phi_f])
  global_Psi_x_f.data = dict(Psi_x_f = [Psi_x_f])
  global_Psi_y_f.data = dict(Psi_y_f = [Psi_y_f])
  global_lamb1_f.data = dict(lamb1_f = [lamb1_f])
  global_lamb2_f.data = dict(lamb2_f = [lamb2_f])
  global_A_2_f.data = dict(A_2_f = [A_2_f])
  global_B_x2_f.data = dict(B_x2_f = [B_x2_f])
  global_B_y2_f.data = dict(B_y2_f = [B_y2_f])
  
  # IFFT of displacements in (kx - x)
  u_o = ifftshift(ifft(ifftshift(u_f)))
  w_o = ifftshift(ifft(ifftshift(w_f)))
  
  # reduce nuber of evaluation points
  x_short = x[select_x]
  z_short = z[select_z.flatten().tolist()]
  u_o_short = u_o[select_z,select_x]
  w_o_short = w_o[select_z,select_x]

  # output displacements (x,z,omega)
  global_u_o.data = dict(u_o = [u_o])
  global_w_o.data = dict(w_o = [w_o]) 
  global_u_o_short.data = dict(u_o_short = [u_o_short])
  global_w_o_short.data = dict(w_o_short = [w_o_short]) 

  # output reduced particle positions
  global_x_short.data = dict(x_short=[x_short])
  global_z_short.data = dict(z_short=[z_short])





###############################################################################
# solve potentials ############################################################
###############################################################################
def solve_potentials():
  [kx] = global_kx.data['kx']
  [z] = global_z.data['z'] 
  [Omega] = global_Omega.data['Omega']
  [A_2_f] = global_A_2_f.data['A_2_f']
  [B_x2_f] = global_B_x2_f.data['B_x2_f']
  [B_y2_f] = global_B_y2_f.data['B_y2_f']
  [Phi_f] = global_Phi_f.data['Phi_f']
  [Psi_x_f] = global_Psi_x_f.data['Psi_x_f']
  [Psi_y_f] = global_Psi_y_f.data['Psi_y_f']
  [lamb1_f] = global_lamb1_f.data['lamb1_f']
  [lamb2_f] = global_lamb2_f.data['lamb2_f']
  [select_z] = global_select_z.data['select_z']
  [select_x] = global_select_x.data['select_x']
  omega = -Omega
  # pre-definde vectors with zeros
  global_dPhi_f_dx.data = dict(dPhi_f_dx = [np.zeros((len(z),len(kx)),
                                                     dtype = complex)])
  global_dPhi_f_dz.data = dict(dPhi_f_dz = [np.zeros((len(z),len(kx)),
                                                     dtype = complex)])
  global_dPsi_y_f_dx.data = dict(dPsi_y_f_dx = [np.zeros((len(z),len(kx)),
                                                         dtype = complex)])
  global_dPsi_y_f_dz.data = dict(dPsi_y_f_dz = [np.zeros((len(z),len(kx)),
                                                         dtype = complex)])
  global_dPhi_o_dx.data = dict(dPhi_o_dx = [np.zeros((len(z),len(kx)),
                                                     dtype = complex)])
  global_dPhi_o_dz.data = dict(dPhi_o_dz = [np.zeros((len(z),len(kx)),
                                                     dtype = complex)])
  global_dPsi_y_o_dx.data = dict(dPsi_y_o_dx = [np.zeros((len(z),len(kx)),
                                                         dtype = complex)])
  global_dPsi_y_o_dz.data = dict(dPsi_y_o_dz = [np.zeros((len(z),len(kx)),
                                                         dtype = complex)])  
  [dPhi_f_dx] = global_dPhi_f_dx.data['dPhi_f_dx']
  [dPhi_f_dz] = global_dPhi_f_dz.data['dPhi_f_dz']
  [dPsi_y_f_dx] = global_dPsi_y_f_dx.data['dPsi_y_f_dx']
  [dPsi_y_f_dz] = global_dPsi_y_f_dz.data['dPsi_y_f_dz']
  [dPhi_o_dx] = global_dPhi_o_dx.data['dPhi_o_dx']
  [dPhi_o_dz] = global_dPhi_o_dz.data['dPhi_o_dz']
  [dPsi_y_o_dx] = global_dPsi_y_o_dx.data['dPsi_y_o_dx']
  [dPsi_y_o_dz] = global_dPsi_y_o_dz.data['dPsi_y_o_dz']

  # solve partial derivatives of potentials in the Fourier domain
  for m in range(0,len(z)):
    z_m = z[m]
    for i in range(0,len(kx)):
      kx_i = kx[i]
      Phi_f_m_i = Phi_f[m,i]
      Psi_y_f_m_i = Psi_y_f[m,i]
      Psi_x_f_m_i = Psi_x_f[m,i]
      lamb1_i = lamb1_f[i]
      lamb2_i = lamb2_f[i]

      dPhi_f_dx[m,i] = Phi_f_m_i*1j*kx_i
      dPhi_f_dz[m,i] = Phi_f_m_i*(-lamb1_i)
      dPsi_y_f_dx[m,i] = Psi_y_f_m_i*1j*kx_i
      dPsi_y_f_dz[m,i] = Psi_y_f_m_i*(-lamb2_i)

  # output in Fourier domain (kx,z,omega)
  global_dPhi_f_dx.data = dict(dPhi_f_dx = [dPhi_f_dx])
  global_dPhi_f_dz.data = dict(dPhi_f_dz = [dPhi_f_dz])
  global_dPsi_y_f_dx.data = dict(dPsi_y_f_dx = [dPsi_y_f_dx])
  global_dPsi_y_f_dz.data = dict(dPsi_y_f_dz = [dPsi_y_f_dz])

  # IFFT of potentials in (kx - x)
  dPhi_o_dx = ifftshift(ifft(ifftshift(dPhi_f_dx)))
  dPhi_o_dz = ifftshift(ifft(ifftshift(dPhi_f_dz)))
  dPsi_y_o_dx = ifftshift(ifft(ifftshift(dPsi_y_f_dx)))
  dPsi_y_o_dz = ifftshift(ifft(ifftshift(dPsi_y_f_dz)))

  # reduce nuber of evaluation points
  dPhi_o_dx_short = dPhi_o_dx[select_z,select_x]
  dPhi_o_dz_short = dPhi_o_dz[select_z,select_x]
  dPsi_y_o_dx_short = dPsi_y_o_dx[select_z,select_x]
  dPsi_y_o_dz_short = dPsi_y_o_dz[select_z,select_x]
  
  # output potentials (x,z,omega)
  global_dPhi_o_dx.data = dict(dPhi_o_dx = [dPhi_o_dx])
  global_dPhi_o_dz.data = dict(dPhi_o_dz = [dPhi_o_dz])
  global_dPsi_y_o_dx.data = dict(dPsi_y_o_dx = [dPsi_y_o_dx])
  global_dPsi_y_o_dz.data = dict(dPsi_y_o_dz = [dPsi_y_o_dz])  
  global_dPhi_o_dx_short.data = dict(dPhi_o_dx_short = [dPhi_o_dx_short])
  global_dPhi_o_dz_short.data = dict(dPhi_o_dz_short = [dPhi_o_dz_short])
  global_dPsi_y_o_dx_short.data = dict(dPsi_y_o_dx_short = [dPsi_y_o_dx_short])
  global_dPsi_y_o_dz_short.data = dict(dPsi_y_o_dz_short = [dPsi_y_o_dz_short])





###############################################################################
# Sliders and Slider functions ################################################
###############################################################################
# material damping ratio
def change_zeta(attr,old,new):
  [zeta] = global_zeta.data['zeta']
  zeta = new
  global_zeta.data = dict(zeta = [zeta])
  update_parameters()
zeta_Slider = LatexSlider(title='D =',
                          value=initial_zeta,start=0.01,end=0.99,step=0.01)
zeta_Slider.on_change('value',change_zeta)

# Poissons ratio
def change_ny(attr,old,new):
  [ny] = global_ny.data['ny']
  ny = new
  ny = round(ny,2)
  global_ny.data = dict(ny = [ny])
  update_parameters()
ny_Slider = LatexSlider(title='\\nu =',
                        value=initial_ny,start=0.05,end=0.45,step=0.05)
ny_Slider.on_change('value',change_ny)

# excitation frequency 
def change_Omega(attr,old,new):
  [Omega] = global_Omega.data['Omega']
  [lamb_zrange_active]  = global_lamb_zrange_active.data['lamb_zrange_active']
  Omega = new
  global_lamb_zrange_active.data = dict(lamb_zrange_active=[True])
  global_Omega.data = dict(Omega = [Omega])
  update_parameters()
Omega_Slider = LatexSlider(title='\\Omega =',
                           value_unit='\\frac{\\mathrm{rad}}{\\mathrm{s}}',
                           value=initial_Omega,start=30,end=300,step=1)
Omega_Slider.on_change('value',change_Omega)

# width of load
def change_b(attr,old,new):
  [b] = global_b.data['b']
  b = new
  global_b.data = dict(b = [b])
  if b == 0:
    b_Slider.title='\\text{point load}\\ b='
  elif b == 16:
    b_Slider.title='\\text{load over entire area}\\ b='
  else:
    b_Slider.title='\\text{line load with width}\\ b='
  update_parameters()
b_Slider = LatexSlider(title=
                '\\text{line load with width}\\ b=',value_unit='\\mathrm{m}',
                       value=initial_b,start=0,end=16,step=0.0625*4)
b_Slider.on_change('value',change_b)

# apply and remove load
def change_p0(new):
  [p0] = global_p0.data['p0']
  p0 = new
  global_p0.data = dict(p0 = [p0])
  update_parameters()
p0_RadioButton = RadioButtonGroup(labels=['p_0=0','p_0=1'], active = 1)
p0_RadioButton.on_click(change_p0)

# change z-range with Slider or automatically with Omega
def change_zrange(attr,old,new):
  [slider_zrange] = global_slider_zrange.data['slider_zrange']
  [slider_zrange_active] = global_slider_zrange_active.data['slider_zrange_active']
  slider_zrange = new
  global_slider_zrange_active.data = dict(slider_zrange_active=[True])
  global_slider_zrange.data = dict(slider_zrange = [slider_zrange])
  update_parameters()
zrange_Slider = RangeSlider(title='z-interval range in m',
                            value=initial_slider_zrange,
                            start=0,end=200,step=1)
zrange_Slider.on_change('value',change_zrange)

# change x-range with Slider
def change_x_range(attr,old,new):
  [x_range] = global_x_range.data['x_range']
  x_range = list(x_range)
  new = list(new)
  x_range = new
  if x_range[1] == 8:
    x_range[1] = 7.9375
  if x_range[0] == -8:
    x_range[0] = -7.9375
  x_range = tuple(x_range)
  new = tuple(new)  
  global_x_range.data = dict(x_range = [x_range])
  update_parameters()
x_range_Slider = RangeSlider(title='x-interval range in m',
                            value=initial_x_range,
                            start=-8,end=8,step=0.25)
x_range_Slider.on_change('value',change_x_range)

# select x-position of particle for potential displacements
def change_chosen_x(attr,old,new):
  [chosen_x] = global_chosen_x.data['chosen_x']
  chosen_x = new
  global_chosen_x.data = dict(chosen_x = [chosen_x])
  update_parameters()
chosen_x_Slider = LatexSlider(title=
                    '\\text{position\\ of\\ observation\\ point\\ in\\ x:}',
                              value=initial_chosen_x,
                              start=-((len(initial_select_z)-1)/2),
                              end=((len(initial_select_z)-1)/2),step=1)
chosen_x_Slider.on_change('value',change_chosen_x)

# select z-position of particle for potential displacements
def change_chosen_z(attr,old,new):
  [chosen_z] = global_chosen_z.data['chosen_z']
  chosen_z = new
  global_chosen_z.data = dict(chosen_z = [chosen_z])
  update_parameters()
chosen_z_Slider = LatexSlider(title=
                    '\\text{position\\ of\\ observation\\ point\\ in\\ z:}',
                              value=initial_chosen_z,start=0,
                              end=(len(initial_select_z)-1),step=1)
chosen_z_Slider.on_change('value',change_chosen_z)

# disable sliders if play is active
def disable_all_sliders(d=True):
  zeta_Slider.disabled = d
  ny_Slider.disabled = d
  Omega_Slider.disabled = d
  b_Slider.disabled = d
  p0_RadioButton.disabled = d
  zrange_Slider.disabled = d
  x_range_Slider.disabled = d
  chosen_x_Slider.disabled = d
  chosen_z_Slider.disabled = d





###############################################################################
# update parameters ###########################################################
###############################################################################
def update_parameters(): 
  [zeta] = global_zeta.data['zeta']
  [ny] = global_ny.data['ny']
  [Omega] = global_Omega.data['Omega']
  [b] = global_b.data['b']
  [p0] = global_p0.data['p0']
  [zrange] = global_zrange.data['zrange']
  [x_range] = global_x_range.data['x_range']
  [x] = global_x.data['x']
  [select_z] = global_select_z.data['select_z']
  [slider_zrange] = global_slider_zrange.data['slider_zrange']
  [lamb_zrange] = global_lamb_zrange.data['lamb_zrange'] 
  [lamb_zrange_active] = global_lamb_zrange_active.data['lamb_zrange_active']
  [slider_zrange_active] = global_slider_zrange_active.data['slider_zrange_active']
  z = global_z.data['z']
  zeta = zeta
  ny = ny
  Omega = Omega
  b = b
  p0 = p0
  zrange = zrange
  x_range = x_range

  # Rayleigh parameters
  index = rayleigh_data_table.data['ny'].index(ny)
  c_r_c_s = rayleigh_data_table.data['c_r_c_s'][index]
  c_p_c_s = rayleigh_data_table.data['c_p_c_s'][index]
  beta_1 = rayleigh_data_table.data['beta_1'][index]
  beta_2 = rayleigh_data_table.data['beta_2'][index]
  C_2_C_1 = rayleigh_data_table.data['C_2_C_1'][index]

  # soil properties and wave parameters
  E = 150*(10**6)*(1-(2*zeta*1j))
  rho = 2200
  G = E/(2*(1+ny))
  my = E/(2*(1+ny))
  lamb = 2*my*ny/(1-2*ny)
  c_p = sqrt((lamb+2*my)/rho)
  lamb_p = (2*pi*c_p)/Omega
  k_p = (2*pi/lamb_p)
  c_s = sqrt(my/rho)
  lamb_s = (2*pi*c_s)/Omega
  k_s = (2*pi/lamb_s)
  c_r = c_s*c_r_c_s
  lamb_r = (2*pi*c_r)/Omega
  k_r = (2*pi/lamb_r)
  
  # change z
  lamb_zrange = (0,int(2*lamb_r.real))
  if slider_zrange_active:
    Z = slider_zrange[1]-slider_zrange[0]
    dz = Z / 80
    z = np.arange(slider_zrange[0],slider_zrange[1],dz)     
  else:
    Z = lamb_zrange[1]-lamb_zrange[0]
    dz = Z / 80
    z = np.arange(lamb_zrange[0],lamb_zrange[1],dz)
    zrange_Slider.value = lamb_zrange

  # change x
  x_range_start_index = np.where(x == x_range[0])[0]
  x_range_end_index = np.where(x == x_range[1])[0]
  select_x = np.linspace(x_range_start_index,x_range_end_index,len(select_z),
                         dtype=int)
  
  # output
  global_E.data = dict(E = [E])
  global_rho.data = dict(rho = [rho])
  global_my.data = dict(my = [my])
  global_lamb.data = dict(lamb = [lamb])
  global_z.data = dict(z = [z])
  global_select_x.data = dict(select_x = [select_x])
  global_c_p.data = dict(c_p = [c_p])
  global_lamb_p.data = dict(lamb_p = [lamb_p])
  global_k_p.data = dict(k_p = [k_p])  
  global_c_s.data = dict(c_s = [c_s])
  global_lamb_s.data = dict(lamb_s = [lamb_s])
  global_k_s.data = dict(k_s = [k_s])  
  global_c_r.data = dict(c_r = [c_r])
  global_lamb_r.data = dict(lamb_r = [lamb_r])
  global_k_r.data = dict(k_r = [k_r])
  global_c_r_c_s.data = dict(c_r_c_s = [c_r_c_s])
  global_c_p_c_s.data = dict(c_p_c_s = [c_p_c_s])
  global_beta_1.data = dict(beta_1 = [beta_1])
  global_beta_2.data = dict(beta_2 = [beta_2])
  global_C_2_C_1.data = dict(C_2_C_1 = [C_2_C_1])
  global_parameters_data_table_source.data = dict(lamb_p = [round(lamb_p.real,2)],
                                                  c_p = [round(c_p.real,2)],
                                                  lamb_s = [round(lamb_s.real,2)],
                                                  c_s = [round(c_s.real,2)],
                                                  lamb_r = [round(lamb_r.real,2)],
                                                  c_r = [round(c_r.real,2)],
                                                  my = [round(my.real/1000000,2)]
                                                  )
  # change axis rage in total displacements plot
  changeaxisranges()

def changeaxisranges():
  [x_range] = global_x_range.data['x_range']
  [z] = global_z.data['z']
  x_range = list(x_range)
  p.x_range.start = x_range[0] - 1
  p.x_range.end = x_range[1] + 1
  p.y_range.start = - z[-1] - z[-1]/30
  p.y_range.end = z[0] + z[-1]/5





###############################################################################
# Buttons and button functions ################################################
###############################################################################
def play_pause():
  if play_pause_button.label == 'Play':
    play()
  else:
    pause()

def pause():
  [active] = global_active.data['active']
  [callback_id] = global_callback_id.data['callback_id']
  play_pause_button.label = 'Play'
  try:
    curdoc().remove_periodic_callback(callback_id)
    global_active.data = dict(active=[False])
  except ValueError:
    print('WARNING: callback_id was already removed - this can happen if stop was pressed after pause, usually no serious problem; if stop was not called this part should be changed')
  except:
    print('This error is not covered: ', sys.exc_info()[0])
    raise

def play():
  [active] = global_active.data['active']
  [callback_id] = global_callback_id.data['callback_id']
  play_pause_button.label = 'Pause'
  disable_all_sliders(True)
  load_fft()
  solve_halfspace()
  solve_potentials()
  callback_id = curdoc().add_periodic_callback(evolve,100)
  global_active.data = dict(active=[True])
  global_callback_id.data = dict(callback_id = [callback_id])
play_pause_button = Button(label='Play', button_type='success',width=100)
play_pause_button.on_click(play_pause)

def stop():
  [t] = global_t.data['t']
  disable_all_sliders(False)
  pause()
  global_t.data = dict(t = [0])
stop_button = Button(label='Stop', button_type='success', width=100)
stop_button.on_click(stop)

def reset():
  stop()
  zeta_Slider.value = initial_zeta
  ny_Slider.value = initial_ny
  Omega_Slider.value = initial_Omega
  b_Slider.value = initial_b
  zrange_Slider.value = initial_slider_zrange
  x_range_Slider.value = initial_x_range
  chosen_x_Slider.value = initial_chosen_x
  chosen_z_Slider.value = initial_chosen_z
  p.x_range.start = -10
  p.x_range.end = 10
  p.y_range.start = -52
  p.y_range.end = 10
reset_button = Button(label='Reset', button_type='success',width=100)
reset_button.on_click(reset)





###############################################################################
# plot particle and displacements #############################################
###############################################################################
t = Title(text='Total displacement of soil particles')
p = Plot(title=t,x_range=Range1d(start=-10,end=10),y_range=Range1d(start=-52,
                                                                   end=10),
       plot_height = 989, plot_width = 800)
p.toolbar.logo=None
xaxis = LinearAxis()
xaxis.axis_label = 'x in [m]'
yaxis = LinearAxis()
yaxis.axis_label = 'z in [m]'
p.title.text_font_size = '15pt'

glyph_line = Line(x='x', y='y', line_color='black', line_width=2)
glyph_surface = Line(x='x', y='y', line_color='black', line_width=1)

glyph_Annulus_static = Annulus(x='x_coord',y='z_coord',outer_radius=.01,
                               fill_color='grey')
glyph_Annulus_moving = Annulus(x='x_coord',y='z_coord',outer_radius=.04,
                               fill_color='saddlebrown',line_alpha=0.7,
                               fill_alpha=0.7)
selected_Annulus_moving = Annulus(x='x_coord',y='z_coord',outer_radius=0.15,
                               fill_color='red',line_alpha=0.7,
                               fill_alpha=0.7)

p.add_glyph(source_line, glyph_line)
p.add_glyph(initial_global_particle_source, glyph_Annulus_static)
p.add_glyph(global_particle_source, glyph_Annulus_moving)
p.add_glyph(selected_Annulus_source, selected_Annulus_moving)
p.add_glyph(surface_source, glyph_surface)
p.add_layout(xaxis, 'below')
p.add_layout(yaxis, 'left')
p.add_tools(PanTool(), WheelZoomTool(), SaveTool(), BoxZoomTool(), ResetTool())
p.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
p.add_layout(Grid(dimension=1, ticker=yaxis.ticker))





###############################################################################
# plot vectors for potentials #################################################
###############################################################################
a = figure(plot_height = 540, plot_width = 540,
           x_range=Range1d(start=-0.2,end=0.2),
           y_range=Range1d(start=-0.2,end=0.2),
           title='Displacement components of the potentials')
a.toolbar.logo=None
a.tools=[PanTool(), WheelZoomTool(), SaveTool(), BoxZoomTool(), ResetTool()]
a.xaxis.axis_label = 'x in [m]'
a.yaxis.axis_label = 'z in [m]'
a.title.text_font_size = '15pt'

dPhi_dx_vector_glyph = Arrow(end=NormalHead(line_color='#0065BD',
                                            fill_color='#0065BD',line_width=2,
                                            size=10),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_dPhi_dx_vector_source,line_color='#0065BD',
                  line_width=3)
dPsi_y_dz_vector_glyph = Arrow(end=NormalHead(line_color='#E37222',
                                             fill_color='#E37222',line_width=2,
                                             size=10, line_alpha=0.7),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_dPsi_y_dz_vector_source,line_color='#E37222',
                  line_width=3,line_alpha=0.7)
dPhi_dz_vector_glyph = Arrow(end=NormalHead(line_color='#A2AD00',
                                            fill_color='#A2AD00',line_width=2,
                                            size=10),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_dPhi_dz_vector_source,line_color='#A2AD00',
                  line_width=3)
dPsi_y_dx_vector_glyph = Arrow(end=NormalHead(line_color='red',
                                             fill_color='red',
                                             line_width=2,size=10,
                                             line_alpha=0.7),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_dPsi_y_dx_vector_source,line_color='red',
                  line_width=3,line_alpha=0.7)
total_potential_vector_glyph = Arrow(end=NormalHead(line_color='black',
                                                    fill_color='black',
                                                    line_width=4,size=12,
                                                    line_alpha=0.5),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=total_potential_vector_source,line_color='black',
                  line_width=4,line_alpha=0.5)
u_rayleigh_vector_glyph = Arrow(end=NormalHead(line_color='purple',
                                               fill_color='purple',
                                               line_width=2,size=10,
                                               line_alpha=0.7),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_u_rayleigh_source,line_color='purple',
                  line_width=3,line_alpha=0.7)
w_rayleigh_vector_glyph = Arrow(end=NormalHead(line_color='purple',
                                               fill_color='purple',
                                               line_width=2,size=10,
                                               line_alpha=0.7),
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_w_rayleigh_source,line_color='purple',
                  line_width=3,line_alpha=0.7)
total_rayleigh_vector_glyph = Arrow(end=NormalHead(line_color='black',
                                                   fill_color='black',
                                                   line_width=4,size=12,
                                                   line_alpha=0.5), 
                  x_start='xS', y_start='zS', x_end='xE', y_end='zE',
                  source=global_rayleigh_vector_source,line_color='black',
                  line_width=4,line_alpha=0.5)
a.add_layout(dPhi_dx_vector_glyph)
a.add_layout(dPsi_y_dz_vector_glyph)   
a.add_layout(dPhi_dz_vector_glyph)
a.add_layout(dPsi_y_dx_vector_glyph)
a.add_layout(total_potential_vector_glyph)
a.add_layout(u_rayleigh_vector_glyph)
a.add_layout(w_rayleigh_vector_glyph)
a.add_layout(total_rayleigh_vector_glyph)





###############################################################################
# table with wave parameters ##################################################
###############################################################################
table_parameters_columns = [TableColumn(field='lamb_p', title='lamb_p [m]'),
                 TableColumn(field='c_p', title='c_p [m/s]'),
                 TableColumn(field='lamb_s', title='lamb_s [m]'),
                 TableColumn(field='c_s', title='c_s [m/s]'),
                 TableColumn(field='lamb_r', title='lamb_r [m]'),
                 TableColumn(field='c_r', title='c_r [m/s]'),
                 TableColumn(field='my', title='G [MN/m^2]'),
                 ]
parameters_data_table = DataTable(source=global_parameters_data_table_source,
                                  columns=table_parameters_columns,
                                  header_row=True,
                                  fit_columns=True,
                                  index_position=None,
                                  height=50
                                  )

table_particlepositions_columns = [TableColumn(field='chosen_x_value',
                    title='coordinate of the observation point in x [m]'),
                  TableColumn(field='chosen_z_value',
                    title='coordinate of the observation point in z [m]')
                  ]

particlepositions_data_table = DataTable(source=global_chosen_particle_data_table_source,
                                         columns=table_particlepositions_columns,
                                         header_row=True,
                                         fit_columns=True,
                                         index_position=None,
                                         height=50
                                         )





###############################################################################
# descriptions ################################################################
###############################################################################
paragraph = LatexDiv(text='''&nbsp;<span style='color: #0065bd;'>$$\\frac{\\partial \\Phi}{\\partial x}$$</span><span style='color: #a2ad00;'>$$\\frac{\\partial \\Phi}{\\partial z}$$</span><span style='color: #e37222;'>$$\\frac{\\partial \\Psi_{y}}{\\partial z}$$</span><span style='color: #ff0000;'>$$\\frac{\\partial \\Psi_{y}}{\\partial x}$$</span><span style='color: #993366;'>$$\\text{Rayleigh}$$</span><span style='color: #993366;'>$$(p_{0}=0)$$</span><span style='color: #000000;'>$$\\text{total}$$</span>''',width=10, height=15)
description_filename = join(dirname(__file__), 'description.html')
description = LatexDiv(text=open(description_filename).read(),
                       render_as_text=False,width=1400)





###############################################################################
# initialise ##################################################################
###############################################################################
def initialise():
  # number of evaluation points
  N = 2**8
  # x vector in time domain
  dx = 0.0625
  B = N*dx
  x = np.arange(-(B/2),(B/2),dx)
  global_x.data = dict(x = [x])
  global_B.data = dict(B = [B])
  load_fft()
  solve_halfspace()
  solve_potentials()
  evolve()

initialise()





###############################################################################
# page layout #################################################################
###############################################################################
doc_layout = layout(children=[column(description, 
                               row(
                                   column(
                                          p
                                          ),
                                   column(row(zeta_Slider,b_Slider),
                                          Spacer(height=30,width=30),
                                          row(ny_Slider,x_range_Slider),
                                          #Spacer(height=10,width=30),
                                          row(Omega_Slider,zrange_Slider),
                                          Spacer(height=10,width=30),
                                          row(Spacer(height=5,width=35),
                                              play_pause_button,
                                              Spacer(height=5,width=35),
                                              stop_button,
                                              Spacer(height=5,width=35),
                                              reset_button,
                                              Spacer(height=5,width=35),
                                              p0_RadioButton),
                                          particlepositions_data_table,
                                          row(chosen_x_Slider,chosen_z_Slider),
                                          Spacer(height=25,width=30),                                        
                                          parameters_data_table,
                                          row(a,
                                          paragraph)
                                          )
                                   )
                               )])





###############################################################################
# bokeh server ################################################################
###############################################################################
curdoc().add_root(doc_layout)
curdoc().title = 'Wave Propagation'