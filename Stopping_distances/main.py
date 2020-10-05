"""
Stopping Distances - compare time and distance dependent description of motion

"""
# general imports
from copy                   import copy

# bokeh imports
from bokeh.io               import curdoc
from bokeh.layouts          import column, row, Spacer
from bokeh.models           import ColumnDataSource
from bokeh.models.widgets   import Button, Select

# internal imports
from SD_Problem       import SD_Problem
from SD_Graphs        import SD_Graphs
from SD_Visualisation import SD_Visualisation

# latex integration
from os.path import dirname, join, split, abspath
import sys, inspect
import yaml
currentdir = dirname(abspath(inspect.getfile(inspect.currentframe())))
parentdir = join(dirname(currentdir), "shared/")
sys.path.insert(0,parentdir) 
from latex_support import LatexDiv

#---------------------------------------------------------------------#

# change language
std_lang = 'en'
flags    = ColumnDataSource(data=dict(show=['off'], lang=[std_lang]))
strings  = yaml.safe_load(open('Stopping_distances/static/strings.json', encoding='utf-8'))

# create each part of the window
Visual  = SD_Visualisation()
Plotter = SD_Graphs()
Prob    = SD_Problem(Visual,Plotter)


######################################
# Change language
######################################

def changeLanguage():
    [lang] = flags.data["lang"]
    if lang == "en":
        setDocumentLanguage('de')
    elif lang == "de":
        setDocumentLanguage('en')

def setDocumentLanguage(lang):
    flags.patch( {'lang':[(0,lang)]} )
    for s in strings:
        if 'checkFlag' in strings[s]:
            flag = flags.data[strings[s]['checkFlag']][0]
            exec( (s + '=\"' + strings[s][flag][lang] + '\"').encode(encoding='utf-8') )
        elif 'isCode' in strings[s] and strings[s]['isCode']:
            exec( (s + '=' + strings[s][lang]).encode(encoding='utf-8') )
        else:
            exec( (s + '=\"' + strings[s][lang] + '\"').encode(encoding='utf-8') )
    
    if (Plotter.s_or_t=='t'):
        Plotter.at.xaxis.axis_label = copy(Plotter.vt.xaxis.axis_label)
    else:
        Plotter.at.xaxis.axis_label = copy(Plotter.vs.xaxis.axis_label)
    

lang_button = Button(button_type="success", label="Zu Deutsch wechseln")
lang_button.on_click(changeLanguage)


######################################
# Page layout
######################################

# add app description
description_filename = join(dirname(__file__), "description.html")
description = LatexDiv(text=open(description_filename).read(), render_as_text=False, width=1200)

## Send to window
curdoc().add_root(column(row(Spacer(width=900),lang_button), description, row(column(Visual.fig,Plotter.Layout),Prob.Layout)))
curdoc().title = split(dirname(__file__))[-1].replace('_',' ').replace('-',' ')  # get path of parent directory and only use the name of the Parent Directory for the tab name. Replace underscores '_' and minuses '-' with blanks ' '
