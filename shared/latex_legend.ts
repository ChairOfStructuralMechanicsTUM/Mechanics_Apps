import { Legend, LegendView } from "models/annotations/legend"
import {Annotation, AnnotationView} from "./annotation"
import {LegendItem} from "./legend_item"
import {GlyphRendererView} from "../renderers/glyph_renderer"
import {Color} from "core/types"
import {Line, Fill, Text} from "core/visuals"
import {FontStyle, TextAlign, TextBaseline, LineJoin, LineCap} from "core/enums"
import {Orientation, LegendLocation, LegendClickPolicy} from "core/enums"
import * as p from "core/properties"
import {get_text_height} from "core/util/text"
import {BBox} from "core/util/bbox"
import {max, all} from "core/util/array"
import {values} from "core/util/object"
import {isString, isArray} from "core/util/types"
import {Context2d} from "core/util/canvas"
import {div, show} from "core/dom"

export class LatexLegendView extends LegendView {
    model: LatexLegend

    protected entryEl: HTMLElement
    protected overlayEl: HTMLElement

    initialize(options: any): void {
        super.initialize(options)
        console.log('hello initialize')
        console.log(this)
        this.overlayEl = this._parent.el.children[0].children[1]
        for (const item of this.model.items) {
            const labels = item.get_labels_list_from_label_prop()
            console.log(labels)
            // console.log(labels.length)
            for (let i = 0, end = labels.length; i < end; i++) {
                const el = div({class: 'bk-annotation-child', style: {display: "none"}})
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
    
        const {ctx} = this.plot_view.canvas_view
        const bbox = this.compute_legend_bbox()
    
        // ctx.save()
        this._draw_legend_box(ctx, bbox)
        this._draw_legend_items(ctx, bbox)
        // ctx.restore()
    }

    protected _draw_legend_items(ctx: Context2d, bbox: LegendBBox): void {
        console.log('_draw_legend_items')
        const {glyph_width, glyph_height} = this.model
        const {legend_padding} = this
        const legend_spacing = this.model.spacing
        const {label_standoff} = this.model
        let xoffset = legend_padding
        let yoffset = legend_padding
        const vertical = this.model.orientation == "vertical"
    
        console.log(this.model.items)
        console.log(this.model.items.entries())
        var index = 0
        for (const item of this.model.items) {
            console.log('item of items')
          const labels = item.get_labels_list_from_label_prop()
          const field = item.get_field_from_label_prop()
          console.log(labels.length)
    
          if (labels.length == 0)
            continue
    
          const active = (() => { switch (this.model.click_policy) {
            case "none": return true
            case "hide": return all(item.renderers, r => r.visible)
            case "mute": return all(item.renderers, r => !r.muted)
          } })()
          console.log(labels)
          for (const label of labels) {
              console.log('for label of labels')
            const x1 = bbox.x + xoffset
            const y1 = bbox.y + yoffset
            const x2 = x1 + glyph_width
            const y2 = y1 + glyph_height
    
            if (vertical)
              yoffset += this.max_label_height + legend_spacing
            else
              xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing
    
            this.visuals.label_text.set_value(ctx)

            // console.log(this._parent.el.children[0].children[1])
            // const labels = item.get_labels_list_from_label_prop()
            // for (let i = 0, end = labels.length; i < end; i++) {
            const el = this.overlayEl.children[index] as HTMLElement
            console.log(this.overlayEl)
            try {
                katex.render(labels[0],el)
            } catch (err) {
                el.textContent = err
            }
            
            el.style.position = 'absolute'
            el.style.left = `${x1 + x2}px`
            el.style.top = `${y1}px`
            el.style.color = `${this.visuals.label_text.text_color.value()}`
            el.style.opacity = `${this.visuals.label_text.text_alpha.value()}`
            el.style.font = `${this.visuals.label_text.font_value()}`
            el.style.lineHeight = "normal"
            show(el)
            // }
            
            // console.log(el)

            // ctx.fillText(label, x2 + label_standoff, y1 + this.max_label_height/2.0)
            for (const r of item.renderers) {
              const view = this.plot_view.renderer_views[r.id] as GlyphRendererView
              view.draw_legend(ctx, x1, x2, y1, y2, field, label)
            }
    
            if (!active) {
              let w: number, h: number
              if (vertical)
                [w, h] = [bbox.width - 2*legend_padding, this.max_label_height]
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
    }
}

LatexLegend.initClass()