from scipy.interpolate import PchipInterpolator
import numpy as np


def get_color_interpolator():
    """
    Creates a function that maps scalar values to RGB colors by applying a colormap defined by the colors below.
    Monotone cubic spline interpolation is used. For mor information see
    http://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
    :return: a function returning colors from scalar values
    """

    # color scheme
    x = [0.0, 0.16, 0.42, 0.6425, 0.8575, 1.0]
    c = [(0, 7, 100),
         (32, 107, 203),
         (237, 255, 255),
         (255, 170, 0),
         (0, 2, 0),
         (0, 7, 100)]  # last color equals first color for making colors cyclic
    # extracting color channels
    r = [c[i][0] for i in range(c.__len__())]
    g = [c[i][1] for i in range(c.__len__())]
    b = [c[i][2] for i in range(c.__len__())]
    # using monotone cubic spline interpolation
    r_interp = PchipInterpolator(x, r)
    g_interp = PchipInterpolator(x, g)
    b_interp = PchipInterpolator(x, b)
    # wrapping all color channels into one function
    c_interp = lambda x: np.array((r_interp(x), g_interp(x), b_interp(x))).transpose()

    return c_interp


def rgb_color_to_bokeh_rgba(color):
    """
    converts a RGB dataset to a RGBA dataset.
    The dataset is formatted in a fashion such that bokeh.plotting.Figure.image is able to parse the dataset. Therefore
    each RGBA value (4 times 8 Byte) is encoded in a single np.uint32 (32 Byte).
    :param color: dataset containing RGB values.
    :return: dataset containing uint32 values that encode RGBA values
    """

    color = color.astype(np.uint32)
    # use bitshift operations and typecasts for converting RGBA values to np.uint32
    img = (
    (color[0, :, :] << (0 * 8)) +   # Red
    (color[1, :, :] << (1 * 8)) +   # Green
    (color[2, :, :] << (2 * 8)) +   # Blue
    (255 << (3 * 8))                # Alpha by default 100%
    ).astype(np.uint32)             # convert to uint32

    return img


def iteration_count_to_rgb_color(data, frequency, max_value):
    """
    calculates a rgb color for each given scalar values in data.
    :param data: set of N scalar values in the range [0,max_value]
    :param frequency: frequency applied for periodical repetition of the colormap. i.e. if the data range is [0,10]
                      and frequency is 2, then the whole colormap gets applied to the range [0,5) and then the same
                      colormap is applied to [5,10] in a periodic fashion.
    :param max_value: maximum value in the dataset. Data values that are equal to max_value are colored black,
                      regardless of the colormap.
    :return: an array of N RGB values.
    """
    # get colormap
    c_interp = get_color_interpolator()
    # color set according to colormap (coloring a periodic fashion with a predefined frequency)
    color = c_interp((data % frequency) / frequency).transpose()
    # explicitly color regions, where maximum iteration was reached, black
    color[0, data == max_value] = 0.0  # red channel = 0
    color[1, data == max_value] = 0.0  # green channel = 0
    color[2, data == max_value] = 0.0  # blue channel = 0

    return color
