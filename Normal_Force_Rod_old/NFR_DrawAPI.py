## Draw Shapes in Plots

#from bokeh.models import ColumnDataSource
from bokeh.models import Arrow, OpenHead, LabelSet
from bokeh.models.glyphs import Patch


from abc import ABCMeta#, abstractmethod

class NFR_DrawAPI(object):
    __metaclass__ = ABCMeta
    

### Types of Masses

class NFR_BlueRod(NFR_DrawAPI):
    def drawPatch(self, fig, CDS, color="#0065BD", width=1):
        fig.patch(x='x', y='y', source=CDS, color=color, line_width=width)
                  
class NFR_BlackShadowRod(NFR_DrawAPI):
    def drawLine(self, fig, CDS, color='black', lw=2, la=0.7):
        fig.line(x='x', y='y', source=CDS, color=color, line_width=lw ,line_alpha=la)


class NFR_BlueArrow(NFR_DrawAPI):
    def drawArrow(self, fig, CDS, color="#0065BD", lw=2):
        arrow_glyph = Arrow(end=OpenHead(line_color="#0065BD",line_width=2, size=5), 
                       x_start='xS', x_end='xE', y_start='yS', y_end='yE',
                       line_width=lw, line_color=color, source=CDS)
        fig.add_layout(arrow_glyph)
        
class NFR_BlueLoad(NFR_DrawAPI):
    def drawPatch(self, fig, CDS, color="#0065BD", alpha=0.1): #0.5
        #fig.patch(x='x', y='y', source=CDS, line_color='black', fill_color=color, fill_alpha=alpha)
        glyph = Patch(x='x', y='y', fill_color=color, fill_alpha=alpha)
        fig.add_glyph(CDS, glyph)
        
        
#        
#        temperature_glyph = Patch(x='x', y='y', fill_color="#0065BD", fill_alpha=0.5)
#plot_main.add_glyph(constant_load_source, constant_load_glyph)




class NFR_BlackLabelText(NFR_DrawAPI):
    def drawLabels(self, fig, CDS):
        #fig.patch(x='x', y='y', source=CDS, line_color='black', fill_color=color, fill_alpha=alpha)
        labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=CDS)
        fig.add_layout(labels)


#main_labels = LabelSet(x='x', y='y', text='name', level='glyph', render_mode='canvas', source=labels_source)
#plot_main.add_layout(main_labels)



class NFR_GreenGraph(NFR_DrawAPI):
    def drawGraph(self, fig, CDS):
        fig.line(x='x', y='y', source=CDS, color="#A2AD00",line_width=2)



