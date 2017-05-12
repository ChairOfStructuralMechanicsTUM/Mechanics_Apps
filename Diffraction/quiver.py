from __future__ import division
import numpy as np
from bokeh.models import ColumnDataSource
import matplotlib as mpl

class Quiver:
    """
    adds a quiver plot to the given bokeh.Figure
    """

    def __init__(self, plot, fix_at_middle=True, **kwargs):
        """
        creates the quiver object for the plot. For a quiver plot we need the following ingredients:
        1. segments for the arrow shaft
        2. patches for the arrow tips
        (3. points marking the base position of the arrow)
        :param plot: referenced plot
        :param fix_at_middle: states wheather the arrows are fixed at the middle or at the beginning to the reference
        point
        :param kwargs: additional arguments passed to the bokeh plotting functions, e.g. color, line width etc
        """
        self._plot = plot
        segment_source = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[]))
        patch_source = ColumnDataSource(data=dict(xs=[], ys=[]))
        self._segments = self._plot.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=segment_source, **kwargs)
        self._patches = self._plot.patches(xs='xs', ys='ys', source=patch_source, **kwargs)
        self._fix_at_middle = fix_at_middle
        if self._fix_at_middle:
            base_source = ColumnDataSource(data=dict(x=[], y=[]))
            self._base = self._plot.circle(x='x', y='y', source=base_source, size=1.5, **kwargs)

    def compute_quiver_data(self, x_grid, y_grid, u_grid, v_grid, h=1.0, scaling=.9, normalize=True):
        """
        computes and updates the quiver data for the given quiver field.
        :param x_grid: x positions on the grid
        :param y_grid: y positions on the grid
        :param u_grid: x components of the arrows
        :param v_grid: y components of the arrows
        :param h: length of one arrow
        :param scaling: scaling of the length w.r.t. normalization
        :param normalize: normalize to length
        """
        # compute quiver data
        x_grid = np.array(x_grid)
        y_grid = np.array(y_grid)
        u_grid = np.array(u_grid)
        v_grid = np.array(v_grid)

        if (x_grid.size > 1):
            if (len(x_grid.shape) == 1):
                h = x_grid[1] - x_grid[0]
            elif (len(x_grid.shape) == 2):
                h = x_grid[0, 1] - x_grid[0, 0]

        data_segments, data_patches, data_base = self.__quiver_to_data(x_grid, y_grid, u_grid, v_grid,
                                                                       h=h, do_normalization=normalize,
                                                                       fix_at_middle=self._fix_at_middle)
        # update data on quiver plot
        self._segments.data_source.data = data_segments
        self._patches.data_source.data = data_patches
        if self._fix_at_middle:
            self._base.data_source.data = data_base

    def clear_quiver_data(self):
        data_segments = dict(x0=[], y0=[], x1=[], y1=[])
        data_patches = dict(xs=[], ys=[])
        self._segments.data_source.data = data_segments
        self._patches.data_source.data = data_patches
        if self._fix_at_middle:
            data_base = dict(x=[], y=[])
            self._base.data_source.data = data_base

    def __quiver_to_data(self, x, y, u, v, h, do_normalization=True, fix_at_middle=True):
        def __normalize(u, v, h):
            length = np.sqrt(u ** 2 + v ** 2)
            if do_normalization:
                u[length > 0.0] *= 1.0 / length[length > 0.0] * h
                v[length > 0.0] *= 1.0 / length[length > 0.0] * h
            u[length == 0.0] = 0.0
            v[length == 0.0] = 0.0
            return u, v

        def quiver_to_segments(x, y, u, v, h):
            x = x.flatten()
            y = y.flatten()
            u = u.flatten()
            v = v.flatten()

            u, v = __normalize(u, v, h)

            x0 = x
            y0 = y
            x1 = x + u
            y1 = y + v

            if fix_at_middle:
                x0 -= u * .5
                y0 -= v * .5
                x1 -= u * .5
                y1 -= v * .5

            return x0, y0, x1, y1

        def quiver_to_arrowheads(x, y, u, v, h):

            def __t_matrix(translate_x, translate_y):
                return np.array([[1, 0, translate_x],
                                 [0, 1, translate_y],
                                 [0, 0, 1]])

            def __r_matrix(rotation_angle):
                c = np.cos(rotation_angle)
                s = np.sin(rotation_angle)
                return np.array([[+c, -s, +0],
                                 [+s, +c, +0],
                                 [+0, +0, +1]])

            def __head_template(x0, y0, u, v, type_id, headsize):
                if type_id is 0:
                    x_patch = 3 * [None]
                    y_patch = 3 * [None]

                    x1 = x0 + u
                    x_patch[0] = x1
                    x_patch[1] = x1 - headsize
                    x_patch[2] = x1 - headsize

                    y1 = y0 + v
                    y_patch[0] = y1
                    y_patch[1] = y1 + headsize / np.sqrt(3)
                    y_patch[2] = y1 - headsize / np.sqrt(3)
                elif type_id is 1:
                    x_patch = 4 * [None]
                    y_patch = 4 * [None]

                    x1 = x0 + u
                    x_patch[0] = x1
                    x_patch[1] = x1 - headsize
                    x_patch[2] = x1 - headsize / 2
                    x_patch[3] = x1 - headsize

                    y1 = y0 + v
                    y_patch[0] = y1
                    y_patch[1] = y1 + headsize / np.sqrt(3)
                    y_patch[2] = y1
                    y_patch[3] = y1 - headsize / np.sqrt(3)
                else:
                    raise Exception("unknown head type!")

                return x_patch, y_patch

            def __get_patch_data(x0, y0, u, v, headsize):

                def angle_from_xy(x, y):
                    return np.arctan2(y,x)

                angle = angle_from_xy(u, v)

                x_patch, y_patch = __head_template(x0, y0, u, v, type_id=0, headsize=headsize)

                T1 = __t_matrix(-x_patch[0], -y_patch[0])
                R = __r_matrix(angle)
                T2 = __t_matrix(x_patch[0], y_patch[0])
                T = T2.dot(R.dot(T1))

                for i in range(x_patch.__len__()):
                    v_in = np.array([x_patch[i], y_patch[i], 1])
                    v_out = T.dot(v_in)
                    x_patch[i], y_patch[i], tmp = v_out

                return x_patch, y_patch

            x = x.flatten()
            y = y.flatten()
            u = u.flatten()
            v = v.flatten()

            u, v = __normalize(u, v, h)

            n_arrows = x.shape[0]
            xs = n_arrows * [None]
            ys = n_arrows * [None]

            headsize = .1 * h
            if fix_at_middle:
                for i in range(n_arrows):
                    x_patch, y_patch = __get_patch_data(x[i] - .5 * u[i], y[i] - .5 * v[i], u[i], v[i], headsize)
                    xs[i] = x_patch
                    ys[i] = y_patch
            else:
                for i in range(n_arrows):
                    x_patch, y_patch = __get_patch_data(x[i], y[i], u[i], v[i], headsize)
                    xs[i] = x_patch
                    ys[i] = y_patch

            return xs, ys

        x0, y0, x1, y1 = quiver_to_segments(x, y, u, v, h)
        ssdict = dict(x0=x0, y0=y0, x1=x1, y1=y1)

        xs, ys = quiver_to_arrowheads(x, y, u, v, h)
        spdict = dict(xs=xs, ys=ys)
        sbdict = dict(x=x.flatten(), y=y.flatten())

        return ssdict, spdict, sbdict