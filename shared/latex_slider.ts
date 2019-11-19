
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


    // render(): void {
    //   super.render()
  
    //   const {start, end, value, step} = this._calc_to()
  
    //   let tooltips: boolean | any[] // XXX
    //   if (this.model.tooltips) {
    //     const formatter = {
    //       to: (value: number): string => this.model.pretty(value),
    //     }
  
    //     tooltips = repeat(formatter, value.length)
    //   } else
    //     tooltips = false
  
    //   if (this.slider_el == null) {
    //     this.slider_el = div() as any
  
    //     noUiSlider.create(this.slider_el, {
    //       cssPrefix: prefix,
    //       range: {min: start, max: end},
    //       start: value,
    //       step,
    //       behaviour: this.model.behaviour,
    //       connect: this.model.connected,
    //       tooltips,
    //       orientation: this.model.orientation,
    //       direction: this.model.direction,
    //     } as any) // XXX: bad typings; no cssPrefix
  
    //     this.noUiSlider.on('slide',  (_, __, values) => this._slide(values))
    //     this.noUiSlider.on('change', (_, __, values) => this._change(values))
  
    //     this._set_keypress_handles()
  
    //     const toggleTooltip = (i: number, show: boolean): void => {
    //       if (!tooltips)
    //         return
    //       const handle = this.slider_el.querySelectorAll(`.${prefix}handle`)[i]
    //       const tooltip = handle.querySelector<HTMLElement>(`.${prefix}tooltip`)!
    //       tooltip.style.display = show ? 'block' : ''
    //     }
  
    //     this.noUiSlider.on('start', (_, i) => toggleTooltip(i, true))
    //     this.noUiSlider.on('end',   (_, i) => toggleTooltip(i, false))
    //   } else {
    //     this.noUiSlider.updateOptions({
    //       range: {min: start, max: end},
    //       start: value,
    //       step,
    //     })
    //   }
  
    //   this._set_bar_color()
  
    //   if (this.model.disabled)
    //     this.slider_el.setAttribute('disabled', 'true')
    //   else
    //     this.slider_el.removeAttribute('disabled')
  
    //   this.title_el = div({class: bk_slider_title})
    //   this._update_title()
  
    //   this.group_el = div({class: bk_input_group}, this.title_el, this.slider_el)
    //   this.el.appendChild(this.group_el)
    // }




    _update_title(): void {

        empty(this.title_el)

        const hide_header = this.model.title == null || (this.model.title.length == 0 && !this.model.show_value)
        this.title_el.style.display = hide_header ? "none" : ""

        // this.title_el.style.whiteSpace = "nowrap"
    
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

            //this.value_el.style.display = "inline-block"
            //this.value_el.style.whiteSpace = "nowrap"

            this.title_el.appendChild(this.value_el)
            //this.group_el.appendChild(this.value_el)
            //this.group_el.insertBefore(this.value_el, this.slider_el)
            // if(this.title_el.parentNode != null){ 
            // var parentDiv1 = this.title_el.parentNode
            // parentDiv1.insertBefore(this.value_el, this.title_el)}
            //this.group_el.insertBefore(this.value_el, this.slider_el)//
          }

          if (this.model.value_unit.length != 0) {
            //this.unit_el = div({ class: "bk-slider-unit" }, this.model.value_unit)
            this.unit_el = span({ class: "bk-slider-unit" }, this.model.value_unit)
            this._render_katex(this.model.value_unit.replace(/^/,'\\,'), this.unit_el)
            //this.unit_el.style.cssFloat = "left"
            //this.value_el.style.marginLeft = '6px'

            console.log("look at widths:")
            console.log(this.title_el.offsetWidth)
            console.log(this.value_el.offsetWidth)

            //this.unit_el.style.display = "inline-block"

            //this.unit_el.style.marginLeft = `${this.title_el.offsetWidth + this.value_el.offsetWidth + 6}px`

//            this.title_el.width = `{this.title_el.offsetWidth + this.value_el.offsetWidth + this.unit_el.offsetWidth}px`

            this.title_el.appendChild(this.unit_el)
            //this.group_el.appendChild(this.unit_el)
            //this.value_el.appendChild(this.unit_el)
            //this.group_el.appendChild(this.unit_el)
            //this.group_el.insertBefore(this.unit_el, this.slider_el)
            // if(this.title_el.parentNode != null){ 
            // var parentDiv2 = this.title_el.parentNode
            // parentDiv2.insertBefore(this.unit_el, this.title_el)}
            //this.el.insertBefore(this.unit_el, this.slider_el)

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