from draggableAxisAlignedRectangle import DraggableAxisAlignedRectangle
from bokeh.models.sources import ColumnDataSource
import numpy as np


class DraggablePost(DraggableAxisAlignedRectangle):

    def __init__(self, plot, w, h, x, y):
        DraggableAxisAlignedRectangle.__init__(self, plot, w, h, x, y)
        # create post holding the cable
        # todo currently this is just a triangle. We should use a more fancy looking post. See Seilbahn_original.jpg
        self._post_height = 5
        post_tip = self._compute_tip_position()
        xs = [[self._pos[0],
               (self._pos + self._dims)[0],
               post_tip[0]]]
        ys = [[(self._pos + self._dims)[1],
               (self._pos + self._dims)[1],
               post_tip[1]]]
        self._my_post_source = ColumnDataSource(data=dict(xs=[], ys=[]))
        self._update_post_data_source(xs, ys)
        plot.patches(xs='xs', ys='ys', source=self._my_post_source)

    def _update_post_data_source(self, xs, ys):
        self._xs = xs
        self._ys = ys
        self._my_post_source.data = dict(xs=self._xs, ys=self._ys)

    def translate(self, dx, dy):
        DraggableAxisAlignedRectangle.translate(self, dx, dy)

        # we have to copy the data and create a new array, not just increment an existing (e.g. numpy) array. Otherwise the datasource is not updated.
        xs = [[xi + dx for xi in x] for x in self._my_post_source.data['xs']]
        ys = [[yi + dy for yi in y] for y in self._my_post_source.data['ys']]

        self._update_post_data_source(xs, ys)

    def _compute_tip_position(self):
        """
        helper function for the position of the tip.
        :return:
        """
        return self._pos + self._dims * .5 + self._post_height * np.array([0, 1])

    def get_post_tip_position(self):
        return self._compute_tip_position()
