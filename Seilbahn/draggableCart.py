from draggableAxisAlignedRectangle import DraggableAxisAlignedRectangle
from bokeh.models.sources import ColumnDataSource
import numpy as np


class DraggableCart(DraggableAxisAlignedRectangle):

    def __init__(self, plot, w, h, x, y):
        DraggableAxisAlignedRectangle.__init__(self, plot, w, h, x, y)
        # create cart
        xs = [np.array([self._pos[0],
                        (self._pos + self._dims)[0],
                        (self._pos + .5 * self._dims)[0]])]
        ys = [np.array([(self._pos - self._dims)[1],
                        (self._pos - self._dims)[1],
                        self._pos[1]])]
        self._my_cart_source = ColumnDataSource(data=dict(xs=[], ys=[]))
        self._update_cart_data_source(xs, ys)
        plot.patches(xs='xs', ys='ys', source=self._my_cart_source)

    def _update_cart_data_source(self, xs, ys):
        self._xs = xs
        self._ys = ys
        self._my_cart_source.data = dict(xs=self._xs, ys=self._ys)

    def translate(self, dx, dy):
        DraggableAxisAlignedRectangle.translate(self, dx, dy)

        # we have to copy the data and create a new array, not just increment an existing (e.g. numpy) array. Otherwise the datasource is not updated.
        xs = [[xi + dx for xi in x] for x in self._my_cart_source.data['xs']]
        ys = [[yi + dy for yi in y] for y in self._my_cart_source.data['ys']]

        self._update_cart_data_source(xs, ys)
