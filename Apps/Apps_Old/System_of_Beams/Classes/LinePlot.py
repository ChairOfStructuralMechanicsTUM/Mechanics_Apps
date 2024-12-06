"""
Classes to organise the output plot
Only used, to pack data together in one class
"""


class LinePlot:
    def __init__(self, x_vals, y_vals, line_color, line_width, legend=None):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.line_color = line_color
        self.line_width = line_width
        self.legend = legend


class PointCol:
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val

    def __str__(self):
        return "x: " + str(self.x_val) + '  y: ' + str(self.y_val)

    def __repr__(self):
        return self.__str__()
