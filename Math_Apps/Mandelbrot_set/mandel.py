from __future__ import division
import numpy as np
from numba import vectorize, guvectorize
import time


def mandel(x0, y0, xw, yw, x_res, y_res, iterate_max, iteration_bound):
    """
    computes the mandelbrot set for a part of the complex plane (computation region). The region is discretized
    by only computing certain pixel values (corresponding to a given resolution).
    :param x0: origin x of computation region
    :param y0: origin y of computation region
    :param xw: width of computation region
    :param yw: height of computation region
    :param x_res: resolution in x direction
    :param y_res: resolution in y direction
    :param iterate_max: maximum number of iterations that are computed
    :param iteration_bound: upper bound for continuing iterating the mandelbrot set
    :return: array containing number of iterations for each gridpoint
    """
    @guvectorize(['void(float64[:,:], float64[:,:],float64[:,:])'], '(m,n),(m,n)->(m,n)', target='parallel')
    def iterate_mandelbrot(c_re, c_im, it_count):
        """
        Calculate the mandelbrot sequence for all points c in the complex plane c = [c_re,c_im]. This function is
        vectorized by using the decorator @guvectorize above.
        :param c_re: a NxM array with real part of points in the complex plane.
        :param c_im: a NxM array with imaginary part of points in the complex plane.
        :param it_count: a NxM array where the iteration count until divergence is saved to.
        """

        apply_smoothening = True  # trigger for applying smooth color algorithm or not. See wikipedia on mandelbrot.

        m, n = c_re.shape

        # mandelbrot iteration algorithm
        for i in range(m):
            for j in range(n):
                re = 0
                im = 0
                count = iterate_max
                for it_n in xrange(iterate_max + 1):
                    xx = re * re
                    yy = im * im
                    xy = re * im
                    re = xx - yy + c_re[i, j]
                    im = 2 * xy + c_im[i, j]
                    if (xx + yy) > iteration_bound:
                        count = it_n
                        break

                if count < iterate_max and apply_smoothening:
                    log_zn = np.log(xx + yy) * .5
                    nu = np.log(log_zn / np.log(2)) / np.log(2)
                    count += 1 - nu

                it_count[i, j] = count

    t0 = time.clock()

    # create grid in the complex plane
    re, im = np.meshgrid(np.linspace(x0, x0 + xw, x_res, dtype=np.float64),
                         np.linspace(y0, y0 + yw, y_res, dtype=np.float64))
    # initialite array where results are saved to
    it_count = np.zeros(re.shape, dtype=np.float64)
    # call vectorized worker function
    print "calling iterate_mandelbrot."
    iterate_mandelbrot(re, im, it_count)
    print "elapsed time:" + str(time.clock() - t0) + " sec"

    return it_count