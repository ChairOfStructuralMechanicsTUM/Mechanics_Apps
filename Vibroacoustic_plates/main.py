# Link bokeh libraries
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer
from bokeh.io import curdoc, show, set_curdoc
from bokeh.models import Div, Label, Plot, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.models.glyphs import Text
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider
from bokeh.models.widgets import TextInput, AutocompleteInput
from bokeh.plotting import figure


# Link third-party python libraries
from math import cos, sin, radians, sqrt, pi, atan2
from functools import partial
import matplotlib.pyplot as plt
import threading
from multiprocessing import Process
import time

# Link custom files

from LatexSupport import LatexLabel
from UnicodeSymbols import *
from Helper import *
from Graphs import *
from GraphClass import GraphObject
from MessageClass import Message
from Functions import *
from Homogenization import *

# TODO: change the name of the module
from InteractiveTable import *


def main( ):
    # Quasi constant
    FrequencyRange = np.logspace( 0, 5, 1000 )
    # the main function only describes both graphical and comunication
    # of the app.
    doc = curdoc()

    # ========================== GRAPHICAL PART ================================

    # CREATE ALL PLOTS:
    Input = figure( title = "",
                    tools = "",
                    width = 500,
                    height = 500 )



    Graph = GraphObject( [ "Wave Velocities",
                           "Wave Velocities plus Limit Frequencies",
                           "Modes in Band",
                           "Modal Density",
                           "Modal Overlap Factor",
                           "Maximum Element Size (FEM)",
                           "Scheme"],
                            FrequencyRange,
                            Width = 850,
                            Height = 550)


    Graph.defineContainers(["WaveVelocity",
                            "WaveVElocityLimitFreq",
                            "ModesInBand",
                            "ModalDensity",
                            "ModalOverlapFactor",
                            "MaxElementSize"
                            "EigenFrequency"])



    # CREATE TABLES:
    # ........................ Elastic Modulus table ...........................
    ELASTIC_MODULUS_TITEL = Div( text = """ELASTIC MODULUS:""" )
    ElasticModulus = InteractiveTable( TableName = "ELASTIC MODULUS",
                                       Rows = 1,
                                       Columns =  3 )

    ElasticModulus.setTitels( [ [ EMODUL_X, EMODUL_Y, EMODUL_Z ] ] )

    OrthotropicData = [ [ "1.10E+10", "3.67E+08", "3.67E+08" ] ]
    IsotropicData = [ [ "1.10E+10", "1.10E+10", "1.10E+10" ] ]
    ElasticModulus.setValues( OrthotropicData )
    ElasticModulus.addBuffer( BufferName =  "DefaultIsotropic",
                              BufferData = IsotropicData )

    ElasticModulus.addBuffer( BufferName = "DefaultOrthotropic",
                              BufferData = OrthotropicData )

    ElasticModulus.addBuffer( BufferName = "GeneralIsotropic",
                              BufferData = IsotropicData )

    ElasticModulus.addBuffer( BufferName = "GeneralOrthotropic",
                              BufferData = OrthotropicData )


    ElasticModulus.addBuffer( BufferName = "Input",
                              BufferData = OrthotropicData )


    # ........................ Shear Modulus table .............................
    SHEAR_MODULUS_TITEL = Div( text = """SHEAR MODULUS:""" )
    ShearModulus = InteractiveTable( TableName = "SHEAR MODULUS",
                                     Rows = 1,
                                     Columns =  3 )

    ShearModulus.setTitels( [ [ EMODUL_XY, EMODUL_XZ, EMODUL_YZ ] ] )
    OrthotropicData = [ [ "6.90E+08", "6.90E+08", "6.90E+07" ] ]
    IsotropicData = [ [ "6.90E+08", "6.90E+08", "6.90E+08" ] ]

    ShearModulus.setValues( OrthotropicData )

    ShearModulus.addBuffer( BufferName =  "DefaultIsotropic",
                              BufferData = IsotropicData )

    ShearModulus.addBuffer( BufferName = "DefaultOrthotropic",
                              BufferData = OrthotropicData )

    ShearModulus.addBuffer( BufferName = "GeneralIsotropic",
                              BufferData = IsotropicData )


    ShearModulus.addBuffer( BufferName = "GeneralOrthotropic",
                              BufferData = OrthotropicData )

    ShearModulus.addBuffer( BufferName = "Input",
                              BufferData = OrthotropicData )


    # ........................ Poissons ratios ................................
    POISSON_RATIO_TITEL = Div( text = """POISSON'S RATIOS:""" )
    PoissonRatios = InteractiveTable( TableName = "POISSON'S RATIOS",
                                      Rows = 2,
                                      Columns = 3 )
    PoissonRatios.setTitels( [ [ POISSON_RATIO_XY,
                                 POISSON_RATIO_XZ,
                                 POISSON_RATIO_YZ ],
                               [ POISSON_RATIO_YX + "\t( auto )",
                                 POISSON_RATIO_ZX + "\t( auto )",
                                 POISSON_RATIO_ZY + "\t( auto )" ] ] )

    DataIsotropic = [ [ "0.42", "0.42", "0.42" ],
                      [ "0.42", "0.42", "0.42" ] ]

    DataOrthotropic = [ [ "0.42", "0.42", "0.3" ],
                        [ "0.014", "0.014", "0.3" ] ]

    PoissonRatios.setValues( DataOrthotropic )

    PoissonRatios.addBuffer( BufferName = "DefaultIsotropic",
                             BufferData = DataIsotropic )

    PoissonRatios.addBuffer( BufferName = "DefaultOrthotropic",
                             BufferData = DataOrthotropic )

    PoissonRatios.addBuffer( BufferName = "GeneralIsotropic",
                             BufferData = DataIsotropic )

    PoissonRatios.addBuffer( BufferName = "GeneralOrthotropic",
                             BufferData = DataOrthotropic )

    PoissonRatios.addBuffer( BufferName = "Input",
                             BufferData = DataOrthotropic )


    # ........................ Material Properties table .......................
    MATERIALS_TITEL = Div( text = """FURTHER MATERIAL PROPERTIES:""" )
    MaterialProperties = InteractiveTable( TableName = "MATERIAL PROPERTIES",
                                           Rows = 1,
                                           Columns = 2 )
    MaterialProperties.setTitels( [ [ "Density", "Loss Factor" ] ] )

    Data = [ [ "450.0", "0.012" ] ]
    MaterialProperties.setValues( Data )

    MaterialProperties.setValues( Data )

    MaterialProperties.addBuffer( BufferName = "DefaultIsotropic",
                                  BufferData = Data )

    MaterialProperties.addBuffer( BufferName = "DefaultOrthotropic",
                                  BufferData = Data )

    MaterialProperties.addBuffer( BufferName = "General",
                                  BufferData = Data )

    MaterialProperties.addBuffer( BufferName = "Input",
                                  BufferData = Data )


    # ........................ Geometry table .......................
    GEOMETRY_TITEL = Div( text = """GEOMETRY:""" )
    GeometryProperties = InteractiveTable( TableName = "GEOMETRY",
                                           Rows =  1,
                                           Columns =  3 )

    GeometryProperties.setTitels( [ [ "Length", "Width", "Thickness of the layers*" ] ] )

    Data = [ [ "2.5", "3.0", "0.027" ] ]
    GeometryProperties.setValues( Data )

    GeometryProperties.setValues( Data )

    GeometryProperties.addBuffer( BufferName = "DefaultIsotropic",
                                  BufferData = Data )

    GeometryProperties.addBuffer( BufferName = "DefaultOrthotropic",
                                  BufferData = Data )

    GeometryProperties.addBuffer( BufferName = "General",
                                  BufferData = Data )

    GeometryProperties.addBuffer( BufferName = "Input",
                                  BufferData = Data )



    ElasticModulus.fillTableWithBufferData( "DefaultOrthotropic" )
    ShearModulus.fillTableWithBufferData( "DefaultOrthotropic" )
    PoissonRatios.fillTableWithBufferData( "DefaultOrthotropic" )
    MaterialProperties.fillTableWithBufferData( "DefaultOrthotropic" )
    GeometryProperties.fillTableWithBufferData( "DefaultOrthotropic" )


    Tables = { "ElasticModulus" : ElasticModulus,
               "ShearModulus" : ShearModulus,
               "PoissonRatios" : PoissonRatios,
               "MaterialProperties" : MaterialProperties,
               "GeometryProperties" : GeometryProperties }


    # CREATE BUTTONS:
    SetDefaultButton = Button( label = "Default",
                               button_type = "primary",
                               width = 100 )


    ApplyButton = Button( label = "Apply",
                          button_type = "primary",
                          width = 100 )


    PrintReport = Button( label = "Print Report",
                          button_type = "primary",
                          width = 100 )


    ShowInput = Button( label = "Show Input",
                        button_type = "primary",
                        width = 100 )


    ModeRadioButtons = RadioButtonGroup( labels = [ "Orthotropic Material",
                                                    "Isotropic Material" ],
                                         width = 500,
                                         active = 0 )


    
    LayersInfo = Message( Color = "black",
                              Size = 2,
                              MessageHeader = "Number of layers: " )

    WarningMessage = Message( Color = "grey",
                              Size = 3 ,
                              MessageHeader = "Warning: " )


    Info = Div( text = "*Thickness of top to center layer separated by "
                       "semicolon or space: <br>"
					   "&nbsp;Symmetric cross section with odd number of layers"
                       " and crosswise layup assumed.",
                render_as_text = False,
                width = 500,
                height = 30 )

    # SPECIFY THE LAYOUT:
    Buttons = row( row( Spacer( width = 50 ),
                        ApplyButton,
                        Spacer( width = 50 ),
                        ShowInput,
                        Spacer( width = 50 ),
                        SetDefaultButton,
                        Spacer( width = 50 ),
                        PrintReport ) )


    LeftSide = column( ModeRadioButtons,
                        ELASTIC_MODULUS_TITEL,
                        ElasticModulus.Table,
                        SHEAR_MODULUS_TITEL,
                        ShearModulus.Table,
                        POISSON_RATIO_TITEL,
                        PoissonRatios.Table,
                        MATERIALS_TITEL,
                        MaterialProperties.Table,
                        GEOMETRY_TITEL,
                        GeometryProperties.Table,
                        LayersInfo.Widget,
                        Info,
                        WarningMessage.Widget )


    RightSide = column( Graph.Widget , Buttons )


    # ========================= COMMUNICATION PART =============================


    # Set up callback function for the "Apply" button
    ApplyButton.on_click( partial( updateData,
                                   Tables,
                                   Graph,
                                   LayersInfo,
                                   WarningMessage ) )


    # Set up callback function for all radion buttons that are responsible
    # for changing the mode, namely: Isotropic and Orthotropic material properties
    ModeRadioButtons.on_click( partial( updateMode,
                                        Tables,
                                        WarningMessage,
                                        Graph ) )


    # Set up callback function for all radion buttons that are responsible
    # for plotting different graphs
    Graph.GraphRadioButtons.on_click( partial( updateGraph, Graph ) )


    # Set up callback function for all the "Default" button that are responsible
    # for assigning the default data to all entries
    SetDefaultButton.on_click( partial( setDeafultSettings,
                                        Tables,
                                        Graph,
                                        LayersInfo,
                                        WarningMessage ) )


    ShowInput.on_click( partial( showInput, Tables, LayersInfo ) )


    # ================= RUN SIMULATION WITH DEFAULT DATA =====================
    updateData( Tables, Graph, LayersInfo, WarningMessage )


    #updateGraph( Graph, 4 )


    # RUN ALL WIDJETS
    doc.add_root( column( Spacer( height = 20 ),
                      row( LeftSide,
                           Spacer( width = 50 ),
                           RightSide,
                           Spacer( width = 50 ) ) ) )



# ===============================================================================
#                               HELPER FUNCTIONS
# ===============================================================================
def updateData( Tables, Graph, LayersInfo, WarningMessage ):

    # clean the warning message
    LayersInfo.clean()
    WarningMessage.clean()

    LayerThicknessBuffer = Tables[ "GeometryProperties" ].getValue( 0, 2 )
    try:

        Layers = getLayersFromString( Tables[ "GeometryProperties" ].getValue( 0, 2 ) )
        LayersInfo.printMessage( str( len( Layers ) ) )
        # Homogenize the input data
        if len(Layers) != 1:
            makeMultiLayerMask( Tables )

            HomogenizedData = homogenize( Tables[ "ElasticModulus" ].getData( )[ 0 ],
                                          Tables[ "ShearModulus" ].getData( )[ 0 ],
                                          Tables[ "PoissonRatios" ].getData( ),
                                          Layers )

            #cangeMode( Tables, WarningMessage, Graph.getMode( ) )

            Tables[ "ElasticModulus" ].assignValuesSet( HomogenizedData[ "ElasticModulus" ] )
            Tables[ "ShearModulus" ].assignValuesSet( HomogenizedData[ "ShearModulus" ] )
            Tables[ "PoissonRatios" ].assignValuesSet( HomogenizedData[ "PoissonRatios" ] )
            Tables[ "GeometryProperties" ].assignValue( 0, 2, HomogenizedData[ "TotalThickness" ] )


        # Part of error handling.Function "isInputNegative" throws an error
        # if there is an element with its negetive value.
        isInputNegative( Tables [ "ElasticModulus" ].getData( ) )
        isInputNegative( Tables [ "ShearModulus" ].getData( ) )
        isInputNegative( Tables [ "PoissonRatios" ].getData( ) )
        isInputNegative( Tables [ "MaterialProperties" ].getData( ) )
        isInputNegative( Tables [ "GeometryProperties" ].getData( ) )

        # update the tables buffers
        makeMask( Tables, Graph.getMode() )

        # before calling user-define functions check the current mode
        cangeMode( Tables, WarningMessage, Graph.getMode() )

        precomputePoissonRatios( Tables )

        # get data from the corresponding tables
        ElasticModulusData = Tables [ "ElasticModulus" ].getData( )
        ShearModulusData = Tables [ "ShearModulus" ].getData( )
        PoissonRatiosData = Tables [ "PoissonRatios" ].getData( )
        MaterialPropertiesData = Tables [ "MaterialProperties" ].getData( )
        GeometryPropertiesData = Tables [ "GeometryProperties" ].getData( )


    #################### CALL USER-SPECIFIC FAUNCTION ##########################

        testInputData( Graph.getMode(), PoissonRatiosData )


        Graph.Containers[ "WaveVelocity" ] = wave_speeds(
                                                ElasticModulusData,
                                                ShearModulusData,
                                                PoissonRatiosData,
                                                MaterialPropertiesData,
                                                GeometryPropertiesData,
                                                bool( Graph.getMode() ),
                                                Graph.getRange() )


        Graph.Containers[ "ModesInBand" ] = ModesInBand(
                                                ElasticModulusData,
                                                ShearModulusData,
                                                PoissonRatiosData,
                                                MaterialPropertiesData,
                                                GeometryPropertiesData,
                                                bool( Graph.getMode( ) ),
                                                Graph.getRange( ) )


        Graph.Containers[ "ModalDensity" ] = ModaleDichte(
                                                Graph.Containers[ "WaveVelocity" ][ "c_L" ],
                                                Graph.Containers[ "WaveVelocity" ][ "c_S" ],
                                                Graph.Containers[ "WaveVelocity" ][ "c_B_eff" ],
                                                Graph.Containers[ "WaveVelocity" ][ "c_g_eff" ],
                                                GeometryPropertiesData,
                                                bool( Graph.getMode( ) ),
                                                Graph.getRange( ) )


        Graph.Containers[ "ModalOverlapFactor" ] = ModalOverlapFactor(
                                                        MaterialPropertiesData,
                                                        Graph.Containers[ "ModalDensity" ],
                                                        Graph.getRange( ) )


        Graph.Containers[ "MaxElementSize" ] = MaximumElementSize(
                                                   Graph.Containers[ "WaveVelocity" ][ "c_B" ],
                                                   Graph.Containers[ "WaveVelocity" ][ "c_B_eff" ],
                                                   Graph.getRange( ) )


        Graph.Containers[ "EigenFrequency" ] = EigenfrequenciesPlate(
                                                      ElasticModulusData,
                                                      ShearModulusData,
                                                      PoissonRatiosData,
                                                      MaterialPropertiesData,
                                                      GeometryPropertiesData,
                                                      bool( Graph.getMode() ),
                                                      Graph.getRange() )

        # Update the current graph with new data
        updateGraph( Graph, Graph.getCurrentGraphNumber( ) )

        WarningMessage.clean()


    except DataCorrupted as Error:
        WarningMessage.printMessage( str(Error) )
        Tables[ "GeometryProperties" ].setValue( 0, 2, LayerThicknessBuffer, "" )


    except WrongLayersThikness as Error:
        WarningMessage.printMessage( str(Error) )


    except TableCorrupted as Error:
        WarningMessage.printMessage( str(Error) )


    except:
        Message = "Error: Unexpected error. Please, refer to the code"
        WarningMessage.printMessage( Message )


def updateGraph( Graph, GraphNumber ):


    # Update the graph ID ( GraphNumber - it's a built-in bohek variable that
    # belongs to the RadioButton widget )
    Graph.setPlottingGraphNumber( GraphNumber )

    plotEigenfrequenciesPlate( Graph )


    # Depict coresponding lines based on the graph chosen by the user
    if (GraphNumber == 0):
        plotWaveSpeedGraph( Graph )

    if (GraphNumber == 1):
        plotWaveSpeedGraphWithLimits( Graph )

    if (GraphNumber == 2):
        plotModesInBand( Graph )

    if (GraphNumber == 3):
        plotModalDensity( Graph )

    if (GraphNumber == 4):
        plotModalOverlapFactor( Graph )

    if (GraphNumber == 5):
        plotMaximumElementSize( Graph )


def updateMode( Tables,
                WarningMessage,
                Graph,
                Properties ):


    WarningMessage.clean( )
    Graph.setMode( Properties )

    #WarningMessage.printMessage( "Click on the Apply button to update grapths..." )
    if Properties == 0:
        Tables[ "ElasticModulus" ].fillTableWithBufferData( "GeneralOrthotropic" )
        Tables[ "ShearModulus" ].fillTableWithBufferData( "GeneralOrthotropic" )
        Tables[ "PoissonRatios" ].fillTableWithBufferData( "GeneralOrthotropic" )

    elif Properties == 1:
        Tables[ "ElasticModulus" ].fillTableWithBufferData( "GeneralIsotropic" )
        Tables[ "ShearModulus" ].fillTableWithBufferData( "GeneralIsotropic" )
        Tables[ "PoissonRatios" ].fillTableWithBufferData( "GeneralIsotropic" )


    cangeMode( Tables, WarningMessage, Graph.getMode() )


def cangeMode( Tables, WarningMessage, Mode ):


    if ( Mode == 1 ):


        UniformValue = Tables[ "ElasticModulus" ].getValue( 0, 0 )
        Tables[ "ElasticModulus" ].setValue( 0, 1, UniformValue )
        Tables[ "ElasticModulus" ].setValue( 0, 2, UniformValue )

        UniformValue = Tables[ "ElasticModulus" ].getFloatValue( 0, 0 ) \
                            / ( 2.0 * ( 1.0 + Tables[ "PoissonRatios" ].getFloatValue( 0, 0 )))
        Tables[ "ShearModulus" ].setValue( 0, 0, '{:.2e}'.format( UniformValue ) )
        Tables[ "ShearModulus" ].setValue( 0, 1, '{:.2e}'.format( UniformValue ) )
        Tables[ "ShearModulus" ].setValue( 0, 2, '{:.2e}'.format( UniformValue )  )

        UniformValue = Tables[ "PoissonRatios" ].getValue( 0, 0 )
        Tables[ "PoissonRatios" ].setValue( 0, 1, UniformValue )
        Tables[ "PoissonRatios" ].setValue( 0, 2, UniformValue )

        try:
            testInputData( Mode, Tables[ "PoissonRatios" ].getData() )
        except DataCorrupted as Error:
            WarningMessage.printMessage( str( Error ) )



    if ( Mode == 0 ):

        Tables[ "ElasticModulus" ].restoreValue( 0, 1 )
        Tables[ "ElasticModulus" ].restoreValue( 0, 2 )

        Tables[ "ShearModulus" ].restoreValue( 0, 0 )
        Tables[ "ShearModulus" ].restoreValue( 0, 1 )
        Tables[ "ShearModulus" ].restoreValue( 0, 2 )

        Tables[ "PoissonRatios" ].restoreValue( 0, 1 )
        Tables[ "PoissonRatios" ].restoreValue( 0, 2 )

        pass
    precomputePoissonRatios( Tables )


def precomputePoissonRatios( Tables ):

    # update value of nu_21
    Temp = Tables[ "PoissonRatios" ].getFloatValue( 0, 0 )    \
           * Tables[ "ElasticModulus" ].getFloatValue ( 0, 1 ) \
           / Tables[ "ElasticModulus" ].getFloatValue( 0, 0 )


    Tables[ "PoissonRatios" ].assignValue( 1, 0, str( round(Temp,5) ) )

    # update value of nu_31
    Temp = Tables[ "PoissonRatios" ].getFloatValue( 0, 1 ) \
           * Tables[ "ElasticModulus" ].getFloatValue( 0, 2 ) \
           / Tables[ "ElasticModulus" ].getFloatValue( 0, 0 )
    Tables[ "PoissonRatios" ].assignValue( 1, 1, str( round(Temp,5) ) )

    # update value of nu_32
    Temp = Tables[ "PoissonRatios" ].getFloatValue( 0, 2 ) \
           * Tables[ "ElasticModulus" ].getFloatValue( 0, 2 ) \
           / Tables[ "ElasticModulus" ].getFloatValue( 0, 1 )

    Tables[ "PoissonRatios" ].assignValue( 1, 2, str( round(Temp,5) ) )


def setDeafultSettings( Tables,
                        Graph,
                        LayersInfo,
                        WarningMessage ):

    WarningMessage.clean()

    if Graph.getMode() == 0:

        Tables[ "ElasticModulus" ].fillTableWithBufferData( "DefaultOrthotropic" )
        Tables[ "ShearModulus" ].fillTableWithBufferData( "DefaultOrthotropic" )
        Tables[ "PoissonRatios" ].fillTableWithBufferData( "DefaultOrthotropic" )
        Tables[ "MaterialProperties" ].fillTableWithBufferData( "DefaultOrthotropic" )
        Tables[ "GeometryProperties" ].fillTableWithBufferData( "DefaultOrthotropic" )

    if Graph.getMode() == 1:
        Tables[ "ElasticModulus" ].fillTableWithBufferData( "DefaultIsotropic" )
        Tables[ "ShearModulus" ].fillTableWithBufferData( "DefaultIsotropic" )
        Tables[ "PoissonRatios" ].fillTableWithBufferData( "DefaultIsotropic" )
        Tables[ "MaterialProperties" ].fillTableWithBufferData( "DefaultIsotropic" )
        Tables[ "GeometryProperties" ].fillTableWithBufferData( "DefaultIsotropic" )

    #Tables[ "ElasticModulus" ].resetByDefault( )
    #Tables[ "ShearModulus" ].resetByDefault( )
    #Tables[ "PoissonRatios" ].resetByDefault( )
    #Tables[ "GeometryProperties" ].resetByDefault( )

    updateData( Tables, Graph, LayersInfo, WarningMessage )


def showInput( Tables, LayersInfo ):

    Tables[ "ElasticModulus" ].fillTableWithBufferData( "Input" )
    Tables[ "ShearModulus" ].fillTableWithBufferData( "Input")
    Tables[ "PoissonRatios" ].fillTableWithBufferData( "Input" )
    Tables[ "MaterialProperties" ].fillTableWithBufferData( "Input" )
    Tables[ "GeometryProperties" ].fillTableWithBufferData( "Input" )

    Layers = getLayersFromString( Tables[ "GeometryProperties" ].getValue( 0, 2 ) )
    LayersInfo.printMessage( str( len( Layers ) ) )


def makeMask( Tables, Mode ):

    # get data from the corresponding tables
    ElasticModulusData = Tables[ "ElasticModulus" ].getRawData( )
    ShearModulusData = Tables[ "ShearModulus" ].getRawData( )
    PoissonRatiosData = Tables[ "PoissonRatios" ].getRawData( )
    MaterialPropertiesData = Tables[ "MaterialProperties" ].getRawData( )
    GeometryPropertiesData = Tables[ "GeometryProperties" ].getRawData( )


    Tables[ "MaterialProperties" ].setBufferData( "General", MaterialPropertiesData )

    Tables[ "GeometryProperties" ].setBufferData( "General", GeometryPropertiesData )


    if Mode == 0:

        Tables[ "ElasticModulus" ].setBufferData( "GeneralOrthotropic",
                                                  ElasticModulusData )

        Tables[ "ShearModulus" ].setBufferData( "GeneralOrthotropic",
                                                ShearModulusData )

        Tables[ "PoissonRatios" ].setBufferData( "GeneralOrthotropic",
                                                 PoissonRatiosData )


    elif Mode == 1:

        Tables[ "ElasticModulus" ].setBufferData( "GeneralIsotropic",
                                                  ElasticModulusData )

        Tables[ "ShearModulus" ].setBufferData( "GeneralIsotropic",
                                                ShearModulusData )

        Tables[ "PoissonRatios" ].setBufferData( "GeneralIsotropic",
                                                 PoissonRatiosData )


def makeMultiLayerMask( Tables ):

    # get data from the corresponding tables
    ElasticModulusData = Tables[ "ElasticModulus" ].getRawData( )
    ShearModulusData = Tables[ "ShearModulus" ].getRawData( )
    PoissonRatiosData = Tables[ "PoissonRatios" ].getRawData( )
    MaterialPropertiesData = Tables[ "MaterialProperties" ].getRawData( )

    # we're using implicit method to get value from tables since the
    # the last entry represents a string of layers thickness
    GeometryPropertiesData = [ [ Tables[ "GeometryProperties" ].getValue( 0, 0 ),
                                 Tables[ "GeometryProperties" ].getValue( 0, 1 ),
                                 Tables[ "GeometryProperties" ].getValue( 0, 2 ) ] ]


    Tables[ "ElasticModulus" ].setBufferData( "Input", ElasticModulusData )
    Tables[ "ShearModulus" ].setBufferData( "Input", ShearModulusData )
    Tables[ "PoissonRatios" ].setBufferData( "Input", PoissonRatiosData )
    Tables[ "MaterialProperties" ].setBufferData( "Input", MaterialPropertiesData )
    Tables[ "GeometryProperties" ].setBufferData( "Input", GeometryPropertiesData )


main( )
