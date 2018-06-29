import { Legend, LegendView } from "models/annotations/legend"
import { Annotation, AnnotationView } from "./annotation"
import { LegendItem } from "./legend_item"
import { GlyphRendererView } from "../renderers/glyph_renderer"
import { Color } from "core/types"
import { Line, Fill, Text } from "core/visuals"
import { FontStyle, TextAlign, TextBaseline, LineJoin, LineCap } from "core/enums"
import { Orientation, LegendLocation, LegendClickPolicy } from "core/enums"
import * as p from "core/properties"
import { get_text_height } from "core/util/text"
import { BBox } from "core/util/bbox"
import { max, all } from "core/util/array"
import { values } from "core/util/object"
import { isString, isArray } from "core/util/types"
import { Context2d } from "core/util/canvas"
import { div, show, hide } from "core/dom"

export class LatexLegendView extends LegendView {
    model: LatexLegend

    protected entryEl: HTMLElement
    protected overlayEl: HTMLElement
    // protected mybbox: BBox

    initialize(options: any): void {
        super.initialize(options)
        console.log('hello initialize')
        // console.log(this)
        this.overlayEl = this._parent.el.children[0].children[1]
        for (const item of this.model.items) {
            const labels = item.get_labels_list_from_label_prop()
            // console.log(labels)
            // console.log(labels.length)
            for (let i = 0, end = labels.length; i < end; i++) {
                const el = div({ class: 'bk-annotation-child', style: { display: "none" } })
                this.overlayEl.appendChild(el)
            }
        }
    }

    render(): void {
        console.log(this)
        if (!this.model.visible)
            return

        if (this.model.items.length == 0)
            return

        const { ctx } = this.plot_view.canvas_view
        // const tsize = this.visuals.label_text.get_value("text_font_size")
        // console.log(tsize)
        // this.visuals.label_text.set_value("text_font_size:25pt")
        var bbox = this.compute_legend_bbox()
        // this.visuals.label_text.set_value("text_font_size:14pt")
        console.log(this.model.max_label_width)
        if (this.model.max_label_width > 0) {
            bbox.width = this.model.max_label_width
        }
            // ctx.save()
        // this.visuals.label_text.text_font_size = 12
        this._draw_legend_box(ctx, bbox)
        var y = this._draw_legend_items(ctx, bbox)
        
        // ctx.restore()
    }

    // compute_legend_bbox(): LegendBBox {
    //     console.log('my compute legend bbox')
    //     var legend_width = 0
    //     var legend_height = 0
    //     var index = 1
    //     for (const item of this.model.items) {
    //         const labels = item.get_labels_list_from_label_prop()
    //         for (const label of labels) {
    //             const el = this.overlayEl.children[index] as HTMLElement
    //             console.log(this.overlayEl)
    //             try {
    //                 katex.render(label, el)
    //             } catch (err) {
    //                 el.textContent = err
    //             }
    //             el.style.position = 'absolute'
    //             el.style.font = `${this.visuals.label_text.font_value()}`
    //             el.style.lineHeight = "normal"
    //             // el.style = "float:left"
    //             show(el)
    //             const el_width = el.offsetWidth
    //             if (legend_width < el_width) {
    //                 legend_width = el_width
    //             }
    //             legend_height += el.offsetHeight
    //             // hide(el)
    //         }
    //     }

    //     const legend_margin = this.model.margin
    //     const panel = this.model.panel != null ? this.model.panel : this.plot_view.frame
    //     const [hr, vr] = panel.bbox.ranges
    //     const { location } = this.model
    //     let sx: number, sy: number
    //     if (isString(location)) {
    //         switch (location) {
    //             case 'top_left':
    //                 sx = hr.start + legend_margin
    //                 sy = vr.start + legend_margin
    //                 break
    //             case 'top_center':
    //                 sx = (hr.end + hr.start) / 2 - legend_width / 2
    //                 sy = vr.start + legend_margin
    //                 break
    //             case 'top_right':
    //                 sx = hr.end - legend_margin - legend_width
    //                 sy = vr.start + legend_margin
    //                 break
    //             case 'bottom_right':
    //                 sx = hr.end - legend_margin - legend_width
    //                 sy = vr.end - legend_margin - legend_height
    //                 break
    //             case 'bottom_center':
    //                 sx = (hr.end + hr.start) / 2 - legend_width / 2
    //                 sy = vr.end - legend_margin - legend_height
    //                 break
    //             case 'bottom_left':
    //                 sx = hr.start + legend_margin
    //                 sy = vr.end - legend_margin - legend_height
    //                 break
    //             case 'center_left':
    //                 sx = hr.start + legend_margin
    //                 sy = (vr.end + vr.start) / 2 - legend_height / 2
    //                 break
    //             case 'center':
    //                 sx = (hr.end + hr.start) / 2 - legend_width / 2
    //                 sy = (vr.end + vr.start) / 2 - legend_height / 2
    //                 break
    //             case 'center_right':
    //                 sx = hr.end - legend_margin - legend_width
    //                 sy = (vr.end + vr.start) / 2 - legend_height / 2
    //                 break
    //             default:
    //                 throw new Error("unreachable code")
    //         }
    //     } else if (isArray(location) && location.length == 2) {
    //         const [vx, vy] = location
    //         sx = panel.xview.compute(vx)
    //         sy = panel.yview.compute(vy) - legend_height
    //     } else
    //         throw new Error("unreachable code")

    //     console.log(legend_height, legend_width)
    //     return { x: sx, y: sy, width: legend_width, height: legend_height }
    // }

    // interactive_bbox(): BBox {
    //     // const {x, y, width, height} = this.compute_legend_bbox()
    //     // return new BBox({x, y, width, height})
    //     return this.mybbox
    // }

    // on_hit(sx: number, sy: number): boolean {
    //     console.log('on_hit:',sx,sy)
    //     for (const el of this.overlayEl.children) {
    //         console.log(el.getBoundingClientRect())
    //     }
    //     return false
    // }

    // protected _draw_legend_box(ctx: Context2d, bbox: LegendBBox, y: number, y2: number): void {
    //     ctx.beginPath()
    //     // ctx.rect(bbox.x, bbox.y, bbox.width, bbox.height) - y.yoffset2/2
    //     ctx.rect(bbox.x, bbox.y-y2/2, bbox.width, y)
    //     // this.visuals.background_fill.set_value(ctx)
    //     // ctx.fill()
    //     if (this.visuals.border_line.doit) {
    //       this.visuals.border_line.set_value(ctx)
    //       ctx.stroke()
    //     }
    //     // const tmp1 = bbox.x
    //     // const tmp2 = bbox.y-y2/2
    //     // const tmp3 = bbox.width
    //     // const tmp4 = y
    //     // this.mybbox = new BBox({tmp1, tmp2, tmp3, tmp4})
    // }

    protected _draw_legend_items(ctx: Context2d, bbox: LegendBBox): [number, number] {
        console.log('_draw_legend_items')
        const { glyph_width, glyph_height } = this.model
        const { legend_padding } = this
        const legend_spacing = this.model.spacing
        const { label_standoff } = this.model
        let xoffset = legend_padding
        let yoffset = legend_padding
        const vertical = this.model.orientation == "vertical"

        // console.log(this.model.items)
        // console.log(this.model.items.entries())
        var index = 0
        var yy = 0

        for (const item of this.model.items) {
            // console.log('item of items')
            const labels = item.get_labels_list_from_label_prop()
            const field = item.get_field_from_label_prop()
            // console.log(labels.length)

            if (labels.length == 0)
                continue

            const active = (() => {
                switch (this.model.click_policy) {
                    case "none": return true
                    case "hide": return all(item.renderers, r => r.visible)
                    case "mute": return all(item.renderers, r => !r.muted)
                }
            })()

            console.log(labels)

            for (const label of labels) {
                console.log('for label of labels')
                const el = this.overlayEl.children[index] as HTMLElement
                // console.log(this.overlayEl)
                try {
                    katex.render(labels[0], el)
                } catch (err) {
                    el.textContent = err
                }
                // var bla = el.getBoundingClientRect()
                // console.log('bboxcool',bla)
                // const xx = el.offsetWidth;
                // var yy = el.offsetHeight;
                // console.log('yy:',yy)
                // const x1 = bbox.x + xx + xoffset
                // const y1 = bbox.y + yy + yoffset
                const x1 = bbox.x + xoffset
                //####### const y1 = bbox.y + yoffset - glyph_height/2
                const y1 = bbox.y + yoffset
                const x2 = x1 + glyph_width
                const y2 = y1 + glyph_height
                
                if (vertical)
                    //##################yoffset += this.max_label_height + legend_spacing+ yy - glyph_height/2
                    yoffset += this.max_label_height + legend_spacing
                else
                    xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing

                this.visuals.label_text.set_value(ctx)

                // console.log(this._parent.el.children[0].children[1])
                // const labels = item.get_labels_list_from_label_prop()
                // for (let i = 0, end = labels.length; i < end; i++) {


                el.style.position = 'absolute'
                el.style.left = `${x1 + x2}px`
                el.style.top = `${y1}px`
                el.style.color = `${this.visuals.label_text.text_color.value()}`
                el.style.opacity = `${this.visuals.label_text.text_alpha.value()}`
                el.style.font = `${this.visuals.label_text.font_value()}`
                el.style.lineHeight = "normal"
                // el.style = "float:bottom"
                show(el)
                // }
                const xx = el.offsetWidth;
                yy = el.offsetHeight;

                // yy = el.offsetHeight;
                // console.log('yy:',yy)
                // console.log('bboxcool',bla)
                // console.log(el)

                // ctx.fillText(label, x2 + label_standoff, y1 + this.max_label_height/2.0)

                for (const r of item.renderers) {
                    const view = this.plot_view.renderer_views[r.id] as GlyphRendererView
                    //###########view.draw_legend(ctx, x1, x2, y1, y2+yy- glyph_height, field, label)
                    view.draw_legend(ctx, x1, x2, y1, y2, field, label)
                }
                
                // if (vertical)
                //     //##################yoffset += this.max_label_height + legend_spacing+ yy - glyph_height/2
                //     yoffset += this.max_label_height + legend_spacing
                // else
                //     xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing

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
                }
            }
            index++
        }
        var yoffset2 = (this.max_label_height + legend_spacing+ yy - glyph_height/2)
        return [yoffset, yoffset2]

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