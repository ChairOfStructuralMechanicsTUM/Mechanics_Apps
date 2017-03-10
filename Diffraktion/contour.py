from __future__ import division
import bokeh
from sympy import sympify, lambdify, diff
import numpy as np
from bokeh.models import ColumnDataSource
import matplotlib as mpl
from tables.description import Col
from warnings import warn

mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class Contour:
    """
    adds a contour plot to a given plot. MatPlotLibs contour plot is utilized for computing the contour data. That data
    is plotted using bokehs multi_line function. Optionally the user can add labels to the contour data using bokehs
    text function.
    """

    def __init__(self, plot, add_label=False, line_color='line_color', **kwargs):
        """
        :param plot: plot where the contour is plotted
        :param add_label: bool to define whether labels are added to the contour
        :param line_color: defining line color, if no line color is supplied, the default line color scheme from
        matplotlib is used
        :param kwargs: additional bokeh line plotting arguments like width, style ect...
        """
        self._plot = plot
        contour_source = ColumnDataSource(data=dict(xs=[], ys=[], line_color=[]))
        self._contour_plot = self._plot.multi_line(xs='xs', ys='ys', line_color=line_color, source=contour_source,
                                                   **kwargs)
        self._add_label = add_label
        if self._add_label:
            label_source = ColumnDataSource(data=dict(xt=[], yt=[], text=[]))
            self._text_label = self._plot.text(x='xt', y='yt', text='text', text_baseline='middle',
                                               text_align='center', source=label_source)

    def compute_contour_data(self, f, isovalue=None):
        """
        computes and updates contour data for the contour plot of this object w.r.t. current user view of the plot
        :param f: function to be considered for the contour
        :param isovalue: plotted isovalues. if no isovalue is provided default matplotlib settings are applied
        """

        # number of pixels in each direction of the plot
        nx = (self._plot.plot_width - 2 * self._plot.min_border) + 1
        ny = (self._plot.plot_height - 2 * self._plot.min_border) + 1
        # generate mesh
        x, y = np.meshgrid(np.linspace(self._plot.x_range.start, self._plot.x_range.end, nx),
                           np.linspace(self._plot.y_range.start, self._plot.y_range.end, ny))
        # evaluate function of grid
        z = f(x, y)
        # compute contour data
        data_contour, data_contour_label = self.__get_contour_data(x, y, z, isovalue=isovalue)
        # update data on contour plot
        self._contour_plot.data_source.data = data_contour
        if self._add_label:
            # update contour labels
            self._text_label.data_source.data = data_contour_label


    def set_contour_data(self, x, y, z, isovalue=None):
        # compute contour data
        data_contour, data_contour_label = self.__get_contour_data(x, y, z, isovalue=isovalue)
        # update data on contour plot
        self._contour_plot.data_source.data = data_contour
        if self._add_label:
            # update contour labels
            self._text_label.data_source.data = data_contour_label
		

    def __get_contour_data(self, x_grid, y_grid, z_grid, isovalue=None):
        """
        wrapper for matplotlib function. Extracting contour information into bokeh compatible data type.
        :param x_grid: grid of x values
        :param y_grid: grid of y values
        :param z_grid: function evaluation matching to x,y grid
        :param isovalue: isovalues to be extracted from contour plot, if no isovalue is provided default matplotlib
        settings are applied
        :return: two dicts, one holding contour information, one holding labelling information
        """
        if isovalue is None:
            cs = plt.contour(x_grid, y_grid, z_grid)
        else:
            cs = plt.contour(x_grid, y_grid, z_grid, isovalue)

        xs = []
        ys = []
        xt = []
        yt = []
        col = []
        text = []
        isolevelid = 0
        for isolevel in cs.collections:
            isocol = isolevel.get_color()[0]
            thecol = 3 * [None]
            theiso = str(cs.get_array()[isolevelid])
            isolevelid += 1
            for i in range(3):
                thecol[i] = int(255 * isocol[i])
            thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

            for path in isolevel.get_paths():
                v = path.vertices
                x = v[:, 0]
                y = v[:, 1]
                xs.append(x.tolist())
                ys.append(y.tolist())
                xt.append(x[int(len(x) / 2)])
                yt.append(y[int(len(y) / 2)])
                text.append(theiso)
                col.append(thecol)

        data_contour = {'xs': xs, 'ys': ys, 'line_color': col}
        data_contour_label = {'xt': xt, 'yt': yt, 'text': text}
        return data_contour, data_contour_label
