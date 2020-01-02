# TODO this script contains a large amount of duplicated code from e.g. Mechanic_Apps/Diffraction/quiver.py etc. should be refactored!

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


def quiver_to_data(x, y, u, v, h, do_normalization=True, fix_at_middle=True):
    warn("quiver to data is deprecated! Use Quiver object instead!")

    def __normalize(u, v, h):
        length = np.sqrt(u ** 2 + v ** 2)
        max_length = np.max(length)
        if do_normalization:
            u[length > 0] *= 1.0 / length[length > 0] * h * .9
            v[length > 0] *= 1.0 / length[length > 0] * h * .9
        elif (max_length is not 0):
            u[length > 0] *= 1.0 / max_length * h * .9
            v[length > 0] *= 1.0 / max_length * h * .9
        else:
            u[:] = 0
            v[:] = 0
        u[length == 0] = 0
        v[length == 0] = 0
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
            return np.array([[c, -s, 0],
                             [s, +c, 0],
                             [0, +0, 1]])

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
                if x == 0:
                    return np.pi * .5 + int(y <= 0) * np.pi
                else:
                    if y >= 0:
                        if x > 0:
                            return np.arctan(y / x)
                        elif x < 0:
                            return -np.arctan(y / -x) + np.pi
                        else:
                            return 1.5 * np.pi
                    else:
                        if x > 0:
                            return -np.arctan(-y / x)
                        elif x < 0:
                            return np.arctan(-y / -x) + np.pi
                        else:
                            return .5 * np.pi

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


def check_user_view(view_data, plot):
    """
    checks for a change in the user view that affects the plotting
    :param view_data: dict containing the current view data
    :param plot: handle to the plot
    :return: bool that states if any relevant parameter has been changed
    """

    user_view_has_changed = (view_data['x_start'][0] != plot.x_range.start) or \
                            (view_data['x_end'][0] != plot.x_range.end) or \
                            (view_data['y_start'][0] != plot.y_range.start) or \
                            (view_data['y_end'][0] != plot.y_range.end)

    return user_view_has_changed


def get_user_view(plot):
    """
    returns the current user view of the plot
    :param plot: a bokeh.plotting.Figure
    :return: a dict that can be used for a bokeh.models.ColumnDataSource
    """
    x_start = plot.x_range.start  # origin x
    y_start = plot.y_range.start  # origin y
    x_end = plot.x_range.end  # final x
    y_end = plot.y_range.end  # final y

    return dict(x_start=[x_start], y_start=[y_start], x_end=[x_end], y_end=[y_end])


def string_to_function_parser(fun_str, args):
    """
    converts a string to a lambda function.
    :param fun_str: string representation of the function
    :param args: symbolic arguments that will be turned into lambda function arguments
    :return:
    """

    fun_sym = sympify(fun_str)
    fun_lam = sym_to_function_parser(fun_sym, args)

    return fun_lam, fun_sym


def sym_to_function_parser(fun_sym, args):
    """
    converts a symbolic expression to a lambda function. The function handles constant and zero symbolic input such that
    on numpy.array input a numpy.array with identical size is returned.
    :param fun_sym: symbolic expression
    :param args: symbols turned into function input arguments
    :return:
    """

    if fun_sym.is_constant():
        fun_lam = lambda *x: np.ones_like(x[0]) * float(fun_sym)
    else:
        fun_lam = lambdify(args, fun_sym, modules=['numpy'])

    return fun_lam


def compute_gradient(fun_sym, args):
    """
    computes the gradient of fun_sym w.r.t. every symbol in args
    :param fun_sym: scalar function
    :param args: arguments to build derivatives
    :return:
    """
    df_sym = []
    for s in args:
        dfds_sym = diff(fun_sym, s)
        df_sym.append(sym_to_function_parser(dfds_sym, args))
    df = lambda x, y: [_(x, y) for _ in df_sym]

    return df, df_sym


def find_closest_on_iso(x0, y0, g):
    # objective function = distance function to original point (x0,y0)
    f = lambda x: (x[0] - x0) ** 2 + (x[1] - y0) ** 2
    df = lambda x: np.array([2 * (x[0] - x0), 2 * (x[1] - y0)])
    # constraint g(x,y) == 0
    cons = ({'type': 'eq', 'fun': lambda x: g(x[0], x[1])})
    # minimize distance to original point under the constraint g(x,y) == 0
    x, y = minimize(f, [x0, y0], constraints=cons, jac=df)['x']

    return x, y


class Interactor:
    """
    adds a click interactor to a given plot. This interactor can detect, if a position in the plot is clicked on, return
    that position and call a respective callback function, if a point is clicked.
    """

    def __init__(self, plot, square_size=5):
        """
        :param plot: plot where the contour is plotted
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
        self._pseudo_square.data_source.selected.on_change('indices', callback_function)

    def clicked_point(self):
        """
        returns the currently clicked on point in the local coordinate system of self._plot
        :return:
        """
        print("HERE")
        if len(self._pseudo_square.data_source.selected.indices) > 0:
            id = self._pseudo_square.data_source.selected.indices[0]
            x_coor = self._pseudo_square.data_source.data['x'][id]
            y_coor = self._pseudo_square.data_source.data['y'][id]
            return x_coor, y_coor
        else:
            return None, None


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
                xt.append(x[len(x) / 2])
                yt.append(y[len(y) / 2])
                text.append(theiso)
                col.append(thecol)

        data_contour = {'xs': xs, 'ys': ys, 'line_color': col}
        data_contour_label = {'xt': xt, 'yt': yt, 'text': text}
        return data_contour, data_contour_label


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
                return np.array([[c, -s, 0],
                                 [s, +c, 0],
                                 [0, +0, 1]])

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
                    if x == 0:
                        return np.pi * .5 + int(y <= 0) * np.pi
                    else:
                        if y >= 0:
                            if x > 0:
                                return np.arctan(y / x)
                            elif x < 0:
                                return -np.arctan(y / -x) + np.pi
                            else:
                                return 1.5 * np.pi
                        else:
                            if x > 0:
                                return -np.arctan(-y / x)
                            elif x < 0:
                                return np.arctan(-y / -x) + np.pi
                            else:
                                return .5 * np.pi

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
