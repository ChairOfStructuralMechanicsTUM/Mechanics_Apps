from __future__ import absolute_import

from bokeh.models import LabelSet
from bokeh.core.properties import Bool

class LatexLabelSet(LabelSet):
    __javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.js"]
    __css__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.css"]
    __implementation__ = "latex_label_set.ts"

    display_mode = Bool(default=False, help="""
    Whether to use display mode for the LaTeX labels.
    """)