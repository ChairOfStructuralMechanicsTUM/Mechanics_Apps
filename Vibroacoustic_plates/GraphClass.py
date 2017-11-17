from bokeh.models.widgets import RadioButtonGroup
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import row, column, Spacer
from bokeh.plotting import figure, reset_output
from bokeh.models import Legend
from copy import deepcopy
from MessageClass import Message
from bokeh.models.annotations import LegendItem
from bokeh.models.glyphs import ImageURL

class GraphCorrupted(Exception):
    pass


class GraphObject:
    # Private class variables
    IMAGE_COUNTER = 0;
    _MAX_NUMBER_OF_LINES = 15
    _MAX_NUMBER_OF_DOTTED_LINES = 3

    def __init__( self, GraphNames, aRange, Width = 650, Height = 550 ):
        """
        The class wraps together several bokeh classes, namely: figure, RadioButtonGroup
        and user-defined class Message. It introduces an abstraction that is
        easy to handle together.

        Within the constructor all lines and labels are defined and the user has to use
        the defined interface of the class to display lines or change the title of
        a particular line.

        An instance of the class also contains a private variable called "Mode" that
        allows to store and distinguish whether it is the Isotropic or Orthotropic case.
        The use can always get the information about the current mode using the
        corresponding interface function.

        The class contains bokeh "RadioButtonGroup" class. Using that the use can
        change the behavior of the class in order to display another piece of information
        in runtime. Using the interface the user can find out what the current tag
        is turned on and assigned other values to lines

        To keep the figure (graph) consistent the user has to provide an instance with
        the range of values along the x axis.

        The class defines the variable called "Widget" that is based on the bokeh
        "column" class. The user has to use "Widget" and use the bokeh interface in order
        to display the class on a browser

        The class allows the user to define containers for data that he/she has computed
        for the graph. It means that the user doesn't have to carry the computed data
        from one function to another. He/she can simply put the data to a container
        and then only pass the current instance of the class within the application

        :param GraphNames: list of strings
        :param aRange: list of floats
        :param Width: int
        :param Height: int
        """

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


        # ........................ Initialize all widgets ..........................

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

        # .............. Assign lines to the graph and generate the legend ..............
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
        """
        The function sets the range of values along the x axis. If the range is just a
        float value the function throws the corresponding error
        :param aRange: list of floats
        :return:
        """
        if len( aRange ) == 0:
            raise GraphCorrupted( "ERROR: the list of argument values is empty" )
        else:
            self.__Range = aRange


    def setMode( self, aMode ):
        """
        The function sets up the mode. If the mode value is not either 0 or 1
        the function throws the corresponding error
        :param aMode: int (0 or 1)
        :return:
        """
        if ( aMode != 0 ) and ( aMode != 1 ):
            raise GraphCorrupted( "ERROR: a wrong mode was set" )
        else:
            self.__Mode = aMode


    def setPlottingGraphNumber( self, Number ):
        """
        The function sets the plot number that can be later retrieved by the user
        :param Number: int
        :return:
        """
        self.__PlottingGraphNumber = Number



    # GETTERS
    def getRange(self):
        """
        The function returns the range of values along the x axis
        :return: list of floats
        """
        return deepcopy( self.__Range )


    def getMode(self):
        """
        The function returns the current mode
        :return: int (0 or 1)
        """
        return self.__Mode


    def getCurrentGraphNumber(self):
        """
        The function returns the current plot number
        :return: int
        """
        return self.__PlottingGraphNumber


    # INTERFACE
    def cleanGraph(self):
        """
        The function cleans the figure (graph) assigning the empy list of all lines.
        The function also removes all line labels

        :return:
        """
        for i in range( GraphObject._MAX_NUMBER_OF_LINES ):
            self.Graph.legend[ 0 ].items[ i ].label[ 'value' ] = ""
            self.GraphData[ i ].data = dict(XData = [], YData = [])
            self.Lines[ i ].glyph.line_color = 'white'


        for i in range( GraphObject._MAX_NUMBER_OF_DOTTED_LINES ):

            # remove circles from the graph
            self.Circles[ i ].data_source.data.update( { "x": [],"y": [] } )

            # adjust the legend of the top lines
            self.Graph.legend[ 0 ].items[ i ] \
                                = LegendItem( label = "",
                                              renderers = [ self.Lines[ i ] ] )

    def defineLine(self, ID ,Name, Color, Style):
        """
        The function defines properties of a line. The user has to specify the line ID
        the class contains in order to change properties of a particular line. It is
        important to keep the order i.e. you have to start from the line with ID = 0,
        and iterate with the step 1.
        :param ID: int
        :param Name: string
        :param Color: string (according the bokeh documentation)
        :param Style: string (according the bokeh documentation)
        :return:
        """

        self.Lines[ ID ].glyph.line_color = Color
        self.Lines[ ID ].glyph.line_dash = Style
        self.Graph.legend[ 0 ].items[ ID ].label[ 'value' ] = Name


    def defineContainers(self, Keys = None):
        """
        The function defines the possible containers that the class can carry. Whenever
        the user computes something based on frequency (range) he/she can store the result
        in the corresponding container. It means that the user doesn't have to carry the
        computed data from one function to another. He/she can simply put the data to
        a container and then only pass the current instance of the class within
        the application.
        :param Keys: list os string
        :return:
        """

        if Keys == None:
            raise( Exception )

        self.Containers = { Key : [] for Key in Keys }
