from bokeh.models import ColumnDataSource
from math import sqrt, floor
from numpy import sign


class DraggablePath:

    def __init__(self, fig):
        """
        initializes a draggable path in a given figure
        :param fig: provided bokeh plot, where the path is created.
        """
        # Control points
        self.control_point_source = []
        self.control_point_x = []
        self.control_point_y = []
        # Path
        self.path_source = ColumnDataSource(data=dict(x=[], y=[]))
        self.Deriv2X = []
        self.Deriv2Y = []
        # Currently grabbed control point
        self.currentNode = -1
        # Ramp
        X = [1, 3.5, 6.64, 8.7, 6.8, 5.54, 10.0, 11.67, 13.9]
        Y = [13, 3.3, 1.4, 3.8, 5.4, 3.16, 1.4, 4.8, 6.4]
        # set control point data
        self.control_point_source = len(X) * [None]  # initialize list
        # create and save path control points
        for i in range(0, len(X)):
            self.control_point_source[i] = ColumnDataSource(data=dict(x=[], y=[]))
            fig.ellipse(x='x', y='y', width=1, height=1, source=self.control_point_source[i],
                        fill_color="#CCCCC6", line_color=None)
        # create and save path
        fig.line(x='x', y='y', source=self.path_source, line_color="black")

        self.compute_path(X, Y)

    def find2Deriv(self, x, f):
        # solve A x = b  with :
        # b=temp
        temp = [0, (f[2] - f[1]) / (x[2] - x[1]) - (f[1] - f[0]) / (x[1] - x[0])]
        # x=f''
        # A_{ii}=(h_i+h_{i+1})/3
        uDiag = [(x[2] - x[0]) / 3.0]
        # A_{i,i+1}=A_{i+1,i}=h_{i+1}/6
        # solve using LU decomposition in O(n)
        for i in range(1, len(x) - 2):
            # temp [i+2] would equal :
            b = (f[i + 2] - f[i + 1]) / (x[i + 2] - x[i + 1]) - (f[i + 1] - f[i]) / (x[i + 1] - x[i])
            # we solve L y = b in the first loop
            # lNow = upper diag of L (only vals of L to determine)
            lNow = (x[i + 1] - x[i]) / (6.0 * uDiag[i - 1])
            # create/solve for y
            temp.append(b - lNow * temp[i])
            # create A_{i,i}=U_{i,i}
            uDiag.append((x[i + 2] - x[i]) / 3.0 - lNow * (x[i + 1] - x[i]) / 6.0)
        n = len(uDiag)
        # solve U x = y
        temp[n] /= uDiag[n - 1]
        for i in range(n - 1, 0, -1):
            temp[i] = (temp[i] - (x[i + 1] - x[i]) * temp[i + 1] / 6.0) / uDiag[i - 1]
        temp.append(0)
        return temp

    def cubicSpline(self, f):
        x = range(0, len(f))
        # find 2nd deriv of f (solution to cubic spline problem)
        f2 = self.find2Deriv(x, f)
        Y = []
        for i in range(0, len(x) - 1):
            xnow = i
            # create path from 20 points (1 at node 19 between nodes)
            Y.append(f[i])
            for j in range(1, 20):
                xnow += 1.0 / 20.0
                Y.append((f2[i] * (i + 1 - xnow) ** 3 + f2[i + 1] * (xnow - i) ** 3) / 6.0
                         + (f[i + 1] - f[i] + (f2[i] - f2[i + 1]) / 6.0) * (xnow - i) + f[i] - f2[i] / 6.0)
        # add final node to path
        Y.append(f[len(x) - 1])
        return (Y, f2)

    def get_height(self, t):
        """
        only return y
        :param t: parameter
        :return:
        """
        x, y = self.get_point(t)
        return y

    def get_point(self, t):
        """
        return x y
        :param t: parameter
        :return:
        """
        i = int(floor(t))
        # if last point then i-1-th segment
        if i == len(self.Deriv2X) - 1:
            i -= 1

        x = (self.Deriv2X[i] * (i + 1 - t) ** 3 + self.Deriv2X[i + 1] * (t - i) ** 3) / 6.0 + \
            ((self.control_point_x[i + 1] - self.control_point_x[i]) + (self.Deriv2X[i] - self.Deriv2X[i + 1]) / 6.0) * (t - i) + \
            self.control_point_x[i] - self.Deriv2X[i] / 6.0
        y = (self.Deriv2Y[i] * (i + 1 - t) ** 3 + self.Deriv2Y[i + 1] * (t - i) ** 3) / 6.0 + \
            ((self.control_point_y[i + 1] - self.control_point_y[i]) + (self.Deriv2Y[i] - self.Deriv2Y[i + 1]) / 6.0) * (t - i) + \
            self.control_point_y[i] - self.Deriv2Y[i] / 6.0

        return x, y

    def dX(self, t):
        """
        return dx/dt at t
        :return:
        """
        i = int(floor(t))
        # if last point then i-1-th segment
        if (i == len(self.Deriv2X) - 1):
            i -= 1
        return ((self.Deriv2X[i + 1] * (t - i) ** 2 - self.Deriv2X[i] * (i + 1 - t) ** 2) / 2.0
                + self.control_point_x[i + 1] - self.control_point_x[i] + (self.Deriv2X[i] - self.Deriv2X[i + 1]) / 6.0)

    def dY(self, t):
        """
        # return dy/dt at t
        :return:
        """
        i = int(floor(t))
        # if last point then i-1-th segment
        if (i == len(self.Deriv2Y) - 1):
            i -= 1
        return ((self.Deriv2Y[i + 1] * (t - i) ** 2 - self.Deriv2Y[i] * (i + 1 - t) ** 2) / 2.0
                + self.control_point_y[i + 1] - self.control_point_y[i] + (self.Deriv2Y[i] - self.Deriv2Y[i + 1]) / 6.0)

    def get_distance(self, t0, t1):
        """
        get distance between (X(t0),Y(t0)) and (X(t1),Y(t1))
        :param t0: parameter defining start point
        :param t1: parameter defining end point
        :return:
        """
        # L= \int_t0^t1 \sqrt{(dx/dt)^2+(dy/dt)^2} sign(dx/dt) dt
        # we use simpson's rule (O(h^4))
        # \int_x1^x2 f(x) dx = h/6 (f(x1)+4f((x1+x2)/2)+f(x2)
        return abs(t1 - t0) / 6.0 * (
            sqrt(self.dX(t0) ** 2 + self.dY(t0) ** 2) * sign(self.dX(t0))
            + 4 * sign(self.dX((t0 + t1) / 2.0)) * sqrt(self.dX((t0 + t1) / 2.0) ** 2 + self.dY((t0 + t1) / 2.0) ** 2)
            + sqrt(self.dX(t1) ** 2 + self.dY(t1) ** 2) * sign(self.dX(t1)))

    def get_normal(self, t):
        """
        Find normal vector at t
        :param t:
        :return:
        """
        (dx, dy) = self.get_derivative(t);
        return -dy, dx

    def get_derivative(self, t):
        """
        Find derivative of path at t
        :param t: parameter
        :return:
        """
        # find nearest nodes
        i1 = int(floor(t * 20))
        i2 = int(floor(t * 20)) + 1
        # if last point then i-1-th segment
        if (i1 == len(self.path_source.data['x']) - 1):
            i1 -= 2
            i2 -= 2
        # use finite differences to compute derivative
        dx = self.path_source.data['x'][i2] - self.path_source.data['x'][i1]
        if (dx == 0):
            return (0, 1)
        dy = (self.path_source.data['y'][i2] - self.path_source.data['y'][i1]) / dx
        # derivative = (1,dy), to "see" path travelling backwards (i.e. loops)
        # we invert derivative if dx=-1
        dx = sign(dx)
        dy *= dx
        # normalise derivative
        norm = sqrt(dx ** 2 + dy ** 2)
        dx /= norm
        dy /= norm
        return dx, dy

    def is_in_node(self, xPos, yPos):
        """
        find index of node in which coordinates are found (return -1 if not in a node)
        :param yPos:
        :return:
        """
        for i in range(0, len(self.control_point_x)):
            if abs(xPos - self.control_point_x[i]) <= 1 and abs(yPos - self.control_point_y[i]) <= 1: # found
                return i
        return -1 # not found

    def modify_path(self, old, new):
        """
        modify path by dragging nodes
        :param old:
        :param new:
        :return:
        """
        # if there is a previous node (not first time the function is called)
        # and the node has not been released (new['x']=-1 on release to prepare for future calls)
        if len(old) == 1 and new[0][u'x'] != -1:
            # if first call for this node
            if self.currentNode == -1:
                # determine which node and remember it
                XStart = old[0][u'x']
                YStart = old[0][u'y']
                self.currentNode = self.is_in_node(XStart, YStart)
            # if not first call then move node
            if self.currentNode != -1:
                # update node position
                self.control_point_source[self.currentNode].data = dict(x=[new[0][u'x']], y=[new[0][u'y']])
                self.control_point_x[self.currentNode] = new[0][u'x']
                self.control_point_y[self.currentNode] = new[0][u'y']
                self.__update_path_data()

            return self.currentNode
        else:
            # when node is released reset current node to -1
            # so a new node is moved next time
            self.currentNode = -1
            return -1

    def compute_path(self, X, Y):
        """
        provide control points and draw respective path
        :param X: x coordinates of control points
        :param Y: y coordinates of control points
        :return:
        """
        self.__update_control_point_data(X, Y)
        self.__update_path_data()

    def __update_control_point_data(self, X, Y):
        """
        update control point data with respect to given X, Y coordinates
        :param X:
        :param Y:
        :return:
        """
        # save nodes in easily accessible list
        self.control_point_x = X
        self.control_point_y = Y
        # update nodes
        for i in range(0, len(X)):
            self.control_point_source[i].data = dict(x=[X[i]], y=[Y[i]])

    def __update_path_data(self):
        """
        update path data with respect to position of control points
        :return:
        """
        # calculate new path
        (x, self.Deriv2X) = self.cubicSpline(self.control_point_x)
        (y, self.Deriv2Y) = self.cubicSpline(self.control_point_y)
        # update path
        self.path_source.data = dict(x=x, y=y)
