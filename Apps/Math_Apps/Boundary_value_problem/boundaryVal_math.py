import numpy as np


def shoot_ode(_, x):
    """
    ode describing the trajectory of a projectile
    :param _: dummy variable, time
    :param x: vector with 4 components (x_position, y_position, x_velocity, y_velocity)
    :return: vector with 4 components (x_velocity, y_velocity, x_acceleration, y_acceleration)
    """
    dx = np.empty(4)

    g = -9.81

    vx = x[2]
    vy = x[3]

    drx = vx
    dry = vy
    dvx = 0
    dvy = g

    dx[:] = [drx, dry, dvx, dvy]

    return dx


def shoot_with_alpha(alpha):
    """
    performs the calculations for shooting an object with a given angle alpha.
    The initial velocity, stopping criteria, step width... are hard coded!
    :param alpha: shooting angle
    :return: two np.arrays: time series with the steps, shooting data for each timestep [rx,ry,vx,vy]
    """
    h = .001
    v0 = 10

    # initial conditions
    rx0 = 0.0
    ry0 = 0.0
    vx0 = v0 * np.cos(alpha * 2 * np.pi / 360.0)
    vy0 = v0 * np.sin(alpha * 2 * np.pi / 360.0)
    x = np.array([rx0, ry0, vx0, vy0])
    x.shape = (4, 1)
    t = np.array([0])

    while x[1, -1] > 0 or x[3, -1] > 0:  # projectile has not hit ground with negative vy
        [t, x] = expl_euler_step(shoot_ode, t, x, h)

    return t, x


def expl_euler_step(f, t, x, h):
    """
    performs one euler step.
    :param f: ode
    :param t: array with former timesteps
    :param x: array with former states
    :param h: stepwidth
    :return: updated arrays t,x with new timestep appended at the end
    """
    xnew = x[:, -1] + h * f(t[-1], x[:, -1])
    xnew = np.reshape(xnew, [4, 1])
    tnew = np.array([t[-1] + h])
    x = np.concatenate((x, xnew), 1)
    t = np.concatenate((t, tnew), 0)
    return t, x


def shoot_error(x_target, x):
    """
    calculates the error of a shoot on the target at x_target.
    :param x_target: position of the target
    :param x: state array holding the complete history of the shoot
    :return: error. A positive sign of the error indicates that the shoot has been to far, a negative sign that it has
    been to short.
    """
    # ==============================================================================
    #
    # ==============================================================================
    x_hit = x[0, -1]  # access last element from the state array and get x position
    error = x_hit - x_target
    return error


def plot_trajectory(fig, x):
    """
    plots the trajectory of a shoot.
    :param fig: bokeh.plotting.Figure the image is plotted in
    :param x: array holding the whole history of the shoot [rx,ry,vx,vy]
    """
    fig.line(x[0, :], x[1, :])  # only plot positions from the state array, no velocities
