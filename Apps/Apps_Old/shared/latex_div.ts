import { Markup, MarkupView } from "models/widgets/markup"
import { div } from "core/dom"
import * as p from "core/properties"

declare namespace katex {
  function render(expression: string, element: HTMLElement, options: {displayMode?: boolean}): void
}


export class LatexDivView extends MarkupView {
  model: LatexDiv

  render(): void {
    super.render()
    var content = div()
    if (this.model.render_as_text)
      content.textContent = this.model.text
    else {
      content.innerHTML = this.model.text
      this.myrender(content)
    }
    this.markup_el.appendChild(content)
  }
  
  myrender(content: any): void {
    // taken from http://sixthform.info/katex/guide.html
    // first, replace all $$ 
    content.innerHTML = content.innerHTML.replace(/(\$\$){1}([\s\S]+?)(\$\$){1}/g, '<div class=\"maths\">$2</div>');
    // replace text dollar signs by %​% temporarily then
    // replace $...$ by <span class="maths">...</span>
    // regular expression \$([\s\S]+?)\$/g consists of all whitespace \s 
    // and non-whitespace characters \S between the dollar signs. See [4]
    content.innerHTML = content.innerHTML.replace(/\\\$/g, '\%\%');
    content.innerHTML = content.innerHTML.replace(/\$([\s\S]+?)\$/g, '<span class=\"maths\">$1</span>');
    // replace \[ ...\] by <div class="maths"> ... </div>
    // but don't replace eg \\[1ex] so temporarily rename them
    // content.innerHTML = content.innerHTML.replace(/\\\\\[/g, '%​%​%');
    content.innerHTML = content.innerHTML.replace(/\\\\\]/g, '%​%​%');
    content.innerHTML = content.innerHTML.replace(/\\\[/g, '<div class=\"maths\">');
    content.innerHTML = content.innerHTML.replace(/\\\]/g, '</div>');
    // put back eg \\[1ex]
    content.innerHTML = content.innerHTML.replace(/%​%​%/g, '\\\\\]');
    // replace \( ...\) by <span class="maths"> ... </span>
    content.innerHTML = content.innerHTML.replace(/\\\(/g, '<span class=\"maths\">');
    content.innerHTML = content.innerHTML.replace(/\\\)/g, '</span>');
    // put back text dollar signs
    content.innerHTML = content.innerHTML.replace(/\%\%/g, '\$');

    // Get all <div or span or p class ="maths"> elements in the document
    var x = content.getElementsByClassName('maths');
    for (var i = 0; i < x.length; i++) {
      // t= katex.render(x[i].textContent,x[i],{ displayMode: true }); 
      // console.log(t)
      try {
        if (x[i].tagName == "DIV") {
          katex.render(x[i].textContent, x[i], { displayMode: true  });
        } else {
          katex.render(x[i].textContent, x[i], { displayMode: false });
        }
      }
      catch (err) {
        console.log('err')
        x[i].style.color = 'red';
        x[i].textContent = err;
      }

    }

    // Optional. Allows use of delimiters in document without them being replaced
    // Use \$ or %​% for $, %​[ for \[, %​] for \], %​( for \(, %​) for \)
    // the following will convert them to the appropriate delimiters
    // content.innerHTML = content.innerHTML.replace(/\%\\[/g, '\\\[');
    // content.innerHTML = content.innerHTML.replace(/\%\\]/g, '\\\]');
    // content.innerHTML = content.innerHTML.replace(/\%\\(/g, '\\\(');
    // content.innerHTML = content.innerHTML.replace(/\%\\)/g, '\\\)');  
  }
}

// export namespace LatexDiv {
//   export interface Attrs extends Markup.Attrs {
//     render_as_text: boolean
//   }

//   export interface Props extends Markup.Props { }
// }

export namespace LatexDiv {
  export type Attrs = p.AttrsOf<Props> 

  export type Props = Markup.Props & {
    render_as_text: p.Property<boolean>
  }
}

export interface LatexDiv extends LatexDiv.Attrs { }

export class LatexDiv extends Markup {

  properties: LatexDiv.Props

  constructor(attrs?: Partial<LatexDiv.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    this.prototype.type = "LatexDiv"
    this.prototype.default_view = LatexDivView

    this.define<LatexDiv.Props>({
      render_as_text: [p.Boolean, false],
    })
  }
}

LatexDiv.initClass()