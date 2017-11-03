class Flag:
    """ This class is created to make built-in python variables to be mutable"""

    def __init__( self, Input ):
        self.__Value = Input

    def getFlag(self):
        return self.__Value


    def setFlag(self, Input ):
        self.__Value = Input


class DataCorrupted(Exception):
    pass


def testInputData( Mode, Nu):

    if ( Mode == 0 ):
        # Checking criteria for stability all values must be positive
        FirstTerm = Nu[ 0 ][ 0 ] * Nu[ 1 ][ 0 ]
        SecondTerm = Nu[ 0 ][ 1 ] * Nu[ 1 ][ 1 ]
        ThirdTerm = Nu[ 0 ][ 2 ] * Nu[ 1 ][ 2 ]
        FourthTerm = 2.0 * Nu[ 0 ][ 0 ] * Nu[ 0 ][ 2 ] * Nu[ 1 ][ 1 ]

        CheckOne = 1 - FirstTerm
        CheckTwo = 1 - SecondTerm
        CheckThree = 1 - ThirdTerm
        CheckFour = 1 - FirstTerm - SecondTerm - ThirdTerm - FourthTerm

        if CheckOne < 0 or CheckTwo < 0 or CheckThree < 0 or CheckFour < 0:
            raise DataCorrupted("The material property is not feasible")

    if (Mode == 1):

        Threshold = 0.49

        if Nu[ 0 ][ 0 ] > Threshold or Nu[ 0 ][ 1 ] > Threshold or Nu[ 0 ][ 2 ] > Threshold:
            raise DataCorrupted("The material property is not feasible.</p>"
                                "<p> Current mode: ISOTROPIC; Threshold: 0.49 </p>"
                                "<p> Change: POISSON'S RATIOS VALUE")
        pass


def isInputNegative( Input ):

    nColumns = 0
    nRows = 0
    if type(Input[ 0 ]) == list:

        nColumns = len( Input[ 0 ] )
        nRows = len( Input )

        for i in xrange( nRows ):
            for j in xrange( nColumns ):
                if Input[ i ][ j ] < 0:
                    raise DataCorrupted("the material properties are not feasible" )

    else:

        for i in xrange( len( Input ) ):

            if Input[ i ] < 0:
                raise DataCorrupted("the material properties are not feasible" )



class WrongLayersThikness(Exception):
    pass


def getLayersFromString( aString ):

    LayersThickness = parseString( aString )
    checkLayerConsistency( LayersThickness )
    Layers = mirrorLayers( LayersThickness )

    return Layers


def parseString( aString ):
    DILIMETERS = [';','|']
    EMPTY_STRING = ''

    Words = aString.split()

    # Go through all dilimeters and parse whatever it's possible to parse
    for Dilimeter in DILIMETERS:
        TempDictionary = []

        for aWord in Words:
            TempList = aWord.split( Dilimeter )

            for Element in TempList:
                if Element != EMPTY_STRING:
                    TempDictionary.append( Element )

        Words = TempDictionary

    # try to cast all words to floats. Catch and process the error if it's possible
        LayersThickness = []
    try:
        for aWord in Words:
            LayersThickness.append( float(aWord) )

    except:
        raise WrongLayersThikness( "The data format for the layers thickness is wrong. "
                                   "The delimiter can be comma, semicolon or space.")

    return LayersThickness

def checkLayerConsistency( Layers ):

    for Layer in Layers:
        if Layer < 0.0:
            raise WrongLayersThikness("The thickness of one of the layers "
                                      "has its negative value")
        if Layer == 0.0:
            raise WrongLayersThikness("The thickness of one of the layers "
                                      "is eqaul to zero" )

    pass

def mirrorLayers( TopLayers ):

    nTopLayers = len( TopLayers )
    if nTopLayers == 1:
        # Return the input data if there is only one layer
        return TopLayers

    nLayers = 2 * ( nTopLayers -1 ) + 1
    Layers = [ 0.0 ] * nLayers

    for i in range( nTopLayers ):
       Layers[ i ] = TopLayers[ i ]
       Layers[ -1 - i ] = TopLayers[ i ]

    return Layers