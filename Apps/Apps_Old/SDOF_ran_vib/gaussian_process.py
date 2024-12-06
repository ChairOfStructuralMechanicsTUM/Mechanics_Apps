import numpy as np
import matplotlib.pyplot as plt
from pyrsistent import v
from scipy.stats import multivariate_normal
from scipy.stats import norm


rng = np.random.default_rng(seed=42)  # seed for repeatability


def squared_exponential_cov(t, sigma, correlation_length):
    cov = sigma**2 * np.exp( - np.subtract.outer(t, t)**2/(correlation_length**2))
    return cov

def cos_cov(t, freq, bandwidth, sigma):
    tau = np.subtract.outer(t, t) 
    frequencies = tau* freq
    cov = sigma**2 * np.cos((2*np.pi)*frequencies) * np.sinc(bandwidth*tau/np.pi)
    return cov

def dirac_delta_cov(G0, t):
    dif = np.abs(np.subtract.outer(t, t))
    for d in range(len(dif)): 
        for i in range(len(dif)):
            if dif[d][i] == 0:
                dif[d][i] = G0**2
            else:
                dif[d][i] = 0
    return dif

def matérn_class(t,l, sigma): #für v = 3/2
    cov = sigma**2 *(1 + np.sqrt(3)*np.abs(np.subtract.outer(t, t))/l) * np.exp(- np.sqrt(3)* np.abs(np.subtract.outer(t, t))/l)
    return cov

def gaussian_function(mean, cov):
    try:  # takes around 0.04 seconds more than just doing eigh
        result = rng.multivariate_normal(mean, cov, method="cholesky")  # is faster but only works on positive definite cov matrices
    except np.linalg.LinAlgError:  # if cov matrix is not positive definite
        result = rng.multivariate_normal(mean=mean, cov=cov, method="eigh")
    return result

def Gaussian_distribution_pdf(u, mean, sigma):
    return 1/np.sqrt(2*np.pi * sigma**2) * np.exp(- 0.5 *(u-mean)**2/(sigma**2)) 

def Gaussian_distribution_cdf(u, mean, sigma):
    d = norm(loc= mean, scale=sigma)
    gauss_cdf = []
    for u_val in u:
        gauss_cdf.append(d.cdf(u_val))
    return gauss_cdf
  

def plot_Gaussian_contours(mu,sigma,N=100):
    """
    Plot contours of a 2D multivariate Gaussian based on N points. Given points x and y are 
    given for the limits of the contours
    nach https://nbviewer.org/github/adamian/adamian.github.io/blob/master/talks/Brown2016.ipynb
    """
    X, Y = np.meshgrid(np.linspace(-5,5,100), np.linspace(-5,5,N))
    rv = multivariate_normal(mu, sigma)
    Z = rv.pdf(np.dstack((X,Y)))
    cs = plt.contour(X,Y,Z)
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
    return xs, ys, col, xt, yt, text






