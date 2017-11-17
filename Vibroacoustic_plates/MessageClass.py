from bokeh.models import Div


class Message:

    def __init__( self, Color = "red",
                  Size = 4,
                  FontStyle = "b",
                  MessageHeader = 'Message: ',
                  Width = 500,
                  Height = 20 ):

        """
        The class represents a widget based on the "Div" bokeh class. A class instance
        is a message that is supposed to be added to the application. The constructor
        defines a public instance of the "Div" class that the user can access using the
        interface given by the bokeh library. The class defines color, size, font style,
        message header, width and height of the message that use can change in runtime.
        :param Color: python string
        :param Size: int
        :param FontStyle: python string. To find out the available parameters,
        please, have a look at the HTML documentation (font style)
        :param MessageHeader: python string
        :param Width: int
        :param Height: int
        """

        self.Header = MessageHeader
        self.Color = Color
        self.Size = Size
        self.FontStyle = FontStyle

        self.Widget = Div( text = "",
                           render_as_text = False,
                           width = Width,
                           height = Height )


    def clean(self):
        """
        The function erases the message and updates the widget (instance)
        :return:
        """
        self.Text = ''
        self._updateObject( )


    def printMessage(self, Text = 'none'):
        """
        The function combines the header and a user's text to a string and set it up as
        the widget message (instance). Afterwards the function updates the widget
        :param Text: python string
        :return:
        """
        self.Text = self.Header + Text
        self._updateObject()


    def _updateObject(self):
        """
        The function updates the widget in order to display the updated message
        to a browser
        :return:
        """
        self.Widget.text = """
        <p><{}><font size="{}" color="{}">
        {}
        </font></{}></p>""".format( self.FontStyle ,self.Size,
                                    self.Color,self.Text,
                                    self.FontStyle )