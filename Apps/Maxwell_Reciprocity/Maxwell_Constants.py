from bokeh.models import ColumnDataSource

################################################################################
#global constants:
################################################################################
a            = 0.5                                                               #width of frames
b            = 0.7                                                               #Height of box
FScale       = 150.0                                                             #Scaling factor
#offsetKraft = 0.08                                                              #
tri_size     = 30                                                                #Default size of Triangle
glob_changer = ColumnDataSource(data=dict(val=[0]))                                                                 #Global variable that changes when 'save deformed button is clicked'
shift        = 0.01                                                              #Shifting factor
#shift2      = 0.015
ps = 0.3                                                                        #used to shift size of plot
plotx0 = 0.1-ps
plotxf = 0.8+ps                                                                 #plot x0 xf, y0, yf. used in plot creation.
ploty0 = -0.4
plotyf = 1.0
#Arrow Sources:
arr_scal        = 450.0                                                         #Scaling factor used for arrows
arr_lw          = 20.0                                                          #Scaling factor used for arrow widths
ground          = 0.07                                                          #height of ground (line made for the moveable side of frame)
