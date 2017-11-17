from bokeh.models.widgets import TextInput
from bokeh.layouts import column, row, Spacer
import numpy as np


class TableCorrupted(Exception):
    pass


class InteractiveTable:
    MINIMUM_WIDGET_HEIGHT = 1

    def __init__( self, TableName, Rows, Columns ):
        """
        The class represents a table that consists of bokeh "TextInput" instances.
        The class defines a bokeh "column" instance that the user can use to display
        the table. The class has the interface that user can use to retrieve
        the information from the table. He/she can also use the interface to change
        or modify the entries within the table. The class allows to create buffers
        that the user can use to store some intermediate information. The user has an
        option to switch between the buffers in order to display some previous
        computations
        :param TableName: string
        :param Rows: int
        :param Columns: int
        """

        self.__TableName = TableName
        self.__nRows = Rows
        self.__nColumns = Columns

        # parameters of entries represented by the "TextInput" class
        self.__LableHeight = 65
        self.__LableWidth = 200
        self.__Buffer = { }

        self.__ModeCounter = np.zeros(( Rows, Columns ), dtype = int)
        self.__initWidgets()


    def __initWidgets(self):
        """
        The function initializes the table using bokeh primitives. At the end the
        function defines the bokeh "column" instance that the user can call to
        display the table on a browser
        :return:
        """
        self.__Widgets = []

        # create the entries and set up the default values
        Rows = []
        for i in range( self.__nRows ):
            TextLabels = []
            for j in range( self.__nColumns ):
                TextLabels.append( TextInput( value = "Default Value",
                                              title = "Default Titel",
                                              width = self.__LableWidth ) )

            self.__Widgets.append( TextLabels )
            Rows.append( row( TextLabels ) )


        # create and init a bokeh "coulmn" instance
        Columns = []
        for Row in Rows:
            Columns.append( Row )
        self.Table = column( Columns )



    def addBuffer(self, BufferName, BufferData = None ):
        """
        The function create an additional buffer that the table can use to store some
        intermediate data
        :param BufferName: string
        :param BufferData: python list that has the same size as the table has
        :return:
        """
        if BufferData == None:
            # Fill out the buffer with the default values if the user doesn't
            # provide the buffer data
            aRow = [ "0.0" ] * self.__nColumns
            BufferData = [ aRow ] * self.__nRows

        self.__TestNewBufferData( BufferData )

        self.__Buffer[ str(BufferName) ] = BufferData


    def getBufferData(self, BufferName ):
        """
        The function tests whether there is a buffer that the user has specified. If it
        exists the function returns the buffer to the user. Otherwise, it throws
        the corresponding error
        :param BufferName: string
        :return: list that has the same shape that the table. the list contains
        table entries
        """
        self.__TestBufferName( BufferName )
        return self.__Buffer[ BufferName ]


    def setBufferData(self, BufferName, Data):
        """
        The function sets up or updates the buffer specified by the user. The function
        checks whether there is the buffer that the user requests. If it doesn't exist
        the function throws the corresponding error. Otherwise the buffer is updated with
        the data provided by the user. If data has different dimension in contrast to
        the table one the function throws the corresponding error
        :param BufferName: string
        :param Data: python list that has the same shape as the table
        :return:
        """
        self.__TestBufferName( BufferName )
        self.__TestNewBufferData( Data )

        self.__Buffer[ BufferName ] = Data


    def makeBufferMask(self, BufferName):
        """
        The function copies the current table state to the specified buffer. If there
        is no the buffer with requested name the function throws the corresponding error
        :param BufferName: string
        :return:
        """
        self.__TestBufferName( BufferName )

        for i in range( self.__nRows ):
            for j in range( self.__nColumns ):
                self.__Buffer[ BufferName ][ i ][ j ] = self.__Widgets[ i ][ j ]


    def fillTableWithBufferData(self, BufferName):
        """
        The function fills the table with the values of the buffer the user
        requests. If the buffer doesn't exist the function throws the corresponding error.
        Otherwise the table is updated with the values of the corresponding table
        :param BufferName: string
        :return:
        """
        self.__TestBufferName( BufferName )

        for i in range( self.__nRows ):
            for j in range( self.__nColumns ):
                self.__Widgets[ i ][ j ].value = self.__Buffer[ BufferName ][ i ][ j ]


    def __TestBufferName(self, BufferName):
        """
        The function tests whether there is a buffer with the requested name. If
        there is no such beffer the function throws the corresponding error.
        The function is private and has to be used only within the class
        :param BufferName:
        :return:
        """
        try:
            return self.__Buffer[ BufferName ]

        except KeyError:
            raise TableCorrupted( "table \"{}\" doesn't have the "
                                  "buffer \"{}\"".format( self.__TableName,
                                                          BufferName ) )


    def __TestNewBufferData(self, Data):
        """
        The function checks whether the size of the data passed by the user correlates
        to the shape of the table. If the shape of the data and the table doesn't match
        the function throws the error. The function is private for the class and has to
        be used within the class.

        :param Data: list of floats that has the same shape as the table has
        :return:
        """


        nRows = len( Data )
        nColumns = len( Data[ 0 ] )

        if nRows != self.__nRows or nColumns != self.__nColumns:
            raise TableCorrupted( "error in \"addBuffer\" function. "
                                  "( buffer name:  \"{}\" ) "
                                  "Wrong dimensions of the buffer data. "
                                  "It doesn't match with the number of rows and "
                                  "columns in the table".format( Data ) )

    def setTitels(self, Titels):
        """
        The function sets the names of the table entries that are going to be displayed
        on browser. The function checks whether the input data has the same shape as
        the table has. If it's not the case the function throws the corresponding error
        :param Titels: list of strings
        :return:
        """


        # Check if the input data is consistent i.e.
        # check the number of rows and columns
        if ( len( Titels ) != self.__nRows ):
            raise TableCorrupted( "ERROR from setValues: wrong number of " + \
                                    "rows were passed")

        for Entry in Titels:
            if ( len(Entry) != self.__nColumns ):
                raise TableCorrupted( "ERROR from setValues: wrong number of " + \
                                       "columns were passed")


        # initilize buffers by default values
        self.__TitelBuffer = Titels

        for Row, i in zip( Titels, range( len( Titels ) ) ):
            for Entry, j in zip( Row, range( len( Row ) ) ):
                self.__Widgets[ i ][ j ].title = Titels[ i ][ j ]



    def setValues(self, Values):
        """
        The function sets up the data that the user passes. At the beginning the function
        checks whether the input data has the same shape as the table has. If it is
        violated the function throws the corresponding error
        :param Values: list of strings
        :return:
        """

        # Check if the input data is consistent i.e.
        # check the number of rows and columns
        if ( len( Values ) != self.__nRows ):
            raise TableCorrupted( "ERROR from setValues: wrong number of " +\
                                    "rows were passed")
        for Entry in Values:
            if ( len(Entry) != self.__nColumns ):
                raise TableCorrupted( "ERROR from setValues: wrong number of " +\
                                       "columns were passed")


        # initilize buffers by default values
        #self.__DefaultValues = deepcopy(Values)
        #self.__ValueBuffer = deepcopy(Values)


        for Row, i in zip( Values, range( len( Values ) ) ):
            for Entry, j in zip( Row, range( len( Row ) ) ):
                self.__Widgets[ i ][ j ].value = Values[ i ][ j ]



    def setValue( self, aRow, aColumn, Value, Titel = "\t( auto )" ):
        """
        The function sets up and updates a cprresponding entry of the table
        that is specified by the user. Whenever the user calls the function it
        updates both entry and its title. The current title is expanded with
        a suffix specified by the user.
        :param aRow: int
        :param aColumn: int
        :param Value: string
        :param Titel: string
        :return:
        """

        if self.__ModeCounter[ aRow ][ aColumn ] == 0:
            #self.__ValueBuffer[aRow][aColumn] = self.__Widgets[aRow][aColumn].value
            self.__TitelBuffer[aRow][aColumn] = self.__Widgets[aRow][aColumn].title
            self.__Widgets[aRow][aColumn].title += "{}".format( Titel )

        self.__Widgets[ aRow ][ aColumn ].value = Value
        self.__ModeCounter[ aRow ][ aColumn ] += 1


    def restoreValue( self, aRow, aColumn ):
        """
        The function restores the title of a particular entry of the table

        IMPORTANT: change the name of the function
        :param aRow: int
        :param aColumn: int
        :return:
        """
        if self.__ModeCounter[ aRow ][ aColumn ] != 0:
            #self.__Widgets[aRow][aColumn].value = self.__ValueBuffer[aRow][aColumn]
            self.__Widgets[aRow][aColumn].title = self.__TitelBuffer[aRow][aColumn]
            self.__ModeCounter[ aRow ][ aColumn ] = 0


    def assignValue(self, aRow, aColumn, Value ):
        """
        The function assigns a float value to a particular entry of the table
        :param aRow: int
        :param aColumn: int
        :param Value: float
        :return:
        """
        self.__Widgets[ aRow ][ aColumn ].value = str( Value )


    def assignValuesSet(self, aList):
        """
        The function assigns a list of floats to the table. The function doesn't check
        consistency of the input data shape with the shape of the table. However,
        the function should check it in the next release
        :param aList: list of floats of the same shape as the table has
        :return:
        """
        if type( aList[ 0 ] ) is list:
            Rows = len( aList )
            Columns = len( aList[ 0 ] )
            for i in range( Rows ):
                for j in range( Columns ):
                    self.__Widgets[ i ][ j ].value = str( aList[ i ][ j ] )

        else:
            Length = len( aList )
            for i in range( Length ):
                self.__Widgets[ 0 ][ i ].value = str( aList[ i ] )


    def getValue(self, aRow, aColumn ):
        """
        The function returns the value of the requested table entry as a string
        :param aRow: int
        :param aColumn: int
        :return: string
        """
        return self.__Widgets[ aRow ][ aColumn ].value


    def getFloatValue(self, aRow, aColumn ):
        """
        The function returns the value of the requested table entry as a float value.
        If it's impossible to conver the table entry to a float number the function
        throws the corresponding error
        :param aRow: int
        :param aColumn: int
        :return: float
        """
        try:
            return float( self.__Widgets[ aRow ][ aColumn ].value )
        except ValueError:
            raise TableCorrupted("wrong formant of the "
                                 "entry: {}, {}; table: {}".format( aRow + 1 ,
                                                                    aColumn + 1,
                                                                    self.__TableName))


    #def resetByDefault(self):
    #
    #    self.__ValueBuffer = deepcopy( self.__DefaultValues )
    #    for i in range( self.__nRows ) :
    #        for j in range( self.__nColumns ):
    #            self.__Widgets[ i ][ j ].value = self.__DefaultValues[ i ][ j ]



    def getData( self ):
        """
        The function returns the list of floats where each entry is the corresponding
        value of the table entry. If it's impossible to convert at least one entry
        of the table to float the function throws the corresponding error
        :return: list of float with the same shape as the shape of the table
        """
        Data = []
        for i in range( self.__nRows ):
            Temp = []

            for j in range( self.__nColumns ):
                try:
                    Temp.append( float( self.__Widgets[ i ][ j ].value ) )
                except ValueError:
                    #self.__Widgets[ i ][ j ].value = self.__DefaultValues[ i ][ j ]
                    raise TableCorrupted("wrong formant of the "
                                         "entry: {}, {}; table: {}".format( i + 1,
                                                                            j + 1,
                                                                            self.__TableName))
            Data.append( Temp )

        return Data


    def getRawData( self ):
        """
        The function returns the list of raw data where each entry is the corresponding
        value of the table entry. If it's impossible to convert at least one entry
        of the table to float the function throws the corresponding error
        :return: list of strings
        """
        Data = [ ]
        for i in range( self.__nRows ):
            Temp = [ ]

            for j in range( self.__nColumns ):
                try:
                    Dummy = float( self.__Widgets[ i ][ j ].value )
                    Temp.append( self.__Widgets[ i ][ j ].value )

                except ValueError:
                    #self.__Widgets[ i ][ j ].value = self.__DefaultValues[ i ][ j ]
                    raise TableCorrupted( "wrong formant of the "
                                          "entry: {}, {};"
                                          " table: {}".format( i + 1,
                                                               j + 1,
                                                               self.__TableName ) )
            Data.append( Temp )
        return Data
