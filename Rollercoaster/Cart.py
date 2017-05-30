from bokeh.models import ColumnDataSource
from numpy import sign

class Cart:

    def __init__(self, fig, path):
        self.source = ColumnDataSource(data=dict(x=[], y=[]))
        self.reset()
        # add cart drawing
        self.draw(path)
        fig.patch(x='x', y='y', fill_color="#0065BD", source=self.source, level='annotation')

    def draw(self, path):
        """
        draw cart after movement
        :return:
        """
        # template cart at position (0,0) with no inclination
        X = [-0.5, 0.5, 0.5, 0.3, 0.1, 0.1, -0.3, -0.3, -0.5]
        Y = [0.0, 0.0, 0.4, 0.7, 0.7, 0.3, 0.3, 0.7, 0.7]

        # find cos(theta)=a/h, sin(theta)=o/h
        # theta angle between line and x axis
        # h=1 as |deriv|=1
        # => cos(theta)=x, sin(theta)=y
        (cosTheta, sinTheta) = path.get_derivative(self.position)
        # get coordinates
        (x, y) = path.get_point(self.position)
        # get direction of travel
        S = sign(self.speed)
        if S == 0:
            S = 1
        for i in range(0, len(X)):
            # apply transform to cart
            xtemp = X[i] * S
            X[i] = xtemp * cosTheta - Y[i] * sinTheta + x
            Y[i] = xtemp * sinTheta + Y[i] * cosTheta + y
        # update cart
        self.source.data = dict(x=X, y=Y)

    def reset(self):
        self.position=0
        self.speed = 0
        self.acceleration = [0, 0]