
# copied from the bokeh examples
# https://github.com/bokeh/bokeh/tree/master/examples/app/surface3d

#-----------------------------------------------------#


from bokeh.core.properties import Any, Dict, Instance, String
from bokeh.models import ColumnDataSource, LayoutDOM

# This defines some default options for the Graph3d feature of vis.js
# See: http://visjs.org/graph3d_examples.html for more details. Note
# that we are fixing the size of this component, in ``options``, but
# with additional work it could be made more responsive.
DEFAULTS = {
    'width':          '500px',
    'height':         '500px',
    'style':          'surface',
    'showPerspective': True,
    'showGrid':        False,
    'keepAspectRatio': True,
    'verticalRatio':   0.2,
    'zMin': -2.0,
    'zMax': +2.0,
    'cameraPosition':  {
        'horizontal': -0.8,
        'vertical':    0.6,
        'distance':    1.6,
    }
}

# This custom extension model will have a DOM view that should layout-able in
# Bokeh layouts, so use ``LayoutDOM`` as the base class. If you wanted to create
# a custom tool, you could inherit from ``Tool``, or from ``Glyph`` if you
# wanted to create a custom glyph, etc.
class diffraction_Surface3d(LayoutDOM):

    # The special class attribute ``__implementation__`` should contain a string
    # of JavaScript (or TypeScript) code that implements the JavaScript side
    # of the custom extension model.
    __implementation__ = "diffraction_surface3d.ts"
    # this is the local resource for the vis.js library
    __javascript__ = ["https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"] ## online resource
    #__javascript__ = ["Diffraction/static/js/vis.min.js"] ## offline resource


    # Below are all the "properties" for this model. Bokeh properties are
    # class attributes that define the fields (and their types) that can be
    # communicated automatically between Python and the browser. Properties
    # also support type validation. More information about properties in
    # can be found here:
    #
    #    https://docs.bokeh.org/en/latest/docs/reference/core/properties.html#bokeh-core-properties

    # This is a Bokeh ColumnDataSource that can be updated in the Bokeh
    # server by Python code
    data_source = Instance(ColumnDataSource)

    # The vis.js library that we are wrapping expects data for x, y, and z.
    # The data will actually be stored in the ColumnDataSource, but these
    # properties let us specify the *name* of the column that should be
    # used for each field.
    x = String

    y = String

    z = String

    # color might not be used from vis.js
    color = String

    # Any of the available vis.js options for Graph3d can be set by changing
    # the contents of this dictionary.
    options = Dict(String, Any, default=DEFAULTS)