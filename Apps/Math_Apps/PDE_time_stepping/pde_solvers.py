from __future__ import division
import scipy.sparse as sp
import scipy.sparse.linalg as lin

import pde_constants

c_heat = pde_constants.heat_conductivity
c_wave = pde_constants.wave_number

def heat_do_explicit_step(ux, u0, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j) with spatial meshwidth h and temporal meshwidth k for
    the 1D heat equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.894 ff."
    Stability criterion:
        r  = k / h**2 <= 1
    :param u0: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u1: solution u(x,t=t+k)
    """

    n = u0.shape[0]
    r = (c_heat ** 2) * k / (h ** 2)
    iteration_matrix = (r * sp.eye(n, n, -1) - 2 * r * sp.eye(n, n) + r * sp.eye(n, n, 1)).tocsr()
    iteration_matrix[0, 0] = 0  # enforcing dirichlet BC -> no change!
    iteration_matrix[0, 1] = 0
    iteration_matrix[n - 1, n - 1] = 0
    iteration_matrix[n - 1, n - 2] = 0
    iteration_matrix += sp.eye(n, n)
    u1 = iteration_matrix.dot(u0)
    return u1


def heat_do_implicit_step(ux, u0, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j) with spatial meshwidth h and temporal meshwidth k for
    the 1D heat equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.894 ff."
    Since we are using an implicit time stepping scheme, there is no stability criterion. We use
    scipy.linalg.solve_banded for solving the implicit equation. Theferfore we need to convert our implicit equation
    into ordered diagonal format:
        u1 = u0 + A_h * u1
    ->  (Id - A_h) * u1 = u0
    This is a system of linear equations: A * x = b with
        A = Id - A_h
        x = u1
        b = u0

    :param u0: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u1: solution u(x,t=t+k)
    """

    n = u0.shape[0]
    r = (c_heat ** 2) * k / (h ** 2)
    iteration_matrix = (r * sp.eye(n, n, -1) - 2 * r * sp.eye(n, n) + r * sp.eye(n, n, 1)).tocsr()
    iteration_matrix[0, 0] = 0  # enforcing dirichlet BC -> no change!
    iteration_matrix[0, 1] = 0
    iteration_matrix[n - 1, n - 1] = 0
    iteration_matrix[n - 1, n - 2] = 0
    iteration_matrix = -iteration_matrix
    iteration_matrix += sp.eye(n, n)
    u1 = lin.spsolve(iteration_matrix, u0)
    return u1


def wave_do_explicit_step(u0, u1, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j-1) and u1 = u^(j) with spatial meshwidth h and temporal
    meshwidth k for the 1D wave equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.904 ff."
    Stability criterion:
        r  = (k / h)**2 <= 1
    :param u0: solution u(x,t=t-k)
    :param u1: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u2: solution u(x,t=t+k)
    """

    n = u0.shape[0]
    r = (c_wave * k / h) ** 2
    a_h = (-2 * r * sp.eye(n, n) + r * sp.eye(n, n, -1) + r * sp.eye(n, n, 1)).tocsr()
    iteration_matrix1 = 2 * sp.eye(n, n) + a_h
    iteration_matrix1[0, 0] = 1
    iteration_matrix1[0, 1] = 0
    iteration_matrix1[n - 1, n - 1] = 1
    iteration_matrix1[n - 1, n - 2] = 0

    iteration_matrix0 = - 1 * sp.eye(n, n).tocsr()
    iteration_matrix0[0, 0] = 0
    iteration_matrix0[n - 1, n - 1] = 0

    u2 = iteration_matrix1.dot(u1) + iteration_matrix0.dot(u0)

    return u2


def wave_do_implicit_step(u0, u1, k, h):
    """
    Does one timestep for given initial conditions at u0 = u^(j-1) and u1 = u^(j) with spatial meshwidth h and temporal
    meshwidth k for the 1D wave equation. For notation an theory see
        "Karpfinger, Hoehere Mathematik in Rezepten, 2.Auflage, p.904 ff."
    Since we are using an implicit time stepping scheme, there is no stability criterion. We are using the central
    second order finite difference stencil for approximating u_tt as well as u_xx and obtain the following implicit
    scheme:
        u_tt = u_xx -> u^(k+1)-2*u^(k)+u^(k-1) = k^2 * .5 * (A_h * u^(k+1) + A_h * u(k-1)),
    where A_h is the spatial discretization matrix with the stencil 1/h^2 * [1 -2  1].

    This results in the implicit update rule:
        (Id - .5 * k^2 * A_h) * u^(k+1) = 2*u^(k) - (Id - .5 * k^2 * A_h) * u^(k-1)

    Where we compute u^(k+1) by solving the band diagonal system using scipy.linalg.solve_banded.

    :param u0: solution u(x,t=t-k)
    :param u1: solution u(x,t=t)
    :param k: temporal meshwidth
    :param h: spatial meshwidth
    :return: u2: solution u(x,t=t+k)
    """

    n = u0.shape[0]
    r = (c_wave * k / h) ** 2
    a_h = (-2 * r * sp.eye(n, n) + r * sp.eye(n, n, -1) + r * sp.eye(n, n, 1)).tocsr()
    a_h[0, 0] = 0
    a_h[0, 1] = 0
    a_h[n - 1, n - 2] = 0
    a_h[n - 1, n - 1] = 0

    iteration_matrix0 = .5 * a_h - 1 * sp.eye(n, n)
    iteration_matrix2 = -.5 * a_h + 1 * sp.eye(n, n)

    rhs = 2 * u1 + iteration_matrix0.dot(u0)

    u2 = lin.spsolve(iteration_matrix2, rhs)
    return u2
