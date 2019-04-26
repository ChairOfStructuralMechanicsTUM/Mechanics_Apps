from numpy.polynomial.laguerre import laggauss
from numpy.polynomial.hermite import hermgauss
import numpy as np

def lagIntegrate(function, n_points):
    """
    0 to infity
    """
    points, weights = laggauss(n_points)
    integrand = np.sum(weights*function(points))
    return integrand


def genHermIntegrate(function, n_points):
    """
    -inf to inf
    """
    points, weights = hermgauss(n_points)
    integrand = np.sum(weights * function(points) )
    return integrand


# print(lagIntegrate(lambda x: x**2, 1))
print(genHermIntegrate(lambda x: (1 / (1+x**2)) * np.exp(x**2), 370))
