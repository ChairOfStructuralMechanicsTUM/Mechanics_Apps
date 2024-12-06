from bokeh.models import ColumnDataSource
import numpy as np
from functions import displacement_monoatomic, superposition_monoatomic_discrete, superposition_monoatomic_analysis


class Monoatomic_chain(object):
    def __init__(self, N, a, r=1):
        self.mass_count = N
        self.mass_distance = a
        x = np.arange(N) * a            # Ruhelage der Massen berechnen
        y = np.zeros(self.mass_count)   # y-Koordinate mit y=0 der selben Größe
        radius = np.ones(self.mass_count) * r  # Radiuswerte für die einzelnen Massen (CDS nur Datensätze gleicher Größe
        self.mass_shape = ColumnDataSource(data=dict(x=x, y=y, radius_mass=radius)) # alle Daten in CDS speichern

    def calculate_monoatomic_dynamics(self, t, k, mass):
        x = []          # Leer Liste anlegen

        for i in range(0, self.mass_count):             # Über alle Massen iterieren
            disp = displacement_monoatomic(mass, k, i, t)           # Verschiebung berechnen
            x.append(i * self.mass_distance + disp * self.mass_distance / 2)   # Neue Position ans Ende von x hinzufügen

        self.mass_shape.data['x'] = x     # x-Koordinate im CDS ändern und damit Grafik der Massen aktualisieren

    def superposition_two_monoatomic_normalmodes(self, t, k_1, k_2, x_range):
        x_real = []     # leere Liste der aktuellen x-Position der Masse
        x = []          # leere Liste der x-Position der Ruhelagen der Massen
        y = []          # leere Liste zum Speichern der aktuellen Verschiebung der Massen (transversal Grafik)
        for i in range(0, self.mass_count):          # Über alle Massen iterieren
            disp_discrete = superposition_monoatomic_discrete(k_1, k_2, i, 1, t)  # Berechnung Verschiebung Superposition
            x.append(i * self.mass_distance)        # zur Liste hinzufügen
            y.append(disp_discrete)                 # zur Liste hinzufügen
            x_real.append(i * self.mass_distance + disp_discrete)       # zur Liste hinzufügen

        self.mass_shape.data['x'] = x_real       # x-Koordinate im CDS ändern und damit Grafik der Massen aktualisieren

        # Berechnung Geschwindigkeitsvektoren, Hüllkurve und Carrier-Welle mit der Analyse Funktion
        y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
            superposition_monoatomic_analysis(k_1, k_2, self.mass_distance, 1 / 4 * self.mass_distance, t, x_range)
        return x, y, y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group

    def plot(self, fig, colour="#0065BD", width=2):     # Plotten der einzelnen Massen als Kreis und Federn als Linie
        fig.line([-self.mass_distance, self.mass_count * self.mass_distance], [0, 0], line_width=width)
        fig.circle(x='x', y='y', radius='radius_mass', color=colour, source=self.mass_shape, line_width=width)
