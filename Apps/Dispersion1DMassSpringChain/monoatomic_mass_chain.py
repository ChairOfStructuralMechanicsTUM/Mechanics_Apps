from bokeh.models import ColumnDataSource
import numpy as np
from functions import displacement_monoatomic, superposition_monoatomic_discrete, superposition_monoatomic_analysis


class Monoatomic_chain(object):
    def __init__(self, N, a, r=1):
        self.mass_count = N
        self.mass_distance = a
        # Ruhelage der Massen berechnen
        x = np.arange(N) * a
        y = np.zeros(self.mass_count)
        # Radiuswerte der einzelnen Massen
        radius = np.ones(self.mass_count) * r
        # alle Daten in CDS speichern
        self.mass_shape = ColumnDataSource(data=dict(x=x, y=y, radius_mass=radius))

    def calculate_monoatomic_dynamics(self, t, k, mass):
        x = []          # Leere Liste anlegen
        for i in range(0, self.mass_count):
            # Verschiebung berechnen
            disp = displacement_monoatomic(mass, k, i, t)
            # Neue Position in Liste speichern
            x.append(i * self.mass_distance + disp * self.mass_distance / 2)

        self.mass_shape.data['x'] = x    # Positionen der Massen im CDS anpassen

    def superposition_two_monoatomic_normalmodes(self, t, k_1, k_2, x_range):
        x_real = []     # leere Liste der aktuellen x-Position der Masse
        x = []          # leere Liste der x-Position der Ruhelagen der Massen
        y = []          # leere Liste der aktuellen Verschiebung der Massen
        for i in range(0, self.mass_count):
            # Berechnung der Verschiebung
            disp_discrete = superposition_monoatomic_discrete(k_1, k_2, i, 1, t)
            # in Listen abspeichern
            x.append(i * self.mass_distance)
            y.append(disp_discrete)
            x_real.append(i * self.mass_distance + disp_discrete)

        self.mass_shape.data['x'] = x_real   # Position im CDS anpassen

        # Berechnung Geschwindigkeitsvektoren, Hüllkurve und Carrier-Welle mit der Analyse Funktion
        y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
            superposition_monoatomic_analysis(k_1, k_2, self.mass_distance, 1, t, x_range)
        return x, y, y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group

    # Plotten der einzelnen Massen als Kreis und Federn als Linie
    def plot(self, fig, colour="#0065BD", width=2):
        fig.line([-self.mass_distance, self.mass_count * self.mass_distance], [0, 0], line_width=width)
        fig.circle(x='x', y='y', radius='radius_mass', color=colour, source=self.mass_shape, line_width=width)
