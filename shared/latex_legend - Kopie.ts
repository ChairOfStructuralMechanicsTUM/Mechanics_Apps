
import { Legend, LegendView } from "models/annotations/legend"
import { GlyphRendererView } from "models/renderers/glyph_renderer"
//import * as p from "core/properties"
import { every } from "core/util/array"
import { Context2d } from "core/util/canvas"
import { div, show } from "core/dom"
import {BBox} from "core/util/bbox"


declare namespace katex {
    function render(expression: string, element: HTMLElement): void
  }


export class LatexLegendView extends LegendView {
    model: LatexLegend

    protected overlayEl: HTMLElement

    initialize(): void {
      super.initialize()
      this.model.orientation = "vertical"

      // set overlay to the correct position
      this.overlayEl = this.plot_view.canvas_view.overlays_el // parent
      for (const item of this.model.items) {
          const labels = item.get_labels_list_from_label_prop()
          for (let i = 0, end = labels.length; i < end; i++) {
              const el = div({ class: 'bk-annotation-child', style: { display: "none" } })
              //const el = div({ class: 'bk-annotation-child'})
              this.overlayEl.appendChild(el)
          }
      }



  }


render(): void {
    if (!this.model.visible)
      return

    if (this.model.items.length == 0)
      return

    // set a backref on render so that items can later signal item_change upates
    // on the model to trigger a re-render
    for (const item of this.model.items) {
      item.legend = this.model
    }

    const {ctx} = this.plot_view.canvas_view
    const bbox = this.compute_legend_bbox()

    // // bbox.width is now read only!
    // if (this.model.max_label_width > 0) {
    //     bbox.width = this.model.max_label_width
    // }

    ctx.save()
    this._draw_legend_box(ctx, bbox)
    this._draw_legend_items(ctx, bbox)

    if (this.model.title)
      this._draw_title(ctx, bbox)

    ctx.restore()
  }

  protected _draw_legend_box(ctx: Context2d, bbox: BBox): void {
    ctx.beginPath()
    ctx.rect(bbox.x, bbox.y, bbox.width, bbox.height)
    this.visuals.background_fill.set_value(ctx)
    ctx.fill()
    if (this.visuals.border_line.doit) {
      this.visuals.border_line.set_value(ctx)
      ctx.stroke()
    }
  }

  protected _draw_legend_items(ctx: Context2d, bbox: BBox): void {
    const {glyph_width, glyph_height} = this.model
    const {legend_padding} = this
    const legend_spacing = this.model.spacing
    const {label_standoff} = this.model
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
          case "hide": return every(item.renderers, r => r.visible)
          case "mute": return every(item.renderers, r => !r.muted)
        }
      })()

      for (const label of labels) {
        const x1 = bbox.x + xoffset
        const y1 = bbox.y + yoffset + this.title_height
        const x2 = x1 + glyph_width
        const y2 = y1 + glyph_height

        if (vertical)
          yoffset += this.max_label_height + legend_spacing
        else
          xoffset += this.text_widths[label] + glyph_width + label_standoff + legend_spacing


        const el_test = this.overlayEl.children[index] as HTMLElement

        this.visuals.label_text.set_value(ctx)


        el_test.style.position = 'absolute'
        el_test.style.left = `${x2 + xoffset}px`
        el_test.style.top = `${y1}px`
        el_test.style.color = `${this.visuals.label_text.text_color.value()}`
        el_test.style.opacity = `${this.visuals.label_text.text_alpha.value()}`
        el_test.style.font = `${this.visuals.label_text.font_value()}`
        el_test.style.lineHeight = "normal"


        try {
          katex.render(labels[0], el_test)
        } catch (err) {
            el_test.textContent = err
            el_test.style.color = "red"
        }


        for (const r of item.renderers) {
          const view = this.plot_view.renderer_views[r.id] as GlyphRendererView
          view.draw_legend(ctx, x1, x2, y1, y2, field, label, item.index)
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


        show(el_test)
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

        // this.define({
        //     max_label_width: [p.Number, 0],
        // })
    }
}

LatexLegend.initClass()