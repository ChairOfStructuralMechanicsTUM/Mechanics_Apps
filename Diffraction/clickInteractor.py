from __future__ import division
import numpy as np
from bokeh.models import ColumnDataSource


class ClickInteractor:
    """
    adds a click interactor to a given plot. This interactor can detect, if a position in the plot is clicked on, return
    that position and call a respective callback function, if a point is clicked.
    """

    def __init__(self, plot, square_size=5):
        """
        :param plot: plot where the interactor is created
        :param square_size: size of the square in pixels. This determines the possible accuracy for detection of user
        input
        """
        self._plot = plot
        self._square_size = square_size
        interactor_source = ColumnDataSource(data=dict(x=[],y=[]))
        # create invisible pseudo squares recognizing, if they are clicked on
        self._pseudo_square = plot.square(x='x', y='y', color=None, line_color=None,
                                          source=interactor_source,
                                          name='pseudo_square',
                                          size=self._square_size)
        # set highlighting behaviour of pseudo squares to stay invisible
        renderer = plot.select(name="pseudo_square")[0]
        renderer.nonselection_glyph = renderer.glyph._clone()
        self.update_to_user_view()

    def update_to_user_view(self):
        """
        updates the interactor on user view change.
        """
        # stepwidth in coordinate system of the plot (in pixels)
        dx = (self._plot.plot_width - 2 * self._plot.min_border) / self._square_size + 1
        dy = (self._plot.plot_height - 2 * self._plot.min_border) / self._square_size + 1
        # generate mesh
        x_small, \
        y_small = np.meshgrid(np.linspace(self._plot.x_range.start, self._plot.x_range.end, dx),
                              np.linspace(self._plot.y_range.start, self._plot.y_range.end, dy))
        # save mesh to data source
        self._pseudo_square.data_source.data = dict(x=x_small.ravel().tolist(),
                                                    y=y_small.ravel().tolist())

    def on_click(self, callback_function):
        """
        sets a callback function to be called, if the interactor is clicked on
        :param callback_function: callback function
        :return:
        """
        self._pseudo_square.data_source.on_change('selected', callback_function)

    def clicked_point(self):
        """
        returns the currently clicked on point in the local coordinate system of self._plot
        :return:
        """
        if self._pseudo_square.data_source.selected is not None:
            if len(self._pseudo_square.data_source.selected['1d']['indices']) > 0:
                id = self._pseudo_square.data_source.selected['1d']['indices'][0]
                x_coor = self._pseudo_square.data_source.data['x'][id]
                y_coor = self._pseudo_square.data_source.data['y'][id]
                return x_coor, y_coor
        else:
            return None, 0