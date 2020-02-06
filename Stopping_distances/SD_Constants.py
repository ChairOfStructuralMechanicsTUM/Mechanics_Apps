# constants

# labels/strings
bl_sqrt = u"\u221A"
bl_quad = u".²"

# standard object widths/heights
math_button_width = 20


# random initial velocity settings
min_random_v = 0.5
max_random_v = 10
steps_v = 0.5

#initial velocity settings
t_update = 0.20   # increase for faster simulation

# distance-dependent velocity settings
max_totT = 0.25   # inrease for faster simulation
min_val  = 0.0005
min_v    = 1e-10



# acceptable characters for input checks
acceptable_characters = u"1234567890.+-*/^()\u221A "   #\u221A = square root in unicode
numbers               = u"1234567890."

# unicode square root
#u'\u221A'



# warning messages
msg_invalid_value    = "<strong>No valid value! Old value restored.</strong>"
#msg_invalid_function = "<strong>No valid function! Old function restored.</strong>"
msg_invalid_function = "<strong>No valid function!</strong>"
msg_empty_field      = "<strong>At least one field is still empty. Please provide both functions before checking.</strong>"