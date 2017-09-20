from bokeh.plotting import figure
from bokeh.models.widgets import RadioButtonGroup
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import row, column, Spacer
from bokeh.plotting import figure, reset_output
from bokeh.models import Legend
from copy import deepcopy
from MessageClass import Message
from bokeh.models.annotations import LegendItem

class GraphCorrupted(Exception):
    pass


class GraphObject:
    """
    That class was designed to hold all necessary data and widgets in one place.
    The class represents one complex widget that consists of three independent
    bokeh widgets, namely: figure, Div and RadioButtonGroup. These widget
    have to communicate to each other passing all relevant information like
    flags, active buttons etc. A user has to pass a list with the names
    of corresponding graphs that is going to be depicted in the
    RadioButtonGroup widget and the range of cuntions
    """

    # Private class variables
    IMAGE_COUNTER = 0;
    _MAX_NUMBER_OF_LINES = 15
    _MAX_NUMBER_OF_DOTTED_LINES = 3

    def __init__( self, GraphNames, aRange, Width = 650, Height = 550 ):

        self.Width = Width
        self.Height = Height
        #.................. Set up all necessary variables ....................
        if len( GraphNames ) == 0:
            raise GraphCorrupted( "ERROR: the list of graph names is empty" )
        else:
            self.__GraphNames = GraphNames


        if len( aRange ) == 0:
            raise GraphCorrupted( "ERROR: the list of argument values is empty" )
        else:
            self.__Range = aRange


        # Mode represents to states, namely: orthotropic(0) and isotropic(1)
        self.__Mode = 0
        self.__PlottingGraphNumber = 0;


        # ......... Initialize all widgets for that particular class ...........

        self.TextWidget = Message( Color = "Black",
                                   Size = 2 ,
                                   FontStyle = "n",
                                   MessageHeader = "",
                                   Width = self.Width  );



        self.GraphRadioButtons = RadioButtonGroup( labels = self.__GraphNames,
                                                   width = self.Width ,
                                                   active = 0 )

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
        self.Graph = figure( title = "",
                             width = self.Width,
                             height = Height,
                             y_axis_type = "log",
                             x_axis_type = "log",
                             tools = TOOLS,
                             toolbar_location = "above",
                             x_range = [1, 10000] )

        self.Graph.y_range.range_padding = 0.0

        self.Graph.yaxis.axis_label = "Default"
        self.Graph.xaxis.axis_label = "Default"

        # Assign lines to the graph and generate the legend
        self.Lines = [ ]
        LegendItems = [ ]
        self.GraphData = [ ]
        for i in range( GraphObject._MAX_NUMBER_OF_LINES ):

            self.GraphData.append( ColumnDataSource( data = dict( XData = [ ],
                                                                  YData = [ ] ) ) )

            self.Lines.append( self.Graph.line( x = 'XData',
                                                y = 'YData',
                                                color = 'black',
                                                line_dash = 'solid',
                                                source = self.GraphData[ i ] ) )

            LegendItems.append( ( "default", [ self.Lines[ i ] ] ) )


        self.Circles = [ ]
        for i in range( GraphObject._MAX_NUMBER_OF_DOTTED_LINES ):

            self.Circles.append( self.Graph.circle( x = [ ],
                                                    y = [ ],
                                                    size = 3.0,
                                                    line_color = "black",
                                                    fill_color = "white",
                                                    line_width = 3 ) )

        legend = Legend( items = LegendItems, location = (0, -30) )
        self.Graph.add_layout( legend, 'right' )



        # Create one common widget that is going to represent the entire class
        self.Widget = row( column( self.GraphRadioButtons,
                                   self.Graph,
                                   self.TextWidget.Widget ) )



    # SETTERS
    def setRange( self, aRange ):
        if len( aRange ) == 0:
            raise GraphCorrupted( "ERROR: the list of argument values is empty" )
        else:
            self.__Range = aRange


    def setMode( self, aMode ):
        if ( aMode != 0 ) and ( aMode != 1 ):
            raise GraphCorrupted( "ERROR: a wrong mode was set" )
        else:
            self.__Mode = aMode


    def setPlottingGraphNumber( self, Number ):
        self.__PlottingGraphNumber = Number



    # GETTERS
    def getRange(self):
        return deepcopy( self.__Range )


    def getMode(self):
        return self.__Mode


    def getCurrentGraphNumber(self):
        return self.__PlottingGraphNumber


    def cleanGraph(self):

        for i in range( GraphObject._MAX_NUMBER_OF_LINES ):
            self.Graph.legend[ 0 ].items[ i ].label[ 'value' ] = ""
            self.GraphData[ i ].data = dict(XData = [], YData = [])
            self.Lines[ i ].glyph.line_color = 'white'


        for i in range( GraphObject._MAX_NUMBER_OF_DOTTED_LINES ):

            # remove circles from the graph
            self.Circles[ i ].data_source.data.update( { "x": [],"y": [] } )

            # adjust the legend of the top lines
            self.Graph.legend[ 0 ].items[ i ] = LegendItem( label = "",
                                                            renderers = [ self.Lines[ i ] ] )

    def defineLine(self, ID ,Name, Color, Style):
        '''
        :param ID: type:integer :: index of the line
        :param Name: type:string :: name of the line on the legend
        :param Color: type:string :: color of the line (According to Bokeh)
        :param Style: type:string :: style of the line (According to Bokeh)
        :return:
        '''
        self.Lines[ ID ].glyph.line_color = Color
        self.Lines[ ID ].glyph.line_dash = Style
        self.Graph.legend[ 0 ].items[ ID ].label[ 'value' ] = Name

        pass

    def defineContainers(self, Keys = None):
        '''

        :param Keys: a list of keys for the Containers. Containers have their
         data structure as a dictionary
         Throw an error if the user doesn't specify the keys
        :return:
        '''
        if Keys == None:
            raise( Exception )

        self.Containers = { Key : [] for Key in Keys }
