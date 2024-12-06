# Link bokeh libraries
from bokeh.io import curdoc, show
from bokeh.models import Div, Label, Plot, ColumnDataSource
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer

# Link third-party python libraries
from functools import partial

# Link custom files
from VibroP_UnicodeSymbols import *
from VibroP_Helper import *
from VibroP_Graphs import *
from VibroP_GraphClass import VibroP_GraphObject
from VibroP_MessageClass import VibroP_Message
from VibroP_Functions import *
from VibroP_Homogenization import homogenize
from VibroP_InteractiveTable import VibroP_TableCorrupted, VibroP_InteractiveTable



def main( ):
    """
    The main function only describes both graphical and comunication parts of the app.
    It creates and initializes all necessary widgets. At the end the function calls
    doc.add_root to display the objects on a browser
    :return:
    """

    # Quasi constant
    FrequencyRange = np.logspace( 0, 5, 1000 )
    doc = curdoc()

    # ========================== GRAPHICAL PART ================================

    # CREATE ALL PLOTS:
    Input = figure( title = "",
                    tools = "",
                    width = 500,
                    height = 500 )



    Graph = VibroP_GraphObject( [ "Wave Velocities",
                           "Wave Velocities plus Limit Frequencies",
                           "Modes in Band",
                           "Modal Density",
                           "Modal Overlap Factor",
                           "Maximum Element Size (FEM)"],
                            FrequencyRange,
                            Width = 950,
                            Height = 650)


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
    ElasticModulus = VibroP_InteractiveTable( TableName = "ELASTIC MODULUS",
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
    ShearModulus = VibroP_InteractiveTable( TableName = "SHEAR MODULUS",
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
    PoissonRatios = VibroP_InteractiveTable( TableName = "POISSON'S RATIOS",
                                      Rows = 2,
                                      Columns = 3 )

    PoissonRatios.setTitels( [ [ POISSON_RATIO_XY,
                                 POISSON_RATIO_XZ,
                                 POISSON_RATIO_YZ ],
                               [ POISSON_RATIO_YX + "\t(auto)",
                                 POISSON_RATIO_ZX + "\t(auto)",
                                 POISSON_RATIO_ZY + "\t(auto)" ] ] )

    PoissonRatios.setDisabled(1, 0, True)
    PoissonRatios.setDisabled(1, 1, True)
    PoissonRatios.setDisabled(1, 2, True)

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
    MaterialProperties = VibroP_InteractiveTable( TableName = "MATERIAL PROPERTIES",
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
    GeometryProperties = VibroP_InteractiveTable( TableName = "GEOMETRY",
                                           Rows =  1,
                                           Columns =  3 )

    GeometryProperties.setTitels( [ [ "Length", "Width", "Thicknesses of the layers*" ] ] )

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
                               button_type = "success",
                               width = 100 )


    ApplyButton = Button( label = "Apply",
                          button_type = "success",
                          width = 100 )


    # PrintReport = Button( label = "Print Report",
    #                       button_type = "primary",
    #                       width = 100 )


    ShowInput = Button( label = "Show Input",
                        button_type = "success",
                        width = 100 )


    ModeRadioButtons = RadioButtonGroup( labels = [ "Orthotropic Material",
                                                    "Isotropic Material" ],
                                         width = 500,
                                         active = 0 )


    
    LayersInfo = VibroP_Message( Color = "black",
                          Size = 2,
                          MessageHeader = "Number of layers: " )

    WarningMessage = VibroP_Message( Color = "red",
                              Size = 3 ,
                              MessageHeader = "Warning: " )


    Info = Div( text = "*Thicknesses of top to center layer separated by "
                       "semicolon or space: <br>"
					   "&nbsp;Symmetric cross section with odd number of layers"
                       " and crosswise layup assumed.",
                render_as_text = False,
                width = 500,
                height = 40 )


    Scheme = Div( text = "<img src='/Vibroacoustic_plates/static/images/scheme.png' width=464 height=220>",
                width = 464,
                height = 220 )

    Description = Div( text = "The application \"Vibroacoustics of Plates\" can be classified in two steps: <br><br>"
                "<b>1.</b> Insert the physical properties of a homogenous plate or of a single layer"
                "&nbsp;in the case of a layered plate (default values are given) on the left and press <i>'Apply'</i>. <br><br>"
                "<b>Notice</b> that in the case of a layered plate, a symmetric cross section"
                "&nbsp;with an odd number of layers and a crosswise layup is assumed (cf. scheme)."
                "&nbsp;Therefore, the thicknesses of the top to the center layer have to be inserted."
                "&nbsp;The material properties are homogenized through the thickness."
                "&nbsp;Thus, the input data of the single layer"
                "&nbsp;is overwritten by homogenized material parameters of the plate after pressing <i>'Apply'</i>."
                "&nbsp;The input data of the single layers can be checked by pressing the"
                "&nbsp;button <i>'Show Input'</i>. <br><br>"
                "<b>2.</b> On the right, dynamic properties of the plate and of"
                "&nbsp;its wave types are plotted. These can be studied"
                "&nbsp;using e.g. the zoom function and saved as .png.<br><br>"
                "&nbsp;Please refer to the following publication for further explanations and references:<br><br>"
                "&nbsp;Winter, C.: Frequency Dependent Modeling for the Prediction of the Sound Transmission in Timber Constructions. (2018)."

					   ,
                render_as_text = False,
                width = 1000,
                height = 50 )
    
    Title = Div ( text = "<b><h1> Vibroacoustics of Plates</b><h1>",
                 render_as_text = False,
                 width = 900,
                 height = 80)

    # SPECIFY THE LAYOUT:
    Buttons = row( row( Spacer( width = 50),
                        ApplyButton,
                        Spacer( width = 50),
                        ShowInput,
                        Spacer( width = 50),
                        SetDefaultButton ) )

    Headline = row( column( Title, Description ), Spacer( width = 50 ), Scheme )
	
    LeftSide = column( ModeRadioButtons,
                        Spacer(height=20),
                        ELASTIC_MODULUS_TITEL,
                        ElasticModulus.Table,
                        Spacer(height=20),
                        SHEAR_MODULUS_TITEL,
                        ShearModulus.Table,
                        Spacer(height=20),
                        POISSON_RATIO_TITEL,
                        PoissonRatios.Table,
                        Spacer(height=20),
                        MATERIALS_TITEL,
                        MaterialProperties.Table,
                        Spacer(height=20),
                        GEOMETRY_TITEL,
                        GeometryProperties.Table,
                        LayersInfo.Widget,
                        Spacer(height=10),
                        Info,
                        Spacer( height = 20 ),
                        WarningMessage.Widget )


    RightSide = column( Graph.Widget, Spacer( height = 50 ),
     Buttons,
                        Spacer( height = 100 ) )


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
    SetDefaultButton.on_click( partial( setDefaultSettings,
                                        Tables,
                                        Graph,
                                        LayersInfo,
                                        WarningMessage ) )


    ShowInput.on_click( partial( showInput, Tables, LayersInfo ) )


    # ================= RUN SIMULATION WITH DEFAULT DATA =====================
    updateData( Tables, Graph, LayersInfo, WarningMessage )


    # RUN ALL WIDGETS
    doc.add_root(Headline)
    doc.add_root( column( Spacer( height = 150 ),
                      row( LeftSide,
                           Spacer( width = 50 ),
                           RightSide,
                           Spacer( width = 50 ) ) ) )



# ===============================================================================
#                               HELPER FUNCTIONS
# ===============================================================================
def updateData( Tables, Graph, LayersInfo, WarningMessage ):
    """
    At the begining the function reads the layers thickness of a composite material and
    converts its properties to the property of the isotropic one. Then the properties of
    the isotropic material are assigned to the tables if necessary. Additionally
    the function tests the input parameters of the isotropic material on
    consistency.

    At the end the function performs all computations using table data and stores
    the result of them into the Graph instance containers

    :param Tables: dictionary (container with tables)
    :param Graph: an instance of VibroP_GraphObject class
    :param LayersInfo: MessageClass instance
    :param WarningMessage: MessageClass instance
    :return:
    """

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


    #################### CALL USER-SPECIFIC FUNCTION ##########################

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


    except VibroP_DataCorrupted as Error:
        WarningMessage.printMessage( str(Error) )
        Tables[ "GeometryProperties" ].setValue( 0, 2, LayerThicknessBuffer, "" )


    except VibroP_WrongLayersThikness as Error:
        WarningMessage.printMessage( str(Error) )


    except VibroP_TableCorrupted as Error:
        WarningMessage.printMessage( str(Error) )

    #'''
    except:
        Message = "Error: Unexpected error. Please, refer to the code"
        WarningMessage.printMessage( Message )
    #'''

def updateGraph( Graph, GraphNumber ):
    """
    The function calls an appropriate plot-function based on the mode (value) of
    the radio-button
    :param Graph: an instance of VibroP_GraphObject class
    :param GraphNumber: int
    :return:
    """

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

    """
    The function saves the current state of the tables and calls "cangeMode" function
    IMPORTANT: "Properties" is redundant, however, it's necessary to kick off the
    first default run from main()
    :param Tables: dictionary (container with tables)
    :param WarningMessage: MessageClass instance
    :param Graph: an instance of VibroP_GraphObject class
    :param Properties: boolean (Isotropic and Orthotropic)
    :return:
    """

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
    """
    The function performs the following modification to the talbes if the user switches to
    the isotropic case:
        E1 = E2 = E3
        G12 = G13 = G23
        N12 = Nij = ... for all possible i and j within the set (1,2,3)

    If the user switches back to orthotropic case the function restores the data
    of the tables back that was modified for the isotropic case
    :param Tables: dictionary (container with tables)
    :param WarningMessage: MessageClass instance
    :param Mode: boolean (Isotropic and Orthotropic)
    :return:
    """

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
        except VibroP_DataCorrupted as Error:
            WarningMessage.printMessage( str( Error ) )



    if ( Mode == 0 ):

        Tables[ "ElasticModulus" ].restoreValue( 0, 1 )
        Tables[ "ElasticModulus" ].restoreValue( 0, 2 )

        Tables[ "ShearModulus" ].restoreValue( 0, 0 )
        Tables[ "ShearModulus" ].restoreValue( 0, 1 )
        Tables[ "ShearModulus" ].restoreValue( 0, 2 )

        Tables[ "PoissonRatios" ].restoreValue( 0, 1 )
        Tables[ "PoissonRatios" ].restoreValue( 0, 2 )

    precomputePoissonRatios( Tables )


def setDefaultSettings( Tables, Graph, LayersInfo, WarningMessage ):
    """
    The function sets up the default values for the tables
    :param Tables: dictionary (container with tables)
    :param Graph: an instance of VibroP_GraphObject class
    :param LayersInfo: MessageClass instance
    :param WarningMessage: MessageClass instance
    :return:
    """

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

    updateData( Tables, Graph, LayersInfo, WarningMessage )


def precomputePoissonRatios( Tables ):
    """
    The function computes and updates the values of the following table entries:
        N21 = N12 * E2 / E1;
        N31 = N13 * E3 / E1;
        N32 = N23 * E3 / E2;
    These values have to be always computed automatically

    :param Tables: dictionary (container with tables)
    :return:
    """

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


def showInput( Tables, LayersInfo ):
    """
    The function restores the inrormation of the tables that was modified during
    the homogenization procedure. It allows the user to look at the original input date
    :param Tables: dictionary (container with tables)
    :param LayersInfo: MessageClass instance
    :return:
    """

    Tables[ "ElasticModulus" ].fillTableWithBufferData( "Input" )
    Tables[ "ShearModulus" ].fillTableWithBufferData( "Input")
    Tables[ "PoissonRatios" ].fillTableWithBufferData( "Input" )
    Tables[ "MaterialProperties" ].fillTableWithBufferData( "Input" )
    Tables[ "GeometryProperties" ].fillTableWithBufferData( "Input" )

    Layers = getLayersFromString( Tables[ "GeometryProperties" ].getValue( 0, 2 ) )
    LayersInfo.printMessage( str( len( Layers ) ) )


def makeMask( Tables, Mode ):
    """
    The function gets the current data from the table and stores them into
    the corresponding tables buffers to allow the user to retrieve the old info back.
    The function distinguishes the modes and stores the info into either isotropic or
    orthotropic buffes
    :param Tables: dictionary (container with tables)
    :param Mode: boolean (Isotropic or Orthotropic)
    :return:
    """

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
    """
    The function gets the current data from the table and stores them into
    the corresponding tables buffers to allow the user to retrieve the old info back
    :param Tables: dictionary (container with tables)
    :return:
    """

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
