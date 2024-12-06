# general imports
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row, Spacer
from bokeh.models import Button, Label, ColumnDataSource, Legend, \
    Paragraph, Div, BoxAnnotation
from bokeh.models.glyphs import ImageURL

from functions import dis_rel_mono
from math import floor

from monoatomic_mass_chain import Monoatomic_chain
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
chain_length = 64
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
                              y_range=(-2, 2), width=450, height=50, toolbar_location=None)
monoatomic_animation.title.text_font_size = "10pt"
monoatomic_animation.axis.visible = False
monoatomic_animation.grid.visible = False
# monoatomic_animation.outline_line_color = None
monoatomic_animation.toolbar.logo = None
start_time = time.time()
monoatomic_chain.plot(monoatomic_animation)      # monoatomare Kette plotten
elapsed_time = time.time() - start_time
print(f"Frame rendered in {elapsed_time:.4f} seconds")

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
y_ka_mono = dis_rel_mono(ka_mono)
ka_source_mono = ColumnDataSource(data=dict(x=[ka_mono], y=[y_ka_mono]))
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
    # ka_source_mono.data = dict(x=[ka_mono], y=[dis_rel_mono(ka_mono)])
    ka_source_mono.patch({'x': [(0, ka_mono)], 'y': [(0, dis_rel_mono(ka_mono))]})

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


######################################################################################################
# ------------------------------------- Simulation Mass Chains ---------------------------------------
######################################################################################################
# Alle simulations Funktionen die mit den Playbutton verknüpft werden

# --------------- Monoatomic Simulation
def simulate_monoatomic():
    global timer_1       # mit global auf Werte ausserhalb der Funktion zugreifen
    # Berechnung der Displacements
    start_time = time.time()
    monoatomic_chain.calculate_monoatomic_dynamics(timer_1, ka_mono, mass_mono)
    # Anpassung des Timers
    global_timer.text = "Timer [s]:" + str(np.round(timer_1, decimals=2))
    # Nach 60s die Animation automatisch stoppen ansonsten Timer=+timestep
    timer_1 += time_steps
    elapsed_time = time.time() - start_time
    print(f"Frame rendered in {elapsed_time:.4f} seconds")


###########################################################################################################
# ------------------------------------- Play Pause Button -------------------------------------------------
###########################################################################################################


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
        callback_id_mono['id'] = curdoc().add_periodic_callback(simulate_monoatomic, 150)
        playbutton_mono.label = label_playbutton_dictionary.data[language][1][1]
    else:
        curdoc().remove_periodic_callback(callback_id_mono['id'])
        playbutton_mono.label = label_playbutton_dictionary.data[language][1][0]


# Play Button erstellen
playbutton_mono = Button(label=label_playbutton_dictionary.data[language][1][0], button_type='primary', width=150)
playbutton_mono.on_click(play_pause_mono)       # zum Funktionsaufruf die Play-Funktion übergeben


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

    # Bandgap Button
    mono_bandgap_button.label = label_dictionary.data[language][0][0]

    # Plot Titles aktualisieren mit der .title.text Methode
    # Monoatomic
    monoatomic_animation.title.text = label_dictionary.data[language][1]

    # Legend_label
    legend_dispersion_mono.items = [(legend_dictionary_mono.data[language][0], [disp_mono_line_1]), (legend_dictionary_mono.data[language][1], [disp_mono_line_2])]


def change_content():
    global general_app_infos, general_monoatomic_infos, monoatomic_animation_info

    if language == 'deutsch':
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

monoatomiceinheitszelleSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"monoatomicEinheitszelle.png")]))

monoatomicunitcellSource = ColumnDataSource(data=dict(img_url=[str(app_base_path.relative_to
                                                (app_base_path.parent) /"static" /"images" /"monoatomicunitcell.png")]))



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


# Grafik Dictionary mit dem Einheitszellen PNG für beide Sprachen
graphic_library = ColumnDataSource(data=dict(deutsch=[monoatomicunitcellPNG_de],
                                             english=[monoatomicunitcellPNG_en]))

# Alle PNGs in der Sprache anpassen
# Standard
monoatomicunitcellgraphic = graphic_library.data[language][0]


def update_graphics():
    global monoatomicunitcellgraphic
    mono_unitcellPNG.children[1] = graphic_library.data[language][0]



##########################################################################################################
# --------------------------------------- Layout/Menu Auswahl---------------------------------------------
##########################################################################################################

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

# Beinhaltet die gesamte Benutzeroberfläche der monoatomaren WebApp
monoatomic_layout = column(mono_block1, mono_block2)


# Funktion update_layout() zum callback einsetzen
# Standard Einstellung des Layouts
general_layout = column(language_button, monoatomic_layout)
curdoc().locale = 'de_DE'


# general Layout an die Root des Bokeh Dokuments setzen
curdoc().add_root(general_layout)
curdoc().title = str(app_base_path.relative_to(app_base_path.parent)).replace("_", " ").replace("-", " ")

