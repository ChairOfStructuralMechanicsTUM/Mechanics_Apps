from bokeh.models import ColumnDataSource


class DraggableAxisAlignedRectangle:

    def __init__(self, plot, w, h, x, y):
        """
        Createas a draggable axis aligned rectangle
        :param plot: plot where the draggable rectangle is created
        :param w: width of the rectangle
        :param h: height of the rectangle
        :param x: x coordinate of left bottom corner
        :param y: y coordinate of left bottom corner
        """

        self._width = w
        self._height = h
        self._pos_x = x
        self._pos_y = y
        self._my_data_source = ColumnDataSource(data=dict(r=[self._pos_x + self._width],
                                                          l=[self._pos_x],
                                                          b=[self._pos_y],
                                                          t=[self._pos_y + self._height]))
        plot.quad(top='t', bottom='b', left='l', right='r', source=self._my_data_source)

    def is_hit(self, click_pos_x, click_pos_y):
        """
        returns true if click position hits the rectangle
        :param click_pos_x: click position x
        :param click_pos_y: click position y
        :return: return if click hits rectangle
        """
        if abs(self._pos_x - click_pos_x) < self._width and abs(self._pos_y - click_pos_y) < self._height:
            return True
        else:
            return False

    def translate(self, dx, dy):
        self._pos_x += dx
        self._pos_y += dy

        self._my_data_source.data = dict(r=[self._pos_x + self._width],
                                         l=[self._pos_x],
                                         b=[self._pos_y],
                                         t=[self._pos_y + self._height])