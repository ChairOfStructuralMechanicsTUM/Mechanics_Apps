from Maxwell_Frame import Maxwell_Frame

f1              = Maxwell_Frame("F"u"\u2081","n"u"\u2081")                                              #Creation of object Frame 1 "F1". This frame is the first to be deformed
f2              = Maxwell_Frame("F"u"\u2082","n"u"\u2082")                                              #Creation of object Frame 2

#EDIT Start          
def calc_betty_displacements12(f):
    ParamInt = f.get_param()
    i = f.get_mag()
    j = f1.get_param()
    names12 = " w"u"\u2081"u"\u2082" 
    if i == 0:
        f.w12.stream(dict(xS= [], xE= [],
        yS= [], yE=[], name = [] ),rollover=-1)
        f.w12_11.stream(dict(xS= [], xE= [],
        yS= [], yE=[] ),rollover=-1)
        f.w12_12.stream(dict(xS= [], xE= [],
        yS= [], yE= []),rollover=-1)
        f.wdline12.data = dict(x1 = [], x2 = [],
        y1 = [] , y2 = [] )
       
    elif (ParamInt < 30):
        x=0.1
        y=0.85
        x_l=0.1
        y_l=0.8
        if ParamInt < 8:
            dx = ParamInt
            x_betty12 = (f1.pts.data["x"][0]) + (dx/7.0)*((f1.pts.data["x"][1])-(f1.pts.data["x"][0]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >7 and ParamInt <15:
            dx = ParamInt-8
            x_betty12 = (f1.pts.data["x"][1]) + (dx/7.0)*((f1.pts.data["x"][2])-(f1.pts.data["x"][1]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >14 and ParamInt <22:
            dx = ParamInt-15
            x_betty12 = (f1.pts.data["x"][2]) + (dx/7.0)*((f1.pts.data["x"][3])-(f1.pts.data["x"][2]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)   
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >21:
            dx = ParamInt-22
            x_betty12 = (f1.pts.data["x"][3]) + (dx/8.0)*((f1.pts.data["x"][4])-(f1.pts.data["x"][3]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)   
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
    
    elif (30<=ParamInt & ParamInt<=70):
        x=0.9
        y=0.6
        x_l=0.9
        y_l=0.6
        if j <30:
            pts1=5
            pts2=6
            pts3=7
            pts4=8
        else:
            pts1=4
            pts2=5
            pts3=6
            pts4=7

        if ParamInt >= 30 and ParamInt <=39:
            dx = ParamInt-30
            y_betty12 = (f1.pts.data["y"][pts1]) + (dx/10.0)*((f1.pts.data["y"][pts1+1])-(f1.pts.data["y"][pts1]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty12] ),rollover=1)   
            f.w12_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty12], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty12,y_betty12] , y2 = [ y_l, y_l ] )
       
        if ParamInt >= 40 and ParamInt <=49:
            dx = ParamInt-40
            y_betty12 = (f1.pts.data["y"][pts2]) + (dx/10.0)*((f1.pts.data["y"][pts2+1])-(f1.pts.data["y"][pts2]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty12] ),rollover=1)   
            f.w12_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty12], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty12,y_betty12] , y2 = [ y_l, y_l ] )

        if ParamInt >= 50 and ParamInt <=59:
            dx = ParamInt-50
            y_betty12 = (f1.pts.data["y"][pts3]) + (dx/10.0)*((f1.pts.data["y"][pts3+1])-(f1.pts.data["y"][pts3]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty12] ),rollover=1)  
            f.w12_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty12], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty12,y_betty12] , y2 = [ y_l, y_l ] )

        if ParamInt >= 60 and ParamInt <=70:
            dx = ParamInt-60
            y_betty12 = (f1.pts.data["y"][pts4]) + (dx/11.0)*((f1.pts.data["y"][pts4+1])-(f1.pts.data["y"][pts4]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty12] ),rollover=1)   
            f.w12_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty12], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty12,y_betty12] , y2 = [ y_l, y_l ] )
 
    elif (ParamInt > 70):
        x=0.8
        y=0.85
        x_l=0.8
        y_l=0.8
        if j < 30:
            pts1=10
            pts2=11
            pts3=12
            pts4=13
        else:
            pts1=8
            pts2=9
            pts3=10
            pts4=11

        if ParamInt >70 and ParamInt <79:
            dx = ParamInt-71
            x_betty12 = (f1.pts.data["x"][pts1]) + (dx/8.0)*((f1.pts.data["x"][pts1+1])-(f1.pts.data["x"][pts1]))

            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >78 and ParamInt <86:
            dx = ParamInt-79
            x_betty12 = (f1.pts.data["x"][pts2]) + (dx/6.0)*((f1.pts.data["x"][pts2+1])-(f1.pts.data["x"][pts2]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >85 and ParamInt <93:
            dx = ParamInt-86
            x_betty12 = (f1.pts.data["x"][pts3]) + (dx/6.0)*((f1.pts.data["x"][pts3+1])-(f1.pts.data["x"][pts3]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1) 
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >92:
            dx = ParamInt-93
            x_betty12 = (f1.pts.data["x"][pts4]) + dx/8.0*((f1.pts.data["x"][pts4+1])-(f1.pts.data["x"][pts4]))
            f.w12.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names12] ),rollover=1)
            f.w12_11.stream(dict(xS= [x], xE= [x_betty12],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w12_12.stream(dict(xS= [x_betty12], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline12.data = dict(x1 = [ x_betty12, x_betty12 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )         
#EDIT End

#EDIT Start          
def calc_betty_displacements21(f):
    ParamInt = f1.get_param()
    #print ParamInt
    #i = f.get_mag()
    names21 = " w"u"\u2082"u"\u2081" 
    
    if ParamInt < 30:
        x=0.1
        y=-0.16
        x_l=0.1
        y_l=-0.15
        if ParamInt < 8:
            dx = ParamInt
            x_betty21 = (f2.pts.data["x"][0]) + (dx/7.0)*((f2.pts.data["x"][1])-(f2.pts.data["x"][0]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >7 and ParamInt <15:
            dx = ParamInt-8
            x_betty21 = (f2.pts.data["x"][1]) + (dx/7.0)*((f2.pts.data["x"][2])-(f2.pts.data["x"][1]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >14 and ParamInt <22:
            dx = ParamInt-15
            x_betty21 = (f2.pts.data["x"][2]) + (dx/7.0)*((f2.pts.data["x"][3])-(f2.pts.data["x"][2]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
        if ParamInt >21:
            dx = ParamInt-22
            x_betty21 = (f2.pts.data["x"][3]) + (dx/8.0)*((f2.pts.data["x"][4])-(f2.pts.data["x"][3]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)   
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [y_l ,ParamInt / 30.0 * 0.5 + 0.1] , y2 = [ y_l, ParamInt / 30.0 * 0.5 + 0.1 ] )
    elif ((30 <= ParamInt) & (ParamInt <= 70)):
        x=-0.1
        y=0.6
        x_l=-0.1
        y_l=0.6
        if ParamInt >= 30 and ParamInt <=39:
            dx = ParamInt-30
            y_betty21 = (f2.pts.data["y"][4]) + (dx/10.0)*((f2.pts.data["y"][5])-(f2.pts.data["y"][4]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty21] ),rollover=1)    
            f.w21_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty21], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty21,y_betty21] , y2 = [ y_l, y_l ] )
       
        if ParamInt >= 40 and ParamInt <=49:
            dx = ParamInt-40
            y_betty21 = (f2.pts.data["y"][5]) + (dx/10.0)*((f2.pts.data["y"][6])-(f2.pts.data["y"][5]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty21] ),rollover=1)    
            f.w21_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty21], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty21,y_betty21] , y2 = [ y_l, y_l ] )

        if ParamInt >= 50 and ParamInt <=59:
            dx = ParamInt-50
            y_betty21 = (f2.pts.data["y"][6]) + (dx/10.0)*((f2.pts.data["y"][7])-(f2.pts.data["y"][6]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty21] ),rollover=1)   
            f.w21_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty21], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty21,y_betty21] , y2 = [ y_l, y_l ] )

        if ParamInt >= 60 and ParamInt <=70:
            dx = ParamInt-60
            y_betty21 = (f2.pts.data["y"][7]) + (dx/11.0)*((f2.pts.data["y"][8])-(f2.pts.data["y"][7]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x],
                yS= [y_l], yE=[y_betty21] ),rollover=1)    
            f.w21_12.stream(dict(xS= [x], xE= [x],
                yS= [y_betty21], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1 ]  , x2 = [x_l,(ParamInt - 30) / 40.0 * 0.7 + 0.1] ,
            y1 = [y_betty21,y_betty21] , y2 = [ y_l, y_l ] )

    elif (ParamInt > 70):
        x=0.8
        y=-0.16
        x_l=0.8
        y_l=-0.15
        if ParamInt >70 and ParamInt <79:
            dx = ParamInt-71
            x_betty21 = (f2.pts.data["x"][8]) + (dx/8.0)*((f2.pts.data["x"][9]) - (f2.pts.data["x"][8]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)   
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >78 and ParamInt <86:
            dx = ParamInt-79
            x_betty21 = (f2.pts.data["x"][9]) + (dx/6.0)*((f2.pts.data["x"][10])-(f2.pts.data["x"][9]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >85 and ParamInt <93:
            dx = ParamInt-86
            x_betty21 = (f2.pts.data["x"][10]) + (dx/6.0)*((f2.pts.data["x"][11])-(f2.pts.data["x"][10]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)   
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )
        if ParamInt >92:
            dx = ParamInt-93
            x_betty21 = (f2.pts.data["x"][11]) + dx/8.0*((f2.pts.data["x"][12])-(f2.pts.data["x"][11]))
            f.w21.stream(dict(xS= [x], xE= [x],
                yS= [y], yE=[y], name = [names21] ),rollover=1)
            f.w21_11.stream(dict(xS= [x], xE= [x_betty21],
                yS= [y_l], yE=[y_l] ),rollover=1)  
            f.w21_12.stream(dict(xS= [x_betty21], xE= [x],
                yS= [y_l], yE=[y_l] ),rollover=1)
            f.wdline21.data = dict(x1 = [ x_betty21, x_betty21 ]  , x2 = [ x_l, x_l ] ,
            y1 = [ y_l , 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] , y2 = [ y_l, 0.6 - (ParamInt - 70) / 30.0 * 0.5 ] )         
#EDIT End
