
import { span, empty } from "core/dom"
import * as p from "core/properties"
import { Slider, SliderView } from "models/widgets/slider"
import { AbstractSlider } from "models/widgets/abstract_slider"
import { bk_slider_value } from "styles/widgets/sliders"


declare namespace katex {
    function render(expression: string, element: HTMLElement): void
  }


export class LatexSliderView extends SliderView {
    model: LatexSlider

    protected unit_el: HTMLElement
    protected value_el: HTMLElement


    _update_title(): void {

        empty(this.title_el)

        const hide_header = this.model.title == null || (this.model.title.length == 0 && !this.model.show_value)
        this.title_el.style.display = hide_header ? "none" : ""

        if (!hide_header) {
          if (this.model.title.length != 0) {
            this.title_el.textContent = `${this.model.title}: `
            this._render_katex(this.model.title, this.title_el)
          }

    
          if (this.model.show_value) {
            const {value} = this._calc_to()
            const pretty = value.map((v) => this.model.pretty(v)).join(" .. ")

            this.value_el = span({ class: bk_slider_value }, pretty)
            this._render_katex(pretty, this.value_el)
            this.value_el.style.marginLeft = '6px'

            this.title_el.appendChild(this.value_el)
          }

          if (this.model.value_unit.length != 0) {
            this.unit_el = span({ class: "bk-slider-unit" }, this.model.value_unit)
            this._render_katex(this.model.value_unit.replace(/^/,'\\,'), this.unit_el)
            //this.unit_el.style.cssFloat = "left"
            //this.value_el.style.marginLeft = '6px'

            this.title_el.appendChild(this.unit_el)
          }

        }


    }


      protected _render_katex(text: string, el: HTMLElement): void {
        try {
            katex.render(text, el)
        } catch (err) {
            el.textContent = err
        }
    }

}

export namespace LatexSlider {
    export type Attrs = p.AttrsOf<Props>
    export type Props = AbstractSlider.Props & {
      value_unit: p.Property<string>
    }
}

export interface LatexSlider extends LatexSlider.Attrs { }

export class LatexSlider extends Slider {

    properties: LatexSlider.Props

    constructor(attrs?: Partial<LatexSlider.Attrs>) {
        super(attrs)
    }

    static initClass(): void {
        this.prototype.type = "LatexSlider"
        this.prototype.default_view = LatexSliderView

        // in some apps value_unit is supported

        this.define<LatexSlider.Props>({
            value_unit: [ p.String, ''],
        })

        this.override({
            format: "0[.]00"
        })

    }
}

LatexSlider.initClass()