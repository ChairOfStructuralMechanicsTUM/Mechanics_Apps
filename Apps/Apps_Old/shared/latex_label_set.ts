import {TextAnnotation, TextAnnotationView} from "models/annotations/text_annotation"
import {ColumnarDataSource} from "models/sources/columnar_data_source"
import {ColumnDataSource} from "models/sources/column_data_source"
import {TextVector} from "core/property_mixins"
import {LineJoin, LineCap} from "core/enums"
import {SpatialUnits} from "core/enums"
import {div, display, undisplay} from "core/dom"
import * as p from "core/properties"
import {Size} from "core/layout"
import {Arrayable} from "core/types"
import {Context2d} from "core/util/canvas"


declare namespace katex {
  function render(expression: string, element: HTMLElement, options: {displayMode?: boolean}): void
}

export class LatexLabelSetView extends TextAnnotationView {
  model: LatexLabelSet
  visuals: LatexLabelSet.Visuals

  protected _x: Arrayable<number>
  protected _y: Arrayable<number>
  protected _text: Arrayable<string>
  protected _angle: Arrayable<number>
  protected _x_offset: Arrayable<number>
  protected _y_offset: Arrayable<number>
  protected _display_mode: boolean

    initialize(): void {
    this.model.render_mode = 'css' //LaTeX display only supported in css mode
    
    super.initialize()

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

    const panel = this.panel != null ? this.panel : this.plot_view.frame

    const sx = this.model.x_units == "data" ? xscale.v_compute(this._x) : panel.xview.v_compute(this._x)
    const sy = this.model.y_units == "data" ? yscale.v_compute(this._y) : panel.yview.v_compute(this._y)

    return [sx, sy]
  }

  render(): void {
    
    if (this.el.children.length < this._text.length) {
      for (let i = this.el.children.length, end = this._text.length; i < end; i++) {
        const el = div({class: 'bk-annotation-child', style: {display: "none"}})
        this.el.appendChild(el)
      }
    } else if (this.el.children.length > this._text.length) {
      for (let i = this._text.length, end = this.el.children.length; i < end; i++) {
        if(this.el.lastChild){ // check if it is of None type; if yes, skip
          this.el.removeChild(this.el.lastChild)
        }
      }
    }

    if (!this.model.visible) {
      undisplay(this.el)
    } else{
      display(this.el)
     }

    
    const draw = this._v_css_text.bind(this)
    const {ctx} = this.plot_view.canvas_view

    const [sx, sy] = this._map_data()

    for (let i = 0, end = this._text.length; i < end; i++) {
      draw(ctx, i, this._text[i], sx[i] + this._x_offset[i], sy[i] - this._y_offset[i], this._angle[i])
    }
  }

  protected _get_size(): Size {
    const {ctx} = this.plot_view.canvas_view
    this.visuals.text.set_value(ctx)

    const {width, ascent} = ctx.measureText(this._text[0])
    return {width, height: ascent}
  }

  protected _v_css_text(ctx: Context2d, i: number, text: string, sx: number, sy: number, angle: number): void {
    /** TODO: the css text appears on top of other elements in the bokeh app. perhaps it is possible to make
    katex compatible to the render_mode='canvas' option */
    const el = this.el.children[i] as HTMLElement
    el.textContent = text
    try {
      katex.render(el.textContent, el, { displayMode: this._display_mode })
    } catch (err) {
      el.textContent = err
    }
    
    this.visuals.text.set_vectorize(ctx, i)
    const bbox_dims = this._calculate_bounding_box_dimensions(ctx, text)
    
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
    
    
    const bbox_bounds = this.plot_view.frame.bbox
    // if the label position is outside of the box, do not display it
    if(sx < bbox_bounds.x0 || sx > bbox_bounds.x1 ||
      sy < bbox_bounds.y0 || sy > bbox_bounds.y1)
    {
     el.style.display = "none"
    }
    else{
     display(el)
    }

  }
}

export namespace LatexLabelSet {
  export type Attrs = p.AttrsOf<Props>

  export type Props = TextAnnotation.Props & TextVector & {
    x: p.NumberSpec
    y: p.NumberSpec
    x_units: p.Property<SpatialUnits>
    y_units: p.Property<SpatialUnits>
    text: p.StringSpec
    angle: p.AngleSpec
    x_offset: p.NumberSpec
    y_offset: p.NumberSpec
    source: p.Property<ColumnarDataSource>
    x_range_name: p.Property<string>
    y_range_name: p.Property<string>
    display_mode: p.Property<boolean>

    // line:border_ v
    border_line_color: p.ColorSpec
    border_line_width: p.NumberSpec
    border_line_alpha: p.NumberSpec
    border_line_join: p.Property<LineJoin>
    border_line_cap: p.Property<LineCap>
    border_line_dash: p.Property<number[]>
    border_line_dash_offset: p.Property<number>

    // fill:background_ v
    background_fill_color: p.ColorSpec
    background_fill_alpha: p.NumberSpec
  }

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

    this.define<LatexLabelSet.Props>({
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