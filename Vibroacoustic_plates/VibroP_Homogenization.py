import math


def homogenize( E, G, NU, D ):
    """
    The function takes parameters of a composite material and converts it to
    the properties of an isotropic material.
    Developer: Christoph Winter ( christoph.winter@tum.de )

    :param E: Elastic Modulus. 2D list of floats
    :param G: ShearModulus. 2D list of floats
    :param NU: Poisson Ratios. 2D list of floats
    :param D: Thickness of layers. 1D list of floats
    :return: dictionary that contains the following properties: Elastic Modulus (list),
    Shear Modulus(list), Poisson Ratios (list), Total Thickness (float)
    """
    print("test 02.2._hom_00")
    # Quantity of layers (needs to be uneven)
    Quantity = len(D)
    if Quantity % 2 == 0:
        print ("Amount of layers must be uneven")
        return
    print("test 02.2._hom_01")
    if Quantity == 0:
        print ("No Homogenisation needed")
        return
    print("test 02.2._hom_02")
    # conver the array of NU from 2D to 1D
    nu = []
    for i in range( len(NU) ):
        for Element in NU[ i ]:
            nu.append( Element )
    print("test 02.2._hom_03")
#===============================================================================
# For comprehensibility
# Sum up all layers turned differently
# then the first(and last) layer D[1] + D[3] +...
#===============================================================================

    Turned_Layers = sum(D[1:-1:2])
    # total Thickness
    print("test 02.2._hom_04")
    TN = sum(D)
    G1_eff =(G[0]*(sum(D[0::2]))+G[0]*(Turned_Layers))/TN
    G2_eff = G[1]*G[2]*TN/(G[2]*(sum(D[0::2]))+G[1]*(Turned_Layers))

    G3_eff = G[2]*G[1]*TN/(G[1]*(sum(D[0::2]))+G[2]*(Turned_Layers))
    #====================================
    print("test 02.2._hom_05")
    Matrjoschka = 0
    #copysign(x,y):
    #Return x with the sign of y. (There is no sign() in Python)
    # Middle Part
    for i in range(1,(Quantity+1)//2): # 1,2,3...Quantity  # X%Y rest of modulo division X/Y???
        Matrjoschka = -math.copysign(1,i%2 -1) * (1-E[1]/E[0]) * sum(D[i:-i])**3 + Matrjoschka
    print("test 02.2._hom_06")
    # Homogenisation of Parameters
    E1_eff = E[0]/TN**3 *(TN**3     +   Matrjoschka)
    E2_eff = E[0]/TN**3 *(E[1]/E[0]*TN**3   -   Matrjoschka)
    E3_eff = E[2]
    #====================================
    print("test 02.2._hom_07")
    # nu[0-5]=n12,nu13,nu23,nu21,nu31,nu32
    nu12_eff_1 = ((sum(D[0::2]))*nu[0]+(Turned_Layers)*nu[3])/TN
    nu21_eff_1 = ((sum(D[0::2]))*nu[3]+(Turned_Layers)*nu[0])/TN
    nu13_eff_1 = ((sum(D[0::2]))*nu[1]+(Turned_Layers)*nu[2])/TN
    nu31_eff_1 = ((sum(D[0::2]))*nu[4]+(Turned_Layers)*nu[5])/TN
    nu23_eff_1 = ((sum(D[0::2]))*nu[2]+(Turned_Layers)*nu[1])/TN
    nu32_eff_1 = ((sum(D[0::2]))*nu[5]+(Turned_Layers)*nu[4])/TN
    print("test 02.2._hom_08")
    nu12_eff_2 = nu21_eff_1*E1_eff/E2_eff
    nu21_eff_2 = nu12_eff_1*E2_eff/E1_eff
    nu13_eff_2 = nu31_eff_1*E1_eff/E3_eff
    nu31_eff_2 = nu13_eff_1*E3_eff/E1_eff
    nu23_eff_2 = nu32_eff_1*E2_eff/E3_eff
    nu32_eff_2 = nu23_eff_1*E3_eff/E2_eff
    print("test 02.2._hom_09")
    nu12_eff = (nu12_eff_1 + nu12_eff_2)/2
    nu21_eff = (nu21_eff_1 + nu21_eff_2)/2
    nu13_eff = (nu13_eff_1 + nu13_eff_2)/2
    nu31_eff = (nu31_eff_1 + nu31_eff_2)/2
    nu23_eff = (nu23_eff_1 + nu23_eff_2)/2
    nu32_eff = (nu32_eff_1 + nu32_eff_2)/2
    print("test 02.2._hom_10")
    ### ========= Check and return results  =======
    # Checking criteria for stability all values must be positive
    Check1 =  1-nu12_eff*nu21_eff
    Check2 =  1-nu13_eff*nu31_eff
    Check3 =  1-nu23_eff*nu32_eff
    Check4 =  1-nu12_eff*nu21_eff-nu13_eff*nu31_eff-nu23_eff*nu32_eff-2*nu12_eff*nu23_eff*nu31_eff
    print("test 02.2._hom_11")

    return { "ElasticModulus" : [ format(E1_eff,'.2E'),format(E2_eff,'.2E'),format(E3_eff,'.2E') ],
             "ShearModulus" : [ format(G1_eff,'.2E'),format(G2_eff,'.2E'),format(G3_eff,'.2E') ],
             "PoissonRatios": [ [ format(nu12_eff,'.5f'), format(nu13_eff,'.5f'), format(nu23_eff,'.5f') ],
                                [ format(nu21_eff,'.5f'), format(nu31_eff,'.5f'), format(nu32_eff,'.5f') ] ],
             "TotalThickness" : sum(D) }