import numpy as np

from diffraction_computation import compute_wave_amplitude, compute_fresnel_at_polar, cart2pol


class Grid:

    def __init__(self, x_min, x_max, nx, y_min, y_max, ny):

        self._x, self._y = np.meshgrid(np.linspace(x_min, x_max, num=nx),
                                       np.linspace(y_min, y_max, num=ny))

        self._rho, self._phi = cart2pol(self._x,self._y)

        # values below are set later. This is potential for inheritance!

        self._phi0 = None
        self._wavelength = None
        self._c = None

        self._phiplus = None
        self._phiminus = None

    def set_wave_parameters(self, phi0, wavelength, c):
        self._phi0 = phi0
        self._wavelength = wavelength
        self._c = c
        self._phiplus, self._phiminus = compute_fresnel_at_polar(self._rho, self._phi, self._phi0, self._wavelength)

    def compute_wave_amplitude(self, t):
        return compute_wave_amplitude(self._rho, self._phi, self._phiplus, self._phiminus, self._wavelength, self._phi0, self._c, t)