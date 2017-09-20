from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput
from bokeh.layouts import column, row, Spacer
from copy import deepcopy

import numpy as np
from copy import deepcopy


class TableCorrupted(Exception):
    pass


class InteractiveTable:
    MINIMUM_WIDGET_HEIGHT = 1

    def __init__( self, TableName, Rows, Columns ):
        self.__TableName = TableName
        self.__nRows = Rows
        self.__nColumns = Columns

        self.__LableHeight = 65
        self.__LableWidth = 200
        self.__Buffer = { }

        self.__ModeCounter = np.zeros(( Rows, Columns ), dtype = int)

        self.__initWidgets()


    def __initWidgets(self):
        self.__Widgets = []

        # TODO: add comments
        Rows = []
        for i in range( self.__nRows ):
            TextLabels = []
            for j in range( self.__nColumns ):
                TextLabels.append( TextInput( value = "Default Value",
                                              title = "Default Titel",
                                              width = self.__LableWidth ) )

            self.__Widgets.append( TextLabels )
            Rows.append( row( TextLabels ) )


        Columns = []
        for Row in Rows:
            Columns.append( Row )
        self.Table = column( Columns )



    def addBuffer(self, BufferName, BufferData = None ):

        if BufferData == None:
            # Fill out the buffer with the default values if the user doesn't
            # provide the buffer data
            aRow = [ "0.0" ] * self.__nColumns
            BufferData = [ aRow ] * self.__nRows

        self.__TestNewBufferData( BufferData )

        self.__Buffer[ str(BufferName) ] = BufferData


    def getBufferData(self, BufferName ):
        self.__TestBufferName( BufferName )
        return self.__Buffer[ BufferName ]


    def setBufferData(self, BufferName, Data):
        self.__TestBufferName( BufferName )
        self.__TestNewBufferData( Data )

        self.__Buffer[ BufferName ] = Data


    def makeBufferMask(self, BufferName):
        self.__TestBufferName( BufferName )

        for i in range( self.__nRows ):
            for j in range( self.__nColumns ):
                self.__Buffer[ BufferName ][ i ][ j ] = self.__Widgets[ i ][ j ]


    def fillTableWithBufferData(self, BufferName):
        self.__TestBufferName( BufferName )

        for i in range( self.__nRows ):
            for j in range( self.__nColumns ):
                self.__Widgets[ i ][ j ].value = self.__Buffer[ BufferName ][ i ][ j ]


    def __TestBufferName(self, BufferName):

        try:
            return self.__Buffer[ BufferName ]

        except KeyError:
            raise TableCorrupted( "table \"{}\" doesn't have the "
                                  "buffer \"{}\"".format( self.__TableName,
                                                          BufferName ) )


    def __TestNewBufferData(self, Data):


        nRows = len( Data )
        nColumns = len( Data[ 0 ] )

        if nRows != self.__nRows or nColumns != self.__nColumns:
            raise TableCorrupted( "error in \"addBuffer\" function. "
                                  "( buffer name:  \"{}\" ) "
                                  "Wrong dimensions of the buffer data. "
                                  "It doesn't match with the number of rows and "
                                  "columns in the table".format( Data ) )

    def setTitels(self, Titels):

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

        if self.__ModeCounter[ aRow ][ aColumn ] == 0:
            #self.__ValueBuffer[aRow][aColumn] = self.__Widgets[aRow][aColumn].value
            self.__TitelBuffer[aRow][aColumn] = self.__Widgets[aRow][aColumn].title
            self.__Widgets[aRow][aColumn].title += "{}".format( Titel )

        self.__Widgets[ aRow ][ aColumn ].value = Value
        self.__ModeCounter[ aRow ][ aColumn ] += 1


    def restoreValue( self, aRow, aColumn ):
        if self.__ModeCounter[ aRow ][ aColumn ] != 0:
            #self.__Widgets[aRow][aColumn].value = self.__ValueBuffer[aRow][aColumn]
            self.__Widgets[aRow][aColumn].title = self.__TitelBuffer[aRow][aColumn]
            self.__ModeCounter[ aRow ][ aColumn ] = 0


    def assignValue(self, aRow, aColumn, Value ):
        self.__Widgets[ aRow ][ aColumn ].value = str( Value )


    def assignValuesSet(self, aList):

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
        return self.__Widgets[ aRow ][ aColumn ].value


    def getFloatValue(self, aRow, aColumn ):
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
