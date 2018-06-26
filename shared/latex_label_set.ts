import {TextAnnotation, TextAnnotationView} from "models/annotations/text_annotation"
import {ColumnarDataSource} from "models/sources/columnar_data_source"
import {ColumnDataSource} from "models/sources/column_data_source"
import {NumberSpec, AngleSpec, StringSpec, ColorSpec} from "core/vectorization"
import {TextMixinVector} from "core/property_mixins"
import {LineJoin, LineCap} from "core/enums"
import {SpatialUnits} from "core/enums"
import {div, show, hide} from "core/dom"
import * as p from "core/properties"
import {Arrayable} from "core/types"
import {Context2d} from "core/util/canvas"

export class LatexLabelSetView extends TextAnnotationView {
  model: LatexLabelSet
  visuals: LatexLabelSet.Visuals

  protected _x: Arrayable<number>
  protected _y: Arrayable<number>
  protected _text: Arrayable<string>
  protected _angle: Arrayable<number>
  protected _x_offset: Arrayable<number>
  protected _y_offset: Arrayable<number>
  protected _display_mode: Boolean

  initialize(options: any): void {
    this.model.render_mode = 'css' //LaTeX display only supported in css mode
    
    super.initialize(options)

    this.set_data(this.model.source)
    
    for (let i = 0, end = this._text.length; i < end; i++) {
      const el = div({class: 'bk-annotation-child', style: {display: "none"}})
      this.el.appendChild(el)
    }
  }

  connect_signals(): void {
    super.connect_signals()
  
    this.connect(this.model.change, () => {
      this.set_data(this.model.source)
      this.render()
    })
    this.connect(this.model.source.streaming, () => {
      this.set_data(this.model.source)
      this.render()
    })
    this.connect(this.model.source.patching, () => {
      this.set_data(this.model.source)
      this.render()
    })
    this.connect(this.model.source.change, () => {
      this.set_data(this.model.source)
      this.render()
    })
  }

  set_data(source: ColumnarDataSource): void {
    super.set_data(source)
    this.visuals.warm_cache(source)
  }

  protected _map_data(): [Arrayable<number>, Arrayable<number>] {
    const xscale = this.plot_view.frame.xscales[this.model.x_range_name]
    const yscale = this.plot_view.frame.yscales[this.model.y_range_name]

    const panel = this.model.panel != null ? this.model.panel : this.plot_view.frame

    const sx = this.model.x_units == "data" ? xscale.v_compute(this._x) : panel.xview.v_compute(this._x)
    const sy = this.model.y_units == "data" ? yscale.v_compute(this._y) : panel.yview.v_compute(this._y)

    return [sx, sy]
  }

  render(): void {
    if (!this.model.visible) {
      hide(this.el)
    }

    const draw = this._v_css_text.bind(this)
    const {ctx} = this.plot_view.canvas_view

    const [sx, sy] = this._map_data()

    for (let i = 0, end = this._text.length; i < end; i++) {
      draw(ctx, i, this._text[i], sx[i] + this._x_offset[i], sy[i] - this._y_offset[i], this._angle[i])
    }
  }

  protected _get_size(): number {
    const {ctx} = this.plot_view.canvas_view
    this.visuals.text.set_value(ctx)

    switch (this.model.panel!.side) {
      case "above":
      case "below": {
        const height = ctx.measureText(this._text[0]).ascent
        return height
      }
      case "left":
      case "right": {
        const {width} = ctx.measureText(this._text[0])
        return width
      }
      default:
        throw new Error("unreachable code")
    }
  }

  protected _v_css_text(ctx: Context2d, i: number, text: string, sx: number, sy: number, angle: number): void {
    const el = this.el.children[i] as HTMLElement
    el.textContent = text
    katex.render(el.textContent, el, { displayMode: this.model.display_mode })

    this.visuals.text.set_vectorize(ctx, i)
    const bbox_dims = this._calculate_bounding_box_dimensions(ctx, el.textContent)
    
    // attempt to support vector-style ("8 4 8") line dashing for css mode
    const ld = this.visuals.border_line.line_dash.value()
    const line_dash = ld.length < 2 ? "solid" : "dashed"

    this.visuals.border_line.set_vectorize(ctx, i)
    this.visuals.background_fill.set_vectorize(ctx, i)

    el.style.position = 'absolute'
    el.style.left = `${sx + bbox_dims[0]}px`
    el.style.top = `${sy + bbox_dims[1]}px`
    el.style.color = `${this.visuals.text.text_color.value()}`
    el.style.opacity = `${this.visuals.text.text_alpha.value()}`
    el.style.font = `${this.visuals.text.font_value()}`
    el.style.lineHeight = "normal"  // needed to prevent ipynb css override
    if (angle) {
      el.style.transform = `rotate(${angle}rad)`
    }

    if (this.visuals.background_fill.doit) {
      el.style.backgroundColor = `${this.visuals.background_fill.color_value()}`
    }

    if (this.visuals.border_line.doit) {
      el.style.borderStyle = `${line_dash}`
      el.style.borderWidth = `${this.visuals.border_line.line_width.value()}px`
      el.style.borderColor = `${this.visuals.border_line.color_value()}`
    }

    show(el)
  }
}

export namespace LatexLabelSet {
  // line:border_ v
  export interface BorderLine {
    border_line_color: ColorSpec
    border_line_width: NumberSpec
    border_line_alpha: NumberSpec
    border_line_join: LineJoin
    border_line_cap: LineCap
    border_line_dash: number[]
    border_line_dash_offset: number
  }

  // fill:background_ v
  export interface BackgroundFill {
    background_fill_color: ColorSpec
    background_fill_alpha: NumberSpec
  }

  export interface Mixins extends TextMixinVector, BorderLine, BackgroundFill {}

  export interface Attrs extends TextAnnotation.Attrs, Mixins {
    x: NumberSpec
    y: NumberSpec
    x_units: SpatialUnits
    y_units: SpatialUnits
    text: StringSpec
    angle: AngleSpec
    x_offset: NumberSpec
    y_offset: NumberSpec
    source: ColumnarDataSource
    x_range_name: string
    y_range_name: string
    display_mode: boolean
  }

  export interface Props extends TextAnnotation.Props {}

  export type Visuals = TextAnnotation.Visuals
}

export interface LatexLabelSet extends LatexLabelSet.Attrs {}

export class LatexLabelSet extends TextAnnotation {

  properties: LatexLabelSet.Props

  constructor(attrs?: Partial<LatexLabelSet.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    this.prototype.type = 'LatexLabelSet'
    this.prototype.default_view = LatexLabelSetView

    this.mixins(['text', 'line:border_', 'fill:background_'])

    this.define({
      x:            [ p.NumberSpec                      ],
      y:            [ p.NumberSpec                      ],
      x_units:      [ p.SpatialUnits, 'data'            ],
      y_units:      [ p.SpatialUnits, 'data'            ],
      text:         [ p.StringSpec,   { field: "text" } ],
      angle:        [ p.AngleSpec,    0                 ],
      x_offset:     [ p.NumberSpec,   { value: 0 }      ],
      y_offset:     [ p.NumberSpec,   { value: 0 }      ],
      source:       [ p.Instance,     () => new ColumnDataSource()  ],
      x_range_name: [ p.String,      'default'          ],
      y_range_name: [ p.String,      'default'          ],
      display_mode: [ p.Boolean,      false             ],
    })

    this.override({
      background_fill_color: null,
      border_line_color: null,
    })
  }
}
LatexLabelSet.initClass()