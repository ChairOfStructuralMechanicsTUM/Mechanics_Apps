from bokeh.models.widgets import Div

JS_CODE = """
import {Markup, MarkupView} from "models/widgets/markup"
import {div} from "core/dom"
import * as p from "core/properties"
#dom_1 = require( Dom );
export class LatexDivView extends MarkupView
    render: () ->
        super.render()
        content = div()
        # content = @div()
        content.innerHTML = @model.text
        console.log(content)
        # console.log(@model.text)
        #katex.render(@model.text, @el, {displayMode: true})
        @markupEl.appendChild(content)

export class LatexDiv extends Markup
    type: 'LatexDiv'
    default_view: LatexDivView

"""

class LatexDiv(Div):
    __javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.js"]
    __css__ = ["https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.6.0/katex.min.css"]
    __implementation__ = "latex_div.ts"