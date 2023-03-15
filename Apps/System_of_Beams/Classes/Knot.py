import math

class Knot:
    def __init__(self, kn_id, x, y, kn_type, angleSupport, k=[0, 0, 0], pointload=[0, 0, 0]):
        self.id = kn_id
        self.x_ = x
        self.y_ = y
        self.pointLoad_ = pointload
        self.type = kn_type
        self.angle = math.degrees(angleSupport) # in degree
        self.coupled_el = []                    # connected elements, stores IDs
        self.k = k                              # spring stiffness

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        # TODO What is k, do I need to add this to the plot
        out_str = ""
        out_str += "id: " + str(self.id)
        out_str += "\ttype: " + str(self.type)
        out_str += "\n\tx: " + str(self.x_)
        out_str += "\ty: " + str(self.y_)
        out_str += "\tangle: " + str(self.angle)
        out_str += "\n\tpointload: " + str(self.pointLoad_)
        if self.is_spring():
            out_str += "\n\tSpring stiffness: "
            out_str += "k_x: {}\t k_y: {}\t mom: {}".format(self.k[0], self.k[1], self.k[2])
        if self.coupled_el:
            out_str += "\n\tconnected elements: "
            for el in self.coupled_el:
                out_str += "\t" + str(el) + ","
        return out_str

    def set_pointload(self, f_hori, f_verti, moment):
        self.pointLoad_ = [f_hori, f_verti, moment]

    def reset_pointload(self):
        self.pointLoad_ = [0, 0, 0]

    def add_pointload(self, n, q, mom):
        self.pointLoad_ = [self.pointLoad_[0] + n, self.pointLoad_[1] + q, self.pointLoad_[2] + mom]

    def set_spring_stiffness(self, k_x, k_y, k_mom):
        self.k = [k_x, k_y, k_mom]

    def add_spring_stiffness(self, k_x, k_y, k_mom):
        self.k = [self.k[0] + k_x, self.k[1] + k_y, self.k[2] + k_mom]

    def is_spring(self):
        for el in self.k:
            if el != 0:
                return True
        return False

    def has_pointload(self):
        for el in self.pointLoad_:
            if el != 0:
                return True
        return False

    def add_coupled_el(self, el_to_add):
        """
        Adds a connected element to the list of connected elements
        :param el_to_add: id of the element being coupled. Can be one int or list of ints
        """
        if isinstance(el_to_add, list):
            self.coupled_el.extend(el_to_add)
        else:
            self.coupled_el.append(el_to_add)

    def delete_coupled_el(self, el_to_del):
        """
        Deletes coupled element from list of coupled elements
        :param el_to_del: id of the element that needs to be deleted
        """
        try:
            self.coupled_el.remove(el_to_del)
        except ValueError:
            print("element is not in list")


def get_knot_id(knot):
    return knot.id
