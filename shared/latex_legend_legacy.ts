import { Legend, LegendView } from "models/annotations/legend"
import { GlyphRendererView } from "../renderers/glyph_renderer"
import * as p from "core/properties"
import { all } from "core/util/array"
import { Context2d } from "core/util/canvas"
import { div, show } from "core/dom"

export class LatexLegendView extends LegendView {
    model: LatexLegend

    protected overlayEl: HTMLElement

    initialize(options: any): void {
        super.initialize(options)
        this.model.orientation = "vertical"

        this.overlayEl = this._parent.el.children[0].children[1]
        for (const item of this.model.items) {
            const labels = item.get_labels_list_from_label_prop()
            for (let i = 0, end = labels.length; i < end; i++) {
                const el = div({ class: 'bk-annotation-child', style: { display: "none" } })
                this.overlayEl.appendChild(el)
            }
        }
    }

    render(): void {
        if (!this.model.visible)
            return

        if (this.model.items.length == 0)
            return

        const { ctx } = this.plot_view.canvas_view
        var bbox = this.compute_legend_bbox()
        
        if (this.model.max_label_width > 0) {
            bbox.width = this.model.max_label_width
        }
        
        this._draw_legend_box(ctx, bbox)
        this._draw_legend_items(ctx, bbox)
    }

    protected _draw_legend_items(ctx: Context2d, bbox: LegendBBox): void {
        console.log('_draw_legend_items')
        const { glyph_width, glyph_height } = this.model
        const { legend_padding } = this
        const legend_spacing = this.model.spacing
        const { label_standoff } = this.model
        let xoffset = legend_padding
        let yoffset = legend_padding
        const vertical = this.model.orientation == "vertical"

        var index = 0

        for (const item of this.model.items) {
            const labels = item.get_labels_list_from_label_prop()
            const field = item.get_field_from_label_prop()

            if (labels.length == 0)
                continue

            const active = (() => {
                switch (this.model.click_policy) {
                    case "none": return true
                    case "hide": return all(item.renderers, r => r.visible)
                    case "mute": return all(item.renderers, r => !r.muted)
                }
            })()

            for (const label of labels) {
                const el = this.overlayEl.children[index] as HTMLElement

                const x1 = bbox.x + xoffset
                const y1 = bbox.y + yoffset
                const x2 = x1 + glyph_width
                const y2 = y1 + glyph_height
                
                yoffset += this.max_label_height + legend_spacing
               
                this.visuals.label_text.set_value(ctx)

                el.style.position = 'absolute'
                el.style.left = `${x2 + xoffset}px`
                el.style.top = `${y1}px`
                el.style.color = `${this.visuals.label_text.text_color.value()}`
                el.style.opacity = `${this.visuals.label_text.text_alpha.value()}`
                el.style.font = `${this.visuals.label_text.font_value()}`
                el.style.lineHeight = "normal"
                
                try {
                    katex.render(labels[0], el)
                } catch (err) {
                    el.textContent = err
                    el.style.color = "red"
                }

                for (const r of item.renderers) {
                    const view = this.plot_view.renderer_views[r.id] as GlyphRendererView
                    view.draw_legend(ctx, x1, x2, y1, y2, field, label)
                }
                
                if (!active) {
                    let w: number, h: number
                    if (vertical)
                        [w, h] = [bbox.width - 2 * legend_padding, this.max_label_height]
                    else
                        [w, h] = [this.text_widths[label] + glyph_width + label_standoff, this.max_label_height]

                    ctx.beginPath()
                    ctx.rect(x1, y1, w, h)
                    this.visuals.inactive_fill.set_value(ctx)
                    ctx.fill()
                    
                    el.style.opacity = "0.3"
                }
                
                show(el)
            }

            index++
        }

    }
}

export namespace LatexLegend {
    export interface Attrs extends Legend.Attrs { }
    export interface Props extends Legend.Props { }
}

export interface LatexLegend extends LatexLegend.Attrs { }

export class LatexLegend extends Legend {

    properties: LatexLegend.Props

    constructor(attrs?: Partial<LatexLegend.Attrs>) {
        super(attrs)
    }

    static initClass(): void {
        this.prototype.type = "LatexLegend"
        this.prototype.default_view = LatexLegendView

        this.define({
            max_label_width: [p.Number, 0],
        })
    }
}

LatexLegend.initClass()