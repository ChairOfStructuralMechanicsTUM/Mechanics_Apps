import math
import numpy as np


def wave_speeds( ElasticModulusData,
                 ShearModulusData,
                 PoissonRatiosData,
                 MaterialPropertiesData,
                 GeometryPropertiesData,
                 Isotrop,
                 freq ):
    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param ElasticModulusData: 1D list of flaots
    :param ShearModulusData: 1D list of floats
    :param PoissonRatiosData: 2D list of floats
    :param MaterialPropertiesData: 1D list of floats
    :param GeometryPropertiesData: 1D list of floats
    :param Isotrop: boolean
    :param freq: 1D list of floats
    :return: dictionary with the floowing keys: c_B (1D list of floats),
    c_B_eff (1D list of floats), c_B_shea (float), c_g (list of floats),
    c_g_eff (1D list if floats), c_S ( float ), c_S_outofplane (1D list of floats),
    c_S_outofplane_1 (float), c_S_outofplane_2 (float), c_L (1D list of floats),
    c_L_thick ( float ), f_thickmode_shear (1D list of floats),
    f_thickmode_shear_x (1D list of floats), f_thickmode_shear_y (1D list of floats),
    fR_B (1D list of floats), fR_g (1D list of floats),
    f_thickmode_long (1D list of floats)
    """


    # Wellengeschwindigkeiten
    Subs = len( ElasticModulusData )

    # Omega Vektor
    omeg = np.array( 2 * math.pi * freq )

    # Schubkorrekturfaktor
    kappa = 5.0 / 6

    # allocate numpy arrays
    l = np.zeros( Subs )
    b = np.zeros( Subs )
    d = np.zeros( Subs )
    rho = np.zeros( Subs )
    E1 = np.zeros( Subs )
    E2 = np.zeros( Subs )
    E3 = np.zeros( Subs )

    nu21 = np.zeros( Subs )
    nu13 = np.zeros( Subs )
    nu23 = np.zeros( Subs )

    nu12 = np.zeros( Subs )
    nu31 = np.zeros( Subs )
    nu32 = np.zeros( Subs )

    G12 = np.zeros( Subs )
    G13 = np.zeros( Subs )
    G23 = np.zeros( Subs )
    D_int = np.zeros( Subs )

    # Initialize parameters that have to be return from the function
    c_B = np.zeros( (Subs, freq.size) )
    c_B_eff = np.zeros( (Subs, freq.size) )
    c_B_shear = np.zeros( (Subs, freq.size) )
    c_g = np.zeros( (Subs, freq.size) )
    c_g_eff = np.zeros( (Subs, freq.size) )
    #c_g_eff = np.zeros( (Subs, freq.size) )
    c_S = np.zeros( (Subs, freq.size) )
    c_S_outofplane = np.zeros( (Subs, freq.size) )
    c_S_outofplane_1 = np.zeros( (Subs, freq.size) )
    c_S_outofplane_2 = np.zeros( (Subs, freq.size) )
    c_L = np.zeros( (Subs, freq.size) )
    c_L_thick = np.zeros( (Subs, freq.size) )

    f_thickmode_long = np.zeros( Subs )
    f_thickmode_shear = np.zeros( Subs )
    f_thickmode_shear_x = np.zeros( Subs )
    f_thickmode_shear_y = np.zeros( Subs )

    for i in range( Subs ):
        l[ i ] = np.array( GeometryPropertiesData[ i ][ 0 ] )
        b[ i ] = np.array( GeometryPropertiesData[ i ][ 1 ] )
        d[ i ] = np.array( GeometryPropertiesData[ i ][ 2 ] )
        E1[ i ] = np.array( ElasticModulusData[ i ][ 0 ] )
        E2[ i ] = np.array( ElasticModulusData[ i ][ 1 ] )
        E3[ i ] = np.array( ElasticModulusData[ i ][ 2 ] )

        nu12[ i ] = PoissonRatiosData[ 0 ][ 0 ]
        nu13[ i ] = PoissonRatiosData[ 0 ][ 1 ]
        nu23[ i ] = PoissonRatiosData[ 0 ][ 2 ]

        nu21[ i ] = PoissonRatiosData[ 1 ][ 0 ]
        nu31[ i ] = PoissonRatiosData[ 1 ][ 1 ]
        nu32[ i ] = PoissonRatiosData[ 1 ][ 2 ]

        G12[ i ] = np.array( ShearModulusData[ i ][ 0 ] )
        G13[ i ] = np.array( ShearModulusData[ i ][ 1 ] )
        G23[ i ] = np.array( ShearModulusData[ i ][ 2 ] )
        rho[ i ] = np.array( MaterialPropertiesData[ i ][ 0 ] )
        D_int[ i ] = np.array( MaterialPropertiesData[ i ][ 1 ] )

    ## Berechnung der Wellengeschwindigkeiten
    # debugging


    if Isotrop == True:  # ISO
        # allocate numpy arrays
        c_B = np.zeros( (Subs, freq.size) )
        c_L = np.zeros( (Subs, freq.size) )
		#c_L_thick = np.zeros( (Subs, freq.size) )
        c_S = np.zeros( (Subs, freq.size) )
        c_g = np.zeros( (Subs, freq.size) )
        c_B_shear = np.zeros( (Subs, freq.size) )
        c_B_eff = np.zeros( (Subs, freq.size) )
        c_g_eff = np.zeros( (Subs, freq.size) )
        c_B_eff_1 = np.zeros( (Subs, freq.size) )
        c_B_eff_2 = np.zeros( (Subs, freq.size) )

        fR_B = np.zeros( Subs )
        fR_g = np.zeros( Subs )

        G = np.zeros( Subs )
        B = np.zeros( Subs )
        S = np.zeros( Subs )
        U = np.zeros( Subs )

        f_thickmode_long = np.zeros( Subs )
        f_thickmode_shear = np.zeros( Subs )
        f_thickmode_shear_x = np.zeros( Subs )
        f_thickmode_shear_y = np.zeros( Subs )

        for i in range( Subs ):
            G[ i ] = E1[ i ] / (
            2 * (1 + nu21[ i ]))  # Schubmodul aus isotropem Materialgesetz
            B[ i ] = E1[ i ] * d[ i ] ** 3 / (
            12 * (1 - nu21[ i ] ** 2))  # Biegesteifigkeit

            c_B_shear[ i, : ] = np.sqrt( G[ i ] * kappa / rho[ i ] )  # |

            # S[i]=l[i]*b[i]              # Flaeche der Platte
            # U[i] = 2*l[i]+2*b[i]       #Umfang der Platte
            # |
            c_L[ i, : ] = np.sqrt(
                E1[ i ] / (rho[ i ] * (1 - nu21[ i ] ** 2)) )  # |

            c_L_thick[ i, : ] = np.sqrt( E3[ i ]*( 1 - nu12[ i ] ) #\
                            / ( rho[ i ] * (1 - nu12[ i ] - 2 * nu21[ i ] ** 2)) )
            # |
            # |
            c_S[ i, : ] = np.sqrt( G[ i ] / rho[ i ] )  # |
            # |

            # --Anspassung der Biegemoden an dicke Platte v.a. nach Meier 2000--
            # tw,01.02.17

            # rayleighwellengeschwindigkeit nach Moeser et al 2010
            #c_B_shear[ i, : ] = 1 * c_B_shear[ i,
            #                        : ]  # Abschaetzung Rayleighgeschwindigkeit

            fR_B[ i ] = c_B_shear[ i, 0 ] ** 2 / (2 * math.pi) * np.sqrt(
                (rho[ i ] * d[ i ]) / B[ i ] )  # Grenzfrequenz nach Meier 2000
            fR_g[ i ] = fR_B[ i ] / 4

            c_B[ i, : ] = ((omeg ** 2 * B[ i ]) / (rho[ i ] * d[ i ])) ** (
            1.0 / 4)  # gesamte formel zB Craik
            c_g[ i, : ] = 2 * c_B[ i, : ]
            c_B_eff[ i, : ] = c_B_shear[ i, : ] * freq / fR_B[ i ] * np.sqrt(
                -0.5 + 0.5 * np.sqrt( 1 + (2 * fR_B[
                    i ] / freq) ** 2 ) )  # korrigierte Biegewellengeschwindigkeit dicke Platte
            c_g_eff[ i, : ] = c_B_eff[ i, : ] ** 3 / c_B_shear[ i,
                                                     : ] ** 2 * np.sqrt( 1 + (
            2 * fR_B[
                i ] / freq) ** 2 )  # korrigierte Biegegruppenwellengeschwindigkeit

            f_thickmode_long[ i ] = c_L_thick[ i, 0 ] / (2 * d[ i ])
            f_thickmode_shear[ i ] = c_S[ i, 0 ] / (2 * d[ i ])
            f_thickmode_shear_x[ i ] = f_thickmode_shear[ i ]
            f_thickmode_shear_y[ i ] = f_thickmode_shear[ i ]
            c_B_eff_1[ i, : ] = c_B_eff[ i, : ]
            c_B_eff_2[ i, : ] = c_B_eff[ i, : ]


    elif Isotrop == False:

        # allocate numpy arrays
        c_B = np.zeros( (Subs, freq.size) )
        c_g = np.zeros( (Subs, freq.size) )
        c_L = np.zeros( (Subs, freq.size) )
        c_L_thick = np.zeros( (Subs, freq.size) )

        c_S = np.zeros( (Subs, freq.size) )
        c_S_outofplane = np.zeros( (Subs, freq.size) )
        c_S_outofplane_1 = np.zeros( (Subs, freq.size) )
        c_S_outofplane_2 = np.zeros( (Subs, freq.size) )

        c_B_shear = np.zeros( (Subs, freq.size) )
        c_B_shear_1 = np.zeros( (Subs, freq.size) )
        c_B_shear_2 = np.zeros( (Subs, freq.size) )

        c_B_eff = np.zeros( (Subs, freq.size) )
        c_g_eff = np.zeros( (Subs, freq.size) )
        c_B_eff_1 = np.zeros( (Subs, freq.size) )
        c_g_eff_1 = np.zeros( (Subs, freq.size) )
        c_B_eff_2 = np.zeros( (Subs, freq.size) )
        c_g_eff_2 = np.zeros( (Subs, freq.size) )

        # nu12 = np.zeros(Subs)
        # nu31 = np.zeros(Subs)
        # nu32 = np.zeros(Subs)

        D_nu = np.zeros( Subs )
        S = np.zeros( Subs )
        U = np.zeros( Subs )
        c_L_1 = np.zeros( Subs )
        c_L_2 = np.zeros( Subs )
        B1 = np.zeros( Subs )
        B2 = np.zeros( Subs )
        B = np.zeros( Subs )

        fR_B = np.zeros( Subs )
        fR_g = np.zeros( Subs )
        fR_B_1 = np.zeros( Subs )
        fR_g_1 = np.zeros( Subs )
        fR_B_2 = np.zeros( Subs )
        fR_g_2 = np.zeros( Subs )

        c_B_1 = np.zeros( (Subs, freq.size) )
        c_g_1 = np.zeros( (Subs, freq.size) )
        c_B_2 = np.zeros( (Subs, freq.size) )
        c_g_2 = np.zeros( (Subs, freq.size) )

        f_thickmode_long = np.zeros( Subs )
        f_thickmode_shear = np.zeros( Subs )
        f_thickmode_shear_x = np.zeros( Subs )
        f_thickmode_shear_y = np.zeros( Subs )

        G = np.zeros( Subs )

        # Orthotrope Berechnung

        for i in range( Subs ):
            '''
            nu12[i]=E1[i]/E2[i]*nu21[i]    # Aus orthotropem Materialgesetz
            nu31[i]=E1[i]/E3[i]*nu13[i]
            nu32[i]=E2[i]/E3[i]*nu23[i]
            '''
            # Determinante der Nachgiebigkeitsmatrix nach Wikipedia Orthotropie
            D_nu[ i ] = 1 - nu12[ i ] * nu21[ i ] - nu13[ i ] * nu31[ i ] - \
                        nu23[ i ] * nu32[ i ] - 2 * nu12[ i ] * nu23[ i ] * \
                                                nu31[ i ]

            # Biegesteifigkeit,Anpassung Emodul um Querdehnungsbehinderung zu beruecksichtigen
            B1[ i ] = E1[ i ] * d[ i ] ** 3 / (12 * (1 - nu12[ i ] * nu21[ i ]))
            B2[ i ] = E2[ i ] * d[ i ] ** 3 / (12 * (1 - nu12[ i ] * nu21[ i ]))
            B[ i ] = np.sqrt( B1[ i ] * B2[ i ] )

            # S[i]=l[i]*b[i]              # Flaeche der Platte
            # U[i] = 2*l[i]+2*b[i]        #Umfang der Platte

            # |cw,18.12.16, Anpassung Emodul um Querdehnungsbehinderung zu beruecksichtigen

            c_L_1[ i ] = np.sqrt(
                E1[ i ] / (rho[ i ] * (1 - nu12[ i ] * nu21[ i ])) )
            c_L_2[ i ] = np.sqrt(
                E2[ i ] / (rho[ i ] * (1 - nu12[ i ] * nu21[ i ])) )
            c_L[ i, : ] = np.sqrt( c_L_1[ i ] * c_L_2[ i ] )

            c_L_thick[ i, : ] = np.sqrt(
                E3[ i ] / rho[ i ] * (1 - nu12[ i ] * nu21[ i ]) / D_nu[ i ] )

            c_B_shear_1[ i, : ] = np.sqrt( G13[ i ] * kappa / rho[ i ] )
            c_B_shear_2[ i, : ] = np.sqrt( G23[ i ] * kappa / rho[ i ] )
            c_B_shear[ i, : ] = np.sqrt(
                c_B_shear_1[ i, 0 ] * c_B_shear_2[ i, 0 ] )

            c_S_outofplane_1[ i, : ] = np.sqrt( G13[ i ] / (rho[ i ]) )
            c_S_outofplane_2[ i, : ] = np.sqrt( G23[ i ] / (rho[ i ]) )
            c_S_outofplane[ i, : ] = np.sqrt(
                c_S_outofplane_1[ i, 0 ] * c_S_outofplane_2[ i, 0 ] )
            # | cw,18.12.16 2*G12 anstatt G12 fuer thick plate theory acc. to stiffness matrix

            c_S[ i, : ] = np.sqrt( 2 * G12[ i ] / rho[ i ] )
            # --Anspassung der Biegemoden an dicke Platte v.a. nach Meier 2000--
            # tw,01.02.17

            # Grenzfrequenz nach Meier 2000
            fR_B[ i ] = c_B_shear[ i, 0 ] ** 2 / (2 * math.pi) * np.sqrt(
                (rho[ i ] * d[ i ]) / B[ i ] )  #
            fR_g[ i ] = fR_B[ i ] / 4  #

            fR_B_1[ i ] = c_B_shear_1[ i, 0 ] ** 2 / (2 * math.pi) * np.sqrt(
                (rho[ i ] * d[ i ]) / B1[ i ] )  # Grenzfrequenz nach Meier 2000
            fR_g_1[ i ] = fR_B_1[ i ] / 4

            fR_B_2[ i ] = c_B_shear_2[ i, 0 ] ** 2 / (2 * math.pi) * np.sqrt(
                (rho[ i ] * d[ i ]) / B2[ i ] )  # Grenzfrequenz nach Meier 2000
            fR_g_2[ i ] = fR_B_2[ i ] / 4

            c_B[ i, : ] = ((omeg ** 2 * B[ i ]) / (rho[ i ] * d[ i ])) ** (
            1.0 / 4)  # gesamte formel zB Craik
            c_g[ i, : ] = 2 * c_B[ i, : ]
            c_B_eff[ i, : ] = c_B_shear[ i, : ] * freq / fR_B[ i ] * np.sqrt(
                -0.5 + 0.5 * np.sqrt( 1 + (2 * fR_B[
                    i ] / freq) ** 2 ) )  # korrigierte Biegewellengeschwindigkeit dicke Platte
            c_g_eff[ i, : ] = c_B_eff[ i, : ] ** 3 / c_B_shear[ i,
                                                     : ] ** 2 * np.sqrt( 1 + (
            2 * fR_B[
                i ] / freq) ** 2 )  # korrigierte Biegegruppenwellengeschwindigkeit

            c_B_1[ i, : ] = ((omeg ** 2 * B1[ i ]) / (rho[ i ] * d[ i ])) ** (
            1.0 / 4)  # gesamte formel zB Craik
            c_g_1[ i, : ] = 2 * c_B_1[ i, : ]
            c_B_eff_1[ i, : ] = c_B_shear_1[ i ] * freq / fR_B_1[ i ] * np.sqrt(
                -0.5 + 0.5 * np.sqrt( 1 + (2 * fR_B_1[
                    i ] / freq) ** 2 ) )  # korrigierte Biegewellengeschwindigkeit dicke Platte
            c_g_eff_1[ i, : ] = c_B_eff_1[ i, : ] ** 3 / c_B_shear_1[
                                                             i ] ** 2 * np.sqrt(
                1 + (2 * fR_B_1[
                    i ] / freq) ** 2 )  # korrigierte Biegegruppenwellengeschwindigkeit

            c_B_2[ i, : ] = ((omeg ** 2 * B2[ i ]) / (rho[ i ] * d[ i ])) ** (
            1.0 / 4)  # gesamte formel zB Craik
            c_g_2[ i, : ] = 2 * c_B_2[ i, : ]
            c_B_eff_2[ i, : ] = c_B_shear_2[ i ] * freq / fR_B_2[ i ] * np.sqrt(
                -0.5 + 0.5 * np.sqrt( 1 + (2 * fR_B_2[
                    i ] / freq) ** 2 ) )  # korrigierte Biegewellengeschwindigkeit dicke Platte
            c_g_eff_2[ i, : ] = c_B_eff_2[ i, : ] ** 3 / c_B_shear_2[
                                                             i ] ** 2 * np.sqrt(
                1 + (2 * fR_B_2[
                    i ] / freq) ** 2 )  # korrigierte Biegegruppenwellengeschwindigkeit

            f_thickmode_long[ i ] = c_L_thick[ i, 0 ] / (2 * d[ i ])
            f_thickmode_shear[ i ] = c_S_outofplane[ i, 0 ] / (2 * d[ i ])
            f_thickmode_shear_x[ i ] = c_S_outofplane_1[ i, 0 ] / (2 * d[ i ])
            f_thickmode_shear_y[ i ] = c_S_outofplane_2[ i, 0 ] / (2 * d[ i ])

            # G[i] = np.sqrt(G13[i]*G23[i])

    # Prepare data that have to be returned from the function
    Result = { "c_B": c_B.tolist( )[ 0 ],  #
               "c_B_eff": c_B_eff.tolist( )[ 0 ],  #
               "c_B_shear": c_B_shear.tolist( )[ 0 ][ 0 ],
               "c_g": c_g.tolist( )[ 0 ],  #
               "c_g_eff": c_g_eff.tolist( )[ 0 ],  #
               "c_S": c_S.tolist( )[ 0 ][ 0 ],
               "c_S_outofplane": c_S_outofplane.tolist( )[ 0 ],
               "c_S_outofplane_1": c_S_outofplane_1.tolist( )[ 0 ][ 0 ],
               "c_S_outofplane_2": c_S_outofplane_2.tolist( )[ 0 ][ 0 ],
               "c_L": c_L.tolist( )[ 0 ],
               "c_L_thick": c_L_thick.tolist( )[ 0 ][ 0 ],
               "f_thickmode_shear": f_thickmode_shear.tolist( )[ 0 ],
               "f_thickmode_shear_x": f_thickmode_shear_x.tolist( )[ 0 ],
               "f_thickmode_shear_y": f_thickmode_shear_y.tolist( )[ 0 ],
               "fR_B": fR_B.tolist( )[ 0 ],
               "fR_g": fR_g.tolist( )[ 0 ],
               "f_thickmode_long": f_thickmode_long.tolist( )[ 0 ]}

    return Result


#def ModaleDichte(c_L, c_S, c_B_eff, c_g_eff, Geometry, Isotrop, Bending, Compressional, Shear, Sum):
def ModaleDichte(c_L, c_S, c_B_eff, c_g_eff, Geometry, Isotrop, freq ):
    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param c_L: 1D list of floats
    :param c_S: float
    :param c_B_eff: 1D list of floats
    :param c_g_eff: 1D list of floats
    :param Geometry:1D list of floats
    :param Isotrop: boolean
    :param freq: 1D list of floats
    :return: dictionary with the following keys: bending_np (1D list of floats),
    compressional_np (1D list of floats), shear_np (1D list of floats),
    sum_np (1D list of floats)
    """


    # allocate numpy arrays
    n_f = np.zeros(freq.size)
    delta_f_bend = np.zeros(freq.size)
    delta_f_comp = np.zeros(freq.size)
    delta_f_shear = np.zeros(freq.size)

    bending_np = np.zeros(freq.size)
    compressional_np = np.zeros(freq.size)
    shear_np = np.zeros(freq.size)
    sum_np = np.zeros(freq.size)

    Length = Geometry[ 0 ][ 0 ]
    Width = Geometry[ 0 ][ 1 ]

    # Flaeche der Platte
    Area = Length * Width
    CoeffOne = 2.0 * math.pi
    CoeffTwo = CoeffOne * Area


    for i in range(freq.size):
        n_f[ i ] = ( CoeffTwo * freq[ i ] ) / ( c_B_eff[ i ] * c_g_eff[ i ] )
        delta_f_bend[ i ] = 1.0 / n_f[ i ]
        delta_f_comp[ i ] = ( c_L[ i ] * c_L[ i ] ) / ( CoeffTwo * freq[ i ] )
        delta_f_shear[ i ] = c_S * c_S / ( CoeffTwo * freq[ i ] )
        bending_np[ i ] = 1.0 / ( CoeffOne * delta_f_bend[ i ] )
        compressional_np[ i ] = 1.0 / ( CoeffOne * delta_f_comp[ i ] )
        shear_np[ i ] = 1.0 / ( CoeffOne * delta_f_shear[ i ] )
        sum_np = bending_np[ i ] + shear_np[ i ] + compressional_np[ i ]



    # Prepare data that have to be returned from the function
    Result = { "bending" : bending_np.tolist(),         #eff bemding
               "compressional" : compressional_np.tolist( ),  #quasi/longitudinal
               "shear" : shear_np.tolist( ),
               "sum" : sum_np.tolist( ) }

    return Result


def ModesInBand( ElasticModulusData,
                 ShearModulusData,
                 PoissonRatiosData,
                 MaterialPropertiesData,
                 GeometryPropertiesData,
                 Isotrop,
                 freq ):

    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param ElasticModulusData: 1D list of floats
    :param ShearModulusData: 1D list of floats
    :param PoissonRatiosData: 2D list of floats
    :param MaterialPropertiesData: 1D list of floats
    :param GeometryPropertiesData: 1D list if floats
    :param Isotrop: boolean
    :param freq: 1D list of floats
    :return: dictionary with the following keys: bending (1D list of floats),
    compressional (1D list of floats), shear (1D list of floats), sum (1D list of floats),
    freq_T (1D list of floats)
    """

    fmstart = freq[ 0 ]
    fmend = freq[ -1 ]
    #    fmstart = 0.9765625
    #    fmend = 16000

    B = 1.0 / 3.0
    Baender = (1.0 / B ) * np.log2( fmend / fmstart ) + 1.0
    i = np.linspace( 1, Baender, Baender, dtype = int )

    freq_T = np.zeros( i.size )
    for j in range(i.size):
        freq_T[ j ] = fmstart*2.0**( ( i[ j ] - 1 ) * B );
        pass

    # additional input data
    subs = 1;
    f_o = freq_T * 2.0**(B / 2.0)
    f_u = freq_T * 2.0**(-B / 2.0)
    Delta_F = np.zeros( len( freq_T ) );
    Delta_F = f_o - f_u

    # MATLAB: ModDichteOben = ModaleDichte( para, f_o );
    # MATLAB: ModDichteUnten = ModaleDichte( para, f_u );


    # Prepare the data
    Result = wave_speeds( ElasticModulusData,
                          ShearModulusData,
                          PoissonRatiosData,
                          MaterialPropertiesData,
                          GeometryPropertiesData,
                          Isotrop,
                          freq_T )


    ModDichteOben = ModaleDichte( Result[ "c_L" ],
                                  Result[ "c_S" ],
                                  Result[ "c_B_eff" ],
                                  Result[ "c_g_eff" ],
                                  GeometryPropertiesData,
                                  Isotrop,
                                  f_o )

    ModDichteUnten = ModaleDichte( Result[ "c_L" ],
                                   Result[ "c_S" ],
                                   Result[ "c_B_eff" ],
                                   Result[ "c_g_eff" ],
                                   GeometryPropertiesData,
                                   Isotrop,
                                   f_u )



    bending = [ 0.0 ] * i.size
    compressional = [ 0.0 ] * i.size
    shear = [ 0.0 ] * i.size
    sum = [ 0.0 ] * i.size
    for j in range(i.size):

        bending[ j ] = 0.5 * ( ModDichteOben[ "bending" ][ j ]
                               + ModDichteUnten[ "bending" ][ j ] ) \
                           * Delta_F[ j ] * 2.0 * np.pi

        compressional[ j ] = 0.5 * ( ModDichteOben[ "compressional" ][ j ]
                                     + ModDichteUnten[ "compressional" ][ j ] ) \
                                 * Delta_F[ j ] * 2.0 * np.pi

        shear[ j ] = 0.5 * ( ModDichteOben[ "shear" ][ j ]
                             + ModDichteUnten[ "shear" ][ j ] ) \
                         * Delta_F[ j ] * 2.0 * np.pi

        sum[ j ] = bending[ j ] + compressional[ j ] + shear[ j ]

    return { "bending" : bending,
             "compressional" : compressional,
             "shear" : shear,
             "sum" : sum,
             "freq_T" : freq_T }


def EigenfrequenciesPlate( ElasticModulusData,
                           ShearModulusData,
                           PoissonRatiosData,
                           MaterialPropertiesData,
                           GeometryPropertiesData,
                           Isotrop,
                           freq ):
    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param ElasticModulusData: 1D list of floats
    :param ShearModulusData: 1D list of floats
    :param PoissonRatiosData: 2D list of floats
    :param MaterialPropertiesData: 1D list of floats
    :param GeometryPropertiesData: 1D list of floats
    :param Isotrop: boolean
    :param freq: 1D list of floats
    :return: dictionary with the following keys: f11 (float), f12 (float),
    f21 (float), f22 (float)
    """

    # Input Variables
    thickness = GeometryPropertiesData[ 0 ][ 2 ]
    length = GeometryPropertiesData[ 0 ][ 0 ]
    width = GeometryPropertiesData[ 0 ][ 1 ]
    Density = MaterialPropertiesData[ 0 ][ 0 ]

    #if Isotrop == True:
    if Isotrop == True:

        E = ElasticModulusData[ 0 ][ 0 ]
        nu = PoissonRatiosData[ 0 ][ 0 ]

        # Calculcations
        D = E * thickness**3 / (12.0 * (1.0 - nu*nu))
        mu = Density * thickness;

        # MATLAB: omega = @( m, n ) sqrt( D / mu ) * ((m * pi / length) ^ 2 + (n * pi / width) ^ 2);
        omega = lambda m,n: np.sqrt( D / mu ) * ((m * np.pi / length)**2 + (n * np.pi / width)**2)

        # Output
        Result = { "f11" : omega( 1.0, 1.0 )/(2.0 * np.pi), \
                   "f12" : omega( 1.0, 2.0 )/(2.0 * np.pi), \
                   "f21" : omega( 2.0, 1.0 )/(2.0 * np.pi), \
                   "f22" : omega( 2.0, 2.0 )/(2.0 * np.pi) }


    if Isotrop == False:

        # Input Variables
        # x - 0; y - 1; z - 2

        E_x = ElasticModulusData[ 0 ][ 0 ]
        E_y = ElasticModulusData[ 0 ][ 1 ]

        G_xy = ShearModulusData[ 0 ][ 0 ] # sqrt( 488.9E+09 * 3.211E+08 );

        nu_x = PoissonRatiosData[ 0 ][ 0 ] # nu_xy
        nu_y = PoissonRatiosData[ 1 ][ 0 ] # nu_yx

        D_x = E_x * thickness**2 / (12.0 * (1.0 - nu_x*nu_y))
        D_y = E_y * thickness**2 / (12.0 * (1.0 - nu_x * nu_y))
        D_k = G_xy * thickness**2 / 12.0
        D_xy = D_x * nu_y + 2.0 * D_k


        # MATLAB: omega = @(m,n) pi^2/(length^2*sqrt(Density)) *
        # sqrt(D_x*m^4+2*D_xy*m^2*n^2*(length/width)^2+D_y*n^4*(length/width)^4);

        CoeffOne = ( np.pi**2 ) / ( ( length**2 ) * np.sqrt( Density ) )
        CoeffTwo = 2.0 * D_xy * ( length / width )**2
        CoeffThree = D_y * ( length / width )**4

        omega = lambda m, n: CoeffOne * np.sqrt( D_x*m**4 + CoeffTwo * m**2 * n**2 + CoeffThree * n**4 )

        #Result = [ omega( 1.0, 1.0 )/(2.0 * np.pi), \
        #           omega( 1.0, 2.0 )/(2.0 * np.pi), \
        #           omega( 2.0, 1.0 )/(2.0 * np.pi), \
        #           omega( 2.0, 2.0 )/(2.0 * np.pi) ]

        Result = { "f11" : omega( 1.0, 1.0 )/(2.0 * np.pi), \
                   "f12" : omega( 1.0, 2.0 )/(2.0 * np.pi), \
                   "f21" : omega( 2.0, 1.0 )/(2.0 * np.pi), \
                   "f22" : omega( 2.0, 2.0 )/(2.0 * np.pi) }


    return Result


def ModalOverlapFactor( MaterialPropertiesData,
                        ModalDensities,
                        Frequency ):

    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param MaterialPropertiesData: 1D list of floats
    :param ModalDensities: dictionary with keys: "bending", "compressional" and "shear"
    :param Frequency: 1D list of floats
    :return: dictionary with the following keys: Mhp_Bending (1D list of floats),
    Mhp_Shear (1D list of floats), Mhp_QuasiLongitudinal (1D list of floats)
    """

    BendingDensity = ModalDensities[ "bending" ]
    CompressionalDensity = ModalDensities[ "compressional" ]
    ShearDensity = ModalDensities[ "shear" ]
    LossFactor = MaterialPropertiesData[ 0 ][ 1 ]

    Coeff = 2.0 * np.pi * LossFactor
    Mhp_Bending = [ Coeff * f * d for f, d in zip( Frequency, BendingDensity ) ]
    Mhp_Shear = [ Coeff * f * d for f, d in zip( Frequency, ShearDensity ) ]
    Mhp_QuasiLongitudinal = [ Coeff * f * d for f, d in zip( Frequency, CompressionalDensity ) ]

    return { "Bending" : Mhp_Bending,
             "Shear" : Mhp_Shear,
             "QuasiLongitudinal" : Mhp_QuasiLongitudinal }


def MaximumElementSize( C_B_Array, C_B_eff_Array, Frequency ):

    """
    <description> <reference>
    Developer: Christoph Winter ( christoph.winter@tum.de )
    :param C_B_Array: 1D list of floats
    :param C_B_eff_Array: 1D list of floats
    :param Frequency: 1D list of floats
    :return: dictionary with the following keys: Lamda (1D list of floats),
    Lamda_Eff (1D list of floats), ElementSize (1D list of floats)
    """

    LamdaH = [ C_B / f for C_B, f in zip( C_B_Array, Frequency ) ]
    LamdaH_Effective = [ C_B_eff / f for C_B_eff, f in zip( C_B_eff_Array, Frequency ) ]
    ElementSize = [ 0.25 * Entry for Entry in LamdaH_Effective ]

    return { "Lamda" : LamdaH,
             "Lamda_Eff" : LamdaH_Effective,
             "ElementSize" : ElementSize }