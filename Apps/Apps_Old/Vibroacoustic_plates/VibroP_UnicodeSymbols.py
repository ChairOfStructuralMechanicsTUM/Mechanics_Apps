"""
The file defines the some Greek letters as pre-defined constants that have to be used
within the application. All letters are defined using the unicode encoding
"""

OMEGA_UNICODE = u"\u03C9"
MU_UNICODE = u"\u03BC"
NU_UNICODE = u"\u03B7"
XI_UNICODE = u"\u03BE"
KAPPA_UNICODE = u"\u03BA"
BETA_UNICODE = u"\u03B2"
SIGMA_UNICODE = u"\u03C3"


SUBSCRIPT_ONE = u"\u2081"
SUBSCRIPT_TWO = u"\u2082"
SUBSCRIPT_THREE = u"\u2083"

#-------------------------------------------------------------------------------
#                              User define variables
#-------------------------------------------------------------------------------
#..............................  ELASTIC MODULUS  ..............................
EMODUL_X = "E" + SUBSCRIPT_ONE
EMODUL_Y = "E" + SUBSCRIPT_TWO
EMODUL_Z = "E" + SUBSCRIPT_THREE


EMODUL_XY = "G" + SUBSCRIPT_ONE + SUBSCRIPT_TWO
EMODUL_XZ = "G" + SUBSCRIPT_ONE + SUBSCRIPT_THREE
EMODUL_YZ = "G" + SUBSCRIPT_TWO + SUBSCRIPT_THREE


#....................................   NU  ....................................
POISSON_RATIO_XY = NU_UNICODE + SUBSCRIPT_ONE + SUBSCRIPT_TWO
POISSON_RATIO_XZ = NU_UNICODE + SUBSCRIPT_ONE + SUBSCRIPT_THREE
POISSON_RATIO_YZ = NU_UNICODE + SUBSCRIPT_TWO + SUBSCRIPT_THREE


POISSON_RATIO_YX = NU_UNICODE + SUBSCRIPT_TWO + SUBSCRIPT_ONE
POISSON_RATIO_ZX = NU_UNICODE + SUBSCRIPT_THREE + SUBSCRIPT_ONE
POISSON_RATIO_ZY = NU_UNICODE + SUBSCRIPT_THREE + SUBSCRIPT_TWO
