import numpy as np
import math
from bokeh.plotting import figure

####### Print solutions for u_y, u_z, sigma_xx and tau_xy on console to validate calculations   - on=1, off=0 -
## If you want to print the solutions, set glCantileverPrint to 1. Run the App and set both Forces sliders to the far right (Py=100 and Pz=100). 
## You will get the properties of the beam and the calculated displacements / stresses printed on the console. (note: location (x,y,z) of calculated values vary) 
global glCantileverPrint
glCantileverPrint = 0
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
    
def construct_deformed_beam_centerLine( Pzn, Pyn, E,
                                        noElementsX,
                                        thickness, height, length, elementSizeX,
                                        amplificationFactor, glCantileverCrossSection):




    ## Determine moment of inertia depending on active cross section:
    ## Iy = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iyn = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1):        
        Iyn = 2*(height*(height/10.0)**3.0/12.0) + (height-2*height/10.0)**3*height/10.0/12.0 + 2.0*((height/2.0-height/20)**2.0*height*height/10.0)        
    if(glCantileverCrossSection==2):
        Iyn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iyn = thickness**4.0/36.0  

    ## Iz = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Izn = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Izn = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*(height-2*height/10.0)/12.0        
    if(glCantileverCrossSection==2):
        Izn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Izn = thickness**4.0/48.0    
    
    
    ###### DEFORMATION IN XZn DIRECTION ######

    ## Define list for deformed XZn-centerline
    deformedBeamXZn = list()

    ## Calculate deformation and append element coordinates to list. 
    # Take into account decreasing x-distance between elements due to deformation.
    xComponent = 0.0
    znComponent = 0.0
    for i in range(noElementsX + 1):
        znComponent = - amplificationFactor*Pzn*xComponent*xComponent*( 3.0*length - xComponent )/(6.0*E*Iyn)
        deformedBeamXZn.append( [xComponent, znComponent] )
        angle = np.arctan( ( Pzn/E*Iyn )*( length*xComponent - xComponent*xComponent/2.0) )
        xIncrement = elementSizeX*np.cos( angle )
        xComponent += xIncrement


    ###### DEFORMATION IN XYn DIRECTION ######

    ## Define list for deformed XYn-centerline
    deformedBeamXYn = list()
    
    ## Calculate deformation and append element coordinates to list. 
    # Take into account decreasing x-distance between elements due to deformation.
    xComponent = 0.0
    ynComponent = 0.0
    for i in range(noElementsX + 1):
        ynComponent = - amplificationFactor*Pyn*xComponent*xComponent*( 3.0*length - xComponent )/(6.0*E*Izn)
        deformedBeamXYn.append( [xComponent, ynComponent] )
        angle = np.arctan( ( Pyn/E*Izn )*( length*xComponent - xComponent*xComponent/2.0 ) )
        xIncrement = elementSizeX*np.cos( angle )
        xComponent += xIncrement

    ### PRINTSTART
    if (glCantileverPrint == 1): 
        if xComponent > 5.0 and Pyn==100.0 and Pzn==100.0:
            if glCantileverCrossSection == 0:
                print ("Rectangular CS")
                print ("(length, width, height) = ", "(", length, ", ", thickness, ", ", height, ")")
                print ("Iz = ", Iyn)
                print ("Iy = ", Izn)                
            elif glCantileverCrossSection == 1:
                print ("Double-T CS")
                print ("(length, width_total, width_elements, height) = ", "(", length, ", ", thickness, ", ", thickness/10, ", ", height, ")" )               
                print ("Iz = ", Iyn)
                print ("Iy = ", Izn)                
            elif glCantileverCrossSection == 2:
                print ("Circular CS")
                print ("(length, d) = ", "(", length, ", ", thickness, ")")                
                print ("Iz = ", Iyn)
                print ("Iy = ", Izn)                
            elif glCantileverCrossSection == 3:
                print ("Triangular CS")
                print ("(length, width, height) = ", "(", length, ", ", thickness, ", ", height, ")" )               
                print ("Iz = ", Iyn)
                print ("Iy = ", Izn)                     
            print ("Py = ", Pzn)
            print ("Pz = ", Pyn)
            print ("u_y(x=5, y=0, z=0) = ", znComponent/amplificationFactor)
            print ("u_z(x=5, y=0, z=0) = ", ynComponent/amplificationFactor)
    ### PRINTEND


    return deformedBeamXZn, deformedBeamXYn


## Return color depending on range and current value:
def color_determiner( minimumValue, maximumValue, currentValue, glCantileverCrossSection ):
    if minimumValue == maximumValue:
        return '#'+'66'+'ff'+'66'
    else:
        # Define the four regions seperating between the essential colors: Blue, Sky, Green, Yellow, Red
        minimumPoint = [minimumValue , 816]
        maximumPoint = [maximumValue , 0 ]
        if glCantileverCrossSection != 0: #linear color distribution
            colorIndex = -(minimumPoint[1]-maximumPoint[1])/(maximumPoint[0] - minimumPoint[0]) * currentValue + (minimumPoint[1]-maximumPoint[1])/2
        else: #quadric color distribution
            if currentValue >= 0:
                colorIndex = (minimumPoint[1]-maximumPoint[1])/2 - math.sqrt( currentValue/(maximumPoint[0]) ) * (minimumPoint[1]-maximumPoint[1])/2
            else:
                colorIndex = (minimumPoint[1]-maximumPoint[1])/2 + math.sqrt( -currentValue/(maximumPoint[0]) ) * (minimumPoint[1]-maximumPoint[1])/2
        ratio = colorIndex / minimumPoint[1]      
        # Prevent colorindex from getting too extreme, as this will cause irregularities in painting of beam: 
        if colorIndex<20:
            colorIndex = 20
        if colorIndex>780:
            colorIndex = 780

        if glCantileverCrossSection != 0:
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
        else:
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

def values_determiner( Pzn, Pyn, length, height, thickness, E, elementSizeX, glCantileverCrossSection):
    
    biggestValue = 1.5*calculate_normal_stress(0.0, 0.0, height/2.0, length, height, thickness, 2, 0, 100)
    smallestValue = 1.5*calculate_normal_stress(0.0, 0.0, -height/2.0, length, height, thickness, 2, 0, 100)

    listValuesUpperXY = list()
    listValuesLowerXZ = list()
    rangeSize = length/elementSizeX

    for i in range( int(rangeSize) ):

        valueUpperXY = calculate_normal_stress(i*elementSizeX, height/2.0, 0.0, length, height, thickness, glCantileverCrossSection, Pzn, Pyn)         
        listValuesUpperXY.append( valueUpperXY )

        valueLowerXZ = calculate_normal_stress(i*elementSizeX, 0.0, thickness/2.0, length, height, thickness, glCantileverCrossSection, Pzn, Pyn)        
        listValuesLowerXZ.append( valueLowerXZ )

    return biggestValue, smallestValue, listValuesUpperXY, listValuesLowerXZ
    
## Determine color for each element of input list
def elements_color_determiner( deformed,
                               orientation,
                               listElements, 
                               noElementsX ,
                               noElementsZn ,
                               E , height  ,
                               thickness   ,
                               length, Pzn, Pyn,
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

            
        if orientation == 'XZ':
            # For loop  to             
            for i in range( int( len(listElements)/2 ) ):
                if i %(noElementsZn/2) == 0 and i != 0:
                # update verticalMultiplier to the original value
                    verticalMultiplier = 1.0
                    xIncrement += elementSize
                    counter += 1
                else:
                    pass
            
                x_pos = xIncrement              
                if glCantileverCrossSection==0:
                    yn_pos = -thickness/2.0
                    zn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                elif glCantileverCrossSection==1:
                    zn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    if abs(zn_pos) < height*4.0/10.0:
                        yn_pos = -thickness/10.0/2.0
                    else:
                        yn_pos = -thickness/2.0
                elif glCantileverCrossSection==2:
                    zn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    yn_pos = -np.cos(np.arcsin(zn_pos/(thickness/2.0)))
                elif glCantileverCrossSection==3:
                    zn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)*1.0/2.0-(1.0/6.0)*height                      
                    yn_pos = -(2.0/3.0 + ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0-(1.0/6.0)*height)*0.5
                strainXXup = calculate_normal_stress(x_pos, zn_pos, yn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn) 

                ### PRINTSTART
                if (glCantileverPrint == 1): 
                    if (x_pos > 1.45 and x_pos < 1.55 and zn_pos > 0.45 and Pzn==100 and Pyn==100):
                        if (glCantileverCrossSection==0):
                            print ("Sigma(x=1.5, y=0.5, z=0.5) = ", strainXXup)
                        elif (glCantileverCrossSection==1):
                            print ("Sigma(x=1.5, y=0.5, z=0.5) = ", strainXXup)
                        elif (glCantileverCrossSection==2):
                            print ("Sigma(x=1.5, y=0.5, z=0.0) = ", strainXXup)  
                    if (glCantileverCrossSection==3):
                            if (x_pos > 1.45 and x_pos < 1.55 and zn_pos > 0.33 and Pzn==100 and Pyn==100):
                                print ("Sigma(x=1.5, y=0.33, z=0.5) = ", strainXXup)
                ### PRINTEND


                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    zn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    yn_pos = -thickness/2.0
                elif glCantileverCrossSection==1:
                    zn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    if abs(zn_pos) < height*4.0/10.0:
                        yn_pos = -thickness/10.0/2.0
                    else:
                        yn_pos = -thickness/2.0
                elif glCantileverCrossSection==2:
                    zn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    yn_pos = -np.cos(np.arcsin(zn_pos/(thickness/2.0)))
                elif glCantileverCrossSection==3:
                    zn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)*1.0/2.0-(1.0/6.0)*height                  
                    yn_pos = -(2.0/3.0 - ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0-(1.0/6.0)*height)*0.5

                strainXXbottom = calculate_normal_stress(x_pos, zn_pos, yn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn) 

                elementColor = color_determiner( smallestValue , biggestValue , strainXXup, glCantileverCrossSection )
                colorList.append(elementColor)
                elementColor = color_determiner( smallestValue , biggestValue , strainXXbottom, glCantileverCrossSection )
                colorList.append(elementColor)
                
                verticalMultiplier += 1

    
        if orientation == 'XY':

            for i in range( int( len(listElements)/2 ) ):
                if i %(noElementsZn/2) == 0 and i != 0:
                # update verticalMultiplier to the original value
                    verticalMultiplier = 1.0
                    xIncrement += elementSize
                    counter += 1
                else:
                    pass
            
                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    yn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    zn_pos = height/2.0
                elif glCantileverCrossSection==1:
                    yn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0                    
                    zn_pos = height/2.0
                elif glCantileverCrossSection==2:
                    yn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    zn_pos = np.sin(np.arccos(abs(yn_pos)/(height/2.0)))
                elif glCantileverCrossSection==3:
                    yn_pos = -((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)*1.0/2.0
                    zn_pos = height*1.0/3.0                    

                strainXXbottom = calculate_normal_stress(x_pos, zn_pos, yn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn)        


                x_pos = xIncrement
                if glCantileverCrossSection==0:
                    yn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    zn_pos = height/2.0
                elif glCantileverCrossSection==1:
                    yn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    zn_pos = height/2.0
                elif glCantileverCrossSection==2:
                    yn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)/2.0
                    zn_pos = np.sin(np.arccos(abs(yn_pos)/(height/2.0)))
                elif glCantileverCrossSection==3:
                    yn_pos = ((verticalMultiplier-1.0)*height)/(noElementsZn/2.0-1.0)*1.0/2.0
                    zn_pos = height*1.0/3.0                    

                strainXXup = calculate_normal_stress(x_pos, zn_pos, yn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn)       
            
                elementColor = color_determiner( smallestValue , biggestValue , strainXXup , glCantileverCrossSection )
                colorList.append(elementColor)
                elementColor = color_determiner( smallestValue , biggestValue , strainXXbottom, glCantileverCrossSection )
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
                                 noElementsZn          ,
                                 normalVectors1       ,
                                 normalVectors2
                               ):
    
    listDeformedElements = list()

    for i in range(noElementsX):
        for j in range(int(noElementsZn/2)):

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

def calculate_stresses_xzn_element(x_pos, zn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn):
    sigma_x_l = list()
    sigma_x_r = list()
    tau_xzn = list() 

    ##Element Properties:
    yn_pos = 0
    length_of_element = 2.0

    if(glCantileverCrossSection==3):
        height_of_element = height*2.0/3.0
    else:
        height_of_element = height/2.0
    
    ## Determine moment of inertia depending on active cross section:
    ## Iyn = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0): #0,08333333
        Iyn = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1): #0,04493333
        Iyn = 2*(height*(height/10.0)**3.0/12.0) + (height-2*height/10.0)**3*height/10.0/12.0 + 2.0*((height/2.0-height/20)**2.0*height*height/10.0)        
    if(glCantileverCrossSection==2): #0,04908734
        Iyn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3): #0,02777777
        Iyn = thickness**4.0/36.0  

    ## Izn = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Izn = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Izn = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*(height-2*height/10.0)/12.0        
    if(glCantileverCrossSection==2):
        Izn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Izn = thickness**4.0/48.0    
    
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
    M_yn_l = -(length-(x_pos-length_of_element/2.0)) * Pzn
    M_yn_r = -(length-(x_pos+length_of_element/2.0)) * Pzn
    M_zn_l = -(length-(x_pos-length_of_element/2.0)) * Pyn
    M_zn_r = -(length-(x_pos+length_of_element/2.0)) * Pyn

    ## Calculation of sigma(x,y,z) 
    n=11
    for i in range(n):
        # sigma(x,y,z) = (N(x)/A) + (My*Iz-Mz*Iyz)/(Iy*Iz-Iyz**2)*z + (Mz*Iy-My*Iyz)/(Iy*Iz-Iyz**2)*y
        sigma_x_l.append(M_zn_l/Izn*yn_pos + M_yn_l/Iyn*((i-n+1)/20.0))        
        sigma_x_r.append(M_zn_r/Izn*yn_pos + M_yn_r/Iyn*((i-n+1)/20.0))

    ## Calculation of tau_xzn
    m=10
    s_pos=0 #starting at the bottom
    if glCantileverCrossSection == 0:
        for i in range(m):
            s_pos=float(i)/float(m)*height_of_element
            tau_xzn.append( - Pzn/Izn * 1/2 * (height*s_pos-s_pos**2) )
    elif glCantileverCrossSection == 1:
        for i in range(m):
            s_pos=float(i)/float(m)*height_of_element
            tau_xzn.append( - Pzn/Izn * 1/2 * (height*s_pos-s_pos**2) )
    elif glCantileverCrossSection == 2:
        for i in range(m):
            s_pos=height_of_element-float(i)/float(m)*height_of_element
            tau_xzn.append( - Pzn * 4/(3*math.pi) * ((height/2)**2-s_pos**2)/((height/2)**4 ) )
    elif glCantileverCrossSection == 3:
        for i in range(m):
            s_pos=float(i)/float(m)*height_of_element
            tau_xzn.append( - Pzn/Izn * 1/3 * (height*s_pos-s_pos**2) )

### PRINTSTART
    if (glCantileverPrint == 1): 
        if (Pzn==100 and Pyn==100):
            if(glCantileverCrossSection==3):
                print ("Sigma_xx(x=1.5, y=-0,66, z=0) = ", -1*(sigma_x_l[0]))
            else:
                print ("Sigma_xx(x=1.5, y=-0,5, z=0) = ", -1*(sigma_x_l[0]))
            print ("Tau_xy(x=1.5, y=0, z=0) = ", tau_xzn[-1])
            print ("")               
### PRINTEND

    return sigma_x_l,sigma_x_r,tau_xzn

def calculate_normal_stress(x_pos, zn_pos, yn_pos, length, height, thickness, glCantileverCrossSection, Pzn, Pyn):
    
    ## Declare and initialize sigma:
    sigma = 0

    ## Calculate Iz, Iy and Iyz:
    ## Determine moment of inertia depending on active cross section:
    ## Iy = Sum(Iz_i) + Sum(ez_i^2*A_i)
    if(glCantileverCrossSection==0):
        Iyn = thickness*height**3.0/12.0
    if(glCantileverCrossSection==1):        
        Iyn = 2*(height*(height/10.0)**3.0/12.0) + (height-2*height/10.0)**3*height/10.0/12.0 + 2.0*((height/2.0-height/20)**2.0*height*height/10.0)       
    if(glCantileverCrossSection==2):
        Iyn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Iyn = thickness**4.0/36.0  

    ## Iz = Sum(Iy_i) + Sum(ey_i^2*A_i) = Sum(Iy_i) + 0 
    if(glCantileverCrossSection==0):
        Izn = height*thickness**3.0/12.0
    if(glCantileverCrossSection==1):
        Izn = 2*(height/10.0*height**3.0/12.0) + (height/10.0)**3.0*(height-2*height/10.0)/12.0      
    if(glCantileverCrossSection==2):
        Izn = math.pi*(height)**4.0/64.0
    if(glCantileverCrossSection==3):
        Izn = thickness**4.0/48.0    
    

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
    M_zn = (length-x_pos) * Pyn
    M_yn = (length-x_pos) * Pzn

    ## Calculation of sigma(x,y,z):
    #  Formula: sigma(x,y,z) = (N(x)/A) + (My*Iz-Mz*Iyz)/(Iy*Iz-Iyz**2)*z + (Mz*Iy-My*Iyz)/(Iy*Iz-Iyz**2)*y
    sigma = M_zn/Izn*yn_pos + M_yn/Iyn*zn_pos 
                    
    return sigma