from draggableAxisAlignedRectangle import DraggableAxisAlignedRectangle
from bokeh.models import ColumnDataSource
import numpy as np


class DraggableCart(DraggableAxisAlignedRectangle):

    def __init__(self, plot, w, h, x, y):
        DraggableAxisAlignedRectangle.__init__(self, plot, w, h, x, y)
        # create post holding the cable
        post_height = 5
        self._my_cart_source = ColumnDataSource(dict(xs=[np.array([self._pos_x,
                                                                   self._pos_x + self._width,
                                                                   self._pos_x + .5 * self._width])],
                                                     ys=[np.array([self._pos_y - self._height,
                                                 self._pos_y - self._height,
                                                 self._pos_y])]))
        plot.patches(xs='xs', ys='ys', source=self._my_cart_source)

    def translate(self, dx, dy):
        DraggableAxisAlignedRectangle.translate(self, dx, dy)
        xs = self._my_cart_source.data['xs']
        ys = self._my_cart_source.data['ys']

        new_xs = list(xs)
        new_ys = list(ys)

        for i in range(xs.__len__()):
            new_xs[i] = xs[i] + dx
            new_ys[i] = ys[i] + dy

        self._my_cart_source.data = dict(xs=new_xs,
                                         ys=new_ys)
