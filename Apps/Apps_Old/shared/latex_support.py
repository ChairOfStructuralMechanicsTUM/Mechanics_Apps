from bokeh.models.widgets import Div, Slider
from bokeh.models import Label, LabelSet, Legend
from bokeh.core.properties import Bool, String, Float


katex_js = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.11.1/katex.min.js"
katex_css = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.11.1/katex.min.css"


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
    __implementation__ = "latex_label.ts"

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