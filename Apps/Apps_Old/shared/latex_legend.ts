
import { Legend, LegendView } from "models/annotations/legend"
import { GlyphRendererView } from "models/renderers/glyph_renderer"
import * as p from "core/properties"
import { every } from "core/util/array"
import { Context2d } from "core/util/canvas"
import { div, display } from "core/dom"
import { BBox } from "core/util/bbox"



declare namespace katex {
    function render(expression: string, element: HTMLElement): void
  }


export class LatexLegendView extends LegendView {
    model: LatexLegend

    protected overlay_el: HTMLElement

    initialize(): void {
      super.initialize()
      this.model.orientation = "vertical"

      // set overlay to the correct position
      this.overlay_el = this.plot_view.canvas_view.overlays_el // parent 
      for (const item of this.model.items) {
          const labels = item.get_labels_list_from_label_prop()
          for (let i = 0, end = labels.length; i < end; i++) {
              const el = div({ class: 'bk-annotation-child', style: { display: "none" } })
              //const el = div({ class: 'bk-annotation-child'})
              this.overlay_el.appendChild(el)
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

    // if a max_label_width is defined use this width instead of
    // the standard width, which is not set correctly when using LaTeX
    if (this.model.max_label_width > 0){
      ctx.rect(bbox.x, bbox.y, this.model.max_label_width, bbox.height)  
    }
    else{
      ctx.rect(bbox.x, bbox.y, bbox.width, bbox.height)
    }

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


        const el_latex = this.overlay_el.children[index] as HTMLElement

        this.visuals.label_text.set_value(ctx)

        // set styling of LaTeX output
        el_latex.style.position = 'absolute'
        el_latex.style.left = `${x2 + xoffset}px`
        el_latex.style.top = `${y1}px`
        el_latex.style.color = `${this.visuals.label_text.text_color.value()}`
        el_latex.style.opacity = `${this.visuals.label_text.text_alpha.value()}`
        el_latex.style.font = `${this.visuals.label_text.font_value()}`
        el_latex.style.lineHeight = "normal"

        // render to LaTeX
        try {
          katex.render(labels[0], el_latex)
        } catch (err) {
            el_latex.textContent = err
            el_latex.style.color = "red"
        }

        // don't fill standard text - replaced by LaTeX output
        //ctx.fillText(label, x2 + label_standoff, y1 + this.max_label_height/2.0)

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

          // opcity for inactive legend items
          el_latex.style.opacity = "0.3"
        }

        // display LaTeX output
        display(el_latex)
      }

      index++
    }
  }




}




export namespace LatexLegend {
    export type Attrs = p.AttrsOf<Props>
    export type Props = Legend.Props & { 
      max_label_width: p.Property<number>      
    }
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

        this.define<LatexLegend.Props>({
            max_label_width: [p.Number, 0],
        })
    }
}

LatexLegend.initClass()