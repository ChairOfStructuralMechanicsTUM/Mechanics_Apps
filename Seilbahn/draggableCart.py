from draggableAxisAlignedRectangle import DraggableAxisAlignedRectangle
from bokeh.models import ColumnDataSource
import numpy as np


class DraggableCart(DraggableAxisAlignedRectangle):

    def __init__(self, plot, w, h, x, y):
        DraggableAxisAlignedRectangle.__init__(self, plot, w, h, x, y)
        # create cart
        self._my_cart_source = ColumnDataSource(data=dict(xs=[], ys=[]))
        plot.patches(xs='xs', ys='ys', source=self._my_cart_source)
        self._xs = [np.array([self._pos[0],
                              (self._pos + self._dims)[0],
                              (self._pos + .5 * self._dims)[0]])]
        self._ys = [np.array([self._pos[1],
                              (self._pos + self._dims)[1],
                              (self._pos + .5 * self._dims)[1]])]
        self._update_cart_data_source()

    def _update_cart_data_source(self):
        self._my_cart_source = ColumnDataSource(dict(xs=self._xs, ys=self._ys))

    def translate(self, dx, dy):
        DraggableAxisAlignedRectangle.translate(self, dx, dy)
        xs = self._my_cart_source.data['xs']
        ys = self._my_cart_source.data['ys']

        # we have to copy the data and create a new array. Otherwise the datasource is not updated.
        new_xs = np.array(xs)
        new_ys = np.array(ys)

        new_xs += dx
        new_ys += dy

        self._xs = new_xs
        self._ys = new_ys

        self._update_cart_data_source()
