import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt


global g, dx
g = 9.81  # gravitational acceleration
dx = 1/128
end_time = 8
sample_rate = 128
time_interval = np.linspace(0, end_time, end_time * sample_rate +1)  # time interval

class Properties:  # storing and calculating the Properties of the System or the Force
    def __init__(self):
        self._stiffness = 1
        self._mass = 1
        self._zeta = 0.2
        self._w = 1
        self._wD = 1 
        self.T = 1
        self.f = 1
        self.fD = 1

    @property
    def stiffness(self):
        return self._stiffness

    @stiffness.setter
    def stiffness(self, x):
        self._w = np.sqrt(x / self._mass)  # circular frequecy [rad/s]
        self.T = 2 * np.pi / self._w  # Period [s]
        self.f = 1 / self.T  # frequency of vibration [Hz]
        self._wD = self._w * np.sqrt(1 - pow(self._zeta, 2))  # damped natural circular frequency
        self.fD = self.f * np.sqrt(1 - pow(self._zeta, 2))
        self._stiffness = x

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, x):
        self._w = np.sqrt(self._stiffness / x)  # circular frequency [rad/s]
        self._wD = self._w * np.sqrt(1 - pow(self._zeta, 2))  # damped natural circular frequency
        self.T = 2 * np.pi / self._w  # Period [s]
        self.f = 1 / self.T  # frequency of vibration [Hz]
        self.fD = self.f * np.sqrt(1 - pow(self._zeta, 2))
        self._mass = x
    # @mass.setter
    # def mass(self, x):
    #     self._mass = x
    #     self.stiffness(self._stiffness)

    @property
    def zeta(self):
        return self._zeta

    @zeta.setter
    def zeta(self, x):
        self._w = np.sqrt(self._stiffness / self._mass)  # circular frequency [rad/s]
        self._wD = self._w * np.sqrt(1 - pow(x, 2))  # damped natural circular frequency
        self.T = 2 * np.pi / self._w  # Period [s]
        self.f = 1 / self.T  # frequency of vibration [Hz]
        self.fD = self.f * np.sqrt(1 - pow(x, 2))
        self._zeta = x
    
    # @zeta.setter
    # def zeta(self, x):
    #     self._zeta = x
    #     self.stiffness(self._stiffness)

    @property
    def w(self):
        return self._w

    @property
    def wD(self):
        return self._wD


def unit_impulse_function(t, naturalValue):  # the unit impulse response function for the separate plot
    h = pow(naturalValue.mass * naturalValue.wD, -1) * np.exp(-naturalValue.zeta * naturalValue.w * np.abs(t)) * np.sin(naturalValue.wD * t) 
    return h

def harmonic_transfer_function(f_in, nV):
    w_0 = nV.w 
    w_in = f_in * 2*np.pi
    return 1/(nV.mass*(w_0**2 + 2*complex(0,1)*nV.zeta*w_0*w_in-(w_in)**2))


def cov_deformation(sigma, freq, naturalValue, t, active, G0 = 2):

    if active == 0:

        func = lambda r1, r2, teta: sigma*np.cos((2*np.pi)*freq * (teta -r1 + r2)) * pow(naturalValue.mass * naturalValue.wD, -1) * np.exp(-naturalValue.zeta * naturalValue.w * r1) * np.sin(naturalValue.wD * r2) * pow(naturalValue.mass * naturalValue.wD, -1) * np.exp(-naturalValue.zeta * naturalValue.w * r2) * np.sin(naturalValue.wD * r2)
        ans = []
        for i in t:
            ans.append(pow(naturalValue.mass * naturalValue.wD, -1) * integrate.dblquad(func, 0, 4, lambda r1: 0, lambda r1: 4, args=(i,))[0])
        return ans

    elif active == 1:

        func = lambda r1, r2, teta: sigma * np.exp( - 1/0.5 * (teta - r1 + r2)**2) *  pow(naturalValue.mass * naturalValue.wD, -1) * np.exp(-naturalValue.zeta * naturalValue.w * r1) * np.sin(naturalValue.wD * r2) * pow(naturalValue.mass * naturalValue.wD, -1) * np.exp(-naturalValue.zeta * naturalValue.w * r2) * np.sin(naturalValue.wD * r2)
        ans = []
        for i in t:
            ans.append(pow(naturalValue.mass * naturalValue.wD, -1) * integrate.dblquad(func, 0, 4, lambda r1: 0, lambda r1: 4, args=(i,))[0])
        return ans
    
    elif active == 2:

        return G0/ (4 * naturalValue.mass**2 * naturalValue.zeta *naturalValue.w**3) *np.exp(-naturalValue.zeta * naturalValue.w*np.abs(np.subtract.outer(t, t)[0])) * (np.cos(naturalValue.wD*np.subtract.outer(t, t)[0]) + naturalValue.zeta*naturalValue.w*np.sin(naturalValue.wD*np.abs(np.subtract.outer(t, t)[0]))/naturalValue.wD) # this is G0 calculated concerning angular frequency, however I need to calculate it with Hz so it matches the outcome of the calculation of G0 with the fourier transform 


#failure analysis
def rate_of_upcrossing(u, sigma, sigma_derivative, mean):
    v = sigma_derivative/(2*np.pi*sigma)*np.exp(-1/2 *((u-mean)/sigma)**2)
    return v

def prob_of_surv(v, L_0, t):
    L_x = L_0 * np.exp(-v*t)
    return L_x

def prob_of_failure_time(v, t):
    T_x = v * np.exp(-v * t)
    return T_x