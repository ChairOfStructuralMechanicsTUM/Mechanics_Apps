import numpy as np


##################################
# Dispersionsbeziehung Funktionen
##################################

def dis_rel_mono(ka):
    """ monoatomares Dispersionsverhältnis genormt auf omega/sqrt(4c/m)
    """
    y = np.sin(abs(ka)/2)
    return y


def omega_mono(ka, c=1, m=1):
    """monoatomares Dispersionsverhältnis
    """
    y = np.sqrt(4*c/m) * np.sin(abs(ka)/2)
    return y


def dis_rel_diatom_optical(ka, m_relation, c=1):
    """ diatomares Dispersionsverhältnis (optischer Zweig) genormt auf omega/(sqrt(2c*(1/m_1 + 1/m_2)))
    a = Länge der Einheitszelle
    """
    m_1 = m_relation
    m_2 = 1
    w_3 = np.sqrt(2*c*(1/m_1+1/m_2))
    w = 1/w_3 * np.sqrt(c/(m_1*m_2) * (m_1+m_2+np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(ka))))
    return w


def omega_diatom_optical(k, a, m_relation, c=1):
    """ diatomares Dispersionsverhältnis (optischer Zweig)
        a = Länge der Einheitszelle
    """
    m_1 = m_relation
    m_2 = 1
    w = np.sqrt(c/(m_1*m_2) * (m_1+m_2+np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(k*a))))
    return w


def dis_rel_diatom_acoustic(ka, m_relation, c=1):
    """ diatomares Dispersionsverhältnis (akustischer Zweig) genormt auf omega/(sqrt(2c*(1/m_1 + 1/m_2)));
        a = Länge der Einheitszelle
    """
    m_1 = m_relation
    m_2 = 1
    w_3 = np.sqrt(2*c*(1/m_1+1/m_2))
    w = 1/w_3 * np.sqrt(c/(m_1*m_2) * (m_1+m_2-np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(ka))))
    return w


def omega_diatom_acoustic(k, a, m_relation, c=1):
    """ diatomares Dispersionsverhältnis (akustischer Zweig);
        a = Länge der Einheitszelle
    """
    m_1 = m_relation
    m_2 = 1
    w = np.sqrt(c/(m_1*m_2) * (m_1+m_2-np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(k*a))))
    return w

#####################
# Triatomic System
#####################


def omega_triatom_acou(m_1, m_2, m_3, ka, c=1):
    """ triatomares Dispersionsverhältnis (akustischer Zweig)
        a = Abstand der einzelnen Massen
    """
    t_1 = (8 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 3 - 27 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3) * (
                m_2 * m_3 + m_1 * m_3 + m_1 * m_2) + 54 * (m_1 * m_2 * m_3) ** 2 * np.sin((3 * ka) / 2) ** 2)
    t_2 = (4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) ** (3/2)
    t = t_1 / t_2
    theta = np.arccos(t)
    # formula for the acoustic branch (Unterschiede zu den andern Omegas liegen in einem Phasenversatz im cosinus-Term)
    omega_1 = np.sqrt((-2 * c * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) + 2 * c * np.sqrt(
        4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) * np.cos(
        (np.pi - theta) / 3)) / (-3 * (m_1 * m_2 * m_3)))
    return omega_1


def omega_triatom_optical_one(m_1, m_2, m_3, ka, c=1):
    """ triatomares Dispersionsverhältnis (erster optischer Zweig)
        a = Abstand der einzelnen Massen
    """
    t_1 = (8 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 3 - 27 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3) * (
                m_2 * m_3 + m_1 * m_3 + m_1 * m_2) + 54 * (m_1 * m_2 * m_3) ** 2 * np.sin((3 * ka) / 2) ** 2)
    t_2 = (4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) ** (3 / 2)
    t = t_1 / t_2
    theta = np.arccos(t)

    omega_2 = np.sqrt((-2 * c * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) + 2 * c * np.sqrt(
        4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) * np.cos(
        (np.pi + theta) / 3)) / (-3 * (m_1 * m_2 * m_3)))
    return omega_2


def omega_triatom_optical_two(m_1, m_2, m_3, ka, c=1):
    """ triatomares Dispersionsverhältnis (zweiter optischer Zweig)
        a = Abstand der einzelnen Massen
    """
    t_1 = (8 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 3 - 27 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3) * (
                m_2 * m_3 + m_1 * m_3 + m_1 * m_2) + 54 * (m_1 * m_2 * m_3) ** 2 * np.sin((3 * ka) / 2) ** 2)
    t_2 = (4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) ** (3 / 2)
    t = t_1 / t_2
    theta = np.arccos(t)

    omega_3 = np.sqrt((-2 * c * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) - 2 * c * np.sqrt(
        4 * (m_2 * m_3 + m_1 * m_3 + m_1 * m_2) ** 2 - 9 * (m_1 * m_2 * m_3) * (m_1 + m_2 + m_3)) * np.cos((theta) / 3)) / (
                               -3 * (m_1 * m_2 * m_3)))
    return omega_3


##################################
# Simulationsfunktionen
##################################

def displacement_diatomic_acoustic(m_relation, ka, unit_number, time, c=1):
    """ Berechnung der realen Verschiebungen der leichten und schweren Massen für eine akustische Mode
        im diatomaren System
    """
    m_1 = m_relation
    m_2 = 1
    w = np.sqrt(c/(m_1*m_2) * (m_1+m_2-np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(ka))))
    if ka == 0:
        v_l = 0
        u_l = 0
    else:
        v_l = c/(2*c-w**2*m_2) * ((1 + np.cos(ka))*np.cos(ka*unit_number - w*time)
                                  - np.sin(ka)*np.sin(ka*unit_number - w * time))
        u_l = np.cos(ka*unit_number-w*time)

    # Displacementvector [heavy atom, light atom]
    disp = [u_l, v_l]
    return disp


def displacement_diatomic_optical(m_relation, ka, unit_number, time, c=1):
    """ Berechnung der realen Verschiebungen der leichten und schweren Massen für eine optische Mode
        im diatomaren System
    """
    m_1 = m_relation
    m_2 = 1
    w = np.sqrt(c/(m_1*m_2) * (m_1+m_2+np.sqrt(m_1**2+m_2**2+2*m_1*m_2*np.cos(ka))))
    # Berechnung des Displacements
    u_l = c/(2*c-w**2*m_1) * ((1 + np.cos(ka))*np.cos(ka*unit_number - w*time)
                              + np.sin(ka)*np.sin(ka*unit_number - w * time))
    v_l = np.cos(ka*unit_number-w*time)
    # Displacementvector [heavy atom, light atom]
    disp = [u_l, v_l]
    return disp


def displacement_monoatomic(mass, ka, unit_number, time, c=1):
    """ Berechnung der realen Verschiebungen der Massen für eine Mode im monoatomaren System
    """
    if ka == 0:
        # u_l = 0
        u_l = np.zeros_like(unit_number)
    else:
        w = np.sqrt(4*c/mass) * np.sin(abs(ka)/2)
        # -- Für amplitude a=1
        u_l = np.cos(ka * unit_number - w * time)
    return u_l


def superposition_monoatomic_discrete(ka_1, ka_2, unit_number, amplitude, time):
    """ Berechnung der realen Verschiebungen der Massen für zwei superpositionierte Moden im monoatomaren System
    """
    ka = (ka_1 + ka_2) / 2
    delta_ka = (ka_1 - ka_2) / 2
    omega_1 = omega_mono(ka_1)
    omega_2 = omega_mono(ka_2)
    omega = (omega_1+omega_2)/2
    delta_omega = (omega_1-omega_2)/2
    y = 2 * amplitude * np.cos(ka * unit_number - omega * time) * np.cos(delta_ka * unit_number - delta_omega * time)

    return y


def superposition_monoatomic_analysis(ka_1, ka_2, a, amplitude, time, x_range):
    """ Berechnung der Phasen-, Gruppengeschwindigkeitsvektoren sowie den Verlauf der Hüllkurve der Wellenpakte und
        Carrier-Wellen (monoatomare Superposition)
    """
    # Berechnung der Größen Omega & k nach der Superpositionstheorie von L.Brillouin
    k_1 = ka_1/a
    k_2 = ka_2 / a
    k = (k_1 + k_2) / 2
    delta_k = (k_1 - k_2) / 2
    omega_1 = omega_mono(ka_1)
    omega_2 = omega_mono(ka_2)
    omega = (omega_1+omega_2)/2
    delta_omega = (omega_1-omega_2)/2

    # zwei Listen zum Speichern der y-Werte der kontinuierlichen Hüllkurve und Carrierwelle
    y_carrier_disp = []
    y_envelope_disp = []

    # Auswertung der Displacementfunktion über die Werte der x_range Liste
    for xn in x_range:
        y_carrier = 2*amplitude * np.cos(k*xn - omega * time)*np.cos(delta_k * xn - delta_omega * time)
        y_envelope_form = 2*amplitude * np.cos(delta_k * xn - delta_omega * time)
        y_carrier_disp.append(y_carrier)
        y_envelope_disp.append(y_envelope_form)

    # Divided by zero Vermeiden
    if delta_k == 0:
        v_group = 0
    else:
        v_group = delta_omega / delta_k * time

    # Divided by zero Vermeiden
    if k == 0:
        v_phase_xpos = 0
        v_phase_ypos = 2 * amplitude
    else:
        v_phase_xpos = omega / k * time
        v_phase_ypos = 2 * amplitude * np.cos(delta_k * (omega / k * time) - delta_omega * time)


    return y_carrier_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group


def superposition_diatomic_acoustic_discrete(ka_1, ka_2, a, unit_number, mass_relation, c, time):
    """ Berechnung der realen Verschiebungen der leichten und schweren Massen für zwei superpositionierte akustische
        Moden im diatomaren System
    """
    m_1 = mass_relation
    m_2 = 1
    k_1 = ka_1/a
    k_2 = ka_2/a
    omega_1 = omega_diatom_acoustic(k_1, a, mass_relation)
    omega_2 = omega_diatom_acoustic(k_2, a, mass_relation)

    v_l = c/(2*c-omega_1**2*m_2) * ((1 + np.cos(ka_1))*np.cos(ka_1*unit_number - omega_1*time)
                              - np.sin(ka_1)*np.sin(ka_1*unit_number - omega_1 * time)) \
          +c/(2*c-omega_2**2*m_2) * ((1 + np.cos(ka_2))*np.cos(ka_2*unit_number - omega_2*time)
                              - np.sin(ka_2)*np.sin(ka_2*unit_number - omega_2 * time))
    u_l = np.cos(ka_1*unit_number-omega_1*time)+np.cos(ka_2*unit_number-omega_2*time)
    disp = [u_l, v_l]
    return disp


def superposition_diatomic_optical_discrete(ka_1, ka_2, a, unit_number, mass_relation, c, time):
    """ Berechnung der realen Verschiebungen der leichten und schweren Massen für zwei superpositionierte optische
        Moden im diatomaren System
    """
    m_1 = mass_relation
    m_2 = 1
    k_1 = ka_1/a
    k_2 = ka_2/a
    omega_1 = omega_diatom_optical(k_1, a, mass_relation)
    omega_2 = omega_diatom_optical(k_2, a, mass_relation)

    v_l = np.cos(ka_1*unit_number-omega_1*time) + np.cos(ka_2*unit_number-omega_2*time)
    u_l = c/(2*c-omega_1**2*m_1) * \
          ((1 + np.cos(ka_1))*np.cos(ka_1*unit_number - omega_1*time) + np.sin(ka_1)*np.sin(ka_1*unit_number - omega_1 * time)) \
          + c/(2*c-omega_2**2*m_1) * \
          ((1 + np.cos(ka_2))*np.cos(ka_2*unit_number - omega_2*time) + np.sin(ka_2)*np.sin(ka_2*unit_number - omega_2 * time))
    disp = [u_l, v_l]
    return disp


def superposition_diatomic_acou_analysis(ka_1, ka_2, a, mass_relation, c, time, x_range, amplitude):
    """ Berechnung der Phasen-, Gruppengeschwindigkeitsvektoren sowie den Verlauf der Hüllkurve der Wellenpakte und
        Carrier-Wellen (diatomare akustische Superposition)
    """
    m_1 = mass_relation
    m_2 = 1
    # Berechnung der Größen Omega & k nach der Superpositionstheorie von L.Brillouin
    k_1 = ka_1 / a
    k_2 = ka_2 / a
    k = (k_1 + k_2) / 2
    delta_k = (k_1 - k_2) / 2
    omega_1 = omega_diatom_acoustic(k_1, a, mass_relation)
    omega_2 = omega_diatom_acoustic(k_2, a, mass_relation)
    omega = (omega_1+omega_2)/2
    delta_omega = (omega_1-omega_2)/2

    # zwei Listen zum Speichern der y-Werte der kontinuierlichen Hüllkurve und Carrierwelle
    y_carrier_disp_v_l = []
    y_carrier_disp_u_l = []
    y_envelope_disp = []

    # Auswertung der Displacementfunktion über die Werte der x_range Liste
    for xn in x_range:
        y_carrier_v_l = amplitude * (
            (c/(2*c-omega_1**2*m_2) * ((1 + np.cos(ka_1))*np.cos(k_1*(xn-a/2) - omega_1*time) - np.sin(ka_1)*np.sin(k_1*(xn-a/2) - omega_1 * time))) \
             + (c/(2*c-omega_2**2*m_2) * ((1 + np.cos(ka_2))*np.cos(k_2*(xn-a/2) - omega_2*time) - np.sin(ka_2)*np.sin(k_2*(xn-a/2) - omega_2 * time))))
        y_carrier_u_l = amplitude * (np.cos(k_1 * xn - omega_1 * time) + np.cos(k_2 * xn - omega_2 * time))
        y_carrier_disp_v_l.append(y_carrier_v_l)        # Hinzufügen in die Liste
        y_carrier_disp_u_l.append(y_carrier_u_l)        # Hinzufügen in die Liste

        # Berechnung + Hinzufügen der Envelopefunktion aus der Superposition der Displacementfunktion von u_l
        y_envelope_form = 2 * amplitude * np.cos(delta_k * xn - delta_omega * time)
        y_envelope_disp.append(y_envelope_form)

    # Divided by zero Vermeiden
    if delta_k == 0:
        v_group = 0
    else:
        v_group = delta_omega / delta_k * time

    # Divided by zero Vermeiden
    if k == 0:
        v_phase_xpos = 0
        # Berechnung des Phasengeschwindigkeitsvektor, sodass er sich der Envelope Funktion bewegt
        v_phase_ypos = 2 * amplitude
    else:
        v_phase_xpos = omega / k * time
        # Berechnung des Phasengeschwindigkeitsvektor, sodass er sich der Envelope Funktion bewegt
        v_phase_ypos = 2 * amplitude * np.cos(delta_k * (omega / k * time) - delta_omega * time)

    return y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group


def superposition_diatomic_opti_analysis(ka_1, ka_2, a, mass_relation, c, time, x_range, amplitude):
    """ Berechnung der Phasen-, Gruppengeschwindigkeitsvektoren sowie den Verlauf der Hüllkurve der Wellenpakte und
        Carrier-Wellen (diatomare optische Superposition)
    """
    m_1 = mass_relation
    m_2 = 1
    # Berechnung der Größen Omega & k nach der Superpositionstheorie von L.Brillouin
    k_1 = ka_1 / a
    k_2 = ka_2 / a
    k = (k_1 + k_2) / 2
    delta_k = (k_1 - k_2) / 2
    omega_1 = omega_diatom_optical(k_1, a, mass_relation)
    omega_2 = omega_diatom_optical(k_2, a, mass_relation)
    omega = (omega_1+omega_2)/2
    delta_omega = (omega_1-omega_2)/2

    # zwei Listen zum Speichern der y-Werte der kontinuierlichen Hüllkurve und Carrierwelle
    y_carrier_disp_v_l = []
    y_carrier_disp_u_l = []
    y_envelope_disp = []

    # Auswertung der Displacementfunktion über die Werte der x_range Liste
    for xn in x_range:
        y_carrier_v_l = amplitude * (np.cos(k_1*(xn-a/2)-omega_1*time) + np.cos(k_2*(xn-a/2)-omega_2*time))

        y_carrier_u_l = amplitude * (c/(2*c-omega_1**2*m_1) *
                ((1 + np.cos(ka_1))*np.cos(k_1*xn - omega_1*time) + np.sin(ka_1)*np.sin(k_1*xn - omega_1 * time))
                + c/(2*c-omega_2**2*m_1) *
                ((1 + np.cos(ka_2))*np.cos(k_2*xn - omega_2*time) + np.sin(ka_2)*np.sin(k_2*xn - omega_2 * time)))
        y_carrier_disp_v_l.append(y_carrier_v_l)        # Hinzufügen in die Liste
        y_carrier_disp_u_l.append(y_carrier_u_l)        # Hinzufügen in die Liste

        # Berechnung + Hinzufügen der Envelopefunktion aus der Superposition der Displacementfunktion von v_l
        y_envelope_form = 2 * amplitude * np.cos(delta_k * (xn-a/2) - delta_omega * time)
        y_envelope_disp.append(y_envelope_form)

    # Divided by zero Vermeiden und bei negativer Gruppengeschwindigkeit
    # den Gruppgeschwindigkeitsvektor von rechts bei 120 starten lassen
    if delta_k == 0:
        v_group = 0
        v_group_ypos = 2 * amplitude * np.cos(delta_k * (120 - a / 2) - delta_omega * time)
    elif delta_omega/delta_k < 0:
        v_group = 120 + delta_omega / delta_k * time
        v_group_ypos = 2 * amplitude * np.cos(delta_k * (v_group-a/2) - delta_omega * time)

    # Divided by zero Vermeiden
    if k == 0:
        v_phase_xpos = 0
        # Berechnung des Phasengeschwindigkeitsvektor, sodass er sich der Envelope Funktion bewegt
        v_phase_ypos = 2 * amplitude
    else:
        v_phase_xpos = omega / k * time
        # Berechnung des Phasengeschwindigkeitsvektor, sodass er sich der Envelope Funktion bewegt
        v_phase_ypos = 2 * amplitude * np.cos(delta_k * (omega / k * time - a / 2) - delta_omega * time)


    return y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group, v_group_ypos


########################
# Zusatz (optional)
########################

def diatomic_displacement_monorepr(k, a, m_relation, x_n1, x_n2, time):
        omega_acou = omega_diatom_acoustic(k, a, m_relation)
        omega_opti = omega_diatom_optical(k, a, m_relation)
        disp_m1_acou = []
        disp_m2_acou = []
        disp_m1_opti = []
        disp_m2_opti = []

        for xn1, xn2 in zip(x_n1, x_n2):
            disp_m1_acou.append(np.cos(k * xn1 - omega_acou * time))
            disp_m2_acou.append(np.cos(k * xn2 - omega_acou * time))
            disp_m1_opti.append(np.cos(k * xn1 - omega_opti * time))
            disp_m2_opti.append(np.cos(k * xn2 - omega_opti * time))

        return disp_m1_acou, disp_m2_acou, disp_m1_opti, disp_m2_opti


def triatomic_displacement_monorepr(k, a, m_relation, x_n1, x_n2, x_n3, time):
    m_1 = m_relation
    m_2 = m_relation
    m_3 = m_relation

    omega_acou = omega_triatom_acou(m_1, m_2, m_3, k)
    omega_opti_1 = omega_triatom_optical_one(m_1, m_2, m_3, k)
    omega_opti_2 = omega_triatom_optical_two(m_1, m_2, m_3, k)

    disp_m1_acou = []
    disp_m2_acou = []
    disp_m3_acou = []

    disp_m1_opti_1 = []
    disp_m2_opti_1 = []
    disp_m3_opti_1 = []

    disp_m1_opti_2 = []
    disp_m2_opti_2 = []
    disp_m3_opti_2 = []

    for xn1, xn2, xn3 in zip(x_n1, x_n2, x_n3):
        disp_m1_acou.append(np.cos(k * xn1 - omega_acou * time))
        disp_m2_acou.append(np.cos(k * xn2 - omega_acou * time))
        disp_m3_acou.append(np.cos(k * xn3 - omega_acou * time))

        disp_m1_opti_1.append(np.cos(k * xn1 - omega_opti_1 * time))
        disp_m2_opti_1.append(np.cos(k * xn2 - omega_opti_1 * time))
        disp_m3_opti_1.append(np.cos(k * xn3 - omega_opti_1 * time))

        disp_m1_opti_2.append(np.cos(k * xn1 - omega_opti_2 * time))
        disp_m2_opti_2.append(np.cos(k * xn2 - omega_opti_2 * time))
        disp_m3_opti_2.append(np.cos(k * xn3 - omega_opti_2 * time))

    return disp_m1_acou, disp_m2_acou, disp_m3_acou, disp_m1_opti_1, disp_m2_opti_1, disp_m3_opti_1,\
            disp_m1_opti_2, disp_m2_opti_2, disp_m3_opti_2

