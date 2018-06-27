import { div } from "core/dom"
import { logger } from "core/logging"
import { repeat } from "core/util/array"
import { throttle } from "core/util/callback"

import * as p from "core/properties"

import { Slider, SliderView } from "models/widgets/slider"

export class LatexSliderView extends SliderView {
    model: LatexSlider

    protected unitEl: HTMLElement

    render(): void {
        //copied from abstract_slider.ts
        if (this.sliderEl == null) {
            // XXX: temporary workaround for _render_css()
            super.render()
        }

        if (this.model.callback != null) {
            const callback = () => this.model.callback.execute(this.model)

            switch (this.model.callback_policy) {
                case 'continuous': {
                    this.callback_wrapper = callback
                    break
                }
                case 'throttle': {
                    this.callback_wrapper = throttle(callback, this.model.callback_throttle)
                    break
                }
            }
        }

        const prefix = 'bk-noUi-'

        const { start, end, value, step } = this._calc_to()

        let tooltips: boolean | any[] // XXX
        if (this.model.tooltips) {
            const formatter = {
                to: (value: number): string => this.model.pretty(value),
            }

            tooltips = repeat(formatter, value.length)
        } else
            tooltips = false

        this.el.classList.add("bk-slider")

        if (this.sliderEl == null) {
            this.sliderEl = div() as any
            this.el.appendChild(this.sliderEl)

            noUiSlider.create(this.sliderEl, {
                cssPrefix: prefix,
                range: { min: start, max: end },
                start: value,
                step: step,
                behaviour: this.model.behaviour,
                connect: this.model.connected,
                tooltips: tooltips,
                orientation: this.model.orientation,
                direction: this.model.direction,
            } as any) // XXX: bad typings; no cssPrefix
            this.sliderEl.noUiSlider.on('slide', (_, __, values) => this._slide(values))
            this.sliderEl.noUiSlider.on('change', (_, __, values) => this._change(values))

            // Add keyboard support
            const keypress = (e: KeyboardEvent): void => {
                const spec = this._calc_to()
                let value = spec.value[0]
                switch (e.which) {
                    case 37: {
                        value = Math.max(value - step, start)
                        break
                    }
                    case 39: {
                        value = Math.min(value + step, end)
                        break
                    }
                    default:
                        return
                }

                const pretty = this.model.pretty(value)
                logger.debug(`[slider keypress] value = ${pretty}`)
                this.model.value = value
                this.sliderEl.noUiSlider.set(value)
                if (this.valueEl != null)
                    this.valueEl.textContent = pretty
                katex.render(this.valueEl.textContent, this.valueEl)
                console.log('hello')
                if (this.callback_wrapper != null)
                    this.callback_wrapper()
            }

            const handle = this.sliderEl.querySelector(`.${prefix}handle`)!
            handle.setAttribute('tabindex', '0')
            handle.addEventListener('keydown', keypress)

            const toggleTooltip = (i: number, show: boolean): void => {
                const handle = this.sliderEl.querySelectorAll(`.${prefix}handle`)[i]
                const tooltip = handle.querySelector<HTMLElement>(`.${prefix}tooltip`)!
                tooltip.style.display = show ? 'block' : ''
            }

            this.sliderEl.noUiSlider.on('start', (_, i) => toggleTooltip(i, true))
            this.sliderEl.noUiSlider.on('end', (_, i) => toggleTooltip(i, false))
        } else {
            this.sliderEl.noUiSlider.updateOptions({
                range: { min: start, max: end },
                start: value,
                step: step,
            })
        }

        if (this.titleEl != null)
            this.el.removeChild(this.titleEl)
        if (this.valueEl != null)
            this.el.removeChild(this.valueEl)
        if (this.unitEl != null)
            this.el.removeChild(this.unitEl)

        if (this.model.title != null) {
            if (this.model.title.length != 0) {
                this.titleEl = div({ class: "bk-slider-title" }, this.model.title)
                this._render_katex(this.model.title, this.titleEl)
                this.titleEl.style = "float:left"
                this.el.insertBefore(this.titleEl, this.sliderEl)
            }

            if (this.model.show_value) {
                const pretty = value.map((v) => this.model.pretty(v)).join(" .. ")
                this.valueEl = div({ class: "bk-slider-value" }, pretty)
                this._render_katex(pretty, this.valueEl)
                this.valueEl.style = "float:left; margin-left: 6px"
                this.el.insertBefore(this.valueEl, this.sliderEl)
            }

            if (this.model.value_unit.length != 0) {
                this.unitEl = div({ class: "bk-slider-unit" }, this.model.value_unit)
                this._render_katex(this.model.value_unit, this.unitEl)
                this.unitEl.style = "float:left"
                this.el.insertBefore(this.unitEl, this.sliderEl)
            }
        }

        if (!this.model.disabled) {
            this.sliderEl.querySelector<HTMLElement>(`.${prefix}connect`)!
                .style
                .backgroundColor = this.model.bar_color
        }

        if (this.model.disabled)
            this.sliderEl.setAttribute('disabled', 'true')
        else
            this.sliderEl.removeAttribute('disabled')

        this.sliderEl.style = "float:left"
    }

    protected _render_katex(text: String, el: HTMLElement): void {
        try {
            katex.render(text, el)
        } catch (err) {
            el.textContent = err
        }
    }

}

export namespace LatexSlider {
    export interface Attrs extends Slider.Attrs { }
    export interface Props extends Slider.Props { }
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

        this.define({
            value_unit: [ p.String, ''],
        })

        this.override({
            format: "0[.]00"
        })

    }
}

LatexSlider.initClass()