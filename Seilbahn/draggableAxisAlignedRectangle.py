from bokeh.models import ColumnDataSource
import numpy as np


class DraggableAxisAlignedRectangle:
    """
    class for a rectangle that can be dragged around in the figure by pressing and holding the left mouse button, while
    mouse points on the rectangle. The rectangle can be "dragged".
    """

    def __init__(self, plot, w, h, x, y):
        """
        Createas a draggable axis aligned rectangle
        :param plot: plot where the draggable rectangle is created
        :param w: width of the rectangle
        :param h: height of the rectangle
        :param x: x coordinate of left bottom corner
        :param y: y coordinate of left bottom corner
        """

        self._dims = np.array([w, h])
        self._pos = np.array([x, y])
        self._my_data_source = ColumnDataSource(data=dict(r=[], l=[], b=[], t=[]))
        plot.quad(top='t', bottom='b', left='l', right='r', source=self._my_data_source)
        self._update_rectangle_data_source()

    def _update_rectangle_data_source(self):
        self._my_data_source.data = dict(r=[(self._pos + self._dims)[0]],
                                         l=[self._pos[0]],
                                         b=[self._pos[1]],
                                         t=[(self._pos + self._dims)[1]])

    def is_hit(self, click_pos_x, click_pos_y):
        """
        returns true if click position hits the rectangle
        :param click_pos_x: click position x
        :param click_pos_y: click position y
        :return: return if click hits rectangle
        """
        click_pos = np.array([click_pos_x, click_pos_y])
        pos_diff = self._pos - click_pos
        if abs(pos_diff[0]) < self._dims[0] and abs(pos_diff[1]) < self._dims[1]:
            return True
        else:
            return False

    def translate(self, dx, dy):
        """
        translate rectangle position by dx, dy
        :param dx: shift in x direction
        :param dy: shift in y direction
        :return:
        """
        self._pos += np.array([dx, dy])
        self._update_rectangle_data_source()
