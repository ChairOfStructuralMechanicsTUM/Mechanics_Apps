'''###############################
IMPORTS
###############################'''
# general imports
from sympy                      import Symbol, integrate, Eq
import math
from numpy                      import array, append

# import local files
from Libs.geometriccalc         import knot_dist
from Libs                       import geometriccalc as gc

# from Bending_Beam_modified.Classes.ElementSupportEnum import ElSupEnum
import re
from Classes.ElementSupportEnum import ElSupEnum


class ElementCalculation:
    def __init__(self, el_id, start_knot, end_knot, len_symb, lineloads, temp_props, ei=Symbol('EI'), ea=Symbol('EA'),
                 h=Symbol('h'), k_spring=0):
        """
        :param el_id: id of the current beam element
        :param start_knot: start knot of element --> contains coordinates, type, angle und point loads
        :param end_knot: end knot of element --> contains coordinates, type, angle und point loads
        :param len_symb: returns the length of the beam, e.g. 2 * l
        :param lineloads: [lineload_normal_direction, line_transversal_direction]
        :param temp_props: [constant temperature T, temperature coefficient aT, temperatur gradient dt]
        :param ei: returns EI
        :param ea: returns EA
        :param h:  return h
        """
        self.id_el_ = el_id
        self.h_ = h
        self.ea_ = ea
        self.ei_ = ei
        self.k_spring_ = k_spring
        self.length_ = len_symb
        self.start_knot = start_knot
        self.end_knot = end_knot
        self.lineloads = lineloads
        self.temp_props = temp_props
        self.start_calculation()

    def __str__(self):
        out_str = "id: {}\t x1: {}\t y1: {}\t x2: {}\t y2: {}\t beta: {}\n".format(self.id_el_, self.x1_, self.y1_, self.x2_, self.y2_, self.beta1_)
        out_str += "\t\tl: {}\t h: {}\t EI: {}\t EA: {}\t n: {}\t q: {}\n".format(self.length_, self.h_, self.ei_, self.ea_, self.n_, self.q_)
        out_str += "\t\tk: {}\t start temp: {}\t grad temp: {}\t temp coeff: {}".format(self.k_spring_, self.temp_props.start_temp, self.temp_props.grad_temp, self.temp_props.temp_coeff)
        return out_str

    def __repr__(self):
        return self.__str__()


    @property
    def x1_(self):
        return self.start_knot.x_

    @property
    def y1_(self):
        return self.start_knot.y_

    @property
    def type1_(self):
        return self.start_knot.type

    @property
    def k1_(self):
        return self.start_knot.k

    @property
    def x2_(self):
        return self.end_knot.x_

    @property
    def y2_(self):
        return self.end_knot.y_

    @property
    def type2_(self):
        return self.end_knot.type

    @property
    def k2_(self):
        return self.end_knot.k

    @property
    def dx_(self):
        return self.x2_ - self.x1_

    @property
    def dy_(self):
        return self.y2_ - self.y1_

    @property
    def length_nr_(self):
        return knot_dist(self.start_knot, self.end_knot)

    """line load in normal direction (+ = -->)"""
    @property
    def n_(self):
        return self.lineloads[0]

    """ line load in transverse direction (+ = down)"""
    @property
    def q_(self):
        return self.lineloads[1]

    """ Constant temperature for elongation"""
    @property
    def temp_(self):
        return self.temp_props.start_temp

    """ Temperature gradient for bending"""
    @property
    def temp_diff_(self):
        return self.temp_props.grad_temp

    """ Coefficient for temperature"""
    @property
    def temp_coeff_(self):
        return self.temp_props.temp_coeff

    """ Ids of elements that are connected to this element at the start knot"""
    @property
    def ids_start(self):
        """
        :return: returns ids of the connecting elements at the start of the element
        """
        return [el for el in self.start_knot.coupled_el if el != self.id_el_]

    @property
    def beta1_(self):
        """
        :return: angle of the element to the x-line
        """
        return gc.get_angle(self.start_knot, self.end_knot)

    @property
    def ids_end(self):
        """
        :return: returns ids of the connecting elements at the end of the element
        """
        return [el for el in self.end_knot.coupled_el if el != self.id_el_]

    def set_lineload(self, loads):
        """
        Adds load to the existing lineload list
        :param loads: list of new elements to add: [neq_q, new_n]
        """
        for i in range(0, len(self.lineloads)):
            self.lineloads[i] = loads[i]

    """ Combines all temperature properties in temp_props"""
    def set_temp_props(self, temp_load):
        self.temp_props.start_temp = temp_load.start_temp
        self.temp_props.grad_temp = temp_load.grad_temp
        self.temp_props.temp_coeff = temp_load.temp_coeff

    """ Swaps start and end knot if needed"""
    def check_and_swap_ele(self, check_val):
        if check_val in self.start_knot.coupled_el:
            return
        else:
            # cache = self.start_knot
            # self.start_knot = self.end_knot
            # self.end_knot = cache
            self.start_knot, self.end_knot = self.end_knot, self.start_knot
            return

    """ Swaps start and end knot if needed"""
    def set_start_end_knot_correctly(self):
        all_coupled_el = self.start_knot.coupled_el[:] + self.end_knot.coupled_el[:]
        # all_coupled_el = [x for x in all_coupled_el if x != self.id_el_]
        if len(all_coupled_el) == 2:
            return
        if self.id_el_ == 0:
            if len(all_coupled_el) == 3:
                if len(self.start_knot.coupled_el) > 1:
                    start_coupled_el = [x for x in all_coupled_el if x != self.id_el_]
                    self.check_and_swap_ele(start_coupled_el[0])
                    return
            else:
                smallest_num = min(all_coupled_el)
                self.check_and_swap_ele(smallest_num)
                return
        else:
            smallest_num = min(all_coupled_el)
            self.check_and_swap_ele(smallest_num)
            return

    def start_calculation(self):
        """
        :return: Transforming the forces from global coordinate system to the local coordinate system of the support
        """
        self.external_forces_in_local_coordinates_1_ = self.globalforcestolocal(self.start_knot.pointLoad_, self.start_knot.angle)
        self.external_forces_in_local_coordinates_2_ = self.globalforcestolocal(self.end_knot.pointLoad_, self.end_knot.angle)

        self.N1_glob, self.Q1_glob, self.u1_glob, self.w1_glob, self.N1_beta, self.Q1_beta, self.u1_beta, self.w1_beta \
            = self.globalstartforcestolocal()
        self.N2_glob, self.Q2_glob, self.u2_glob, self.w2_glob, self.N2_beta, self.Q2_beta, self.u2_beta, self.w2_beta \
            = self.globalendforcestolocal()

    def globalforcestolocal(self, knotforcesglobal, betalocal):
        """
        :param knotforcesglobal: knot forces of support in global coordinate system
        :param betalocal: angle of the support
        :return: knot point forces in local coordinate system of the support
        """
        forcessupport = [0, 0, 0]
        forcessupport[0] = knotforcesglobal[0] * round(math.cos(math.radians(betalocal)), 2) - knotforcesglobal[1] * round(math.sin(math.radians(betalocal)), 2)
        forcessupport[1] = knotforcesglobal[0] * round(math.sin(math.radians(betalocal)), 2) + knotforcesglobal[1] * round(math.cos(math.radians(betalocal)), 2)
        forcessupport[2] = knotforcesglobal[2]
        return forcessupport

    def globalstartforcestolocal(self):
        """
        :return: returns the start forces in the local coordinate system of the support
        """
        """ The forces of the local coordinate system of the beam are transformed into the global coordinate system"""
        ang = self.beta1_
        N1_glob = Symbol('N_0' + str(self.id_el_)) * round(math.cos(ang), 2) + Symbol('Q_0' + str(self.id_el_)) * round(math.sin(ang), 2)
        Q1_glob = -Symbol('N_0' + str(self.id_el_)) * round(math.sin(ang), 2) + Symbol('Q_0' + str(self.id_el_)) * round(math.cos(ang), 2)
        u1_glob = Symbol('u_0' + str(self.id_el_)) * round(math.cos(ang), 2) + Symbol('w_0' + str(self.id_el_)) * round(math.sin(ang), 2)
        w1_glob = -Symbol('u_0' + str(self.id_el_)) * round(math.sin(ang), 2) + Symbol('w_0' + str(self.id_el_)) * round(math.cos(ang), 2)

        """ The global forces are transformed to the forces in the coordinate system of the support"""
        angle = self.start_knot.angle
        N1_beta = N1_glob * round(math.cos(math.radians(angle)), 2) - Q1_glob * round(math.sin(math.radians(angle)), 2)
        Q1_beta = N1_glob * round(math.sin(math.radians(angle)), 2) + Q1_glob * round(math.cos(math.radians(angle)), 2)
        u1_beta = u1_glob * round(math.cos(math.radians(angle)), 2) - w1_glob * round(math.sin(math.radians(angle)), 2)
        w1_beta = u1_glob * round(math.sin(math.radians(angle)), 2) + w1_glob * round(math.cos(math.radians(angle)), 2)

        return N1_glob, Q1_glob, u1_glob, w1_glob, N1_beta, Q1_beta, u1_beta, w1_beta

    def globalendforcestolocal(self):
        """
        :return: returns the end forces in the local coordinate system of the support
        """
        """ The forces of the local coordinate system of the beam are tranformed to the global coordinate system"""
        ang = self.beta1_
        N2_glob = Symbol('N_1' + str(self.id_el_)) * round(math.cos(ang), 2) + Symbol('Q_1' + str(self.id_el_)) * round(math.sin(ang), 2)
        Q2_glob = -Symbol('N_1' + str(self.id_el_)) * round(math.sin(ang), 2) + Symbol('Q_1' + str(self.id_el_)) * round(math.cos(ang), 2)
        u2_glob = Symbol('u_1' + str(self.id_el_)) * round(math.cos(ang), 2) + Symbol('w_1' + str(self.id_el_)) * round(math.sin(ang), 2)
        w2_glob = -Symbol('u_1' + str(self.id_el_)) * round(math.sin(ang), 2) + Symbol('w_1' + str(self.id_el_)) * round(math.cos(ang), 2)

        """ The global forces are transformed to the forces in the coordinate system of the support"""
        angle = self.end_knot.angle
        N2_beta = N2_glob * round(math.cos(math.radians(angle)), 2) - Q2_glob * round(math.sin(math.radians(angle)), 2)
        Q2_beta = N2_glob * round(math.sin(math.radians(angle)), 2) + Q2_glob * round(math.cos(math.radians(angle)), 2)
        u2_beta = u2_glob * round(math.cos(math.radians(angle)), 2) - w2_glob * round(math.sin(math.radians(angle)), 2)
        w2_beta = u2_glob * round(math.sin(math.radians(angle)), 2) + w2_glob * round(math.cos(math.radians(angle)), 2)

        return N2_glob, Q2_glob, u2_glob, w2_glob, N2_beta, Q2_beta, u2_beta, w2_beta

    def compute_eqns_int(self):
        """
        :return: sets the equations(N, u, Q, M, phi, w)  for each element(beam, rod) seperately,
        dependencies between start and end of element (local balance at element)
        """
        x = Symbol('x')

        if self.k_spring_ != 0:
            """
            In this case, the element is not a beam or rod, but a spring.
            The spring between element is set up as a line element. The advantage of this method is the automatic
            adjustment of the forces to the local coordinate system of the support (no further transformation needed)
            """
            glN = Eq(Symbol('N_0' + str(self.id_el_)) + self.k_spring_ * (Symbol('u_0' + str(self.id_el_)) - Symbol('u_1' + str(self.id_el_))), 0)
            glu = Eq(Symbol('Q_1' + str(self.id_el_)), 0)
            glQ = Eq(Symbol('Q_0' + str(self.id_el_)), Symbol('Q_1' + str(self.id_el_)))
            glM = Eq(Symbol('M_0' + str(self.id_el_)), Symbol('M_1' + str(self.id_el_)))
            glphi = Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.id_el_)))
            glw = Eq(Symbol('w_1' + str(self.id_el_)), Symbol('w_0' + str(self.id_el_)))

        else:
            """ setting up the equilibrium at the beam or rod element"""
            glN = Eq(Symbol('N_1' + str(self.id_el_)), Symbol('N_0' + str(self.id_el_)) - integrate(self.n_, (x, 0, self.length_)))


            if self.ea_ == float('inf'):
                """ if the beam is rigid(EA --> ∞)"""
                glu = Eq(Symbol('u_1' + str(self.id_el_)), Symbol('u_0' + str(self.id_el_)))
            else:
                glu = Eq(Symbol('u_1' + str(self.id_el_)) + integrate(integrate((self.n_/self.ea_), x), (x, 0, self.length_))
                         - Symbol('N_0' + str(self.id_el_)) *self.length_/self.ea_ - self.temp_coeff_ * self.temp_ * self.length_ - Symbol('u_0' + str(self.id_el_)), 0)

            glQ = Eq(Symbol('Q_1' + str(self.id_el_)), Symbol('Q_0' + str(self.id_el_)) - integrate(self.q_, (x, 0, self.length_)))
            glM = Eq(Symbol('M_1' + str(self.id_el_)), 0 - integrate(integrate(self.q_, x), (x, 0, self.length_)) + Symbol('Q_0' + str(self.id_el_)) \
                  * self.length_ +Symbol('M_0' + str(self.id_el_)))

            if self.ei_ == float('inf'):
                """ if the beam is rigid(EI --> ∞)"""
                glphi = Eq(Symbol('phi_1' + str(self.id_el_)) - Symbol('phi_0' + str(self.id_el_)), 0)
                glw = Eq(Symbol('w_1' + str(self.id_el_)), Symbol('phi_0' + str(self.id_el_)) * self.length_\
                      + Symbol('w_0' + str(self.id_el_)))
            else:
                glphi = Eq(self.ei_ * Symbol('phi_1' + str(self.id_el_)), integrate(integrate(integrate((self.q_), x), x),
                    (x, 0, self.length_)) - (Symbol('Q_0' + str(self.id_el_)) * self.length_ ** 2 / 2) - Symbol('M_0' + str(self.id_el_))*\
                    self.length_ - (self.temp_coeff_ * self.temp_diff_ / self.h_) * self.length_ + self.ei_ *\
                    Symbol('phi_0' + str(self.id_el_)))
                glw = Eq(self.ei_ * Symbol('w_1' + str(self.id_el_)),
                            integrate(integrate(integrate(integrate((self.q_), x), x), x), (x, 0, self.length_)) \
                            - Symbol('Q_0' + str(self.id_el_)) * self.length_ ** 3 / 6 - Symbol('M_0' + str(self.id_el_)) *\
                            self.length_ ** 2 / 2+ self.ei_ * Symbol('phi_0' + str(self.id_el_)) * self.length_ -\
                            (self.temp_coeff_ * self.temp_diff_ / self.h_) * self.length_ ** 2 / 2 + self.ei_ * Symbol('w_0' + str(self.id_el_)))

        return glN, glu, glQ, glM, glphi, glw

    def set_eqnsstart(self, type1, el):
        """
        :param type1: type of support or joint
        :param el: list of all elements
        :return: returns a set of equations for the boundary conditions at the start knot
        """
        condition = array([])
        forces = self.external_forces_in_local_coordinates_1_
        k = self.k1_
        if type1 == ElSupEnum.SUPPORT_CLAMPED.value:
            condition = append(condition, Eq(Symbol('u_0' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('w_0' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_FIXED_END.value:
            condition = append(condition, Eq(Symbol('u_0' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              0 - forces[2] - k[2] * Symbol('phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('w_0' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_END.value:
            condition = append(condition, Eq(self.N1_beta, 0 - forces[0] + k[0] * self.u1_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              0 - forces[2] - k[2] * Symbol('phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(self.w1_beta, 0))
        elif type1 == ElSupEnum.FREE_END.value:
            condition = append(condition, Eq(self.N1_beta, 0 - forces[0] + k[0] * self.u1_beta))
            condition = append(condition, Eq(self.Q1_beta, 0 - forces[1] + k[1] * self.w1_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              0 - forces[2] - k[2] * Symbol('phi_0' + str(self.id_el_))))
        elif type1 == ElSupEnum.SUPPORT_FIXED_JOINT.value:
            condition = append(condition, Eq(Symbol('u_0' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)), 0 - k[2] * (
                        Symbol('phi_0' + str(self.id_el_)) - Symbol('phi_1' + str(self.ids_start[0])))))
            condition = append(condition, Eq(Symbol('w_0' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value:
            condition = append(condition, Eq(Symbol('u_0' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_start, 'M_1', el) - forces[2] - k[2] * Symbol(
                                  'phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.ids_start[0]))))
            condition = append(condition, Eq(Symbol('w_0' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_JOINT.value:
            condition = append(condition, Eq(self.N1_beta, self.adding_functions_of_elements(1, 'N', el, self.ids_start) - forces[0] + k[0] * self.u1_beta))
            condition = append(condition, Eq(self.u1_beta, el[self.ids_start[0]].u2_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)), 0 - k[2] * (
                        Symbol('phi_0' + str(self.id_el_)) - Symbol('phi_1' + str(self.ids_start[0])))))
            condition = append(condition, Eq(self.w1_beta, 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value:
            condition = append(condition, Eq(self.N1_beta,
                              self.adding_functions_of_elements(1, 'N', el, self.ids_start) - forces[0] + k[
                                  0] * self.u1_beta))
            condition = append(condition, Eq(self.u1_beta, el[self.ids_start[0]].u2_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_start, 'M_1', el) - forces[2] - k[2] * Symbol(
                                  'phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.ids_start[0]))))
            condition = append(condition, Eq(self.w1_beta, 0))
        elif type1 == ElSupEnum.THROUGH_ELEMENT.value:
            condition = append(condition, Eq(self.N1_beta,
                              self.adding_functions_of_elements(1, 'N', el, self.ids_start) - forces[0] + k[
                                  0] * self.u1_beta))
            condition = append(condition, Eq(self.u1_beta, el[self.ids_start[0]].u2_beta))
            condition = append(condition, Eq(self.Q1_beta,
                              self.adding_functions_of_elements(1, 'Q', el, self.ids_start) - forces[1] + k[
                                  1] * self.w1_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_start, 'M_1', el) - forces[2] - k[2] * Symbol(
                                  'phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.ids_start[0]))))
            condition = append(condition, Eq(self.w1_beta, el[self.ids_start[0]].w2_beta))

        elif type1 == ElSupEnum.JOINT.value:
            condition = append(condition, Eq(self.N1_beta,
                              self.adding_functions_of_elements(1, 'N', el, self.ids_start) - forces[0] + k[
                                  0] * self.u1_beta))
            condition = append(condition, Eq(self.u1_beta, el[self.ids_start[0]].u2_beta))
            condition = append(condition, Eq(self.Q1_beta,
                              self.adding_functions_of_elements(1, 'Q', el, self.ids_start) - forces[1] + k[
                                  1] * self.w1_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              0 - k[2] * (Symbol('phi_0' + str(self.id_el_)) - Symbol(
                                  'phi_1' + str(self.ids_start[0])))))
            condition = append(condition, Eq(self.w1_beta, el[self.ids_start[0]].w2_beta))
        elif type1 == ElSupEnum.JOINT_TRANSVERSE_FORCE.value:
            condition = append(condition, Eq(self.N1_beta,
                              self.adding_functions_of_elements(1, 'N', el, self.ids_start) - forces[0] + k[
                                  0] * self.u1_beta))
            condition = append(condition, Eq(self.u1_beta, el[self.ids_start[0]].u2_beta))
            condition = append(condition, Eq(self.Q1_beta,
                              0 + k[1] * (self.w1_beta - el[self.ids_start[0]].w2_beta)))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_start, 'M_1', el) - forces[2] - k[2] * Symbol(
                                  'phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.ids_start[0]))))
        elif type1 == ElSupEnum.JOINT_NORMAL_FORCE.value:
            condition = append(condition, Eq(self.N1_beta, 0 + k[0] * (self.u1_beta - el[self.ids_start[0]].u2_beta)))
            condition = append(condition, Eq(self.Q1_beta,
                              self.adding_functions_of_elements(1, 'Q', el, self.ids_start) - forces[1] + k[
                                  1] * self.w1_beta))
            condition = append(condition, Eq(Symbol('M_0' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_start, 'M_1', el) - forces[2] - k[2] * Symbol(
                                  'phi_0' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), Symbol('phi_1' + str(self.ids_start[0]))))
            condition = append(condition, Eq(self.w1_beta, el[self.ids_start[0]].w2_beta))
        elif type1 == ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value:
            condition = append(condition, Eq(self.u1_beta, 0))
            condition = append(condition, Eq(self.Q1_beta, 0 + k[1] * self.w1_beta - forces[1]))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_NORMAL_FORCE.value:
            condition = append(condition, Eq(self.w1_beta, 0))
            condition = append(condition, Eq(self.N1_beta, 0 + k[0] * self.u1_beta - forces[1]))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), 0))
        return condition

    def set_eqnsend(self, type1, el):
        """
        :param type1: type of support or joint
        :param el: list of all elements
        :return: returns conditions at the end of the element
        """
        condition = array([])
        k = self.k2_
        forces = self.external_forces_in_local_coordinates_2_

        if type1 == ElSupEnum.SUPPORT_CLAMPED.value:
            condition = append(condition, Eq(Symbol('u_1' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('w_1' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_FIXED_END.value:
            condition = append(condition, Eq(Symbol('u_1' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + forces[2] + k[2] * Symbol('phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('w_1' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_END.value:
            condition = append(condition, Eq(self.N2_beta, 0 + forces[0] - k[0] * self.u2_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + forces[2] + k[2] * Symbol('phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(self.w2_beta, 0))
        elif type1 == ElSupEnum.FREE_END.value:
            condition = append(condition, Eq(self.N2_beta, 0 + forces[0] - k[0] * self.u2_beta))
            condition = append(condition, Eq(self.Q2_beta, 0 + forces[1] - k[1] * self.w2_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + forces[2] + k[2] * Symbol('phi_1' + str(self.id_el_))))
        elif type1 == ElSupEnum.SUPPORT_FIXED_JOINT.value:
            condition = append(condition, Eq(Symbol('u_1' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + k[2] * (Symbol('phi_1' + str(self.id_el_)) - Symbol('phi_0' + str(self.ids_end[0])))))
            condition = append(condition, Eq(Symbol('w_1' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_FIXED_CONTINUOUS.value:
            condition = append(condition, Eq(Symbol('u_1' + str(self.id_el_)), 0))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_end, 'M_0', el) + forces[2] + k[2] * Symbol(
                                  'phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), Symbol('phi_0' + str(self.ids_end[0]))))
            condition = append(condition, Eq(Symbol('w_1' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_JOINT.value:
            condition = append(condition, Eq(self.N2_beta, self.adding_functions_of_elements(0, 'N', el, self.ids_end) + forces[0] - k[
                0] * self.u2_beta))
            condition = append(condition, Eq(self.u2_beta, el[self.ids_end[0]].u1_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + k[2] * (Symbol('phi_1' + str(self.id_el_)) - Symbol('phi_0' + str(self.ids_end[0])))))
            condition = append(condition, Eq(self.w2_beta, 0))
        elif type1 == ElSupEnum.SUPPORT_ROLLER_CONTINUOUS.value:
            condition = append(condition, Eq(self.N2_beta, self.adding_functions_of_elements(0, 'N', el, self.ids_end) + forces[0] - k[
                0] * self.u2_beta))
            condition = append(condition, Eq(self.u2_beta, el[self.ids_end[0]].u1_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_end, 'M_0', el) + forces[2] + k[2] * Symbol(
                                  'phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), Symbol('phi_0' + str(self.ids_end[0]))))
            condition = append(condition, Eq(self.w2_beta, 0))
        elif type1 == ElSupEnum.THROUGH_ELEMENT.value:
            condition = append(condition, Eq(self.N2_beta, self.adding_functions_of_elements(0, 'N', el, self.ids_end) + forces[0]
                              - k[0] * self.u2_beta))
            condition = append(condition, Eq(self.u2_beta, el[self.ids_end[0]].u1_beta))
            condition = append(condition, Eq(self.Q2_beta, self.adding_functions_of_elements(0, 'Q', el, self.ids_end) + forces[1] - k[
                1] * self.w2_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_end, 'M_0', el) + forces[2] + k[2] * Symbol(
                                  'phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), Symbol('phi_0' + str(self.ids_end[0]))))
            condition = append(condition, Eq(self.w2_beta, el[self.ids_end[0]].w1_beta))
        elif type1 == ElSupEnum.JOINT.value:
            condition = append(condition, Eq(self.N2_beta, self.adding_functions_of_elements(0, 'N', el, self.ids_end) + forces[0] - k[
                0] * self.u2_beta))
            condition = append(condition, Eq(self.u2_beta, el[self.ids_end[0]].u1_beta))
            condition = append(condition, Eq(self.Q2_beta, self.adding_functions_of_elements(0, 'Q', el, self.ids_end) + forces[1] - k[
                1] * self.w2_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              0 + k[2] * (Symbol('phi_1' + str(self.id_el_)) - Symbol('phi_0' + str(self.ids_end[0])))))
            condition = append(condition, Eq(self.w2_beta, el[self.ids_end[0]].w1_beta))
        elif type1 == ElSupEnum.JOINT_TRANSVERSE_FORCE.value:
            condition = append(condition, Eq(self.N2_beta, self.adding_functions_of_elements(0, 'N', el, self.ids_end) + forces[0] - k[
                0] * self.u2_beta))
            condition = append(condition, Eq(self.u2_beta, el[self.ids_end[0]].u1_beta))
            condition = append(condition, Eq(self.Q2_beta, 0 - k[1] * (self.w2_beta - el[self.ids_end[0]].w1_beta)))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_end, 'M_0', el) + forces[2] + k[2] * Symbol(
                                  'phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), Symbol('phi_0' + str(self.ids_end[0]))))
        elif type1 == ElSupEnum.JOINT_NORMAL_FORCE.value:
            condition = append(condition, Eq(self.N2_beta, 0 - k[0] * (self.u2_beta - el[self.ids_end[0]].u1_beta)))
            condition = append(condition, Eq(self.Q2_beta, self.adding_functions_of_elements(0, 'Q', el, self.ids_end) + forces[1] - k[
                1] * self.w2_beta))
            condition = append(condition, Eq(Symbol('M_1' + str(self.id_el_)),
                              self.adding_multiple_elements(self.ids_end, 'M_0', el) + forces[2] + k[2] * Symbol(
                                  'phi_1' + str(self.id_el_))))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), Symbol('phi_0' + str(self.ids_end[0]))))
            condition = append(condition, Eq(self.w2_beta, el[self.ids_end[0]].w1_beta))
        elif type1 == ElSupEnum.SUPPORT_TRANSVERSE_FORCE.value:
            condition = append(condition, Eq(self.u2_beta, 0))
            condition = append(condition, Eq(self.Q2_beta, 0 - k[1] * self.w2_beta + forces[1]))
            condition = append(condition, Eq(Symbol('phi_1' + str(self.id_el_)), 0))
        elif type1 == ElSupEnum.SUPPORT_NORMAL_FORCE.value:
            condition = append(condition, Eq(self.w2_beta, 0))
            condition = append(condition, Eq(self.N2_beta, 0 - k[0] * self.u1_beta + forces[1]))
            condition = append(condition, Eq(Symbol('phi_0' + str(self.id_el_)), 0))
        return condition

    def adding_multiple_elements(self, ids = [], symbol_funtion = '', el = []):
        """
        :param ids of start or end
        :param symbol_funtion: What should be returned --> string ('phi','M')
        :param el: list of all elements
        :return: returns sum of forces OR displacements
        """
        s = 0
        for i in range(0, len(ids)):
            if '0' in symbol_funtion:
                if self.end_knot.id == el[ids[i]].end_knot.id:
                    temp = symbol_funtion
                    symbol_function_new = temp.replace('0', '1')
                    if i == 0:
                        s = - Symbol(symbol_function_new + str(ids[0]))
                    else:
                        s = s - Symbol(symbol_function_new + str(ids[i]))
                else:
                    if i == 0:
                        s = Symbol(symbol_funtion + str(ids[0]))
                    else:
                        s = s + Symbol(symbol_funtion + str(ids[i]))
            else:
                if self.start_knot.id == el[ids[i]].start_knot.id:
                    temp = symbol_funtion
                    symbol_function_new = temp.replace('1', '0')
                    if i == 0:
                        s = - Symbol(symbol_function_new + str(ids[0]))
                    else:
                        s = s - Symbol(symbol_function_new + str(ids[i]))
                else:
                    if i == 0:
                        s = Symbol(symbol_funtion + str(ids[0]))
                    else:
                        s = s + Symbol(symbol_funtion + str(ids[i]))
        return s

    def adding_functions_of_elements(self, position, func = '', el = [], ids = []):
        """
        This function is needed for calculating if multiple elements are connected with only one element (Verzweigung)
        :param position: start == 0 and end ==1
        :param func: What should be returned --> N or Q
        :param el: list of all elements
        :param ids: start or end ids
        :return: The sum of N or Q of all boardering elements
        """
        result = 0
        if position == 0:
            if func == 'N':
                for i in range(0, len(ids)):
                    if self.end_knot.id == el[ids[i]].end_knot.id:
                        if i == 0:
                            result = - el[ids[0]].N2_beta
                        else:
                            result = result - el[ids[i]].N2_beta
                    else:
                        if i == 0:
                            result = el[ids[0]].N1_beta
                        else:
                            result = result + el[ids[i]].N1_beta
            if func == 'Q':
                for i in range(0, len(ids)):
                    if self.end_knot.id == el[ids[i]].end_knot.id:
                        if i == 0:
                            result = - el[ids[0]].Q2_beta
                        else:
                            result = result - el[ids[i]].Q2_beta
                    else:
                        if i == 0:
                            result = el[ids[0]].Q1_beta
                        else:
                            result = result + el[ids[i]].Q1_beta
            if func == 'w':
                result2 = []
                for i in range(0, len(ids)):
                    if self.end_knot.id == el[ids[i]].end_knot.id:
                        result2 = append(result2, el[ids[i]].w1_beta)

                    else:
                        result2.append(el[ids[i]].w2_beta)
                result = result2
            if func == 'u':
                result2 = []
                for i in range(0, len(ids)):
                    if self.end_knot.id == el[ids[i]].end_knot.id:
                        result2 = append(result2, el[ids[i]].u1_beta)

                    else:
                        result2.append(el[ids[i]].u2_beta)
                result = result2
            if func == 'phi':
                result2 = []
                for i in range(0, len(ids)):
                    if self.end_knot.id == el[ids[i]].end_knot.id:
                        result2 = append(Symbol('phi_0' + str(ids[i])))

                    else:
                        result2.append(Symbol('phi_1' + str(ids[i])))
                result = result2
        elif position == 1:
            if func == 'N':
                for i in range(0, len(ids)):
                    if self.start_knot.id == el[ids[i]].start_knot.id:
                        if i == 0:
                            result = - el[ids[0]].N1_beta
                        else:
                            result = result - el[ids[i]].N1_beta
                    else:
                        if i == 0:
                            result = el[ids[0]].N2_beta
                        else:
                            result = result + el[ids[i]].N2_beta
            if func == 'Q':
                for i in range(0, len(ids)):
                    if self.start_knot.id == el[ids[i]].start_knot.id:
                        if i == 0:
                            result = - el[ids[0]].Q1_beta
                        else:
                            result = result - el[ids[i]].Q1_beta
                    else:
                        if i == 0:
                            result = el[ids[0]].Q2_beta
                        else:
                            result = result + el[ids[i]].Q2_beta
            if func == 'w':
                result2 = []
                for i in range(0, len(ids)):
                    if self.start_knot.id == el[ids[i]].start_knot.id:
                        result2 = append(result2, el[ids[i]].w2_beta)

                    else:
                        result2 = append(result2, el[ids[i]].w1_beta)
                result = result2
            if func == 'u':
                result2 = []
                for i in range(0, len(ids)):
                    if self.start_knot.id == el[ids[i]].start_knot.id:
                        result2 = append(result2, el[ids[i]].u2_beta)

                    else:
                        result2 = append(result2, el[ids[i]].u1_beta)
                result = result2
            if func == 'phi':
                result2 = []
                for i in range(0, len(ids)):
                    if self.start_knot.id == el[ids[i]].start_knot.id:
                        result2 = append(Symbol('phi_1' + str(ids[i])))

                    else:
                        result2.append(Symbol('phi_0' + str(ids[i])))
                result = result2
        else:
            result = 0
        return result

