import matplotlib.pyplot as plt
import numpy as np
import random
from Colors import *

from bokeh.io import reset_output
from bokeh.models import ColumnDataSource
from bokeh.models.annotations import LegendItem
from GraphClass import GraphObject


def plotWaveSpeedGraphWithLimits( GraphInstance ):

    GraphInstance.cleanGraph()
    GraphInstance.Graph.yaxis.axis_label = "Wave Velocity in m/s"
    GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

    # Find the maximum values in both x and y direction to be able to
    # depict both vertical and horizontal lines
    MaxCoordinateY = max( GraphInstance.Containers[ "WaveVelocity" ][ "c_g" ] )
    MinCoordinateY = min( GraphInstance.Containers[ "WaveVelocity" ][ "c_B_eff" ] )

    MaxCoordinateX = max( GraphInstance.getRange( ) )
    MinCoordinateX = min( GraphInstance.getRange( ) )

    COUNTER = 0

    # ............................ c_L graph ...................................
    # 'Quasi-longitudial, in-plane'
    RangeX = [ MinCoordinateX, MaxCoordinateX ]
    RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_L" ][ 0 ],
               GraphInstance.Containers[ "WaveVelocity" ][ "c_L" ][ 0 ] ]


    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                              YData = RangeY )

    #if GraphInstance.getMode() == 0:

    GraphInstance.defineLine( COUNTER, 'Quasi-longitudial, in-plane',
                                  DARK_BLUE,
                                  'solid' )

    #elif GraphInstance.getMode() == 1:

    #    GraphInstance.defineLine( COUNTER, 'Quasi-longitudial',
    #                              DARK_BLUE,
    #                              'solid' )

    COUNTER += 1

    # .................... c_L_thick graph .............................
    # 'Longitudinal out-of-plane'
    RangeX = [ MinCoordinateX, MaxCoordinateX ]
    RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_L_thick" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "c_L_thick" ] ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                               YData = RangeY )

    GraphInstance.defineLine( COUNTER, 'Longitudinal, out-of-plane',
                              DARK_BLUE,
                              'dashed' )

    COUNTER += 1
    # ............................ c_S graph ...................................
    # 'Shear, in-plane'
    RangeX = [ MinCoordinateX, MaxCoordinateX ]
    RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_S" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "c_S" ] ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                              YData = RangeY )

    if GraphInstance.getMode( ) == 0:

        GraphInstance.defineLine( COUNTER, 'Shear, in-plane',
                                  LIGHT_BLUE,
                                  'solid' )

    elif GraphInstance.getMode( ) == 1:

        GraphInstance.defineLine( COUNTER, 'Shear',
                                  LIGHT_BLUE,
                                  'solid' )

    COUNTER += 1


    if GraphInstance.getMode() == 0:
        # ................... c_S_outofplane_1 graph ...........................
        # 'Shear out-of-plane prop. (G32)'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_S_outofplane_1" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_S_outofplane_1" ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                   YData = RangeY )

        GraphInstance.defineLine( COUNTER, 'Shear, out-of-plane propagation (G31)',
                                  LIGHT_BLUE,
                                  'dashed' )

        COUNTER += 1

        # ................... c_S_outofplane_2 graph ............................
        # 'Shear out-of-plane prop. (G31)'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_S_outofplane_2" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_S_outofplane_2" ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                   YData = RangeY )

        GraphInstance.defineLine( COUNTER, 'Shear, out-of-plane propagation (G32)',
                                  LIGHT_BLUE,
                                  'dashed' )


        COUNTER += 1
    # ......................... c_B_shear graph ................................
    # 'Shear (corrected), out-of-plane displ.'
    RangeX = [ MinCoordinateX, MaxCoordinateX ]
    RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_B_shear" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "c_B_shear" ] ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                              YData = RangeY )

    GraphInstance.defineLine( COUNTER, 'Shear (corrected), out-of-plane displ.',
                              LIGHT_BLUE,
                              'dashdot' )

    COUNTER += 1
    # ............................ c_B graph ...................................
    # 'Effective bending (thick plate)'
    GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                              YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_B" ] )

    GraphInstance.defineLine( COUNTER, 'Pure bending (thin plate)',
                              GREEN,
                              'dashed' )

    COUNTER += 1
    # .......................... c_B_eff graph .................................
    # 'Pure bending (thin plate)'
    GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                              YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_B_eff" ] )

    GraphInstance.defineLine( COUNTER, 'Effective bending (thick plate)',
                              GREEN,
                              'solid' )

    COUNTER += 1
    # ............................ c_g graph ...................................
    # 'Group (bending)'
    GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                              YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_g" ] )

    GraphInstance.defineLine( COUNTER, 'Group (bending)',
                              ORANGE,
                              'dashed' )

    COUNTER += 1
    # .......................... c_g_eff graph .................................
    # 'Group (effective bending)'
    GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                              YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_g_eff" ] )

    GraphInstance.defineLine( COUNTER, 'Group (effective bending)',
                              ORANGE,
                              'solid' )

    COUNTER += 1
    # .................... fR_B graph .............................
    # 'Thin-Plate-Limit Group'
    RangeX = [ GraphInstance.Containers[ "WaveVelocity" ][ "fR_g" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "fR_g" ] ]
    RangeY = [ MinCoordinateY, MaxCoordinateY ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                               YData = RangeY )

    GraphInstance.defineLine( COUNTER, 'Thin-Plate-Limit Group',
                              ORANGE,
                              'dotted' )

    COUNTER += 1
    # .................... fR_B graph .............................
    # 'Thin-Plate-Limit Phase'
    RangeX = [ GraphInstance.Containers[ "WaveVelocity" ][ "fR_B" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "fR_B" ] ]
    RangeY = [ MinCoordinateY, MaxCoordinateY ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                               YData = RangeY )

    GraphInstance.defineLine( COUNTER, 'Thin-Plate-Limit Phase',
                              GREEN,
                              'dotted' )

    COUNTER += 1
    # ................... f_thickmode_shear_y graph ............................
    if GraphInstance.getMode() == 0:

        # '1st Thickness-shear resonance (G32)'
        RangeX = [ GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_shear_y" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_shear_y" ] ]
        RangeY = [ MinCoordinateY, MaxCoordinateY ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                  YData = RangeY )

        #plt.loglog( RangeX, RangeY, linestyle = '--', color = LIGHT_BLUE )
        GraphInstance.defineLine( COUNTER, '1st Thickness-shear resonance (G32)',
                                  LIGHT_BLUE,
                                  'dotted' )

        COUNTER += 1

    # .................... f_thickmode_shear_x graph .............................
    # '1st Thickness-shear resonance (G31)'
    RangeX = [ GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_shear_x" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_shear_x" ] ]
    RangeY = [ MinCoordinateY, MaxCoordinateY ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                              YData = RangeY )

    if GraphInstance.getMode() == 0:

        GraphInstance.defineLine( COUNTER, '1st Thickness-shear resonance (G31)',
                                  LIGHT_BLUE,
                                  'dotted' )

    elif GraphInstance.getMode() == 1:

        GraphInstance.defineLine( COUNTER, '1st Thickness-shear resonance',
                                  LIGHT_BLUE,
                                  'dotted' )

    COUNTER += 1

    # ................... f_thickmode_stretch graph ............................
    # '1st Thickness-stretch resonance'
    RangeX = [ GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_long" ],
               GraphInstance.Containers[ "WaveVelocity" ][ "f_thickmode_long" ] ]
    RangeY = [ MinCoordinateY, MaxCoordinateY ]

    GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                              YData = RangeY )


    GraphInstance.defineLine( COUNTER, '1st Thickness-stretch resonance',
                              DARK_BLUE,
                              'dotted' )

    COUNTER += 1

def plotWaveSpeedGraph( GraphInstance ):

        GraphInstance.cleanGraph()
        GraphInstance.Graph.yaxis.axis_label = "Wave Velocity in m/s"
        GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

        # Find the maximum values in both x and y direction to be able to
        # depict both vertical and horizontal lines
        MaxCoordinateY = max( GraphInstance.Containers[ "WaveVelocity" ][ "c_g" ] )
        MaxCoordinateX = max( GraphInstance.getRange( ) )
        MinCoordinateY = min( GraphInstance.Containers[ "WaveVelocity" ][ "c_B_eff" ] )
        MinCoordinateX = min( GraphInstance.getRange( ) )

        COUNTER = 0
        # ............................ c_L graph ...................................
        # 'Quasi-longitudial, in-plane'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_L" ][ 0 ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_L" ][ 0 ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                  YData = RangeY )

        if GraphInstance.getMode( ) == 0:

            GraphInstance.defineLine( COUNTER, 'Quasi-longitudial, in-plane',
                                      DARK_BLUE,
                                      'solid' )

        elif GraphInstance.getMode( ) == 1:

            GraphInstance.defineLine( COUNTER, 'Quasi-longitudial',
                                      DARK_BLUE,
                                      'solid' )

        COUNTER += 1
        # .................... c_L_thick graph .............................
        # 'Longitudinal out-of-plane'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_L_thick" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_L_thick" ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                  YData = RangeY )

        GraphInstance.defineLine( COUNTER, 'Longitudinal, out-of-plane',
                                  DARK_BLUE,
                                  'dashed' )

        COUNTER += 1
        # ............................ c_S graph ...................................
        # 'Shear, in-plane'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_S" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_S" ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                  YData = RangeY )

        if GraphInstance.getMode() == 0:

            GraphInstance.defineLine( COUNTER, 'Shear, in-plane',
                                      LIGHT_BLUE,
                                      'solid' )

        elif GraphInstance.getMode() == 1:

            GraphInstance.defineLine( COUNTER, 'Shear',
                                      LIGHT_BLUE,
                                      'solid' )

        COUNTER += 1

        if GraphInstance.getMode( ) == 0:
            # ................... c_S_outofplane_1 graph ...........................
            # 'Shear out-of-plane prop. (G32)'
            RangeX = [ MinCoordinateX, MaxCoordinateX ]
            RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][
                           "c_S_outofplane_1" ],
                       GraphInstance.Containers[ "WaveVelocity" ][
                           "c_S_outofplane_1" ] ]

            GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                      YData = RangeY )

            GraphInstance.defineLine( COUNTER,
                                      'Shear, out-of-plane propagation (G31)',
                                      LIGHT_BLUE,
                                      'dashed' )

            COUNTER += 1
            # ................... c_S_outofplane_2 graph ............................
            # 'Shear out-of-plane prop. (G31)'
            RangeX = [ MinCoordinateX, MaxCoordinateX ]
            RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][
                           "c_S_outofplane_2" ],
                       GraphInstance.Containers[ "WaveVelocity" ][
                           "c_S_outofplane_2" ] ]

            GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                      YData = RangeY )

            GraphInstance.defineLine( COUNTER,
                                      'Shear, out-of-plane propagation (G32)',
                                      LIGHT_BLUE,
                                      'dashed' )

            COUNTER += 1

        # ......................... c_B_shear graph ................................
        # 'Shear (corrected), out-of-plane displ.'
        RangeX = [ MinCoordinateX, MaxCoordinateX ]
        RangeY = [ GraphInstance.Containers[ "WaveVelocity" ][ "c_B_shear" ],
                   GraphInstance.Containers[ "WaveVelocity" ][ "c_B_shear" ] ]

        GraphInstance.GraphData[ COUNTER ].data = dict( XData = RangeX,
                                                  YData = RangeY )

        GraphInstance.defineLine( COUNTER, 'Shear (corrected), out-of-plane displ.',
                                  LIGHT_BLUE,
                                  'dashdot' )

        COUNTER += 1
        # ............................ c_B graph ...................................
        # 'Pure bending (thin plate)'
        GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                                  YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_B" ] )

        GraphInstance.defineLine( COUNTER, 'Pure bending (thin plate)',
                                  GREEN,
                                  'dashed' )

        COUNTER += 1
        # .......................... c_B_eff graph .................................
        # 'Effective bending (thick plate)'
        GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                                  YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_B_eff" ] )

        GraphInstance.defineLine( COUNTER, 'Effective bending (thick plate)',
                                  GREEN,
                                  'solid' )

        COUNTER += 1
        # ............................ c_g graph ...................................
        # 'Group (bending)'
        GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                                  YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_g" ] )

        GraphInstance.defineLine( COUNTER, 'Group (bending)',
                                  ORANGE,
                                  'dashed' )

        COUNTER += 1
        # .......................... c_g_eff graph .................................
        # 'Group (effective bending)'
        GraphInstance.GraphData[ COUNTER ].data = dict( XData = GraphInstance.getRange(),
                                                  YData = GraphInstance.Containers[ "WaveVelocity" ][ "c_g_eff" ] )

        GraphInstance.defineLine( COUNTER, 'Group (effective bending)',
                                  ORANGE,
                                  'solid' )

        COUNTER += 1

def plotModesInBand( GraphInstance ):

    GraphInstance.cleanGraph( )
    GraphInstance.Graph.yaxis.axis_label = "Number of Modes per one-third octave band"
    GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

    # ............................ bending_np graph ............................
    # 'Effective bending (thick plate)'
    GraphInstance.GraphData[ 0 ].data = dict( XData = GraphInstance.Containers[ "ModesInBand" ][ "freq_T" ],
                                              YData = GraphInstance.Containers[ "ModesInBand" ][ "bending" ] )

    GraphInstance.defineLine( 0, 'Effective bending (thick plate)',
                              GREEN,
                              'solid' )


    GraphInstance.Circles[ 0 ].data_source.data.update({"x" : GraphInstance.GraphData[ 0 ].data[ "XData" ],
                                                        "y" : GraphInstance.GraphData[ 0 ].data[ "YData" ]})

    GraphInstance.Graph.legend[ 0 ].items[ 0 ] = LegendItem( label = 'Effective bending (thick plate)',
                                                             renderers = [ GraphInstance.Lines[ 0 ],
                                                             GraphInstance.Circles[ 0 ] ] )

    GraphInstance.Circles[ 0 ].glyph.line_color = GREEN
    GraphInstance.Circles[ 0 ].glyph.fill_color = GREEN


    # ............................ compressional_np graph ......................
    # 'Shear, in-plane'
    GraphInstance.GraphData[ 1 ].data = dict( XData = GraphInstance.Containers[ "ModesInBand" ][ "freq_T" ],
                                              YData = GraphInstance.Containers[ "ModesInBand" ][ "shear" ] )

    GraphInstance.defineLine( 1, 'Shear, in-plane',
                              LIGHT_BLUE,
                              'solid' )

    GraphInstance.Circles[ 1 ].data_source.data.update({"x" : GraphInstance.GraphData[ 1 ].data[ "XData" ],
                                                        "y" : GraphInstance.GraphData[ 1 ].data[ "YData" ]})



    GraphInstance.Graph.legend[ 0 ].items[ 1 ] = LegendItem( label = 'Shear, in-plane',
                                                             renderers = [ GraphInstance.Lines[ 1 ],
                                                                           GraphInstance.Circles[ 1 ] ] )

    GraphInstance.Circles[ 1 ].glyph.line_color = LIGHT_BLUE
    GraphInstance.Circles[ 1 ].glyph.fill_color = LIGHT_BLUE





    # ............................ shear_np graph ..............................
    # 'Quasi-longitudial, in plane'




    GraphInstance.GraphData[ 2 ].data = dict( XData = GraphInstance.Containers[ "ModesInBand" ][ "freq_T" ],
                                              YData = GraphInstance.Containers[ "ModesInBand" ][ "compressional" ] )

    GraphInstance.defineLine( 2, 'Quasi-longitudial, in plane',
                              DARK_BLUE,
                              'solid' )



    GraphInstance.Circles[ 2 ].data_source.data.update({"x" : GraphInstance.GraphData[ 2 ].data[ "XData" ],
                                                        "y" : GraphInstance.GraphData[ 2 ].data[ "YData" ]})



    GraphInstance.Graph.legend[ 0 ].items[ 2 ] = LegendItem( label = 'Quasi-longitudial, in plane',
                                                             renderers = [ GraphInstance.Lines[ 2 ],
                                                                           GraphInstance.Circles[ 2 ] ] )

    GraphInstance.Circles[ 2 ].glyph.line_color = DARK_BLUE
    GraphInstance.Circles[ 2 ].glyph.fill_color = DARK_BLUE




def plotModalDensity( GraphInstance ):

    GraphInstance.cleanGraph( )
    GraphInstance.Graph.yaxis.axis_label = "Modal Density in s/rad"
    GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

    # ............................ bending_np graph ............................
    # 'Quasi-longitudinal, in-plane'
    GraphInstance.GraphData[ 2 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "ModalDensity" ][ "compressional" ] )

    GraphInstance.defineLine( 2, 'Quasi-longitudinal, in-plane',
                              DARK_BLUE,
                              'solid' )

    # ............................ bending_np graph ............................
    # 'Shear, in-plane'
    GraphInstance.GraphData[ 1 ].data = dict( XData = GraphInstance.getRange( ),
                                                YData = GraphInstance.Containers[ "ModalDensity" ][ "shear" ] )

    GraphInstance.defineLine( 1, 'Shear, in-plane',
                              LIGHT_BLUE,
                              'solid' )

    # ............................ bending_np graph ............................
    # 'Effective bending (thick plate)'
    GraphInstance.GraphData[ 0 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "ModalDensity" ][ "bending" ] )

    GraphInstance.defineLine( 0, 'Effective bending (thick plate)',
                              GREEN,
                              'solid' )


def plotModalOverlapFactor( GraphInstance ):

    GraphInstance.cleanGraph( )
    GraphInstance.Graph.yaxis.axis_label = "Half Power Bandwith Modal Overlap Factor"
    GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

    # ...................... Mhp_QuasiLongitudinal graph .......................
    # 'Quasi-longitudinal, in-plane'
    GraphInstance.GraphData[ 2 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "ModalOverlapFactor" ][ "QuasiLongitudinal" ] )

    GraphInstance.defineLine( 2, 'Quasi-longitudinal, in-plane',
                              DARK_BLUE,
                              'solid' )

    # ......................... Mhp_Shear graph ................................
    # 'Shear, in-plane'
    GraphInstance.GraphData[ 1 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "ModalOverlapFactor" ][ "Shear" ] )

    GraphInstance.defineLine( 1, 'Shear, in-plane',
                              LIGHT_BLUE,
                              'solid' )

    # ........................ Mhp_Effective graph .............................
    # 'Effective bending (thick plate)'
    GraphInstance.GraphData[ 0 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "ModalOverlapFactor" ][ "Bending" ] )

    GraphInstance.defineLine( 0, 'Effective bending (thick plate)',
                              GREEN,
                              'solid' )


def plotMaximumElementSize( GraphInstance ):

    GraphInstance.cleanGraph( )
    GraphInstance.Graph.yaxis.axis_label = "Wave length / Max. Element Size in m"
    GraphInstance.Graph.xaxis.axis_label = "Frequency in Hz"

    # ......................        LamdaH graph         .......................
    # 'Bending Wave Length'
    GraphInstance.GraphData[ 0 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "MaxElementSize" ][ "Lamda" ] )

    GraphInstance.defineLine( 0, 'Bending Wave Length',
                              GREEN,
                              'dotted' )

    # .....................  LamdaH_Effective graph  ...........................
    # 'Effective Bending Wave Length'
    GraphInstance.GraphData[ 1 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "MaxElementSize" ][ "Lamda_Eff" ] )

    GraphInstance.defineLine( 1, 'Effective Bending Wave Length',
                              GREEN,
                              'solid' )


    # ........................ ElementSize graph ...............................
    # 'Maximum Element Size \n(Quadratic Shape Functions)'
    GraphInstance.GraphData[ 2 ].data = dict( XData = GraphInstance.getRange( ),
                                              YData = GraphInstance.Containers[ "MaxElementSize" ][ "ElementSize" ] )

    GraphInstance.defineLine( 2, 'Max. Elem. Size: quadr. shape fct.',
                              GRAY,
                              'solid' )


def plotEigenfrequenciesPlate( GraphInstance ):
    Text = "</p>The first four Eigenfrequencies of a four-sided simply " \
           "supported Kirchhoff-plate: <p>" \
           "f<sub>11</sub> = {} Hz, f<sub>12</sub> = {} Hz, " \
           "f<sub>21</sub> = {} Hz, f<sub>22</sub> = {} Hz".format(
        round( GraphInstance.Containers[ "EigenFrequency" ][ "f11" ], 2 ),
        round( GraphInstance.Containers[ "EigenFrequency" ][ "f12" ], 2 ),
        round( GraphInstance.Containers[ "EigenFrequency" ][ "f21" ], 2 ),
        round( GraphInstance.Containers[ "EigenFrequency" ][ "f22" ], 2 )
    )


    GraphInstance.TextWidget.printMessage( Text )
    pass
    '''
    plt.clf( )

    cell_text = [ str(round(Element,3)) for Element in GraphInstance.Functions[ 6 ] ]

    columns = ( '$F_{11}$', '$F_{12}$', '$F_{21}$', '$F_{22}$' )
    colors = plt.cm.BuPu( np.linspace( 0, 0.5, len( columns ) ) )

    table = plt.table( cellText = [ cell_text ],
                       colColours = colors,
                       colLabels = columns,
                       loc = 'center',
                       cellLoc = 'center',
                       bbox = (0.0, 0.4, 0.6, 0.6))

    plt.axis( 'off' )
    table.auto_set_font_size( False )
    table.set_fontsize( 8.5 )

    Counter = GraphInstance.getImageCounter( )

    plt.savefig( './static/images/Eigenfrequencies%d.png' % Counter,
                 bbox_inches = 'tight', pdi = 150)

    #GraphInstance.updateTestGraph( "Eigenfrequencies", Counter )
    '''