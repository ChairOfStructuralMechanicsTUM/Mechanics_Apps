from bokeh.models import ColumnDataSource
import os
from scipy import ndimage
import numpy as np
from math import ceil, floor, cos, sin


class Drawable:

    def __init__(self, p, filepath):
        """

        :param p: plot into which we draw
        :param filepath: relative path to the image source
        """
        self.draw_data = ColumnDataSource(data=dict(image=[], xS=[], yS=[], h=[], w=[]))
        self.orig_image = None
        self.orig_size = None
        self.p = p
        self.filepath = filepath

    def replace_image(self, new_filepath):
        print "replacing image"
        self.filepath = new_filepath
        x, y, w, h = self.draw_data.data['xS'][0],self.draw_data.data['yS'][0], self.draw_data.data['w'][0], self.draw_data.data['h'][0],
        self.draw_at(x, y, w, h)

    def __convertForBokeh(self, img):
        """
        transform saved image to a bokeh readable format.

        bokeh reads a 2D array.
        If we have a 3D array (usually the case {1st dim = x, 2nd dim = y, 3rd dim  = rgba}) then reorganise it so bokeh can read it

        :param img: input image (ndimage)
        :return:
        """

        if img.ndim > 2:
            if img.shape[2] == 3:
                # if the 3rd dimension only contains 3 elements (rgb), then add opacity (assumed to be fully opaque) dstack adds values at deepest levels in img values added are 255*matrix(with necessary size)
                img = np.dstack([img, np.ones(img.shape[:2], np.uint8) * 255])
            # view transforms 4 8bit integers into 1 32bit integer (8*4=32) i.e. 4 2bit integers to 1 8bit integer would be: [0 1 2 3] == [00 01 10 11] => [00011011] = [27] squeeze removes 1D arrays, i.e. : [[1], [2], [3], [4]] becomes [1, 2, 3, 4]
            img = np.squeeze(img.view(np.uint32))
        # thus we have a 2D array in bokeh readable format which can be returned
        return img

    def draw_at(self, x, y, w, h, pad_fraction=0):
        """

        :param x: x coordinates of picture
        :param y: y coordinates of picture
        :param w: width
        :param h: height
        :param pad_fraction: part of the dimensions that is padded around the picture
        :return:
        """

        # find path to file
        dir = os.path.dirname(__file__)
        absolute_filepath = os.path.join(dir, self.filepath)
        # upload file
        img = ndimage.imread(absolute_filepath)
        # convert file to bokeh readable image
        img = self.__convertForBokeh(img)
        # pad image so rotation can occur within frame
        size = img.shape
        padding_size = [int(ceil(size[0] * pad_fraction)), int(ceil(size[1] * pad_fraction))]
        img = np.lib.pad(img, ((padding_size[0], padding_size[0]), (padding_size[1], padding_size[1])), 'constant', constant_values=(0))
        x -= pad_fraction * w
        y -= pad_fraction * h
        w *= 1 + 2 * pad_fraction
        h *= 1 + 2 * pad_fraction
        # save information to ColumnDataSource and other variables for rotation later
        self.orig_image = img
        self.orig_size = img.shape
        # bokeh reads in the opposite direction to scipy so -1 corrects this
        self.draw_data.data = dict(image=[img[::-1, :]], xS=[x], yS=[y], w=[w], h=[h])
        # render image
        self.p.image_rgba(image='image', x='xS', y='yS', dw='w', dh='h', source=self.draw_data, level='annotation')

    def get_position(self):
        x = self.draw_data.data['xS'][0]
        y = self.draw_data.data['yS'][0]
        return x, y

    def move_to(self, pos):
        """
        modify the position. If any of the position coordinates is none, this position is not changed.
        :param pos:
        :return:
        """
        new_data = dict(self.draw_data.data)
        if pos[0] is not None:
            new_data['xS'] = [pos[0]]
        if pos[1] is not None:
            new_data['yS'] = [pos[1]]

        # update ColumnDataSource
        self.draw_data.data = new_data
        return new_data['xS'][0], new_data['yS'][0]


    def rotate_to(self, angle, center):
        """
        rotate original image by angle about rotation center
        :param angle:
        :param center:
        :return:
        """
        # rearrange 2D matrix into 3D matrix by splitting each 32bit int into 4 8bit ints
        # this makes it easier to access values
        img = self.orig_image.view(np.uint8).reshape(self.orig_size[0], self.orig_size[1], 4)
        # create new blank image
        new_img = np.zeros(img.shape, dtype=np.uint8)
        # cos(theta) and sin(theta) do not vary over loop so they are calculated in advance
        cos_theta = cos(angle)
        sin_theta = sin(angle)
        theta = angle
        # fill new_img with rotated img
        for i in range(0, self.orig_size[0]):
            Y = i - center[0]
            for j in range(0, self.orig_size[1]):
                X = j - center[1]
                if (img[i, j, 3] != 0):
                    # find new coordinates
                    Xcoord = center[0] + X * sin_theta + Y * cos_theta
                    Ycoord = center[1] + X * cos_theta - Y * sin_theta
                    # not all pixels are necessarily covered so filling 2 pixels prevents holes
                    # appearing in the image (up to theta=65)
                    if (new_img[int(floor(Xcoord)), int(floor(Ycoord)), 3] == 0):
                        new_img[int(floor(Xcoord)), int(floor(Ycoord)), :] = img[i, j, :]
                    if (new_img[int(ceil(Xcoord)), int(ceil(Ycoord)), 3] == 0):
                        new_img[int(ceil(Xcoord)), int(ceil(Ycoord)), :] = img[i, j, :]
        # convert new_img into bokeh readable format
        new_img = np.squeeze(new_img.view(np.uint32))
        # update ColumnDataSource
        new_data = self.draw_data.data
        new_data['image'] = [new_img[::-1, :]]
        self.draw_data.data = new_data