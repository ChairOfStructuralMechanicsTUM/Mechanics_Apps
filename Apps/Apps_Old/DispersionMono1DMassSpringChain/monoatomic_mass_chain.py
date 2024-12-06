from bokeh.models import ColumnDataSource
import numpy as np
from functions import superposition_monoatomic_discrete, superposition_monoatomic_analysis


class Monoatomic_chain:
    def __init__(self, N, a, r=1):
        self.mass_count = N
        self.mass_distance = a
        self.length = self.mass_count * self.mass_distance

        # Initiale Positionen und Radien der Massen (Ruhelage)
        x = np.arange(N) * a
        y = np.zeros(self.mass_count)
        radius = np.ones(self.mass_count) * r

        # Daten in ColumnDataSource speichern
        self.mass_shape = ColumnDataSource(data=dict(x=x, y=y, radius_mass=radius))

    def calculate_monoatomic_dynamics(self, t, k, mass):
        # Nutze NumPy für Vektorisierung
        indices = np.arange(self.mass_count)
        # Verschiebung für alle Massen auf einmal berechnen
        disp = self.displacement_monoatomic(mass, k, indices, t)
        # Neue Positionen berechnen
        x = indices * self.mass_distance + disp * self.mass_distance / 2
        # Aktualisiere die Datenquelle
        self.mass_shape.data['x'] = x

    @staticmethod
    def displacement_monoatomic(mass, ka, unit_numbers, time, c=1):
        """ Berechnung der realen Verschiebungen der Massen für eine Mode im monoatomaren System
        """
        if ka == 0:
            # Verschiebung ist null, wenn ka = 0
            return np.zeros_like(unit_numbers)
        else:
            # Frequenzberechnung (konstante Werte nur einmal berechnen)
            w = np.sqrt(4 * c / mass) * np.sin(abs(ka) / 2)
            # Berechne die Verschiebung für alle Einheiten (vektorisiert)
            return np.cos(ka * unit_numbers - w * time)

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

        self.mass_shape.data['x'] = x_real  # Position im CDS anpassen


        # Berechnung Geschwindigkeitsvektoren, Hüllkurve und Carrier-Welle mit der Analyse Funktion
        y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
            superposition_monoatomic_analysis(k_1, k_2, self.mass_distance, 1, t, x_range)
        return x, y, y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group

    # Plotten der einzelnen Massen als Kreis und Federn als Linie
    def plot(self, fig, colour="#0065BD", width=2):
        if not fig.renderers:  # nur wenn keine Renderers (Linien) existieren
            print('Federkette wurde geplottet')
            fig.line([-self.mass_distance, self.length], [0, 0], line_width=width)
        fig.circle(x='x', y='y', radius='radius_mass', color=colour, source=self.mass_shape, line_width=width)
