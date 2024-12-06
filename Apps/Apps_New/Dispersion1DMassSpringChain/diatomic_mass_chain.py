from bokeh.models import ColumnDataSource
import numpy as np
from functions import displacement_diatomic_acoustic, displacement_diatomic_optical, \
    superposition_diatomic_acoustic_discrete, superposition_diatomic_acou_analysis, superposition_diatomic_optical_discrete,\
    superposition_diatomic_opti_analysis


class Diatomic_chain(object):
    def __init__(self, N, a, mass_relation):
        self.unitcell_anzahl = N
        self.unitcell_abstand = a
        self.mass_anzahl = N*2
        self.mass_abstand = a/2
        self.mass_relation = mass_relation
        # x-Positionen der Massen
        x_heavy = []    # schwere Masse M_1
        x_light = []    # leichte Masse M_2
        # Berechnung der x-Positionen der Massen m_1 und m_2
        for i in range(0, self.unitcell_anzahl):
            x_heavy.append((2 * i) * self.mass_abstand)
            x_light.append((2 * i + 1) * self.mass_abstand)
        # y-Position der Massen auf y=0 setzen
        y = np.zeros(self.unitcell_anzahl)
        # Radiuswerte der Massen (Standard radius=1); Radius der leichten Massen mit dem Massenverhältnis skalieren
        radius_heavy = np.ones(self.unitcell_anzahl)
        radius_light = np.ones(self.unitcell_anzahl) * 1/self.mass_relation
        # Definieren der Dictionaries, welche alle benötigten Informationen zum plotten Massepunkte beinhaltet
        self.shape_rest_heavy = ColumnDataSource(data=dict(x=x_heavy, y=y, radius_mass=radius_heavy))
        self.shape_rest_light = ColumnDataSource(data=dict(x=x_light, y=y, radius_mass=radius_light))

    def calculate_diatomic_acoustic_dynamics(self, time, ka, mass_relation):
        # Listen für die x-Positionen der schweren und leichten Masse
        x_heavy = []
        x_light = []
        # Iterierend über jede Einheitszelle die Verschiebung berechnen
        for i in range(0, self.unitcell_anzahl):
            disp = displacement_diatomic_acoustic(mass_relation, ka, i, time)      # Rückgabe der Funktion ist ein Array
            x_heavy.append((2*i)*self.mass_abstand + disp[0]*1)         # zur Liste hinzufügen
            x_light.append((2 * i+1) * self.mass_abstand + disp[1]*1)       # zur Liste hinzufügen
        # x-Koordinaten in den CDS ändern und damit Grafik der Massen aktualisieren
        self.shape_rest_heavy.data['x'] = x_heavy
        self.shape_rest_light.data['x'] = x_light

    def superposition_two_acoustic_normalmodes(self, time, ka_1, ka_2, mass_relation, c, x_range):
        # Listen für die resultierenden x-Positionen, die Auslenkungen und die Position der Ruhelagen der beiden Massen
        x_heavy_real = []
        y_heavy = []
        x_heavy = []

        x_light_real = []
        y_light = []
        x_light = []
        # Iterierend über jede Einheitszelle die Verschiebung aus der Superposition berechnen
        for i in range(0, self.unitcell_anzahl):
            # Berechnung der Verschiebungen
            disp = superposition_diatomic_acoustic_discrete(ka_1, ka_2, self.unitcell_abstand, i, mass_relation, c, time)
            # Berechnung der Ruhelage, Displacements, x-Position der Masse in der Kette
            x_heavy_real.append((2 * i) * self.mass_abstand + disp[0])      # resultierende x-Position hinzufügen
            x_heavy.append((2 * i) * self.mass_abstand)                     # Ruhelage hinzufügen
            y_heavy.append(disp[0])                                         # resultierende Verschiebung hinzufügen

            x_light_real.append((2*i+1) * self.mass_abstand + disp[1])      # resultierende x-Position hinzufügen
            x_light.append((2*i+1) * self.mass_abstand)                     # Ruhelage hinzufügen
            y_light.append(disp[1])                                         # resultierende Verschiebung hinzufügen

        # x-Koordinaten in den CDS ändern und damit Grafik der Massen aktualisieren
        self.shape_rest_heavy.data['x'] = x_heavy_real
        self.shape_rest_light.data['x'] = x_light_real

        # Berechnung Geschwindigkeitsvektoren, Hüllkurve und Carrier-Wellen mit der Analyse Funktion
        y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
            superposition_diatomic_acou_analysis(ka_1, ka_2, self.unitcell_abstand, mass_relation, c,
                                                 time, x_range, 1)

        return x_heavy, y_heavy, x_light, y_light, y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp,\
               v_phase_xpos, v_phase_ypos, v_group

    def calculate_diatomic_optical_dynamics(self, time, ka, mass_relation):
        # Listen für die x-Positionen der schweren und leichten Masse
        x_heavy = []
        x_light = []
        # Iterierend über jede Einheitszelle die Verschiebung berechnen
        for i in range(0, self.unitcell_anzahl):
            disp = displacement_diatomic_optical(mass_relation, ka, i, time)
            x_heavy.append((2*i)*self.mass_abstand + disp[0]*1)             # zur Liste hinzufügen
            x_light.append((2 * i+1) * self.mass_abstand + disp[1]*1)       # zur Liste hinzufügen

        # x-Koordinaten in den CDS ändern und damit Grafik der Massen aktualisieren
        self.shape_rest_heavy.data['x'] = x_heavy
        self.shape_rest_light.data['x'] = x_light

    def superposition_two_optical_normalmodes(self, time, ka_1, ka_2, mass_relation, c, x_range):
        # Listen für die resultierenden x-Positionen, die Auslenkungen und die Positionen der Ruhelage der beiden Massen
        x_heavy_real = []
        y_heavy = []
        x_heavy = []

        x_light_real = []
        y_light = []
        x_light = []
        # Berechnung der Verschiebung der Massen mittels Iteration über jede Einheitszelle
        for i in range(0, self.unitcell_anzahl):
            # Berechnung der Verschiebungen
            disp = superposition_diatomic_optical_discrete(ka_1, ka_2, self.unitcell_abstand, i, mass_relation, c, time)

            # Berechnung der Ruhelage, Displacements, x-Position der Masse in der Kette
            x_heavy_real.append((2 * i) * self.mass_abstand + disp[0] * 1)      # resultierende x-Position hinzufügen
            x_heavy.append((2 * i) * self.mass_abstand)                         # Ruhelage hinzufügen
            y_heavy.append(disp[0] * 1)                                         # resultierende Verschiebung hinzufügen

            x_light_real.append((2*i+1) * self.mass_abstand + disp[1] * 1)      # resultierende x-Position hinzufügen
            x_light.append((2*i+1) * self.mass_abstand)                         # Ruhelage hinzufügen
            y_light.append(disp[1] * 1)                                         # resultierende Verschiebung hinzufügen

        # x-Koordinaten in den CDS ändern und damit Grafik der Massen aktualisieren
        self.shape_rest_heavy.data['x'] = x_heavy_real
        self.shape_rest_light.data['x'] = x_light_real

        # Berechnung Geschwindigkeitsvektoren, Hüllkurve und Carrier-Wellen mit der Analyse Funktion
        y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
            superposition_diatomic_opti_analysis(ka_1, ka_2, self.unitcell_abstand, mass_relation, c,
                                                 time, x_range, 1)
        return x_heavy, y_heavy, x_light, y_light, y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp,\
               v_phase_xpos, v_phase_ypos, v_group

    def plot(self, fig, colour="#0065BD", width=1):      # Plotten der einzelnen Massen als Kreis und Federn als Linie
        fig.line([-self.mass_abstand, self.unitcell_anzahl*2*self.mass_abstand], [0, 0], line_width=2)
        fig.circle(x='x', y='y', radius='radius_mass', color='blue', source=self.shape_rest_heavy, line_width=width)
        fig.circle(x='x', y='y', radius='radius_mass', color=colour, source=self.shape_rest_light, line_width=width)

    def change_size_rel(self, new):         # Methode zum Ändern des Radius der Masse bei Änderung des Massenverhältnis
        self.mass_relation = new
        self.shape_rest_light.data['radius_mass'] = np.ones(self.unitcell_anzahl) * 1/self.mass_relation
