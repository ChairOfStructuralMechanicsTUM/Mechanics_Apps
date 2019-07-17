## Draw Shapes in Plots

#from bokeh.models import ColumnDataSource
from bokeh.models import Arrow, OpenHead


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
        
        