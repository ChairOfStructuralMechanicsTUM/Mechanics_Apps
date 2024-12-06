# general imports
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row, Spacer
from bokeh.models import Button, Label, ColumnDataSource, Legend, \
    Paragraph, Div, BoxAnnotation
from bokeh.models.glyphs import ImageURL

from functions import dis_rel_mono, dis_rel_diatom_acoustic, dis_rel_diatom_optical
from math import floor

from monoatomic_mass_chain import Monoatomic_chain
from diatomic_mass_chain import Diatomic_chain
import time
# Using pathlib
import pathlib
import sys
# Dateipfad herausfinden in der Umgebung, wo die WebApp am Ende laufen wird
shareddir = str(pathlib.Path(__file__).parent.parent.resolve() / "shared" ) + "/"
sys.path.insert(0,shareddir)
app_base_path = pathlib.Path(__file__).resolve().parents[0]
from latex_support import LatexDiv, LatexLabel, LatexLabelSet, LatexSlider, LatexLegend     #sc: import latex

# Standard Spracheinstellung
language = 'english'

######################
# Language dictionarys
######################
# Dict für alle Label und Title von den Plots
label_dictionary = ColumnDataSource(data=dict(deutsch=[['Frequenzsperrband anzeigen', 'Frequenzsperrband ausblenden'],
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die ausgewählte Normalmode:',
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die superpositionierten Normalmoden:',
                                'Visualisierung der longitudinal Verschiebungen der diskreten Massepunkte über die y-Achse',
                                ['Frequenzsperrbänder anzeigen', 'Frequenzsperrbänder ausblenden'],
                                                       'Longitudinale Verschiebung',
                                                       'Ruhelage des diskreten Massepunkts',
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die ausgewählte akustische Normalmode:',
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die ausgewählte optische Normalmode:',
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die superpositionierten akustischen Normalmoden:',
                                'Visualisierung der Dynamik der Masse-Feder-Kette für die superpositionierten optischen Normalmoden:',

                                                       ],
                                              english=[['Show Bandgap', 'Hide Bandgap'],
                                'Visualization of the dynamics of the mass-spring chain for the selected normal mode',
                                'Visualization of the dynamics of the mass-spring chain for the superimposed normal modes:',
                                'Visualization of the longitudinal displacements of the discrete mass points via the y-axis',
                                ['Show Bandgaps', 'Hide Bandgaps'],
                                                       'Longitudinal Displacement',
                                                       'Equilibrium position of the discrete mass point',
                                'Visualization of the dynamics of the mass-spring chain for the selected acoustical normal mode',
                                'Visualization of the dynamics of the mass-spring chain for the selected optical normal mode',
                                'Visualization of the dynamics of the mass-spring chain for the superimposed acoustical normal modes:',
                                'Visualization of the dynamics of the mass-spring chain for the superimposed optical normal modes:'
                                                       ]))
# Dict für alle Legenden innerhalb des monoatomaren-Menu
legend_dictionary_mono = ColumnDataSource(data=dict(deutsch=["Akustischer Zweig", 'μ',
                                                        'μ₁ (2.Animation)', 'μ₂ (2.Animation)',
                                                            'Position einer Masse','Carrier-Welle','Hüllkurve der Wellenpakete',
                                                             'Phasengeschwindigkeitsvektor', 'Gruppengeschwindigkeitsvektor'
                                                             ],
                                                    english=["Acoustical Branch", 'μ',
                                                        'μ₁ (2.Animation)', 'μ₂ (2.Animation)',
                                                             'Position of a mass', 'Carrier-Wave','Envelope of the wavepackets',
                                                             'phase velocity vector', 'group velocity vector'
                                                             ]))
# Dict für alle Legenden innerhalb des diatomaren-Menu
legend_dictionary_di = ColumnDataSource(data=dict(deutsch=["Akustischer Zweig",'Optischer Zweig', 'dimensionsloser Wellenvektor',
                                                        'μ₁ - akustische Superposition (2.Animation)',
                                                        'μ₂ - akustische Superposition (2.Animation)',
                                                        'μ₁ - optische Superposition (2.Animation)',
                                                        'μ₂ - optische Superposition (2.Animation)',
                                                        'Position der schweren Masse', 'Position der leichten Masse',
                                                        'Carrier-Welle der schweren Massen','Carrier-Welle der leichten Massen',
                                                        'Hüllkurve der Wellenpakete',
                                                        'Phasengeschwindigkeitsvektor', 'Gruppengeschwindigkeitsvektor'
                                                             ],
                                                    english=["Acoustical Branch", "Optical Branch", 'dimensionless wavevector',
                                                        'μ₁ - acoustic Superposition (2.Animation)',
                                                        'μ₂ - acoustic Superposition(2.Animation)',
                                                        'μ₁ - optical Superposition (2.Animation)',
                                                        'μ₂ - optical Superposition(2.Animation)',
                                                        'Position of the heavy mass', 'Position of the light mass',
                                                        'Carrier-Wave of the heavy masses', 'Carrier-Wave of the light masses',
                                                        'Envelope of the wavepackets',
                                                        'phase velocity vector', 'group velocity vector'
                                                             ]))
# Dict für alle Playbutton Label
label_playbutton_dictionary = ColumnDataSource(data=dict(deutsch=[['Monoatomare Superposition Animation starten', 'Monoatomare Superposition Animation pausieren'],
                                                                  ['Monoatomare Animation starten', 'Monoatomare Animation pausieren'],
                                                                  ['Diatomare Animation starten', 'Diatomare Animation pausieren'],
                                                                  ['Starte diatomare Superposition Animation (akustischer Zweig)', 'Monoatomare Superposition Animation pausieren (akustischer Zweig)'],
                                                                  ['Starte diatomare Superposition Animation (optischer Zweig)', 'Monoatomare Superposition Animation pausieren (optischer Zweig)']
                                                                  ],

                                                         english=[['Start Monoatomic Superposition', 'Pause Monoatomic Superposition'],
                        ['Start Monoatomic Animation', 'Pause Monoatomic Animation'],
                        ['Start Diatomic Animation', 'Pause Diatomic Animation'],
                        ['Start Diatomic Superposition Animation (acoustic branch)', 'Pause Diatomic Superposition Animation(acoustic branch)'],
                        ['Start Diatomic Superposition Animation (optical branch)', 'Pause Diatomic Superposition Animation(optical branch)']

                             ]))

##########################
# Standardwerte festelegen
##########################

# Einstellungen der Masse Feder Ketten
mass_mono = 1
mass_relation = 2
ka_mono = np.pi * 0
ka_di = np.pi * 0
mass_abstand = 4
chain_length = 128
mass_anzahl = floor(chain_length/mass_abstand)
c = 1

# Timer-Einstellungen
time_steps = 0.1
# Erster Timer für die erste Animation
timer_1 = 0
global_timer = Paragraph(text="Timer [s]:" + str(np.round(timer_1, decimals=2)),
                         style={'font-style': 'italic', 'font-size': '14px'})       #sc: styles --> style
# Zweiter Timer für Superpositionsanimationen
timer_2 = 0
global_timer_superpos = Paragraph(text="Timer [s]:" + str(np.round(timer_2, decimals=2)),
                         style={'font-style': 'italic', 'font-size': '14px'})       #sc: styles --> style


def reset_time():       # Timer zurücksetzen
    global timer_1, timer_2
    timer_1 = 0
    timer_2 = 0

################################################################################
# ----------------------- Monoatomic
################################################################################

# --- Instanzieren der gesamten Kette
monoatomic_chain = Monoatomic_chain(mass_anzahl, mass_abstand)

# -- Plot zur Visualisierung der monoatomaren Kette anlegen
monoatomic_animation = figure(title=label_dictionary.data[language][1], tools="", x_range=(-2, chain_length-2),
                              y_range=(-2, 2), width=900, height=50, toolbar_location=None)
monoatomic_animation.title.text_font_size = "10pt"
monoatomic_animation.axis.visible = False
monoatomic_animation.grid.visible = False
# monoatomic_animation.outline_line_color = None
monoatomic_animation.toolbar.logo = None
monoatomic_chain.plot(monoatomic_animation)      # monoatomare Kette plotten

# -- Dispersionrelation Graph
# Dispersionsbeziehung auswerten
mono_ka_val = np.linspace(-np.pi, np.pi, 300)
y_val = dis_rel_mono(mono_ka_val)

# Visualisierung des Bandgaps
mono_bandgap_box = BoxAnnotation(bottom=1, top=None, right=None, left=None, fill_color='red', fill_alpha=0.2) 
mono_bandgap_box.visible = False                    # Standard zu Beginn nicht sichtbar

# Dispersionsbeziehung plotten (mono)
fig_dispersion_mono = figure(x_range=(-np.pi, np.pi), y_range=(0, 1.1), width=850, height=500, toolbar_location=None)
fig_dispersion_mono.yaxis.axis_label = "ω / √(4c/M)"
fig_dispersion_mono.xaxis.axis_label = "μ"
disp_mono_line_1 = fig_dispersion_mono.line(mono_ka_val, y_val, line_width=2, color='green')
fig_dispersion_mono.add_layout(mono_bandgap_box)   # Bandgap Markierung ins Layout hinzufügen

######################################
# Ka-Button monoatomic
######################################
# CDS mit den ausgewählten ka-Werten zum Plotten des Punkts im Dispersiongraph
ka_source_mono = ColumnDataSource(data=dict(x=[ka_mono], y=[dis_rel_mono(ka_mono)]))
# Textfelder zum darstellen des gewählten Werts
ka_mono_button_label = Paragraph(text="μ= " + str(np.round(ka_mono, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style
ka_di_button_label = Paragraph(text="μ= " + str(np.round(ka_di, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style

# Callback Funktionen des ka- & BandgapButton


def mono_ka_plus_button_callback():
    global ka_mono
    if ka_mono + 2*np.pi/mass_anzahl <= 3.1:            # Nur die zulässigen Punkte auswählen lassen
        ka_mono += 2 * np.pi / mass_anzahl
    else:
        ka_mono = np.pi
    ka_mono_button_label.text = "μ= " + str(np.round(ka_mono, decimals=2))    # Text aktualisieren mit neuem Wert
    update_plot()       # Punkt in Grafik aktualisieren
    reset_time()        # Nach jeder Umstellung von t=0 starten


def mono_ka_minus_button_callback():
    global ka_mono
    if ka_mono - 2*np.pi/mass_anzahl >= -3.1:
        ka_mono -= 2 * np.pi / mass_anzahl
    else:
        ka_mono = - np.pi
    ka_mono_button_label.text = "μ= " + str(np.round(ka_mono, decimals=2))
    update_plot()
    reset_time()


def mono_bandgap_button_callback():     # Ändert die Sichtbarkeit der Bandgap Box nach jedem Click auf den Button
    if not mono_bandgap_box.visible:
        mono_bandgap_box.visible = True
        mono_bandgap_button.label = label_dictionary.data[language][0][1] # Label aus dem Dict abhängig gewählten Sprache
    else:
        mono_bandgap_box.visible = False
        mono_bandgap_button.label = label_dictionary.data[language][0][0]


# Funktion zum aktualisieren der CDS mit den Daten für die ka-Punkte in den Dispersionsgrafiken
def update_plot():
    ka_source_mono.data = dict(x=[ka_mono], y=[dis_rel_mono(ka_mono)])
    ka_source_di_opt.data = dict(x=[ka_di], y=[dis_rel_diatom_optical(ka_di, m_relation=mass_relation)])
    ka_source_di_acou.data = dict(x=[ka_di], y=[dis_rel_diatom_acoustic(ka_di, m_relation=mass_relation)])
    ka_source_mono_superpos.data = dict(ka_1=[ka_mono_superpos1], ka_2=[ka_mono_superpos2],
                                                     y_1=[dis_rel_mono(ka_mono_superpos1)],
                                                     y_2=[dis_rel_mono(ka_mono_superpos2)])
    ka_source_di_acou_superpos.data = dict(ka_1=[ka_di_acou_superpos1], ka_2=[ka_di_acou_superpos2],
                                        y_1=[dis_rel_diatom_acoustic(ka_di_acou_superpos1, mass_relation)],
                                        y_2=[dis_rel_diatom_acoustic(ka_di_acou_superpos2, mass_relation)])
    ka_source_di_opti_superpos.data = dict(ka_1=[ka_di_opti_superpos1], ka_2=[ka_di_opti_superpos2],
                                           y_1=[dis_rel_diatom_optical(ka_di_opti_superpos1, mass_relation)],
                                           y_2=[dis_rel_diatom_optical(ka_di_opti_superpos2, mass_relation)])


# Gewählten Wellenvektor plotten
disp_mono_line_2 = fig_dispersion_mono.circle('x', 'y', source=ka_source_mono, color='red')

##############
# Monoatomic Buttons
##############

# Plus Button
mono_ka_plus_button = Button(label="+", button_type="primary", width=50)
mono_ka_plus_button.on_click(mono_ka_plus_button_callback)
# Minus Button
mono_ka_minus_button = Button(label="-", button_type="primary",width=50)
mono_ka_minus_button.on_click(mono_ka_minus_button_callback)
# Bandgap Button
mono_bandgap_button = Button(label=label_dictionary.data[language][0][0], button_type='primary', width=50)
mono_bandgap_button.on_click(mono_bandgap_button_callback)

################################################################################
# ----------------------- Superposition of two monoatomic Normal modes
################################################################################
# Standardwerte festlegen
ka_mono_superpos1 = np.pi * 0
ka_mono_superpos2 = np.pi * 0

##########
# buttons
##########
ka_source_mono_superpos = ColumnDataSource(data=dict(ka_1=[ka_mono_superpos1], ka_2=[ka_mono_superpos2],
                                                     y_1=[dis_rel_mono(ka_mono_superpos1)],
                                                     y_2=[dis_rel_mono(ka_mono_superpos2)]))
# ka-Anzeige anlegen
ka_mono_superpos1_button_label = Paragraph(text="μ₁= " + str(np.round(ka_mono_superpos1, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'}) #sc: styles --> style
ka_mono_superpos2_button_label = Paragraph(text="μ₂= " + str(np.round(ka_mono_superpos2, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'}) #sc: styles --> style
# ka-Punkte in die Dispersionsgrafik hinzufügen
disp_mono_line_3 = fig_dispersion_mono.circle('ka_1', 'y_1', source=ka_source_mono_superpos, fill_color='black', size=5)
disp_mono_line_4 = fig_dispersion_mono.circle('ka_2', 'y_2', source=ka_source_mono_superpos, fill_color='blue', size=5)

# Legende muss seperat definiert und auf eine Variable gespeichert werden
# um die interaktive Anpassung der Sprache zu ermöglichen
legend_dispersion_mono = Legend(items=[(legend_dictionary_mono.data[language][0], [disp_mono_line_1]), (legend_dictionary_mono.data[language][1], [disp_mono_line_2]),
                                       (legend_dictionary_mono.data[language][2], [disp_mono_line_3]), (legend_dictionary_mono.data[language][3], [disp_mono_line_4])])

# Legende des Dispersionsgraphs rechts neben den DispersionsPlot hinzufügen
fig_dispersion_mono.add_layout(legend_dispersion_mono, 'right')


# Callback Funktionen der ka-Button
def mono_superpos1_ka_plus_button_callback():
    global ka_mono_superpos1
    if ka_mono_superpos1 + 2*np.pi/mass_anzahl <= 3.1:
        ka_mono_superpos1 += 2 * np.pi / mass_anzahl
    else:
        ka_mono_superpos1 = np.pi
    ka_mono_superpos1_button_label.text = "μ₁= " + str(np.round(ka_mono_superpos1, decimals=2))
    update_plot()       # ka-Punkte aktualisieren
    reset_time()


def mono_superpos1_ka_minus_button_callback():
    global ka_mono_superpos1
    if ka_mono_superpos1 - 2*np.pi/mass_anzahl > 0:
        ka_mono_superpos1 -= 2 * np.pi / mass_anzahl
    else:
        ka_mono_superpos1 = 0
    ka_mono_superpos1_button_label.text = "μ₁= " + str(np.round(ka_mono_superpos1, decimals=2))
    update_plot()       # ka-Punkte aktualisieren
    reset_time()


def mono_superpos2_ka_plus_button_callback():
    global ka_mono_superpos2
    if ka_mono_superpos2 + 2*np.pi/mass_anzahl <= 3.1:
        ka_mono_superpos2 += 2 * np.pi / mass_anzahl
    else:
        ka_mono_superpos2 = np.pi
    ka_mono_superpos2_button_label.text = "μ₂= " + str(np.round(ka_mono_superpos2, decimals=2))
    update_plot()       # ka-Punkte aktualisieren
    reset_time()


def mono_superpos2_ka_minus_button_callback():
    global ka_mono_superpos2
    if ka_mono_superpos2 - 2*np.pi/mass_anzahl > 0:
        ka_mono_superpos2 -= 2 * np.pi / mass_anzahl
    else:
        ka_mono_superpos2 = 0
    ka_mono_superpos2_button_label.text = "μ₂= " + str(np.round(ka_mono_superpos2, decimals=2))
    update_plot()       # ka-Punkte aktualisieren
    reset_time()

#Button alegen und Callback Funktionen übergeben
# Plus Button
mono_superpos1_ka_plus_button = Button(label="+", button_type="primary", width=50)
mono_superpos1_ka_plus_button.on_click(mono_superpos1_ka_plus_button_callback)

mono_superpos2_ka_plus_button = Button(label="+", button_type="primary", width=50)
mono_superpos2_ka_plus_button.on_click(mono_superpos2_ka_plus_button_callback)
# Minus Button
mono_superpos1_ka_minus_button = Button(label="-", button_type="primary", width=50)
mono_superpos1_ka_minus_button.on_click(mono_superpos1_ka_minus_button_callback)

mono_superpos2_ka_minus_button = Button(label="-", button_type="primary", width=50)
mono_superpos2_ka_minus_button.on_click(mono_superpos2_ka_minus_button_callback)


############################
# Simulation setup Superposition
############################
# Masse Feder Ketten Animation anlegen
superposition_animation = Monoatomic_chain(mass_anzahl, mass_abstand)
monoatomic_superpos_animation = figure(title=label_dictionary.data[language][2], tools="",
                                       x_range=(-2, chain_length-2), y_range=(-2, 2), width=1200, height=50, toolbar_location=None)
monoatomic_superpos_animation.title.text_font_size = "10pt"
monoatomic_superpos_animation.axis.visible = False
monoatomic_superpos_animation.grid.visible = False
# monoatomic_superpos_animation.outline_line_color = None
monoatomic_superpos_animation.toolbar.logo = None
superposition_animation.plot(monoatomic_superpos_animation)     # Kette plotten

# Transversal Darstellung plotten
x_range = np.linspace(0, chain_length, chain_length*10)
superposition_stats_conti = ColumnDataSource(dict(x_carrier=[x_range], y_carrier=[0],
                                                  x_modulation=[x_range], y_modulation=[0]))   # kont. Verlauf speichern
superposition_stats_discrete = ColumnDataSource(dict(discrete_x=[0], discrete_y=[0]))     # diskr. Auswertung speichern
superposition_stats_velocity = ColumnDataSource(dict(phase_x=[0], phase_y=[0], group_x=[0], group_y=[0])) # Geschwindigkeitsvektor speichern
# Transversal Plot anlegen
displacement_over_y = figure(title=label_dictionary.data[language][3], tools="", x_range=(0, chain_length),
                              y_range=(-0.6*mass_abstand, 0.6*mass_abstand), width=1200, height=200, toolbar_location=None)
displacement_over_y.yaxis.axis_label = label_dictionary.data[language][5]   # Label aus dem Sprach dict
displacement_over_y.xaxis.axis_label = label_dictionary.data[language][6]   # Label aus dem Sprach dict

# Plotten der einzelnen Inhalte
# Displacement
dispovery_line_1 = displacement_over_y.circle('discrete_x', 'discrete_y', source=superposition_stats_discrete)
dispovery_line_2 = displacement_over_y.line('x_carrier', 'y_carrier', source=superposition_stats_conti)
dispovery_line_3 = displacement_over_y.line('x_modulation', 'y_modulation', source=superposition_stats_conti, line_dash="dashed")

# Velocity
dispovery_line_4 = displacement_over_y.circle('phase_x', 'phase_y', source=superposition_stats_velocity, color='black')
dispovery_line_5 = displacement_over_y.circle('group_x', 'group_y', source=superposition_stats_velocity, color='red')

# Legende mithilfe des CDS dictionary definieren
legend_disp_over_y = Legend(items=[(legend_dictionary_mono.data[language][4], [dispovery_line_1]), (legend_dictionary_mono.data[language][5], [dispovery_line_2]),
                                   (legend_dictionary_mono.data[language][6], [dispovery_line_3]), (legend_dictionary_mono.data[language][7], [dispovery_line_4]),
                                   (legend_dictionary_mono.data[language][8], [dispovery_line_5])])

# Legende rechts neben den Plot hinzufügen
displacement_over_y.add_layout(legend_disp_over_y, 'right')

################################################################################
# ----------------------- Diatomic
################################################################################
# Einstellungen der Masse Feder Ketten
mass_source = ColumnDataSource(dict(m=[mass_relation]))
unitcell_number = floor(mass_anzahl/2)
unitcell_length = mass_abstand * 2

# CDS zum speichern der gewählten ka-Werte
ka_source_di_opt = ColumnDataSource(data=dict(x=[ka_di], y=[dis_rel_diatom_optical(ka_di, m_relation=mass_relation)]))
ka_source_di_acou = ColumnDataSource(data=dict(x=[ka_di], y=[dis_rel_diatom_acoustic(ka_di, m_relation=mass_relation)]))

# Instanzierung der Kette der optischen Moden
diatomic_optical_chain = Diatomic_chain(unitcell_number, unitcell_length, mass_relation)

# Instanzierung der Kette der akustischen Moden
diatomic_acoustic_chain = Diatomic_chain(unitcell_number, unitcell_length, mass_relation)

##############
# -- Plot zur Visualisierung der diatomaren Kette anlegen
##############

# Optical Plot
diatomic_optical_animation = figure(title=label_dictionary.data[language][8], tools="",
                                    x_range=(-2, chain_length-2), y_range=(-2, 2), width=1000,
                                    height=55, toolbar_location=None)
diatomic_optical_animation.title.text_font_size = "10pt"
diatomic_optical_animation.axis.visible = False
diatomic_optical_animation.grid.visible = False
# diatomic_optical_animation.outline_line_color = None
diatomic_optical_animation.toolbar.logo = None

# Acoustic Plot
diatomic_acoustic_animation = figure(title=label_dictionary.data[language][7], tools="",
                                     x_range=(-2, chain_length-2), y_range=(-2, 2), width=1000,
                                     height=55, toolbar_location=None)
diatomic_acoustic_animation.title.text_font_size = "10pt"
diatomic_acoustic_animation.axis.visible = False
diatomic_acoustic_animation.grid.visible = False
# diatomic_acoustic_animation.outline_line_color = None
diatomic_acoustic_animation.toolbar.logo = None

# Plotten der beiden Ketten
diatomic_optical_chain.plot(diatomic_optical_animation)
diatomic_acoustic_chain.plot(diatomic_acoustic_animation)

# -- Dispersionrelation Graph
# Dispersionsbeziehung auswerten
di_ka_val = np.linspace(-np.pi, np.pi, 200)
# Band Gaps
di_bandgap_box1 = BoxAnnotation(bottom=np.sqrt(2*c/mass_relation)/(np.sqrt(2*c*(1/mass_relation+1/1))),
                                top=np.sqrt(2*c/1)/ (np.sqrt(2*c*(1/mass_relation+1/1))), right=None, left=None,
                                fill_color='red', fill_alpha=0.2)
di_bandgap_box2 = BoxAnnotation(bottom=1,
                                top=None, right=None, left=None,
                                fill_color='red', fill_alpha=0.2)
# Standard erst nicht sichtabr
di_bandgap_box1.visible = False
di_bandgap_box2.visible = False

# ------------- Mass Button
mass_button_label = Paragraph(text="M₁ / M₂= " + str(mass_relation))

# CDS mit den ausgewerteten Ka-Punkte zum Plotten
diatomic_optical = ColumnDataSource(data=dict(x=di_ka_val, y=dis_rel_diatom_optical(di_ka_val, mass_relation)))
diatomic_acoustical = ColumnDataSource(data=dict(x=di_ka_val, y=dis_rel_diatom_acoustic(di_ka_val, mass_relation)))

# Button Callbacks definieren
################################
def mass_plus_button_callback():
    global mass_relation
    mass_relation += 0.1
    update_diatomic_plot()


def mass_minus_button_callback():
    global mass_relation
    if mass_relation > 1:
        mass_relation -= 0.1
    else:
        mass_relation = 1
    update_diatomic_plot()


def di_ka_plus_button_callback():
    global ka_di
    if ka_di + 2*np.pi/unitcell_number <= 3.1:
        ka_di += 2 * np.pi / unitcell_number
    else:
        ka_di = np.pi
    ka_di_button_label.text = "μ= " + str(np.round(ka_di, decimals=2))
    update_plot()
    reset_time()


def di_ka_minus_button_callback():
    global ka_di
    if ka_di - 2*np.pi/unitcell_number >= -3.1:
        ka_di -= 2 * np.pi / unitcell_number
    else:
        ka_di = - np.pi
    ka_di_button_label.text = "μ= " + str(np.round(ka_di, decimals=2))
    update_plot()
    reset_time()


def di_bandgap_button_callback():
    if not di_bandgap_box1.visible:
        di_bandgap_box1.visible = True
        di_bandgap_box2.visible = True
        di_bandgap_button.label = label_dictionary.data[language][4][1]
    else:
        di_bandgap_box1.visible = False
        di_bandgap_box2.visible = False
        di_bandgap_button.label = label_dictionary.data[language][4][0]


#Nach Auswahl einmal alle Daten in den Grafiken anpassen
def update_diatomic_plot():
    mass_button_label.text = "M₁ / M₂= " + str(np.round(mass_relation, decimals=2))
    diatomic_optical.data = dict(x=di_ka_val, y=dis_rel_diatom_optical(di_ka_val, m_relation=mass_relation))
    diatomic_acoustical.data = dict(x=di_ka_val, y=dis_rel_diatom_acoustic(di_ka_val, m_relation=mass_relation))
    ka_source_di_opt.data = dict(x=[ka_di], y=[dis_rel_diatom_optical(ka_di, m_relation=mass_relation)])
    ka_source_di_acou.data = dict(x=[ka_di], y=[dis_rel_diatom_acoustic(ka_di, m_relation=mass_relation)])
    mass_source.data = dict(m=[mass_relation])
    ka_source_di_acou_superpos.data = dict(ka_1=[ka_di_acou_superpos1], ka_2=[ka_di_acou_superpos2],
                                           y_1=[dis_rel_diatom_acoustic(ka_di_acou_superpos1, mass_relation)],
                                           y_2=[dis_rel_diatom_acoustic(ka_di_acou_superpos2, mass_relation)])
    ka_source_di_opti_superpos.data = dict(ka_1=[ka_di_opti_superpos1], ka_2=[ka_di_opti_superpos2],
                                           y_1=[dis_rel_diatom_optical(ka_di_opti_superpos1, mass_relation)],
                                           y_2=[dis_rel_diatom_optical(ka_di_opti_superpos2, mass_relation)])
    update_diatomic_chain_visuals()         # Radius der Massen muss angepasst werden


# Anpassung radius der Massen nac Massenverhältnisänderung
def update_diatomic_chain_visuals():
    diatomic_acoustic_chain.change_size_rel(mass_relation)
    diatomic_optical_chain.change_size_rel(mass_relation)
    superposition_di_acou_animation.change_size_rel(mass_relation)
    superposition_di_opti_animation.change_size_rel(mass_relation)
    di_bandgap_box1.bottom = np.sqrt(2 * c / mass_relation) / (np.sqrt(2*c*(1/mass_relation+1/1)))
    di_bandgap_box1.top = np.sqrt(2 * c / 1) / (np.sqrt(2*c*(1/mass_relation+1/1)))


####################
# Diatomic Buttons
####################
# Ka Buttons
# Plus Button
di_ka_plus_button = Button(label="+", button_type="primary", width=50)
di_ka_plus_button.on_click(di_ka_plus_button_callback)
# Minus Button
di_ka_minus_button = Button(label="-", button_type="primary", width=50)
di_ka_minus_button.on_click(di_ka_minus_button_callback)

# Mass Button
# Plus Button
mass_plus_button = Button(label="+", button_type="primary", width=50)
mass_plus_button.on_click(mass_plus_button_callback)
# Minus Button
mass_minus_button = Button(label="-", button_type="primary", width=50)
mass_minus_button.on_click(mass_minus_button_callback)

# Band Gap Buttons
di_bandgap_button = Button(label=label_dictionary.data[language][4][0], button_type='primary', width=100)
di_bandgap_button.on_click(di_bandgap_button_callback)

# Dispersionsgrafik anlegen (diatomar)
fig_dispersion_di = figure(x_range=(-np.pi, np.pi), y_range=(0, 1.2), width=1000, height=500, toolbar_location=None)
fig_dispersion_di.yaxis.axis_label ="ω / √[2c * (1/M₁ + 1/M₂)]"
fig_dispersion_di.xaxis.axis_label = "μ"

# Zweige plotten
acoustic_dispersion_line = fig_dispersion_di.line('x', 'y', source=diatomic_acoustical, line_width=2, line_color='green')
optical_dispersion_line = fig_dispersion_di.line('x', 'y', source=diatomic_optical, line_width=2, line_color='SteelBlue')
# Ka-Punkte plotten
ka_dispersion_di = fig_dispersion_di.circle('x', 'y', source=ka_source_di_opt, fill_color='red', size=5)
fig_dispersion_di.circle('x', 'y', source=ka_source_di_acou, fill_color='red', size=5)
# Band Gaps in den Plot einfügen
fig_dispersion_di.add_layout(di_bandgap_box1)
fig_dispersion_di.add_layout(di_bandgap_box2)

#######################################################
# Superposition of two diatomic Normal modes
#######################################################
# Acoustic
# ########################################################################################
# Standardwerte festlegen
ka_di_acou_superpos1 = np.pi * 0
ka_di_acou_superpos2 = np.pi * 0

# CDS zum speichern der gewählten ka-Werte
ka_source_di_acou_superpos = ColumnDataSource(data=dict(ka_1=[ka_di_acou_superpos1], ka_2=[ka_di_acou_superpos2],
                                                     y_1=[dis_rel_diatom_acoustic(ka_di_acou_superpos1, mass_relation)],
                                                     y_2=[dis_rel_diatom_acoustic(ka_di_acou_superpos2, mass_relation)]))
ka_di_acou_superpos1_button_label = \
    Paragraph(text="μ₁= " + str(np.round(ka_di_acou_superpos1, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style
ka_di_acou_superpos2_button_label = \
    Paragraph(text="μ₂= " + str(np.round(ka_di_acou_superpos2, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style

# ka-Werte in die Dispersionsbeziehung plotten
ka_1_di_acouplot = fig_dispersion_di.circle('ka_1', 'y_1', source=ka_source_di_acou_superpos, fill_color='black', size=5)
ka_2_di_acouplot = fig_dispersion_di.circle('ka_2', 'y_2', source=ka_source_di_acou_superpos, fill_color='orange', size=5)

# Button Callbacks definieren
################################

def di_acou_superpos1_ka_plus_button_callback():
    global ka_di_acou_superpos1
    if ka_di_acou_superpos1 + 2*np.pi/unitcell_number <= 3.1:
        ka_di_acou_superpos1 += 2 * np.pi / unitcell_number     # ausschließlich zulässige Werte
    else:
        ka_di_acou_superpos1 = np.pi
    ka_di_acou_superpos1_button_label.text = "μ₁= " + str(np.round(ka_di_acou_superpos1, decimals=2))
    update_plot()
    reset_time()


def di_acou_superpos1_ka_minus_button_callback():
    global ka_di_acou_superpos1
    if ka_di_acou_superpos1 - 2*np.pi/unitcell_number > 0:
        ka_di_acou_superpos1 -= 2 * np.pi / unitcell_number     # ausschließlich zulässige Werte
    else:
        ka_di_acou_superpos1 = 0
    ka_di_acou_superpos1_button_label.text = "μ₁= " + str(np.round(ka_di_acou_superpos1, decimals=2))
    update_plot()
    reset_time()


def di_acou_superpos2_ka_plus_button_callback():
    global ka_di_acou_superpos2
    if ka_di_acou_superpos2 + 2*np.pi/unitcell_number <= 3.1:
        ka_di_acou_superpos2 += 2 * np.pi / unitcell_number     # ausschließlich zulässige Werte
    else:
        ka_di_acou_superpos2 = np.pi
    ka_di_acou_superpos2_button_label.text = "μ₂= " + str(np.round(ka_di_acou_superpos2, decimals=2))
    update_plot()
    reset_time()


def di_acou_superpos2_ka_minus_button_callback():
    global ka_di_acou_superpos2
    if ka_di_acou_superpos2 - 2*np.pi/unitcell_number > 0:
        ka_di_acou_superpos2 -= 2 * np.pi / unitcell_number     # ausschließlich zulässige Werte
    else:
        ka_di_acou_superpos2 = 0
    ka_di_acou_superpos2_button_label.text = "μ₂= " + str(np.round(ka_di_acou_superpos2, decimals=2))
    update_plot()       # Plots aktualisieren
    reset_time()


# Plus Button
di_acou_superpos1_ka_plus_button = Button(label="+", button_type="primary", width=50)
di_acou_superpos1_ka_plus_button.on_click(di_acou_superpos1_ka_plus_button_callback)

di_acou_superpos2_ka_plus_button = Button(label="+", button_type="primary", width=50)
di_acou_superpos2_ka_plus_button.on_click(di_acou_superpos2_ka_plus_button_callback)

# Minus Button
di_acou_superpos1_ka_minus_button = Button(label="-", button_type="primary", width=50)
di_acou_superpos1_ka_minus_button.on_click(di_acou_superpos1_ka_minus_button_callback)

di_acou_superpos2_ka_minus_button = Button(label="-", button_type="primary", width=50)
di_acou_superpos2_ka_minus_button.on_click(di_acou_superpos2_ka_minus_button_callback)

##################
# Simulation setup Superposition Acoustic Modes
##################
superposition_di_acou_animation = Diatomic_chain(unitcell_number, unitcell_length, mass_relation)
diatomic_acou_superpos_animation = figure(title=label_dictionary.data[language][9],
                                       x_range=(-2, chain_length-2), y_range=(-2, 2), width=1200, height=55, tools="",
                                          toolbar_location=None)
diatomic_acou_superpos_animation.title.text_font_size = "10pt"
diatomic_acou_superpos_animation.axis.visible = False
diatomic_acou_superpos_animation.grid.visible = False
#diatomic_acou_superpos_animation.outline_line_color = None
diatomic_acou_superpos_animation.toolbar.logo = None
# Plot chain
superposition_di_acou_animation.plot(diatomic_acou_superpos_animation)

# Plot displacement over y of superposition
x_range = np.linspace(0, chain_length, chain_length*10)
superposition_di_acou_stats_conti = ColumnDataSource(dict(x_carrier_u_l=[x_range], y_carrier_u_l=[0],
                                                          x_carrier_v_l=[x_range], y_carrier_v_l=[0],
                                                          x_envelope=[x_range], y_envelope=[0]))
superposition_di_acou_stats_discrete = ColumnDataSource(dict(discrete_x_heavy=[0], discrete_y_heavy=[0],
                                                     discrete_x_light=[0], discrete_y_light=[0]))
superposition_di_acou_stats_velocity = ColumnDataSource(dict(phase_x=[0], phase_y=[0], group_x=[0], group_y=[0]))
displacement_over_y_di_acou = figure(title=label_dictionary.data[language][3], x_range=(0, chain_length),
                              y_range=(-1.1*mass_abstand, 1.1*mass_abstand), width=1200, height=200,tools="",
                                          toolbar_location=None)
displacement_over_y_di_acou.yaxis.axis_label = label_dictionary.data[language][5]
displacement_over_y_di_acou.xaxis.axis_label = label_dictionary.data[language][6]
dispovery_acou_line_1 = displacement_over_y_di_acou.circle('discrete_x_heavy', 'discrete_y_heavy', source=superposition_di_acou_stats_discrete,
                                                           fill_color='blue')
dispovery_acou_line_2 = displacement_over_y_di_acou.circle('discrete_x_light', 'discrete_y_light', source=superposition_di_acou_stats_discrete,
                                                           fill_color='gray')

dispovery_acou_line_3 = displacement_over_y_di_acou.line('x_carrier_u_l', 'y_carrier_u_l', source=superposition_di_acou_stats_conti,
                                                         line_color='blue')
dispovery_acou_line_4 = displacement_over_y_di_acou.line('x_carrier_v_l', 'y_carrier_v_l', source=superposition_di_acou_stats_conti,
                                                         line_color='gray')
dispovery_acou_line_5 = displacement_over_y_di_acou.line('x_envelope', 'y_envelope', source=superposition_di_acou_stats_conti, line_dash="dashed",
                                                         line_color='black')

# Velocity
dispovery_acou_line_6 = displacement_over_y_di_acou.circle('phase_x', 'phase_y', source=superposition_di_acou_stats_velocity, color='black')
dispovery_acou_line_7 = displacement_over_y_di_acou.circle('group_x', 'group_y', source=superposition_di_acou_stats_velocity, color='red')
# Legenden definieren für die Superposition der akustischen Moden
legend_disp_di_acou = Legend(items=[(legend_dictionary_di.data[language][7], [dispovery_acou_line_1]), (legend_dictionary_di.data[language][8], [dispovery_acou_line_2]),
                                    (legend_dictionary_di.data[language][9], [dispovery_acou_line_3]), (legend_dictionary_di.data[language][10], [dispovery_acou_line_4]),
                                    (legend_dictionary_di.data[language][11], [dispovery_acou_line_5]), (legend_dictionary_di.data[language][12], [dispovery_acou_line_6]),
                                    (legend_dictionary_di.data[language][13], [dispovery_acou_line_7])])
# Legende rechts neben den Plot hinzufügen
displacement_over_y_di_acou.add_layout(legend_disp_di_acou, 'right')
#####################################################################################
# Optical Superposition
######################################################################################

ka_di_opti_superpos1 = np.pi * 0
ka_di_opti_superpos2 = np.pi * 0

##########
# buttons
##########
ka_source_di_opti_superpos = ColumnDataSource(data=dict(ka_1=[ka_di_opti_superpos1], ka_2=[ka_di_opti_superpos2],
                                                     y_1=[dis_rel_diatom_optical(ka_di_opti_superpos1, mass_relation)],
                                                     y_2=[dis_rel_diatom_optical(ka_di_opti_superpos2, mass_relation)]))
ka_di_opti_superpos1_button_label = \
    Paragraph(text="μ₁= " + str(np.round(ka_di_opti_superpos1, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style
ka_di_opti_superpos2_button_label = \
    Paragraph(text="μ₂= " + str(np.round(ka_di_opti_superpos2, decimals=2)), style={'font-style': 'italic', 'font-size': '16px'})   #sc: styles --> style

ka_1_di_optiplot = fig_dispersion_di.circle('ka_1', 'y_1', source=ka_source_di_opti_superpos, fill_color='purple', size=5)
ka_2_di_optiplot = fig_dispersion_di.circle('ka_2', 'y_2', source=ka_source_di_opti_superpos, fill_color='blue', size=5)

# Legende des Dispersionsplots definieren
legend_dispersion_di = Legend(items=[(legend_dictionary_di.data[language][0], [acoustic_dispersion_line]), (legend_dictionary_di.data[language][1], [optical_dispersion_line]),
                                     (legend_dictionary_di.data[language][2], [ka_dispersion_di]), (legend_dictionary_di.data[language][3], [ka_1_di_acouplot]),
                                     (legend_dictionary_di.data[language][4], [ka_2_di_acouplot]),
                                     (legend_dictionary_di.data[language][5], [ka_1_di_optiplot]),
                                     (legend_dictionary_di.data[language][6], [ka_2_di_optiplot])])

# Legende rechts neben den Plot hinzufügen
fig_dispersion_di.add_layout(legend_dispersion_di, 'right')


def di_opti_superpos1_ka_plus_button_callback():
    global ka_di_opti_superpos1
    if ka_di_opti_superpos1 + 2*np.pi/unitcell_number <= 3.1:
        ka_di_opti_superpos1 += 2 * np.pi / unitcell_number
    else:
        ka_di_opti_superpos1 = np.pi
    ka_di_opti_superpos1_button_label.text = "μ₁= " + str(np.round(ka_di_opti_superpos1, decimals=2))
    update_plot()
    reset_time()


def di_opti_superpos1_ka_minus_button_callback():
    global ka_di_opti_superpos1
    if ka_di_opti_superpos1 - 2*np.pi/unitcell_number > 0:
        ka_di_opti_superpos1 -= 2 * np.pi / unitcell_number
    else:
        ka_di_opti_superpos1 = 0
    ka_di_opti_superpos1_button_label.text = "μ₁= " + str(np.round(ka_di_opti_superpos1, decimals=2))
    update_plot()
    reset_time()


def di_opti_superpos2_ka_plus_button_callback():
    global ka_di_opti_superpos2
    if ka_di_opti_superpos2 + 2*np.pi/unitcell_number <= 3.1:
        ka_di_opti_superpos2 += 2 * np.pi / unitcell_number
    else:
        ka_di_opti_superpos2 = np.pi
    ka_di_opti_superpos2_button_label.text = "μ₂= " + str(np.round(ka_di_opti_superpos2, decimals=2))
    update_plot()
    reset_time()


def di_opti_superpos2_ka_minus_button_callback():
    global ka_di_opti_superpos2
    if ka_di_opti_superpos2 - 2*np.pi/unitcell_number > 0:
        ka_di_opti_superpos2 -= 2 * np.pi / unitcell_number
    else:
        ka_di_opti_superpos2 =0
    ka_di_opti_superpos2_button_label.text = "μ₂= " + str(np.round(ka_di_opti_superpos2, decimals=2))
    update_plot()
    reset_time()


# Plus Button
di_opti_superpos1_ka_plus_button = Button(label="+", button_type="primary", width=50)
di_opti_superpos1_ka_plus_button.on_click(di_opti_superpos1_ka_plus_button_callback)

di_opti_superpos2_ka_plus_button = Button(label="+", button_type="primary", width=50)
di_opti_superpos2_ka_plus_button.on_click(di_opti_superpos2_ka_plus_button_callback)
# Minus Button
di_opti_superpos1_ka_minus_button = Button(label="-", button_type="primary", width=50)
di_opti_superpos1_ka_minus_button.on_click(di_opti_superpos1_ka_minus_button_callback)

di_opti_superpos2_ka_minus_button = Button(label="-", button_type="primary", width=50)
di_opti_superpos2_ka_minus_button.on_click(di_opti_superpos2_ka_minus_button_callback)

##################
# Simulation setup Superposition Optical Modes
##################
# Masse Feder Ketten Animation anlegen
superposition_di_opti_animation = Diatomic_chain(unitcell_number, unitcell_length, mass_relation)
diatomic_opti_superpos_animation = figure(title=label_dictionary.data[language][10],
                                       x_range=(-2, chain_length-2), y_range=(-2, 2), width=1200, height=55, tools="",
                                          toolbar_location=None)
diatomic_opti_superpos_animation.title.text_font_size = "10pt"
diatomic_opti_superpos_animation.axis.visible = False
diatomic_opti_superpos_animation.grid.visible = False
# diatomic_opti_superpos_animation.outline_line_color = None
diatomic_opti_superpos_animation.toolbar.logo = None
superposition_di_opti_animation.plot(diatomic_opti_superpos_animation)      # Plotten

# Transversal Darstellung plotten
x_range = np.linspace(0, chain_length, chain_length*10)
# CDS mit allen wichtigen Infos über Geschwindigkeit, Hüllkurve und Carrierwelle
superposition_di_opti_stats_conti = ColumnDataSource(dict(x_carrier_u_l=[x_range], y_carrier_u_l=[0],
                                                          x_carrier_v_l=[x_range], y_carrier_v_l=[0],
                                                          x_envelope=[x_range], y_envelope=[0]))
superposition_di_opti_stats_discrete = ColumnDataSource(dict(discrete_x_heavy=[0], discrete_y_heavy=[0],
                                                     discrete_x_light=[0], discrete_y_light=[0]))
superposition_di_opti_stats_velocity = ColumnDataSource(dict(phase_x=[0], phase_y=[0], group_x=[0], group_y=[0]))
displacement_over_y_di_opti = figure(title=label_dictionary.data[language][3], x_range=(0, 120),
                              y_range=(-1.1*mass_abstand, 1.1*mass_abstand), width=1200, height=200, tools="",
                                          toolbar_location=None)
displacement_over_y_di_opti.yaxis.axis_label = label_dictionary.data[language][5]       # Label aus Sprachen dict
displacement_over_y_di_opti.xaxis.axis_label = label_dictionary.data[language][6]        # Label aus Sprachen dict

# Transversale Darstellungen plotten
# Diskrete Massepunkte
dispovery_opti_line_1 = displacement_over_y_di_opti.circle('discrete_x_heavy', 'discrete_y_heavy', source=superposition_di_opti_stats_discrete,
                           fill_color='blue')
dispovery_opti_line_2 = displacement_over_y_di_opti.circle('discrete_x_light', 'discrete_y_light', source=superposition_di_opti_stats_discrete,
                        fill_color='gray')
# Carrier-wellen
dispovery_opti_line_3 = displacement_over_y_di_opti.line('x_carrier_u_l', 'y_carrier_u_l', source=superposition_di_opti_stats_conti,
                                 line_color='blue')
dispovery_opti_line_4 = displacement_over_y_di_opti.line('x_carrier_v_l', 'y_carrier_v_l', source=superposition_di_opti_stats_conti,
                                 line_color='gray')
# Hüllkurve
dispovery_opti_line_5 = displacement_over_y_di_opti.line('x_envelope', 'y_envelope', source=superposition_di_opti_stats_conti, line_dash="dashed",
                         line_color='black')

# Velocity
dispovery_opti_line_6 = displacement_over_y_di_opti.circle('phase_x', 'phase_y', source=superposition_di_opti_stats_velocity, color='black')
dispovery_opti_line_7 = displacement_over_y_di_opti.circle('group_x', 'group_y', source=superposition_di_opti_stats_velocity, color='red')

# Legenden definieren für die Superposition der optischen Moden
legend_disp_di_opti = Legend(items=[(legend_dictionary_di.data[language][7], [dispovery_opti_line_1]), (legend_dictionary_di.data[language][8], [dispovery_opti_line_2]),
                                    (legend_dictionary_di.data[language][9], [dispovery_opti_line_3]), (legend_dictionary_di.data[language][10], [dispovery_opti_line_4]),
                                    (legend_dictionary_di.data[language][11], [dispovery_opti_line_5]), (legend_dictionary_di.data[language][12], [dispovery_opti_line_6]),
                                    (legend_dictionary_di.data[language][13], [dispovery_opti_line_7])])
# Legende rechts neben den Plot hinzufügen
displacement_over_y_di_opti.add_layout(legend_disp_di_opti, 'right')

######################################################################################################
# ------------------------------------- Simulation Mass Chains ---------------------------------------
######################################################################################################
# Alle simulations Funktionen die mit den Playbutton verknüpft werden

def simulate_diatomic():          # Funktion ruft die beiden einzelnen Simulationsfunktioonen auf
    global timer_1
    simulate_diatomic_optical()
    simulate_diatomic_acoustical()
    global_timer.text = "Timer [s]:" + str(np.round(timer_1, decimals=2))
    if timer_1 >= 60:
        play_pause_diatomic()
    else:
        timer_1 += time_steps


# --------------- Monoatomic Simulation
def simulate_monoatomic():
    global timer_1       # mit global auf Werte ausserhalb der Funktion zugreifen
    # Berechnung der Displacements
    monoatomic_chain.calculate_monoatomic_dynamics(timer_1, ka_mono, mass_mono)
    # Anpassung des Timers
    global_timer.text = "Timer [s]:" + str(np.round(timer_1, decimals=2))
    # Nach 60s die Animation automatisch stoppen ansonsten Timer=+timestep
    if timer_1 >= 60:
        play_pause_mono()
        reset_time()
    else:
        timer_1 += time_steps




# ------------------ Optical Simulation
def simulate_diatomic_optical():
    global timer_1, ka_di
    diatomic_optical_chain.calculate_diatomic_optical_dynamics(timer_1, ka_di, mass_source.data['m'][0])


# ------------------ Acoustic Simulation
def simulate_diatomic_acoustical():
    global timer_1, ka_di
    diatomic_acoustic_chain.calculate_diatomic_acoustic_dynamics(timer_1, ka_di, mass_source.data['m'][0])


# ------------- Superposition Animations
def simulate_monoatomic_superposition_animation():
    global ka_mono_superpos1, ka_mono_superpos2, timer_2, x_range
    x, y, y_group_disp, y_envelope_disp, v_phase_xpos, v_phase_ypos, v_group = \
        superposition_animation.superposition_two_monoatomic_normalmodes(timer_2, ka_mono_superpos1, ka_mono_superpos2,
                                                                         x_range)
    superposition_stats_conti.data = dict(x_carrier=x_range, y_carrier=y_group_disp,
                                          x_modulation=x_range, y_modulation=y_envelope_disp)
    superposition_stats_discrete.data = dict(discrete_x=x, discrete_y=y)
    superposition_stats_velocity.data = dict(phase_x=[v_phase_xpos], phase_y=[v_phase_ypos], group_x=[v_group],
                                             group_y=[2*0.25*mass_abstand])
    global_timer_superpos.text = "Timer [s]:" + str(np.round(timer_2, decimals=2))
    if timer_2 >= 60:
        play_pause_mono_superpos()
        reset_time()
    else:
        timer_2 += time_steps


def simulate_diatomic_acou_superposition_animation():
    global ka_di_acou_superpos1, ka_di_acou_superpos2, timer_2, x_range
    x_heavy, y_heavy, x_light, y_light, y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp,  v_phase_xpos,\
    v_phase_ypos, v_group = superposition_di_acou_animation.superposition_two_acoustic_normalmodes(
        timer_2, ka_di_acou_superpos1, ka_di_acou_superpos2, mass_relation, c, x_range)
    superposition_di_acou_stats_conti.data = dict(x_carrier_u_l=x_range, y_carrier_u_l=y_carrier_disp_u_l,
                                                          x_carrier_v_l=x_range, y_carrier_v_l=y_carrier_disp_v_l,
                                                  x_envelope=x_range, y_envelope=y_envelope_disp)
    superposition_di_acou_stats_discrete.data = dict(discrete_x_heavy=x_heavy, discrete_y_heavy=y_heavy,
                                                     discrete_x_light=x_light, discrete_y_light=y_light)
    superposition_di_acou_stats_velocity.data = dict(phase_x=[v_phase_xpos], phase_y=[v_phase_ypos], group_x=[v_group],
                                             group_y=[2])
    global_timer_superpos.text = "Timer [s]:" + str(np.round(timer_2, decimals=2))

    timer_2 += time_steps


def simulate_diatomic_opti_superposition_animation():
    global ka_di_opti_superpos1, ka_di_opti_superpos2, timer_2, x_range
    x_heavy, y_heavy, x_light, y_light, y_carrier_disp_v_l, y_carrier_disp_u_l, y_envelope_disp,  v_phase_xpos,\
    v_phase_ypos, v_group, v_group_y_pos = superposition_di_opti_animation.superposition_two_optical_normalmodes(
        timer_2, ka_di_opti_superpos1, ka_di_opti_superpos2, mass_relation, c, x_range)
    superposition_di_opti_stats_conti.data = dict(x_carrier_u_l=x_range, y_carrier_u_l=y_carrier_disp_u_l,
                                                          x_carrier_v_l=x_range, y_carrier_v_l=y_carrier_disp_v_l,
                                                  x_envelope=x_range, y_envelope=y_envelope_disp)
    superposition_di_opti_stats_discrete.data = dict(discrete_x_heavy=x_heavy, discrete_y_heavy=y_heavy,
                                                     discrete_x_light=x_light, discrete_y_light=y_light)
    superposition_di_opti_stats_velocity.data = dict(phase_x=[v_phase_xpos], phase_y=[v_phase_ypos], group_x=[v_group],
                                             group_y=[v_group_y_pos])
    global_timer_superpos.text = "Timer [s]:" + str(np.round(timer_2, decimals=2))

    timer_2 += time_steps

###########################################################################################################
# ------------------------------------- Play Pause Button -------------------------------------------------
###########################################################################################################


# ------------ Superposition Monoatomic
# Anlegen des Standards 'Status' für den Play Button
default_active_mono_superpos = ColumnDataSource(data=dict(Active=[False]))
# ID des periodic-callbacks abspeichern -- wichtig zum entfernen des Callbacks
callback_id_mono_superpos = dict(id=None)


def play_pause_mono_superpos():
    global default_active_mono_superpos, callback_id_mono_superpos

    default_active_mono_superpos.data['Active'][0] = not default_active_mono_superpos.data['Active'][0]
    status = default_active_mono_superpos.data['Active'][0]

    if status:
        callback_id_mono_superpos['id'] = curdoc().add_periodic_callback(simulate_monoatomic_superposition_animation,100)
        playbutton_mono_superpos.label = label_playbutton_dictionary.data[language][0][1]

    else:
        curdoc().remove_periodic_callback(callback_id_mono_superpos['id'])
        playbutton_mono_superpos.label = label_playbutton_dictionary.data[language][0][0]


playbutton_mono_superpos = Button(label=label_playbutton_dictionary.data[language][0][0], button_type='primary', width=150)
playbutton_mono_superpos.on_click(play_pause_mono_superpos)

# ------------ Monoatomic
# Anlegen des Standards 'Status' des Play Button
default_active_mono = ColumnDataSource(data=dict(Active=[False]))
# ID des periodic-callbacks abspeichern -- wichtig zum entfernen des Callbacks
callback_id_mono = dict(id=None)


def play_pause_mono():
    global default_active_mono, callback_id_mono    # mit global auf Werte ausserhalb der Funktion zugreifen
    # Status des Play-Button anpassen mit der booleschen Operation 'not'
    default_active_mono.data['Active'][0] = not default_active_mono.data['Active'][0]
    status = default_active_mono.data['Active'][0]

    # je nach Status einen Callback hinzufügen oder entfernen
    if status:
        # periodischer Callback, der alle 100ms die Funktion zur Berechnung der Verschiebung auswertet
        callback_id_mono['id'] = curdoc().add_periodic_callback(simulate_monoatomic, 100)
        playbutton_mono.label = label_playbutton_dictionary.data[language][1][1]
    else:
        curdoc().remove_periodic_callback(callback_id_mono['id'])
        playbutton_mono.label = label_playbutton_dictionary.data[language][1][0]


# Play Button erstellen
playbutton_mono = Button(label=label_playbutton_dictionary.data[language][1][0], button_type='primary', width=150)
playbutton_mono.on_click(play_pause_mono)       # zum Funktionsaufruf die Play-Funktion übergeben


# ------------ Superposition Acoustic Diatomic
# Anlegen des Standards 'Status' für den Play Button
default_active_di_acou_superpos = ColumnDataSource(data=dict(Active=[False]))
# ID des periodic-callbacks abspeichern -- wichtig zum entfernen des Callbacks
callback_id_di_acou_superpos = dict(id=None)


def play_pause_di_acou_superpos():
    global default_active_di_acou_superpos, callback_id_di_acou_superpos

    default_active_di_acou_superpos.data['Active'][0] = not default_active_di_acou_superpos.data['Active'][0]
    status = default_active_di_acou_superpos.data['Active'][0]

    if status:
        callback_id_di_acou_superpos['id'] = curdoc().add_periodic_callback(simulate_diatomic_acou_superposition_animation,100)
        playbutton_di_acou_superpos.label = label_playbutton_dictionary.data[language][3][1]
        playbutton_di_opti_superpos.disabled = True
        playbutton_diatomic.disabled = True


    else:
        curdoc().remove_periodic_callback(callback_id_di_acou_superpos['id'])
        playbutton_di_acou_superpos.label = label_playbutton_dictionary.data[language][3][0]
        playbutton_di_opti_superpos.disabled = False
        playbutton_diatomic.disabled = False


playbutton_di_acou_superpos = Button(label=label_playbutton_dictionary.data[language][3][0], button_type='primary')
playbutton_di_acou_superpos.on_click(play_pause_di_acou_superpos)


# ------------ Superposition Acoustic Diatomic
# Anlegen des Standards 'Status' für den Play Button
default_active_di_opti_superpos = ColumnDataSource(data=dict(Active=[False]))
callback_id_di_opti_superpos = dict(id=None)


def play_pause_di_opti_superpos():
    global default_active_di_opti_superpos, callback_id_di_opti_superpos

    default_active_di_opti_superpos.data['Active'][0] = not default_active_di_opti_superpos.data['Active'][0]
    status = default_active_di_opti_superpos.data['Active'][0]

    if status:
        callback_id_di_opti_superpos['id'] = curdoc().add_periodic_callback(simulate_diatomic_opti_superposition_animation, 100)
        playbutton_di_opti_superpos.label = label_playbutton_dictionary.data[language][4][1]
        playbutton_di_acou_superpos.disabled = True
        playbutton_diatomic.disabled = True

    else:
        curdoc().remove_periodic_callback(callback_id_di_opti_superpos['id'])
        playbutton_di_opti_superpos.label = label_playbutton_dictionary.data[language][4][0]
        playbutton_di_acou_superpos.disabled = False
        playbutton_diatomic.disabled = False


playbutton_di_opti_superpos = Button(label=label_playbutton_dictionary.data[language][4][0], button_type='primary')
playbutton_di_opti_superpos.on_click(play_pause_di_opti_superpos)



# ---------- Diatomic Chain
# Anlegen des Standards 'Status' für den Play Button
default_active_diatomic = ColumnDataSource(data=dict(Active=[False]))
callback_id_diatomic = dict(id=None)


def play_pause_diatomic():
    global timer_1
    # '= not' invertiert den aktuell hinterlegten Booleschen Wert
    default_active_diatomic.data['Active'][0] = not default_active_diatomic.data['Active'][0]
    status = default_active_diatomic.data['Active'][0]

    if status:
        callback_id_diatomic['id'] = curdoc().add_periodic_callback(simulate_diatomic, 100)
        playbutton_diatomic.label = label_playbutton_dictionary.data[language][2][1]
        playbutton_di_opti_superpos.disabled = True
        playbutton_di_acou_superpos.disabled = True

    else:
        curdoc().remove_periodic_callback(callback_id_diatomic['id'])
        playbutton_diatomic.label = label_playbutton_dictionary.data[language][2][0]
        playbutton_di_opti_superpos.disabled = False
        playbutton_di_acou_superpos.disabled = False


playbutton_diatomic = Button(label=label_playbutton_dictionary.data[language][2][0], button_type='primary',width=150)
playbutton_diatomic.on_click(play_pause_diatomic)
#
#
#
#


# ------------------------------------------------- HTML Texte -------------------------------------------
##################
# Sprache wechseln
##################
# Anlegen der Variablen für die Übergabe der HTML Texte aus der change content() funktion
######################################
# Monoatomic Divs vordefinieren
######################################
general_app_infos = LatexDiv(render_as_text=False, width=1000, height=270)
general_monoatomic_infos = LatexDiv(render_as_text=False, width=1000, height=630)
monoatomic_animation_info = LatexDiv(render_as_text=False, width=1000, height=450)
mono_superposition_info = LatexDiv(render_as_text=False, width=1000, height=660)
superposition_explained = LatexDiv(render_as_text=False, width=1000, height=100)

######################################
# Diatomic Divs vordefinieren
######################################
general_app_infos_diatomic = LatexDiv(render_as_text=False, width=1000, height=400)
general_diatomic_infos = LatexDiv(render_as_text=False, width=1000, height=1000)
diatomic_animation_info = LatexDiv(render_as_text=False, width=1000, height=810)
di_superposition_info = LatexDiv(render_as_text=False, width=1000, height=720)
di_superposition_acou_explained = LatexDiv(render_as_text=False, width=1000, height=150)
di_superposition_opti_explained = LatexDiv(render_as_text=False, width=1000, height=150)


# Callback Funktion zum change language Button
def change_language():
    global language             # global Variable zur Änderung der zu Beginn angelegten Variable 'language'
    if language == 'deutsch':
        language = 'english'
        language_button.label = 'Zu deutsch wechseln'
    elif language == 'english':
        language = 'deutsch'
        language_button.label = 'Switch to english'
    # Aufruf zum ändern der Inhalte
    change_content()        # HTML
    update_labels()         # Label
    update_graphics()       # Bilder


# Alle Labels in der Sprache anpassen
def update_labels():
    global legend_dispersion_mono
    # PlayButton
    print(f"undate labels wurde aufgerufen")
    playbutton_mono_superpos.label = label_playbutton_dictionary.data[language][0][0]
    playbutton_mono.label = label_playbutton_dictionary.data[language][1][0]
    playbutton_diatomic.label = label_playbutton_dictionary.data[language][2][0]
    playbutton_di_acou_superpos.label = label_playbutton_dictionary.data[language][3][0]
    playbutton_di_opti_superpos.label = label_playbutton_dictionary.data[language][4][0]

    # Bandgap Button
    mono_bandgap_button.label = label_dictionary.data[language][0][0]
    di_bandgap_button.label = label_dictionary.data[language][4][0]

    # Plot Titles aktualisieren mit der .title.text Methode
    # Monoatomic
    monoatomic_animation.title.text = label_dictionary.data[language][1]
    monoatomic_superpos_animation.title.text = label_dictionary.data[language][2]
    displacement_over_y.title.text = label_dictionary.data[language][3]
    # Diatomic
    diatomic_acoustic_animation.title.text = label_dictionary.data[language][7]
    diatomic_optical_animation.title.text = label_dictionary.data[language][8]
    diatomic_acou_superpos_animation.title.text = label_dictionary.data[language][9]
    diatomic_opti_superpos_animation.title.text = label_dictionary.data[language][10]
    displacement_over_y_di_acou.title.text = label_dictionary.data[language][3]
    displacement_over_y_di_opti.title.text = label_dictionary.data[language][3]

    # Axis Label
    # Monoatomic
    displacement_over_y.yaxis.axis_label = label_dictionary.data[language][5]
    displacement_over_y.xaxis.axis_label = label_dictionary.data[language][6]
    # Diatomic
    displacement_over_y_di_acou.yaxis.axis_label = label_dictionary.data[language][5]
    displacement_over_y_di_acou.xaxis.axis_label = label_dictionary.data[language][6]
    displacement_over_y_di_opti.yaxis.axis_label = label_dictionary.data[language][5]
    displacement_over_y_di_opti.xaxis.axis_label = label_dictionary.data[language][6]

    # Legend_label
    legend_dispersion_mono.items = [(legend_dictionary_mono.data[language][0], [disp_mono_line_1]), (legend_dictionary_mono.data[language][1], [disp_mono_line_2]),
                                    (legend_dictionary_mono.data[language][2], [disp_mono_line_3]), (legend_dictionary_mono.data[language][3], [disp_mono_line_4])]
    legend_disp_over_y.items = [(legend_dictionary_mono.data[language][4], [dispovery_line_1]), (legend_dictionary_mono.data[language][5], [dispovery_line_2]),
                                (legend_dictionary_mono.data[language][6], [dispovery_line_3]), (legend_dictionary_mono.data[language][7], [dispovery_line_4]),
                                (legend_dictionary_mono.data[language][8], [dispovery_line_5])]
    legend_dispersion_di.items = [(legend_dictionary_di.data[language][0], [acoustic_dispersion_line]), (legend_dictionary_di.data[language][1], [optical_dispersion_line]),
                                  (legend_dictionary_di.data[language][2], [ka_dispersion_di]), (legend_dictionary_di.data[language][3], [ka_1_di_acouplot]),
                                  (legend_dictionary_di.data[language][4], [ka_2_di_acouplot]),
                                  (legend_dictionary_di.data[language][5], [ka_1_di_optiplot]),
                                  (legend_dictionary_di.data[language][6], [ka_2_di_optiplot])]
    legend_disp_di_acou.items = [(legend_dictionary_di.data[language][7], [dispovery_acou_line_1]), (legend_dictionary_di.data[language][8], [dispovery_acou_line_2]),
                                 (legend_dictionary_di.data[language][9], [dispovery_acou_line_3]), (legend_dictionary_di.data[language][10], [dispovery_acou_line_4]),
                                 (legend_dictionary_di.data[language][11], [dispovery_acou_line_5]), (legend_dictionary_di.data[language][12], [dispovery_acou_line_6]),
                                 (legend_dictionary_di.data[language][13], [dispovery_acou_line_7])]
    legend_disp_di_opti.items = [(legend_dictionary_di.data[language][7], [dispovery_opti_line_1]), (legend_dictionary_di.data[language][8], [dispovery_opti_line_2]),
                                    (legend_dictionary_di.data[language][9], [dispovery_opti_line_3]), (legend_dictionary_di.data[language][10], [dispovery_opti_line_4]),
                                    (legend_dictionary_di.data[language][11], [dispovery_opti_line_5]), (legend_dictionary_di.data[language][12], [dispovery_opti_line_6]),
                                    (legend_dictionary_di.data[language][13], [dispovery_opti_line_7])]


def change_content():
    global general_app_infos, general_monoatomic_infos, monoatomic_animation_info, mono_superposition_info, superposition_explained,\
        general_diatomic_infos, diatomic_animation_info, di_superposition_info, di_superposition_acou_explained,\
        di_superposition_opti_explained

    if language == 'deutsch':
        print(f"if language deutsch wurde aufgerufen; Changing language to: {language}")
        # # Monoatomare HTMLs einlesen und die Texte auf einer Variable ablegen
        # with open(app_base_path / r"static\Html\monoatomic\deutsch\mono_beschreibung.html", 'r') as file:   #sc: pfade angepasst bis zeile 1237
            # mono_html_content1 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\deutsch\ÜberschriftIntro.html", 'r') as file:
            # mono_html_content11 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\deutsch\monoatomareAnimationsbeschreibung.html", 'r') as file:
            # mono_html_content2 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\deutsch\superposition_beschreibung.html", 'r') as file:
            # mono_html_content3 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\deutsch\superposition_erklärung.html", 'r') as file:
            # mono_html_content4 = file.read()
            
        mono_html_content1_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"deutsch"/"mono_beschreibung.html")
        mono_html_content1 = LatexDiv(text=open(mono_html_content1_filename).read(), render_as_text=False, width=1000)
        mono_html_content11_filenamed= str(app_base_path / "static"/"Html"/"monoatomic"/"deutsch"/"ÜberschriftIntro.html")
        mono_html_content11 = LatexDiv(text=open(mono_html_content11_filenamed).read(), render_as_text=False, width=1000)
        mono_html_content2_filenamed= str(app_base_path / "static"/"Html"/"monoatomic"/"deutsch"/"monoatomareAnimationsbeschreibung.html")
        mono_html_content2 = LatexDiv(text=open(mono_html_content2_filenamed).read(), render_as_text=False, width=1000)
        mono_html_content3_filenamed= str(app_base_path / "static"/"Html"/"monoatomic"/"deutsch"/"superposition_beschreibung.html")
        mono_html_content3 = LatexDiv(text=open(mono_html_content3_filenamed).read(), render_as_text=False, width=1000)
        mono_html_content4_filenamed= str(app_base_path / "static"/"Html"/"monoatomic"/"deutsch"/"superposition_erklärung.html")
        mono_html_content4 = LatexDiv(text=open(mono_html_content4_filenamed).read(), render_as_text=False, width=1000)
        
        # Diatomare HTMLs
        '''
        'with open(app_base_path / r"static\Html\diatomic\deutsch\diatomar_beschreibung.html", 'r') as file:
            di_html_content1 = file.read()
        with open(app_base_path / r"static\Html\diatomic\deutsch\diatomareAnimationbeschreibung.html", 'r') as file:
            di_html_content2 = file.read()
        with open(app_base_path / r"static\Html\diatomic\deutsch\di_superposition_beschreibung.html", 'r') as file:
            di_html_content3 = file.read()
        with open(app_base_path / r"static\Html\diatomic\deutsch\di_superposition_acou_erklärung.html", 'r') as file:
            di_html_content4 = file.read()
        with open(app_base_path / r"static\Html\diatomic\deutsch\di_superposition_opti_erklärung.html", 'r') as file:
            di_html_content5 = file.read()
        with open(app_base_path / r"static\Html\diatomic\deutsch\ÜberschriftIntro.html", 'r') as file: 
            di_html_content11 = file.read()
        '''

        di_html_content1_filename = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "diatomar_beschreibung.html")
        di_html_content1 = LatexDiv(text=open(di_html_content1_filename).read(), render_as_text=False, width=1000)
        di_html_content11_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "ÜberschriftIntro.html")
        di_html_content11 = LatexDiv(text=open(di_html_content11_filenamed).read(), render_as_text=False,
                                       width=1000)
        di_html_content2_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "diatomareAnimationbeschreibung.html")
        di_html_content2 = LatexDiv(text=open(di_html_content2_filenamed).read(), render_as_text=False, width=1000)
        di_html_content3_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "di_superposition_beschreibung.html")
        di_html_content3 = LatexDiv(text=open(di_html_content3_filenamed).read(), render_as_text=False, width=1000)
        di_html_content4_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "di_superposition_acou_erklärung.html")
        di_html_content4 = LatexDiv(text=open(di_html_content4_filenamed).read(), render_as_text=False, width=1000)
        di_html_content5_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "deutsch" / "di_superposition_opti_erklärung.html")
        di_html_content5 = LatexDiv(text=open(di_html_content5_filenamed).read(), render_as_text=False, width=1000)

    elif language == 'english':
        # Monoatomic HTMLs
        mono_html_content1_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"english"/"mono_beschreibung.html")
        mono_html_content1 = LatexDiv(text=open(mono_html_content1_filename).read(), render_as_text=False, width=1000)
        mono_html_content11_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"english"/"ÜberschriftIntro.html")
        mono_html_content11 = LatexDiv(text=open(mono_html_content11_filename).read(), render_as_text=False, width=1000)
        mono_html_content2_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"english"/"monoatomareAnimationsbeschreibung.html")
        mono_html_content2 = LatexDiv(text=open(mono_html_content2_filename).read(), render_as_text=False, width=1000)
        mono_html_content3_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"english"/"superposition_beschreibung.html")
        mono_html_content3 = LatexDiv(text=open(mono_html_content3_filename).read(), render_as_text=False, width=1000)
        mono_html_content4_filename= str(app_base_path / "static"/"Html"/"monoatomic"/"english"/"superposition_erklärung.html")
        mono_html_content4 = LatexDiv(text=open(mono_html_content4_filename).read(), render_as_text=False, width=1000)
        #with open(app_base_path / r"static\Html\monoatomic\english\mono_beschreibung.html", 'r') as file:
        # with open(app_base_path / "description.html", 'r') as file:
            # mono_html_content1_raw = file.read()
            # mono_html_content1 = LatexDiv(mono_html_content1_raw, render_as_text=False, width=1000)
        # with open(app_base_path / r"static\Html\monoatomic\english\ÜberschriftIntro.html", 'r') as file:
            # mono_html_content11 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\english\monoatomareAnimationsbeschreibung.html", 'r') as file:
            # mono_html_content2 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\english\superposition_beschreibung.html", 'r') as file:
            # mono_html_content3 = file.read()
        # with open(app_base_path / r"static\Html\monoatomic\english\superposition_erklärung.html", 'r') as file:
            # mono_html_content4 = file.read()
            
        # Diatomic HTMLs
        #with open(app_base_path / r"static\Html\diatomic\english\diatomar_beschreibung.html", 'r') as file:
        #    di_html_content1 = file.read()
        #with open(app_base_path / r"static\Html\diatomic\english\diatomareAnimationbeschreibung.html", 'r') as file:
        #    di_html_content2 = file.read()
        #with open(app_base_path / r"static\Html\diatomic\english\di_superposition_beschreibung.html", 'r') as file:
        #    di_html_content3 = file.read()
        #with open(app_base_path / r"static\Html\diatomic\english\di_superposition_acou_erklärung.html", 'r') as file:
        #    di_html_content4 = file.read()
        #with open(app_base_path / r"static\Html\diatomic\english\di_superposition_opti_erklärung.html", 'r') as file:
        #    di_html_content5 = file.read()
        #with open(app_base_path / r"static\Html\diatomic\english\ÜberschriftIntro.html", 'r') as file:
        #    di_html_content11 = file.read()

        di_html_content1_filename = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "diatomar_beschreibung.html")
        di_html_content1 = LatexDiv(text=open(di_html_content1_filename).read(), render_as_text=False, width=1000)
        di_html_content11_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "ÜberschriftIntro.html")
        di_html_content11 = LatexDiv(text=open(di_html_content11_filenamed).read(), render_as_text=False,
                                     width=1000)
        di_html_content2_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "diatomareAnimationbeschreibung.html")
        di_html_content2 = LatexDiv(text=open(di_html_content2_filenamed).read(), render_as_text=False, width=1000)
        di_html_content3_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "di_superposition_beschreibung.html")
        di_html_content3 = LatexDiv(text=open(di_html_content3_filenamed).read(), render_as_text=False, width=1000)
        di_html_content4_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "di_superposition_acou_erklärung.html")
        di_html_content4 = LatexDiv(text=open(di_html_content4_filenamed).read(), render_as_text=False, width=1000)
        di_html_content5_filenamed = str(
            app_base_path / "static" / "Html" / "diatomic" / "english" / "di_superposition_opti_erklärung.html")
        di_html_content5 = LatexDiv(text=open(di_html_content5_filenamed).read(), render_as_text=False, width=1000)

    # Aktualisiere die Inhalte der Div-Widgets
    # Monoatomic
    # general_app_infos.text = mono_html_content11
    # general_monoatomic_infos.text = mono_html_content1
    # monoatomic_animation_info.text = mono_html_content2
    # mono_superposition_info.text = mono_html_content3
    # superposition_explained.text = mono_html_content4
    general_app_infos.text = mono_html_content11.text
    #print("Inhalt von mono_html_content11:")
    #print(mono_html_content11.text)
    #print(f"general_app_infos: {column(general_app_infos)}")
    general_monoatomic_infos.text = mono_html_content1.text
    monoatomic_animation_info.text = mono_html_content2.text
    mono_superposition_info.text = mono_html_content3.text
    superposition_explained.text = mono_html_content4.text
    # Diatomic
    general_app_infos_diatomic.text = di_html_content11.text
    general_diatomic_infos.text = di_html_content1.text
    diatomic_animation_info.text = di_html_content2.text
    di_superposition_info.text = di_html_content3.text
    di_superposition_acou_explained.text = di_html_content4.text
    di_superposition_opti_explained.text = di_html_content5.text


# Button zum Sprachen wechseln festlegen
language_button = Button(label="Zu deutsch wechseln", button_type="success", width=200)
language_button.on_click(change_language)

# Standard Sprach-Einstellung laden
change_content()

#################################################
# Static graphics laden
#################################################
# URLs anlegen die zum Static Ordner führen
monoatomicpictureSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"MonoatomareKette.png")]))
diatomicpictureSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"DiatomareKette.png")]))
monoatomiceinheitszelleSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"monoatomicEinheitszelle.png")]))
diatomiceinheitszelleSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"diatomicEinheitszelle.png")]))

monoatomicunitcellSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"monoatomicunitcell.png")]))
diatomicunitcellSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"diatomicunitcell.png")]))


#####################
# Monoatomic Statics
#####################
# ############# PLOT 1: MonoatomicChain ##########################
# Anlegen des Plots
monoatomicPNG = figure(
                       width=800,
                       height=int(800/6.52),
                       x_range = (0, 1004),
                       y_range= ( 0,154) ,
                       tools = ''
                  )
# Alles deaktivieren was ein Plotformat erkennen lassen würde
monoatomicPNG.axis.major_tick_line_color = None
monoatomicPNG.axis.major_label_text_color = None
monoatomicPNG.axis.minor_tick_line_color = None
monoatomicPNG.axis.axis_line_color = None
monoatomicPNG.grid.visible = False
monoatomicPNG.toolbar.logo = None
monoatomicPNG.outline_line_color = None

# Bild als Glyph dem Plot hinzufügen (mit dem link aus den zuvor angelegten CDS)
monoatomicPNG.add_glyph(monoatomicpictureSource, ImageURL(url='img_url', x=0, y=154, w=1004, h=154))

# ############# PLOT 2: MonoatomicEinheitszelle (German) ##########################
monoatomicunitcellPNG_de = figure(
                       width=150,
                       height=int(150/1.02),
                       x_range = (0, 299),
                       y_range= ( 0,292) ,
                       tools = ''
                  )
monoatomicunitcellPNG_de.axis.major_tick_line_color = None
monoatomicunitcellPNG_de.axis.major_label_text_color = None
monoatomicunitcellPNG_de.axis.minor_tick_line_color = None
monoatomicunitcellPNG_de.axis.axis_line_color = None
monoatomicunitcellPNG_de.grid.visible = False
monoatomicunitcellPNG_de.toolbar.logo = None
monoatomicunitcellPNG_de.outline_line_color = None

monoatomicunitcellPNG_de.add_glyph(monoatomiceinheitszelleSource, ImageURL(url='img_url', x=0, y=292, w=299, h=292))

# ############# PLOT 3: MonoatomicEinheitszelle (english) ##########################
monoatomicunitcellPNG_en = figure(
                       width=150,
                       height=int(150/1.02),
                       x_range = (0, 299),
                       y_range= ( 0,292) ,
                       tools = ''
                  )
monoatomicunitcellPNG_en.axis.major_tick_line_color = None
monoatomicunitcellPNG_en.axis.major_label_text_color = None
monoatomicunitcellPNG_en.axis.minor_tick_line_color = None
monoatomicunitcellPNG_en.axis.axis_line_color = None
monoatomicunitcellPNG_en.grid.visible = False
monoatomicunitcellPNG_en.toolbar.logo = None
monoatomicunitcellPNG_en.outline_line_color = None

monoatomicunitcellPNG_en.add_glyph(monoatomicunitcellSource, ImageURL(url='img_url', x=0, y=292, w=299, h=292))


#####################
# Diatomic Statics
#####################
# ############# PLOT 1: Diatomicchain ##########################
# Anlegen des Plots
diatomicPNG = figure(
                       width=900,
                       height=int(900/6.79),
                       x_range=(0, 1692),
                       y_range=(0, 249),
                       tools=''
                  )
# Alles deaktivieren was ein Plotformat erkennen lassen würde
diatomicPNG.axis.major_tick_line_color = None
diatomicPNG.axis.major_label_text_color = None
diatomicPNG.axis.minor_tick_line_color = None
diatomicPNG.axis.axis_line_color = None
diatomicPNG.grid.visible = False
diatomicPNG.toolbar.logo = None
diatomicPNG.outline_line_color = None

diatomicPNG.add_glyph(diatomicpictureSource, ImageURL(url='img_url', x=0, y=249, w=1692, h=249))

# ############# PLOT 2: DiatomicEinheitszelle (German) ##########################
diatomicunitcellPNG_de = figure(
                       width=300,
                       height=int(300/2.02),
                       x_range=(0, 593),
                       y_range=(0, 294),
                       tools=''
                  )
diatomicunitcellPNG_de.axis.major_tick_line_color = None
diatomicunitcellPNG_de.axis.major_label_text_color = None
diatomicunitcellPNG_de.axis.minor_tick_line_color = None
diatomicunitcellPNG_de.axis.axis_line_color = None
diatomicunitcellPNG_de.grid.visible = False
diatomicunitcellPNG_de.toolbar.logo = None
diatomicunitcellPNG_de.outline_line_color = None

diatomicunitcellPNG_de.add_glyph(diatomiceinheitszelleSource, ImageURL(url='img_url', x=0, y=294, w=593, h=294))

# ############# PLOT 3: MonoatomicEinheitszelle (english) ##########################
diatomicunitcellPNG_en = figure(
                       width=300,
                       height=int(300/2.02),
                       x_range=(0, 593),
                       y_range=(0, 294),
                       tools=''
                  )
diatomicunitcellPNG_en.axis.major_tick_line_color = None
diatomicunitcellPNG_en.axis.major_label_text_color = None
diatomicunitcellPNG_en.axis.minor_tick_line_color = None
diatomicunitcellPNG_en.axis.axis_line_color = None
diatomicunitcellPNG_en.grid.visible = False
diatomicunitcellPNG_en.toolbar.logo = None
diatomicunitcellPNG_en.outline_line_color = None

diatomicunitcellPNG_en.add_glyph(diatomicunitcellSource, ImageURL(url='img_url', x=0, y=294, w=593, h=294))


# Grafik Dictionary mit dem Einheitszellen PNG für beide Sprachen
graphic_library = ColumnDataSource(data=dict(deutsch=[monoatomicunitcellPNG_de, diatomicunitcellPNG_de],
                                             english=[monoatomicunitcellPNG_en, diatomicunitcellPNG_en]))

# Alle PNGs in der Sprache anpassen
# Standard
monoatomicunitcellgraphic = graphic_library.data[language][0]
diatomicunitcellgraphic = graphic_library.data[language][1]


def update_graphics():
    global monoatomicunitcellgraphic, diatomicunitcellgraphic
    mono_unitcellPNG.children[1] = graphic_library.data[language][0]
    di_unitcellPNG.children[1] = graphic_library.data[language][1]


##########################################################################################################
# --------------------------------------- Layout/Menu Auswahl---------------------------------------------
##########################################################################################################
######################################
# Superposition Monoatomic Layout
######################################

ka_buttons1_mono_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_mono_superpos1_button_label),
                                                               Spacer(height=1), row(mono_superpos1_ka_minus_button,
                                                                                     Spacer(width=mono_superpos1_ka_plus_button.width),
                                                                                     mono_superpos1_ka_plus_button)))
ka_buttons2_mono_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_mono_superpos2_button_label),
                                                               Spacer(height=1), row(mono_superpos2_ka_minus_button,
                                                                                     Spacer(width=mono_superpos2_ka_plus_button.width),
                                                                                     mono_superpos2_ka_plus_button)))
superpos_buttons = column(global_timer_superpos, playbutton_mono_superpos, Spacer(height=5),
                          ka_buttons1_mono_superpos_layout,
                          ka_buttons2_mono_superpos_layout)


######################################
# Monoatomic Layout
######################################
ka_buttons_mono_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_mono_button_label), Spacer(height=1),
                                                      row(mono_ka_minus_button, Spacer(width=20), mono_ka_plus_button)))
monoatomic_buttons = column(global_timer, playbutton_mono, mono_bandgap_button, Spacer(height=5), ka_buttons_mono_layout)
# Seperate Definition des Layouts der veränderlichen PNGs um besser auf die children zuzugreifen zu können (Sprachwechsel)
mono_unitcellPNG = row(Spacer(width=420), monoatomicunitcellgraphic)
# Definition der einzelnen Layout Teile
mono_block1 = column(general_app_infos, column(row(Spacer(width=85), monoatomicPNG), mono_unitcellPNG), column(general_monoatomic_infos))
mono_block2 = column(column(monoatomic_animation_info,
                            row(monoatomic_buttons, fig_dispersion_mono), column(monoatomic_animation)),
                     )
mono_superpos_block2 = column(mono_superposition_info, column(row(superpos_buttons, column(monoatomic_superpos_animation,
                            displacement_over_y))), superposition_explained)
# Beinhaltet die gesamte Benutzeroberfläche der monoatomaren WebApp
monoatomic_layout = column(mono_block1, mono_block2, mono_superpos_block2)
print("wir kamen nochmal beim monoatomic layout vorbei")

######################################
# Superposition Diatomic Layout
######################################
ka_buttons1_di_acou_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_di_acou_superpos1_button_label),
                                                               Spacer(height=1), row(di_acou_superpos1_ka_minus_button,
                                                                                     Spacer(width=20),
                                                                                     di_acou_superpos1_ka_plus_button)))
ka_buttons2_di_acou_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_di_acou_superpos2_button_label),
                                                               Spacer(height=1), row(di_acou_superpos2_ka_minus_button,
                                                                                     Spacer(width=20),
                                                                                     di_acou_superpos2_ka_plus_button)))
ka_buttons1_di_opti_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_di_opti_superpos1_button_label),
                                                               Spacer(height=1), row(di_opti_superpos1_ka_minus_button,
                                                                                     Spacer(width=20),
                                                                                     di_opti_superpos1_ka_plus_button)))
ka_buttons2_di_opti_superpos_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_di_opti_superpos2_button_label),
                                                               Spacer(height=1), row(di_opti_superpos2_ka_minus_button,
                                                                                     Spacer(width=20),
                                                                                     di_opti_superpos2_ka_plus_button)))
superpos_buttons_acou = column(global_timer_superpos, playbutton_di_acou_superpos, Spacer(height=5),
                               ka_buttons1_di_acou_superpos_layout,
                               ka_buttons2_di_acou_superpos_layout)
superpos_buttons_opti = column(playbutton_di_opti_superpos, Spacer(height=5),
                               ka_buttons1_di_opti_superpos_layout,
                               ka_buttons2_di_opti_superpos_layout)

######################################
# Diatomic Layout
######################################
ka_buttons_di_layout = row(Spacer(width=15), column(row(Spacer(width=10), ka_di_button_label), Spacer(height=1),
                                                    row(di_ka_minus_button, Spacer(width=20),
                                                        di_ka_plus_button)))
mass_buttons_di_layout = row(Spacer(width=15), column(row(Spacer(width=10), mass_button_label), Spacer(height=1),
                                                    row(mass_minus_button, Spacer(width=20),
                                                        mass_plus_button)))
diatomic_buttons = column(global_timer, playbutton_diatomic, di_bandgap_button, Spacer(height=5),
                            ka_buttons_di_layout, mass_buttons_di_layout)

# Seperate Definition des Layouts der veränderlichen PNGs um besser auf die children zuzugreifen zu können (Sprachwechsel)
di_unitcellPNG = row(Spacer(width=370), diatomicunitcellgraphic)
# Definition der einzelnen Layout Teile
di_block1 = column(general_app_infos_diatomic, column(row(Spacer(width=40), diatomicPNG), di_unitcellPNG), general_diatomic_infos)
di_block2 = column(column(diatomic_animation_info,
                            column(row(diatomic_buttons, fig_dispersion_di),
                                column(diatomic_optical_animation, diatomic_acoustic_animation)))
                     )
di_acou_superpos_block2 = column(di_superposition_info, column(row(superpos_buttons_acou, column(diatomic_acou_superpos_animation,
                                                                     displacement_over_y_di_acou))), di_superposition_acou_explained)

di_opti_superpos_block2 = column(column(row(superpos_buttons_opti, column(diatomic_opti_superpos_animation,
                                                                     displacement_over_y_di_opti))), di_superposition_opti_explained)
# Beinhaltet die gesamte Benutzeroberfläche der monoatomaren WebApp
diatomic_layout = column(di_block1, di_block2, di_acou_superpos_block2, di_opti_superpos_block2)

##################
# Menu-Auswahl Button erstellen
##################
menu_selection = Button(label="Diatomic Mass-Spring-Chain", button_type="primary", width=100)


# Ein Update der Layouts mittels curodc().clear() -> curdoc().add_root(newlayout)
# hatte nicht funktioniert ohne ein reload des bokeh servers
def update_layout():
    if menu_selection.label == "Diatomic Mass-Spring-Chain":
        # entfernen des Layouts
        general_layout.children.remove(monoatomic_layout)
        # das andere Layout an die letzte Stelle des general Layouts anbringen
        general_layout.children.append(diatomic_layout)
        # Beschriftung des Buttons anpassen
        menu_selection.label = "Monoatomic Mass-Spring-Chain"
    elif menu_selection.label == "Monoatomic Mass-Spring-Chain":
        general_layout.children.remove(diatomic_layout)
        general_layout.children.append(monoatomic_layout)
        menu_selection.label = "Diatomic Mass-Spring-Chain"


# Menue-Button definieren
menu_selection.on_click(update_layout)      # Funktion update_layout() zum callback einsetzen
# Standard Einstellung des Layouts
general_layout = column(menu_selection, language_button, monoatomic_layout)
curdoc().locale = 'de_DE'


# general Layout an die Root des Bokeh Dokuments setzen
curdoc().add_root(general_layout)
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_", " ").replace("-", " ")

