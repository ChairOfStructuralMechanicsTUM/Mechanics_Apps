import numpy as np
import math
from bokeh.plotting import figure

####### Print solutions for u_y, u_z, sigma_xx and tau_xy to validate calculations   - on=1, off=0 -
global glPrint
glPrint = 1
#######

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




    ## Determine moment of inertia depending on active cross section:
    ## Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3.0/12.0) + height**3*height/10.0/12.0 + 2.0*((height/2.0)**2.0*height*height/10.0)        
    if(glCantileverCrossSection==2):
        Iz = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iz = thickness**4.0/36.0  

    ## Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*height/12.0        
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iy = thickness**4.0/48.0    
    
    
    ###### DEFORMATION IN XY DIRECTION ######

    ## Define list for deformed XZ-centerline
    deformedBeamXY = list()

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

    ### PRINTSTART
    if (glPrint == 1): 
        if xComponent > 5.0 and Pz==100.0 and Py==100.0:
            if glCantileverCrossSection == 0:
                print "Rectangular CS"
                print "(length, width, height) = ", "(", length, ", ", thickness, ", ", height, ")"
                print "Iz = ", Iz
                print "Iy = ", Iy                
            elif glCantileverCrossSection == 1:
                print "Double-T CS"
                print "(length, width_total, width_elements, height) = ", "(", length, ", ", thickness, ", ", thickness/10, ", ", height, ")"                
                print "Iz = ", Iz
                print "Iy = ", Iy                
            elif glCantileverCrossSection == 2:
                print "Circular CS"
                print "(length, d) = ", "(", length, ", ", thickness, ")"                
                print "Iz = ", Iz
                print "Iy = ", Iy                
            elif glCantileverCrossSection == 3:
                print "Triangular CS"
                print "(length, width, height) = ", "(", length, ", ", thickness, ", ", height, ")"                
                print "Iz = ", Iz
                print "Iy = ", Iy                     
            print "Py = ", Py
            print "Pz = ", Pz 
            print "u_y(x=5, y=0, z=0) = ", yComponent/amplificationFactor
            print "u_z(x=5, y=0, z=0) = ", zComponent/amplificationFactor
    ### PRINTEND


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
        ratio = colorIndex / maximumPoint[1]      
        # Prevent colorindex from getting too extreme, as this will cause irregularities in painting of beam: 
        if colorIndex<20:
            colorIndex = 20
        if colorIndex>780:
            colorIndex = 780

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
    
    biggestValue = 1.5*calculate_normal_stress(0.0, 0.0, height/2.0, length, height, thickness, 2, 0, 100)
    smallestValue = 1.5*calculate_normal_stress(0.0, 0.0, -height/2.0, length, height, thickness, 2, 0, 100)

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
            # Pz = -Pz  
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
                if glCantileverCrossSection==0:
                    z_pos = thickness/2.0
                    y_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                elif glCantileverCrossSection==1:
                    y_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    if abs(y_pos) < height*4.0/10.0:
                        z_pos = thickness/10.0/2.0
                    else:
                        z_pos = thickness/2.0
                elif glCantileverCrossSection==2:
                    y_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    z_pos = np.cos(np.arcsin(y_pos/(thickness/2.0)))
                elif glCantileverCrossSection==3:

                    y_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)*1.0/2.0-(1.0/6.0)*height                      
                    z_pos = (2.0/3.0 + ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0-(1.0/6.0)*height)*0.5
                strainXXup = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz) 

                ### PRINTSTART
                if (glPrint == 1): 
                    if (x_pos > 1.45 and x_pos < 1.55 and y_pos > 0.45 and Py==100 and Pz==100):
                        if (glCantileverCrossSection==0):
                            print "Sigma(x=1.5, y=0.5, z=0.5) = ", strainXXup
                        elif (glCantileverCrossSection==1):
                            print "Sigma(x=1.5, y=0.5, z=0.5) = ", strainXXup
                        elif (glCantileverCrossSection==2):
                            print "Sigma(x=1.5, y=0.5, z=0.0) = ", strainXXup  
                    if (glCantileverCrossSection==3):
                            if (x_pos > 1.45 and x_pos < 1.55 and y_pos > 0.33 and Py==100 and Pz==100):
                                print "Sigma(x=1.5, y=0.33, z=0.5) = ", strainXXup
                ### PRINTEND


                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    y_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    z_pos = thickness/2.0
                elif glCantileverCrossSection==1:
                    y_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    if abs(y_pos) < height*4.0/10.0:
                        z_pos = thickness/10.0/2.0
                    else:
                        z_pos = thickness/2.0
                elif glCantileverCrossSection==2:
                    y_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    z_pos = np.cos(np.arcsin(y_pos/(thickness/2.0)))
                elif glCantileverCrossSection==3:
                    y_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)*1.0/2.0-(1.0/6.0)*height                  
                    z_pos = (2.0/3.0 - ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0-(1.0/6.0)*height)*0.5

                strainXXbottom = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz) 




                elementColor = color_determiner( smallestValue , biggestValue , strainXXup )
                colorList.append(elementColor)
                elementColor = color_determiner( smallestValue , biggestValue , strainXXbottom )
                colorList.append(elementColor)
                
                verticalMultiplier += 1

    
        if orientation == 'XZ':  

            for i in range( int( len(listElements)/2 ) ):
                if i %(noElementsY/2) == 0 and i != 0:
                # update verticalMultiplier to the original value
                    verticalMultiplier = 1.0
                    xIncrement += elementSize
                    counter += 1
                else:
                    pass
            
                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    z_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    y_pos = height/2.0
                elif glCantileverCrossSection==1:
                    z_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0                    
                    y_pos = height/2.0
                elif glCantileverCrossSection==2:
                    z_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    y_pos = np.sin(np.arccos(abs(z_pos)/(height/2.0)))
                elif glCantileverCrossSection==3:
                    z_pos = ((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)*1.0/2.0
                    y_pos = height*1.0/3.0                    

                strainXXbottom = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz)        


                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    z_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    y_pos = height/2.0
                elif glCantileverCrossSection==1:
                    z_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    y_pos = height/2.0
                elif glCantileverCrossSection==2:
                    z_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)/2.0
                    y_pos = np.sin(np.arccos(abs(z_pos)/(height/2.0)))
                elif glCantileverCrossSection==3:
                    z_pos = -((verticalMultiplier-1.0)*height)/(noElementsY/2.0-1.0)*1.0/2.0
                    y_pos = height*1.0/3.0                    

                strainXXup = calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz)       
            
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
    
       
def create_coordinates_list( listElements):
    
    listXCoord = list()
    listYCoord = list()
    for element in listElements:
        listXCoord.append([ element.lowerLeftPosition[0], 
                            element.upperLeftPosition[0],
                            element.upperRightPosition[0],
                            element.lowerRightPosition[0]])
        listYCoord.append([ element.lowerLeftPosition[1], 
                            element.upperLeftPosition[1],
                            element.upperRightPosition[1],
                            element.lowerRightPosition[1]])    



    return listXCoord , listYCoord


def calculate_stresses_xy_element(x_pos, y_pos, length, height, thickness, glCantileverCrossSection, Py, Pz):
    sigma_x_l = list()
    sigma_x_r = list()
    tau_xy = list() 

    ##Element Properties:
    z_pos = 0
    length_of_element = 2.0

    if(glCantileverCrossSection==3):
        height_of_element = height*2.0/3.0
    else:
        height_of_element = height/2.0
    
    ## Determine moment of inertia depending on active cross section:
    ## Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3.0/12.0) + height**3*height/10.0/12.0 + 2.0*((height/2.0)**2.0*height*height/10.0)        
    if(glCantileverCrossSection==2):
        Iz = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iz = thickness**4.0/36.0  

    ## Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*height/12.0        
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iy = thickness**4.0/48.0    
    
    ## Iyz = Sum(Iyz_i) + Sum(ey_i*ez_i*A_i) = 0 + Sum(ey_i*ez_i*A_i) - Deviation momentum is zero because of symmetry of cross sections
    if(glCantileverCrossSection==0):
        Iyz = 0.0
    if(glCantileverCrossSection==1):
        Iyz = 0.0
    if(glCantileverCrossSection==2):
        Iyz = 0.0
    if(glCantileverCrossSection==3):
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

### PRINTSTART
    if (glPrint == 1): 
        if (Py==100 and Pz==100):
            if(glCantileverCrossSection==3):
                print "Sigma_xx(x=1.5, y=-0,66, z=0) = ", -1*(sigma_x_l[0])
            else:
                print "Sigma_xx(x=1.5, y=-0,5, z=0) = ", -1*(sigma_x_l[0])
            print "Tau_xy(x=1.5, y=0, z=0) = ", tau_xy[-1]
            print ""               
### PRINTEND

    return sigma_x_l,sigma_x_r,tau_xy


def calculate_normal_stress(x_pos, y_pos, z_pos, length, height, thickness, glCantileverCrossSection, Py, Pz):
    
    ## Declare and initialize sigma:
    sigma = 0

    ## Calculate Iz, Iy and Iyz:
    ## Determine moment of inertia depending on active cross section:
    ## Iz = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iz = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1):        
        Iz = 2*(height*(height/10.0)**3.0/12.0) + height**3*height/10.0/12.0 + 2.0*((height/2.0)**2.0*height*height/10.0)        
    if(glCantileverCrossSection==2):
        Iz = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iz = thickness**4.0/36.0  

    ## Iy = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Iy = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Iy = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*height/12.0        
    if(glCantileverCrossSection==2):
        Iy = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iy = thickness**4.0/48.0    
    

    #  Calculation of Iyz:   Iyz = Sum(Iyz_i) + Sum(ey_i*ez_i*A_i) = 0 + Sum(ey_i*ez_i*A_i) 
    #  Deviation momentum is zero because of symmetry of cross sections
    if(glCantileverCrossSection==0):
        Iyz = 0.0
    if(glCantileverCrossSection==1):
        Iyz = 0.0
    if(glCantileverCrossSection==2):
        Iyz = 0.0
    if(glCantileverCrossSection==3):
        Iyz = 0.0

    ## Calculation of momentum M_y and M_z:
    M_y = (length-x_pos) * Pz
    M_z = (length-x_pos) * Py

    ## Calculation of sigma(x,y,z):
    #  Formula: sigma(x,y,z) = (N(x)/A) + (My*Iz-Mz*Iyz)/(Iy*Iz-Iyz**2)*z + (Mz*Iy-My*Iyz)/(Iy*Iz-Iyz**2)*y
    sigma = (M_y*Iz - M_z*Iyz)/(Iy*Iz-Iyz**2.0)*z_pos + (M_z*Iy - M_y*Iyz)/(Iy*Iz-Iyz**2.0)*y_pos 
                    
    return sigma