from __future__ import division

import numpy as np
from bokeh.models import ColumnDataSource
import vtk
from vtk.util import numpy_support


class diffraction_Contour:
    """
    adds a contour plot to a given plot. MatPlotLibs contour plot is utilized for computing the contour data. That data
    is plotted using bokehs multi_line function. Optionally the user can add labels to the contour data using bokehs
    text function.
    """

    def __init__(self, plot, add_label=False, line_color='line_color', path_filter = 0, **kwargs):
        """
        :param plot: plot where the contour is plotted
        :param add_label: bool to define whether labels are added to the contour
        :param line_color: defining line color, if no line color is supplied, the default line color scheme from
        matplotlib is used
        :param path_filter: paths with less than this number of vertices are ignored. This removes noise/features.
        :param kwargs: additional bokeh line plotting arguments like width, style ect...
        """
        self._plot = plot
        #contour_source = ColumnDataSource(data=dict(xs=[], ys=[], line_color=[]))
        contour_source = ColumnDataSource(data=dict(x0=[], x1=[], y0=[], y1=[]))
        #self._contour_plot = self._plot.multi_line(xs='xs', ys='ys', source=contour_source, **kwargs)
        self._contour_plot = self._plot.segment(x0='x0', x1='x1', y0='y0', y1='y1', color=line_color, source=contour_source, **kwargs)
        self._path_filter = path_filter
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
        #data_contour, data_contour_label = self.__get_contour_data_mpl(x, y, z, isovalue=isovalue)
        data_contour, data_contour_label = self.__get_contour_data_vtk(x, y, z, isovalue=isovalue)
        # update data on contour plot
        self._contour_plot.data_source.data = data_contour
        if self._add_label:
            # update contour labels
            self._text_label.data_source.data = data_contour_label

    def set_contour_data(self, x, y, z, isovalue=None):
        # compute contour data
        #data_contour, data_contour_label = self.__get_contour_data_mpl(x, y, z, isovalue=isovalue)
        data_contour, data_contour_label = self.__get_contour_data_vtk(x, y, z, isovalue=isovalue)
        # update data on contour plot
        self._contour_plot.data_source.data = data_contour
        if self._add_label:
            # update contour labels
            self._text_label.data_source.data = data_contour_label

    # def __get_contour_data_mpl(self, x_grid, y_grid, z_grid, isovalue=None):
    #     """
    #     wrapper for matplotlib function. Extracting contour information into bokeh compatible data type.
    #     :param x_grid: grid of x values
    #     :param y_grid: grid of y values
    #     :param z_grid: function evaluation matching to x,y grid
    #     :param isovalue: isovalues to be extracted from contour plot, if no isovalue is provided default matplotlib
    #     settings are applied
    #     :return: two dicts, one holding contour information, one holding labelling information
    #     """
    #     if isovalue is None:
    #         cs = plt.contour(x_grid, y_grid, z_grid)
    #     else:
    #         cs = plt.contour(x_grid, y_grid, z_grid, isovalue)

    #     xs = []
    #     ys = []
    #     xt = []
    #     yt = []
    #     col = []
    #     text = []
    #     isolevelid = 0
    #     for isolevel in cs.collections:
    #         isocol = isolevel.get_color()[0]
    #         thecol = 3 * [None]
    #         theiso = str(cs.get_array()[isolevelid])
    #         isolevelid += 1
    #         for i in range(3):
    #             thecol[i] = int(255 * isocol[i])
    #         thecol = '#%02x%02x%02x' % (thecol[0], thecol[1], thecol[2])

    #         for path in isolevel.get_paths():
    #             v = path.vertices
    #             if v.shape[0] > self._path_filter: # we only consider paths with more than path_filter vertices
    #                 x = v[:, 0]
    #                 y = v[:, 1]
    #                 xs.append(x)
    #                 ys.append(y)
    #                 xt.append(x[int(len(x) / 2)])
    #                 yt.append(y[int(len(y) / 2)])
    #                 text.append(theiso)
    #                 col.append(thecol)

    #     data_contour = {'xs': xs, 'ys': ys, 'line_color': col}
    #     data_contour_label = {'xt': xt, 'yt': yt, 'text': text}
    #     return data_contour, data_contour_label

    def __get_contour_data_vtk(self, x_grid, y_grid, z_grid, isovalue=[0]):

        """
        wrapper for vtk marching squares function. Extracting contour information into bokeh compatible data type.
        Less comfortable (no text labels, no coloring) but faster then __get_contour_data_mpl
        :param x_grid:
        :param y_grid:
        :param z_grid:
        :param isovalue:
        :return:
        """
        nx, ny = x_grid.shape

        xmin = self._plot.x_range.start
        xmax = self._plot.x_range.end
        ymin = self._plot.y_range.start
        ymax = self._plot.y_range.end

        hx = (xmax - xmin) / (nx - 1)
        hy = (ymax - ymin) / (ny - 1)
        
        image = vtk.vtkImageData()
        image.SetDimensions(nx, ny, 1)
        image.SetOrigin(xmin, ymin, 0)
        image.SetSpacing(hx, hy, 0)

        data = vtk.vtkDoubleArray()
        data.SetNumberOfComponents(1)
        data.SetNumberOfTuples(image.GetNumberOfPoints())
        data.SetName("Values")

        # we load the z_data into vtk datatypes
        vtk_data_array = numpy_support.numpy_to_vtk(z_grid.ravel(), deep=True, array_type=vtk.VTK_DOUBLE)
        image.AllocateScalars(vtk.VTK_DOUBLE, 1)
        image.GetPointData().SetScalars(vtk_data_array)

        # apply marchign squares
        ms = vtk.vtkMarchingSquares()
        ms.SetInputData(image)
        for i in range(isovalue.__len__()):  # set isovalues
            ms.SetValue(i, isovalue[i])
        ms.SetImageRange(0, image.GetDimensions()[0], 0, image.GetDimensions()[1], 0, 0)
        ms.Update()

        # read output
        poly = ms.GetOutput()
        points = poly.GetPoints()
        lines = poly.GetLines()

        pts = numpy_support.vtk_to_numpy(points.GetData())  # get points
        line_idx = numpy_support.vtk_to_numpy(lines.GetData())  # get lines

        # lines are encoded as [nVerticesLine1, firstId, secondId, ... , nVerticesLine2...]
        # We always have 2 vertices per line. This justifies the stride 3 pattern below
        even_idx = line_idx[1::3]
        odd_idx = line_idx[2::3]

        x0 = pts[odd_idx, 0]
        y0 = pts[odd_idx, 1]
        x1 = pts[even_idx, 0]
        y1 = pts[even_idx, 1]

        data_contour = {'x0': x0, 'x1': x1, 'y0': y0, 'y1': y1}
        data_contour_label = {}
        return data_contour, data_contour_label



