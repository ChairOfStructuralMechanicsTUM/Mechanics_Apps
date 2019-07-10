from bokeh.models.widgets import Div, Slider
from bokeh.models import Label, LabelSet, Legend
from bokeh.core.properties import Bool, String, Float

LATEX_LABEL_JS_CODE = """
import {Label, LabelView} from "models/annotations/label"

export class LatexLabelView extends LabelView
  render: () ->

    #--- Start of copied section from ``Label.render`` implementation

    # Here because AngleSpec does units tranform and label doesn't support specs
    switch @model.angle_units
      when "rad" then angle = -1 * @model.angle
      when "deg" then angle = -1 * @model.angle * Math.PI/180.0

    panel = @model.panel ? @plot_view.frame

    xscale = @plot_view.frame.xscales[@model.x_range_name]
    yscale = @plot_view.frame.yscales[@model.y_range_name]

    sx = if @model.x_units == "data" then xscale.compute(@model.x) else panel.xview.compute(@model.x)
    sy = if @model.y_units == "data" then yscale.compute(@model.y) else panel.yview.compute(@model.y)

    sx += @model.x_offset
    sy -= @model.y_offset

    #--- End of copied section from ``Label.render`` implementation

    # Must render as superpositioned div (not on canvas) so that KaTex
    # css can properly style the text
    @_css_text(@plot_view.canvas_view.ctx, "", sx, sy, angle)

    # ``katex`` is loaded into the global window at runtime
    # katex.renderToString returns a html ``span`` element
    katex.render(@model.text, @el, {displayMode: true})

export class LatexLabel extends Label
  type: 'LatexLabel'
  default_view: LatexLabelView
"""

katex_js = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.1/katex.min.js"
katex_css = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.1/katex.min.css"


class LatexDiv(Div):
    __javascript__ = [katex_js]
    __css__ = [katex_css]
    __implementation__ = "latex_div.ts"

class LatexSlider(Slider):
    __javascript__ = [katex_js]
    __css__ = [katex_css]
    __implementation__ = "latex_slider.ts"

    value_unit = String(default='', help="""
    The unit in LaTeX math mode code to be displayed behind the slider value.
    """)

class LatexLabelSet(LabelSet):
    __javascript__ = [katex_js]
    __css__ = [katex_css]
    __implementation__ = "latex_label_set.ts"

    display_mode = Bool(default=False, help="""
        Whether to use display mode for the LaTeX labels.
        """)

class LatexLabel(Label):
    """A subclass of the Bokeh built-in `Label` that supports rendering
    LaTex using the KaTex typesetting library.

    Only the render method of LabelView is overloaded to perform the
    text -> latex (via katex) conversion. Note: ``render_mode="canvas``
    isn't supported and certain DOM manipulation happens in the Label
    superclass implementation that requires explicitly setting
    `render_mode='css'`).
    """
    __javascript__ = [katex_js]
    __css__ = [katex_css]
    __implementation__ = LATEX_LABEL_JS_CODE

class LatexLegend(Legend):
    """
    A subclass of the built-in `Legend` that supports rendering
    LaTeX using the KaTeX typesetting library.

    Only vertical legends are supported, the `orientation` keyword
    is overwritten.
    """
    __javascript__ = [katex_js]
    __css__ = [katex_css]
    __implementation__ = "latex_legend.ts"

    max_label_width = Float(default=0, help="""
        Maximum width of the legend box. Automatic calculation of the width is not supported yet.
        """)