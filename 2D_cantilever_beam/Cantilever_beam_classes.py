import numpy as np
import math
from bokeh.plotting import figure


### FUNCTION NOT USED!! --> CUT ###
def generate_colorbar(palette, low=0, high=15, plot_height = 100, plot_width = 500):

    y = np.linspace(low,high,len(palette))
    dy = y[1]-y[0]
    fig = figure(tools="", y_range = [0, 1], x_range = [low, high],plot_width = plot_width, plot_height=plot_height)
    fig.toolbar_location=None
    fig.yaxis.visible = None
    fig.rect(x=y, y=0.5, color=palette, width=dy, height = 1)
    return fig

## Build array for x- and y-coordinates of elements with y=0. Construct similar array for z=0.
def construct_undeformed_beam_centerline( noElementsX, noElementsY, noElementsZ,
                                          elementSizeX
                                        ):
    
    undeformedBeamXY = list()
    yComponent = 0.0
    xComponent = 0.0
    for i in range(noElementsX + 1):
        undeformedBeamXY.append( [ xComponent, yComponent ] )
        xIncrement = elementSizeX
        xComponent += xIncrement        
    
    undeformedBeamXZ = undeformedBeamXY
    
    return undeformedBeamXY, undeformedBeamXZ

## Define element class with node coordinates as data members
class element():
    
    def __init__( self, lowerLeftPos,lowerRightPos, upperLeftPos,upperRightPos):
        self.lowerLeftPosition = lowerLeftPos
        self.upperRightPosition = upperRightPos
        self.lowerRightPosition = lowerRightPos
        self.upperLeftPosition = upperLeftPos

## Define coords class 
class coords():
    
    def __init__( self, data):
        self.data = data
    

def construct_deformed_beam_centerLine( Py, Pz, E,
                                        noElementsX,
                                        thickness, height, length, elementSizeX,
                                        amplificationFactor, glCantileverCrossSection):

    ## For rectangular cross sections:
    # v(x) = Px^2(3L - x)/6EI
    # I = bh^3/12
    # strainxx(top) = -6P(L-x)/bh^2E
    # strainxx(bottom) = 6P(L-x)/bh^2E  
    #######

    ###### DEFORMATION IN XY DIRECTION ######

    ## Define list for deformed XZ-centerline
    deformedBeamXY = list()

    ## Determine moment of inertia depending on active cross section:
    # Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3/12
    elif(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3/12.0) + height/10.0/12 + 2*((height/2.0)**2*height/10.0)        
    elif(glCantileverCrossSection==2):
        Iz = math.pi*(height/2)**4/4  
    
    ## Calculate deformation and append element coordinates to list. 
    # Take into account decreasing x-distance between elements due to deformation.
    xComponent = 0.0
    yComponent = 0.0
    for i in range(noElementsX + 1):
        yComponent = amplificationFactor*Py*xComponent*xComponent*( 3.0*length - xComponent )/(6.0*E*Iz)
        deformedBeamXY.append( [xComponent, yComponent] )
        angle = np.arctan((Py/E*Iz)*(length*xComponent-xComponent*xComponent/2.0))
        xIncrement = elementSizeX*np.cos(angle)
        xComponent += xIncrement


    ###### DEFORMATION IN XZ DIRECTION ######

    ## Define list for deformed XZ-centerline
    deformedBeamXZ = list()

    ## Determine moment of inertia depending on active cross section:
    #Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3/12
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3/12) + (height/10.0)**3*height/12
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height/2)**4/4

    ## Calculate deformation and append element coordinates to list. 
    # Take into account decreasing x-distance between elements due to deformation.
    xComponent = 0.0
    zComponent = 0.0
    for i in range(noElementsX + 1):
        zComponent = -amplificationFactor*Pz*xComponent*xComponent*( 3.0*length - xComponent )/(6.0*E*Iy)
        deformedBeamXZ.append( [xComponent, zComponent] )
        angle = np.arctan( ( Pz/E*Iy )*( length*xComponent - xComponent*xComponent/2.0 ) )
        xIncrement = elementSizeX*np.cos( angle )
        xComponent += xIncrement
        
    return deformedBeamXY, deformedBeamXZ

## Return color depending on range and current value:
def color_determiner( minimumValue, maximumValue, currentValue ):
    if minimumValue == maximumValue:
        return '#'+'66'+'ff'+'66'
    else:
        # Define the four regions seperating between the essential colors: Blue, Sky, Green, Yellow, Red
        minimumPoint = [minimumValue , 0]
        maximumPoint = [maximumValue , 816 ]
        colorIndex = (maximumPoint[1] /(maximumPoint[0] - minimumPoint[0]))*(currentValue - minimumPoint[0])
        # Prevent colorindex from getting too low, as this will cause irregularities in painting of beam: 
        if colorIndex<20:
            colorIndex = 20
        ratio = colorIndex / maximumPoint[1]


        # Cases
        if ratio <= 0.25:
            R = '33'
            B = 'ff'
            # determine G
            value = (255.0 / 204.0) * ( colorIndex )
            hexG = hex( int(value) )
            FstringHexG,SstringHexG = hexG.split( 'x' )
            G = SstringHexG
            
        elif ratio <= 0.50:
            R = '33'
            G = 'ff'
            # determine B
            value = ((51.0 - 255.0) / 204.0) * ( colorIndex - 408.0 ) + 51.0
            hexB = hex( int(value) )
            FstringHexB,SstringHexB = hexB.split( 'x' )
            B = SstringHexB  
            
        elif ratio <= 0.75:
            G = 'ff'
            B = '33'
            # determine R
            value = ((255.0 - 51.0) / 204.0) * ( colorIndex - 612.0 ) + 255.0
            hexR = hex( int(value) )
            FstringHexR,SstringHexR = hexR.split( 'x' )
            R = SstringHexR         
        
        else:
            R = 'ff'
            B = '33'
            # determine G
            value = ((51.0 - 255.0) / 204.0) * ( colorIndex - 816.0 ) + 51.0
            hexG = hex( int(value) )
            FstringHexG,SstringHexG = hexG.split( 'x' )
            G = SstringHexG  
        
        return '#'+R+G+B


def construct_normal_vectors( deformedBeam ):
    # Constructing normals (parallel to deformed centerline, pointing back and forward)
    normalVector1 = list()
    normalVector2 = list()
    for i in range( len( deformedBeam ) ):
        if i == 0:
            # These appended normal vectors are valid for beam clamped at its left end
            normalVector1.append( [0, 1] )
            normalVector2.append( [0,-1] )
        else:
            dx = deformedBeam[i][0] - deformedBeam[i-1][0]
            dy = deformedBeam[i][1] - deformedBeam[i-1][1]
            length = np.sqrt(dx*dx + dy*dy)
            normal1 = [-dy/length , dx/length]  
            normal2 = [ dy/length ,-dx/length]
            normalVector1.append( normal1 )
            normalVector2.append( normal2 )
    
    # Averaging normals
    averageNormalVector1 = list()
    averageNormalVector2 = list()
    for i in range( len( deformedBeam ) ):
        if i == len( deformedBeam ) - 1:
            normal1 = normalVector1[i]
            normal2 = normalVector2[i]
            averageNormalVector1.append( normal1 )
            averageNormalVector2.append( normal2 )
        elif i == 0:
            averageNormalVector1.append( [0,1] )
            averageNormalVector2.append( [0,-1] )
        else:
            xComp1 = (normalVector1[i][0] + normalVector1[i+1][0]) / 2.0
            xComp2 = (normalVector2[i][0] + normalVector2[i+1][0]) / 2.0
            yComp1 = (normalVector1[i][1] + normalVector1[i+1][1]) / 2.0
            yComp2 = (normalVector2[i][1] + normalVector2[i+1][1]) / 2.0
            normal1 = [xComp1,yComp1]
            normal2 = [xComp2,yComp2]
            averageNormalVector1.append(normal1)
            averageNormalVector2.append(normal2)
    
    return averageNormalVector1, averageNormalVector2

def values_determiner( Py, Pz, length, height, thickness, E, elementSizeX, glCantileverCrossSection):

    # Determine biggest and smallest value at left end of cantilever:
    biggestValue =  max(
                        calculate_normal_stress(0.0, height/2.0, height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, -height/2.0, height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, height/2.0, -height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, -height/2.0, -height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz) )
    smallestValue = min(
                        calculate_normal_stress(0.0, height/2.0, height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, -height/2.0, height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, height/2.0, -height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz),
                        calculate_normal_stress(0.0, -height/2.0, -height/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz) )

    listValuesUpperXY = list()
    listValuesLowerXZ = list()
    rangeSize = length/elementSizeX

    for i in range( int(rangeSize) ):

        valueUpperXY = calculate_normal_stress(i*elementSizeX, height/2.0, 0.0, length, height, thickness, glCantileverCrossSection, Py, Pz)         
        listValuesUpperXY.append( valueUpperXY )

        valueLowerXZ = calculate_normal_stress(i*elementSizeX, 0.0, thickness/2.0, length, height, thickness, glCantileverCrossSection, Py, Pz)        
        listValuesLowerXZ.append( valueLowerXZ )

    return biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ
    
## Determine color for each element of input list
def elements_color_determiner( deformed,
                               orientation,
                               listElements, 
                               noElementsX ,
                               noElementsY ,
                               E , height  ,
                               thickness   ,
                               length, Py, Pz,
                               biggestValue,
                               smallestValue,
                               listAdditionalValues,
                               glCantileverCrossSection
                             ):
    
    # Define list for color of elements
    colorList = list()

    if deformed == True:
        elementSize = length/noElementsX    
        xIncrement = 0.0
        verticalMultiplier = 1.0
        counter = 0

            
        if orientation == 'XY':
            # For loop  to             
            for i in range( int( len(listElements)/2 ) ):
                if i %(noElementsY/2) == 0 and i != 0:
                # update verticalMultiplier to the original value
                    verticalMultiplier = 1.0
                    xIncrement += elementSize
                    counter += 1
                else:
                    pass
            
                x_pos = xIncrement
                y_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                z_pos = thickness/2.0
                strainXXup = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz) 

                x_pos = xIncrement
                y_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                z_pos = thickness/2.0
                strainXXbottom = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection,  Py, Pz) 

                elementColor = color_determiner( smallestValue , biggestValue , strainXXup )
                colorList.append(elementColor)
                elementColor = color_determiner( smallestValue , biggestValue , strainXXbottom )
                colorList.append(elementColor)
                
                verticalMultiplier += 1

    
        if orientation == 'XZ':     
            Pz = -Pz      
            for i in range( int( len(listElements)/2 ) ):
                if i %(noElementsY/2) == 0 and i != 0:
                # update verticalMultiplier to the original value
                    verticalMultiplier = 1.0
                    xIncrement += elementSize
                    counter += 1
                else:
                    pass
            
                x_pos = xIncrement
                y_pos = height/2.0
                z_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                strainXXup = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz)        

                x_pos = xIncrement
                y_pos = height/2.0
                z_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                strainXXbottom = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection,  Py, Pz)       
            
                elementColor = color_determiner( smallestValue , biggestValue , strainXXup )
                colorList.append(elementColor)
                elementColor = color_determiner( smallestValue , biggestValue , strainXXbottom )
                colorList.append(elementColor)

                verticalMultiplier += 1

    ## If beam undeformed, paint all green:
    else:
        for i in range( int( len(listElements) ) ):
            colorList.append( '#B3B6B7' )
            
    return colorList  
    
def construct_deformed_elements( deformedBeam         ,
                                 axialDirElementSize  ,
                                 lateralDirElementSize,
                                 noElementsX          , 
                                 noElementsY          ,
                                 normalVectors1       ,
                                 normalVectors2
                               ):
    
    listDeformedElements = list()

    for i in range(noElementsX):
        for j in range(int(noElementsY/2)):

            lowerLeftPos1  = [ deformedBeam[i][0]   + float(j)  *axialDirElementSize  *normalVectors1[i][0]  ,
                               deformedBeam[i][1]   + float(j)  *lateralDirElementSize  *normalVectors1[i][1]   ]
            lowerRightPos1 = [ deformedBeam[i+1][0] + float(j)  *axialDirElementSize  *normalVectors1[i+1][0],
                               deformedBeam[i+1][1] + float(j)  *lateralDirElementSize  *normalVectors1[i+1][1] ]
            upperLeftPos1  = [ deformedBeam[i][0]   + float(j+1)*axialDirElementSize  *normalVectors1[i][0]  ,
                               deformedBeam[i][1]   + float(j+1)*lateralDirElementSize*normalVectors1[i][1]   ]
            upperRightPos1 = [ deformedBeam[i+1][0] + float(j+1)*axialDirElementSize  *normalVectors1[i+1][0],
                               deformedBeam[i+1][1] + float(j+1)*lateralDirElementSize*normalVectors1[i+1][1] ]
    
            lowerLeftPos2  = [ deformedBeam[i][0]   + float(j)  *axialDirElementSize  *normalVectors2[i][0]  ,
                               deformedBeam[i][1]   + float(j)  *lateralDirElementSize*normalVectors2[i][1]   ]
            lowerRightPos2 = [ deformedBeam[i+1][0] + float(j)  *axialDirElementSize  *normalVectors2[i+1][0],
                               deformedBeam[i+1][1] + float(j)  *lateralDirElementSize*normalVectors2[i+1][1] ]
            upperLeftPos2  = [ deformedBeam[i][0]   + float(j+1)*axialDirElementSize  *normalVectors2[i][0]  ,
                               deformedBeam[i][1]   + float(j+1)*lateralDirElementSize*normalVectors2[i][1]   ]
            upperRightPos2 = [ deformedBeam[i+1][0] + float(j+1)*axialDirElementSize  *normalVectors2[i+1][0],
                               deformedBeam[i+1][1] + float(j+1)*lateralDirElementSize*normalVectors2[i+1][1] ]
    
            listDeformedElements.append( element(lowerLeftPos1 ,lowerRightPos1, upperLeftPos1, upperRightPos1) )        
            listDeformedElements.append( element(lowerLeftPos2 ,lowerRightPos2, upperLeftPos2, upperRightPos2) )     
    
    return listDeformedElements
    
       
def create_coordinates_list( listElements ):
    
    listXCoord = list()
    listYCoord = list()
    for element in listElements:
        listXCoord.append([ element.lowerLeftPosition[0]  , 
                            element.upperLeftPosition[0]  ,
                            element.upperRightPosition[0] ,
                            element.lowerRightPosition[0] ])
        listYCoord.append([ element.lowerLeftPosition[1]  , 
                            element.upperLeftPosition[1]  ,
                            element.upperRightPosition[1] ,
                            element.lowerRightPosition[1] ])    
    
    return listXCoord , listYCoord


def calculate_stresses_xy_element(x_pos, y_pos, length, height, thickness, glCantileverCrossSection, Py, Pz):
    sigma_x_l = list()
    sigma_x_r = list()
    tau_xy = list() 

    ##Element Properties:
    z_pos = 0
    length_of_element = 2.0
    height_of_element = height/2.0
    
    ## Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3.0/12.0
    elif(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3.0/12.0) + height/10.0/12.0 + 2.0*((height/2.0)**2.0*height/10.0)        
    elif(glCantileverCrossSection==2):
        Iz = math.pi*(height/2.0)**4.0/4.0  

    ## Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*height/12.0        
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height/2.0)**4.0/4.0

    ## Iyz = Sum(Iyz_i) + Sum(ey_i*ez_i*A_i) = 0 + Sum(ey_i*ez_i*A_i) - Deviation momentum is zero because of symmetry of cross sections
    if(glCantileverCrossSection==0):
        Iyz = 0.0
    if(glCantileverCrossSection==1):
        Iyz = 0.0
    if(glCantileverCrossSection==2):
        Iyz = 0.0

    ## Calculation of Momentum M_y & M_z
    M_y_l = -(length-(x_pos-length_of_element/2.0)) * Pz
    M_y_r = -(length-(x_pos+length_of_element/2.0)) * Pz
    M_z_l = -(length-(x_pos-length_of_element/2.0)) * Py
    M_z_r = -(length-(x_pos+length_of_element/2.0)) * Py

    ## Calculation of sigma(x,y,z) 
    n=11
    for i in range(n):
        # sigma(x,y,z) = (N(x)/A) + (My*Iz-Mz*Iyz)/(Iy*Iz-Iyz**2)*z + (Mz*Iy-My*Iyz)/(Iy*Iz-Iyz**2)*y
        sigma_x_l.append((M_y_l*Iz - M_z_l*Iyz)/(Iy*Iz-Iyz**2.0)*z_pos + (M_z_l*Iy-M_y_l*Iyz)/(Iy*Iz-Iyz**2.0)*((i-n+1)/20.0))        
        sigma_x_r.append((M_y_r*Iz - M_z_r*Iyz)/(Iy*Iz-Iyz**2.0)*z_pos + (M_z_r*Iy-M_y_r*Iyz)/(Iy*Iz-Iyz**2.0)*((i-n+1)/20.0))
    
    ## Calculation of tau_xy
    m=10
    for i in range(m):
        # tau_xy(s,z) = -(Q_y(x)*S_z(s))/(Iy*thickness) = -(Q_y(x)*((height/2-s_+/2)*(s_+*length_of_element))/(Iy*thickness), with s starting at y=y_pos and s_max=height_of_element
        tau_xy.append(-(Py*(-y_pos-float(i)/float(m)*height_of_element/2.0)*(float(i)/float(m)/height_of_element*length_of_element))/(Iz*length_of_element))

    return sigma_x_l,sigma_x_r,tau_xy


def calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz):
    
    ## Declare and initialize sigma:
    sigma = 0

    ## Calculate Iz, Iy and Iyz:
    # Calculation of Iz:  Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3.0/12.0
    elif(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3.0/12.0) + height/10.0/12.0 + 2.0*((height/2.0)**2.0*height/10.0)        
    elif(glCantileverCrossSection==2):
        Iz = math.pi*(height/2.0)**4.0/4.0  
    #  Calculation of Iy:  Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*height/12.0        
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height/2.0)**4.0/4.0
    #  Calculation of Iyz:   Iyz = Sum(Iyz_i) + Sum(ey_i*ez_i*A_i) = 0 + Sum(ey_i*ez_i*A_i) 
    #  Deviation momentum is zero because of symmetry of cross sections
    if(glCantileverCrossSection==0):
        Iyz = 0.0
    if(glCantileverCrossSection==1):
        Iyz = 0.0
    if(glCantileverCrossSection==2):
        Iyz = 0.0

    ## Calculation of momentum M_y and M_z:
    M_y = (length-x_pos) * Pz
    M_z = (length-x_pos) * Py

    ## Calculation of sigma(x,y,z):
    #  Formula: sigma(x,y,z) = (N(x)/A) + (My*Iz-Mz*Iyz)/(Iy*Iz-Iyz**2)*z + (Mz*Iy-My*Iyz)/(Iy*Iz-Iyz**2)*y
    sigma = (M_y*Iz - M_z*Iyz)/(Iy*Iz-Iyz**2.0)*z_pos + (M_z*Iy-M_y*Iyz)/(Iy*Iz-Iyz**2.0)*y_pos 
    return sigma
