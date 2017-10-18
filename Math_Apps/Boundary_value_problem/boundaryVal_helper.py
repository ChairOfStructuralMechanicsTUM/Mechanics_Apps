from __future__ import division

from scipy import ndimage
import os
import numpy as np

import boundaryVal_settings as bv_settings

def prepareImgBokehRGBA(img):
    if img.ndim > 2: # could also be img.dtype == np.uint8
        if img.shape[2] == 3: # alpha channel not included
            img = np.dstack([img, np.ones(img.shape[:2], np.uint8) * 255])
        img = np.squeeze(img.view(np.uint32))
    return img


def draw_image(fig, img, x, y, scale_x, scale_y):
    """
    draw an image at a given position. Scale the image by a given factor.
    :param fig: bokeh.plotting.Figure the image is plotted in
    :param img: raw image data. A np array of the shape (xpixel,ypixel,4). The 4 values are (r,g,b,a)
    :param x: x position of lower left corner
    :param y: y position of lower left corner
    :param scale_x: scaling in x dimension, w.r.t. plot dimensionality
    :param scale_y: scaling in y dimension, w.r.t. plot dimensionality
    """
    img = prepareImgBokehRGBA(img)
    fig.image_rgba(image=[img[::-1,:]], x=[x], y=[y],
                   dw=[img.shape[1]/img.shape[1]*scale_x],
                   dh=[img.shape[0]/img.shape[1]*scale_y])


def draw_cannon(fig):
    """
    draw the cannon picture
    :param fig: bokeh.plotting.Figure in which the cannon is drawn
    """

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'Pictures/cannon.png')
    img = ndimage.imread(filename)

    scaling_cannon = 60
    scaling_cannon_x = scaling_cannon*(bv_settings.max_x-bv_settings.min_x)/bv_settings.fig_width
    scaling_cannon_y = scaling_cannon*(bv_settings.max_y-bv_settings.min_y)/bv_settings.fig_height

    x = -0.5*img.shape[1]/img.shape[1]*scaling_cannon_x
    y = -0.5*img.shape[0]/img.shape[1]*scaling_cannon_y

    draw_image(fig, img, x, y, scaling_cannon_x, scaling_cannon_y)



def draw_target_at(fig, x_target):
    """
    draws the target picture at a given position
    :param fig: bokeh.plotting.Figure in which the target is drawn
    :param x_target: x position of the target
    """

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'Pictures/target.png')
    img = ndimage.imread(filename)

    scaling_target = 30
    scaling_target_x = scaling_target*(bv_settings.max_x-bv_settings.min_x)/bv_settings.fig_width
    scaling_target_y = scaling_target*(bv_settings.max_y-bv_settings.min_y)/bv_settings.fig_height

    x = x_target - .5 * img.shape[1] / img.shape[1] * scaling_target_x
    y = -.5*img.shape[0]/img.shape[1]*scaling_target_y

    draw_image(fig, img, x, y, scaling_target_x, scaling_target_y)