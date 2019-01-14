#trash


'''
class SupportB(Force):
    def __init__(self,name):
        Force.__init__(self,name,0.0,1.0)

    def fun_clear(self):
        self.triangle_source = ColumnDataSource(data=dict(x= [], y= [], size = []))
        self.arrow_source.data = dict(xS= [], xE= [], yS= [], yE=[], lW = [])
'''


class Force(Beam):
    def __init__(self,name,which=0):
        Beam.__init__(self)
        self.mag = 100.0
        self.magi = 100.0
        self.loci = self.xf/2
        self.loc = 0
        self.xS = 0
        self.xE = 0
        self.yS = 0
        self.yE = 0
        self.lW = 0
        self.name = name
        self.which = which
        self.dy = []                        #deflection caused by force
        self.arrow_source = ColumnDataSource(data=dict(xS=[], xE=[], yS=[], yE=[], lW = []))

        if (which == 2 ):
            print "hi"
            self.loc_slider = Slider(title=self.name + " lalaPosition",value = self.xf,start = self.x0, end = self.xf, step = 1/self.resol)
            self.loc = self.xf
        else:
            self.loc_slider = Slider(title=self.name + " Position",value = self.loci,start = self.x0, end = self.xf, step = 1/self.resol)

        self.mag_slider = Slider(title=self.name + " amplitude", value=self.magi, start=-2*self.magi, end=2*self.magi, step=1)
        self.arrow_glyph = Arrow(end=OpenHead(line_color="#003359",line_width= 4,size=10),
            x_start='xS', y_start='yS', x_end='xE', y_end='yE',line_width = "lW", source=self.arrow_source,line_color="#003359" )

    def change_loc(self):
        pass
    def change_mag(self):
        pass

    def update_arrow(self, l):
        if self.which==0:
            self.loc = self.loc_slider.value
            self.mag = self.mag_slider.value
        elif self.which==1: #A position support
            self.loc = 0
            #self.mag = fun_mag(self.b)
        elif self.which==2: #B position support
            self.loc = self.loc_slider.value
            #self.mag = fun_mag(self.a)

        self.xS = [self.loc]
        self.xE = [self.loc]
        self.lW = [abs(self.mag/40.0)]
        if self.mag<0:
            self.yS = [1-(self.mag/200.0)]
            self.yE = [1]
        elif self.mag>0:
            self.yS = [-1-(self.mag/200.0)]
            self.yE = [-1]
        else:
            self.yS = [-5]
            self.yE = [-5]
            self.xS = [-5]
            self.xE = [-5]
        self.dy = Fun_Deflection(self.loc,l - self.loc, l, self.mag, np.linspace(self.x0,self.xf,self.resol), self.xf, self.resol, self.E, self.I)
        self.arrow_source.data = dict(xS= self.xS, xE= self.xE, yS= self.yS, yE=self.yE, lW = self.lW )





        '''
        def Fun_Update(attr,old,new):
            #1names = []
            #1rmag = 0
            #1rloc = 0
            #1rdy  = np.ones(beam.resol) * 0
            for i in range(0,number):
                flist[i].update_arrow(fb.loc_slider.value)         #update the concentrated loads
                rmag += flist[i].mag
                rloc += flist[i].loc
                rdy  = np.add(rdy,flist[i].dy)
                #names.append(flist[i].name)
            rloc = rloc / number
            a = rloc - beam.x0
            b = fb.loc - rloc
            beam.source.data['y'] = rdy

            if fb.loc_slider.value == 0: #cantilever
                Fun_Cantilever()
            else:
            #Update the support forces
                #1fa.mag = Fun_F(rmag,b,fb.loc_slider.value)
                #1fb.mag = Fun_F(rmag,a,fb.loc_slider.value)
                #1fa.update_arrow(fb.loc_slider.value)
                #1fb.update_arrow(fb.loc_slider.value)
                #1triangle_source.data = dict(x = [0.0,fb.loc], y = [0-move_tri, 0-move_tri], size = [20,20])
                #names = names + fa.name + fb.name
        '''


### SASCHA KUBISCH 14-01-2019:
   
# FUNCTION: Calculation of deflection:
def Fun_Deflection(a,b,l,p_mag,x):
    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew    


   
    # if radio_button_group.active == 0:    
    #     ynew = []
    #     ynew1 = []
    #     ynew2 = []
    #     for i in range(0,int(l*(resol/10) ) ):
    #         if a > l:
    #             dy = ( ( p_mag * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (x[i]**2) )
    #         else:
    #             if x[i] < a:
    #                 dy = ( ( p_mag * b * x[i]) / (6 * E * I * l) ) * ( (l**2) - (b**2) - (x[i]**2) )
    #             elif x[i] == a:
    #                 dy = ( p_mag * (a**2) * (b**2) ) / (3 * E * I * l)
    #             elif x[i] > a and x[i] <= l:
    #                 dy = ( (p_mag * a * (l-x[i]) ) / (6 * E * I * l) ) * ( (2*l*x[i]) - (x[i]**2) - (a**2) )
    #         # dy = 0
    #         ynew1.append(dy)
    #     new_range = int(resol - l*10)
    #     for i in range(0,new_range):
    #         # dy1 = 0
    #         dy1 = -1 *( ( (p_mag * a * b * x[i]) / (6 * E * I * l) ) * (l + a) )
    #         ynew2.append(dy1)
    #     ynew = ynew1 + ynew2
    #     return ynew


    # if radio_button_group.active == 1:
    #     ynew = []
    #     for i in range(0,int(resol) ):
    #         if a > l:
    #             f1_mag = 1.0*p_mag*a/l*(l-a/2.0)
    #             f2_mag = p_mag*a-f1_mag
    #             #calculate phi(x1=0) and phi(x2=0):
    #             phi_x1_0 = 1.0/E/I*(f1_mag*l**2.0/6.0 - p_mag*l**3.0/24.0) 
    #             phi_x2_0 = 1.0/E/I*(p_mag*l**3.0/6.0-f1_mag*l**2.0/2.0+ E*I*phi_x1_0)
    #             phi_x3_0 = 1.0/E/I*(p_mag*a**3.0/6.0 - (f1_mag + f2_mag - p_mag *l)*a**2.0/2.0 - (f1_mag*l - p_mag*l**2.0/2.0)*a + E*I*phi_x2_0)
    #             if x[i]<l:
    #                 dy = 1.0/E/I * (p_mag*x[i]**4.0/24.0 - f1_mag*x[i]**3.0/6.0 + E*I*phi_x1_0*x[i])
    #             if x[i]>=l and x[i]<a:
    #                 dy= 1.0/E/I * (p_mag*(x[i]-l)**4.0/24.0 - (f1_mag + f2_mag - p_mag*l)*(x[i]-l)**3.0/6.0 - (f1_mag*l - p_mag*l**2.0/2.0)*(x[i]-l)**2.0/2.0 + E*I*(x[i]-l)*phi_x2_0 ) 
        #         if x[i]>=a:
        #             #approximate free end with simple linear funtion:
        #             if x[i-1]<a:
        #                 index=i
        #             dy = ((ynew[index-2]-ynew[index-1])/(x[index-2]-x[index-1]))*(x[i]-a) + ynew[index-1]     
        #   ### FIND SOLUTION BEGIN
        #     else:  #l>=a
        #         f1_mag = 1.0* p_mag*a/l*(l - a + a/2.0)
        #         f2_mag = p_mag*a-f1_mag
        #         #calculate phi(x1=0) and phi(x2=0):
        #         phi_x1_0 = -1.0/E/I/(l+a)* (p_mag*l**4.0/24.0 - (f1_mag - p_mag*a)*l**3.0/6.0 - (f1_mag*a - p_mag*a**2.0/2.0)*l**2.0/2.0 + l*(p_mag*a**3.0/6.0 - f1_mag*a**2.0/2.0) + p_mag*a**4.0/24.0 - f1_mag*a**3.0/6.0 ) 
        #         phi_x2_0 = 1.0/E/I * (p_mag*a**3.0/6.0 - f1_mag*a**2.0/2.0 + E*I*phi_x1_0)
        #         if x[i]<a:
        #             dy = 1.0/E/I * (p_mag*x[i]**4.0/24.0 - f1_mag*x[i]**3.0/6.0 + E*I*phi_x1_0*x[i])
        #         if x[i]>=a and x[i]<l:
        #             dy_x1_a= 1.0/E/I * (p_mag*a**4.0/24.0 - f1_mag*a**3.0/6.0 + E*I*phi_x1_0*a)
        #             dy= 1.0/E/I*(p_mag*(x[i]-a)**4.0/24.0 - (f1_mag + p_mag* a)*(x[i]-a)**3.0/6.0 - (f1_mag*a + (p_mag*a**2.0)/2.0)*(x[i]-a)**2.0/2.0 + E*I*phi_x2_0 + E*I*dy_x1_a )
        #         if x[i]>=l:
        #             ##approximate free end with simple linear funtion:
        #             if x[i-1]<l:
        #                 index=i
        #             dy = ((ynew[index-2]-ynew[index-1])/(x[index-2]-x[index-1]))*(x[i]-l) + ynew[index-1] 
        #    ### FIND SOLUTION END
        #     ynew.append(dy)
        # return ynew

    # if radio_button_group.active == 2:
        # ynew = []
        # print a
        # for i in range(0,int(resol) ):
            # dy = 0
        #     ynew.append(dy)
        # return ynew

        
# FUNCTION: Cantilever Deflection function:
def Fun_C_Deflection(p,b,x):
    '''Calculates the deflection of the beam when it is cantilever'''

    ynew = []
    for i in range(0,int(resol) ):
        dy = 0
        ynew.append(dy)
    return ynew  
    
    # #b is the distance from the wall to the concentrated load
    # if radio_button_group.active == 0:
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                     #the free end and the concentrated load.
    #     for i in range(0,resol):
    #         if x[i] < a:
    #             #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #             dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         elif x[i] == a:
    #             dy = ( p * (b**3) ) / (3 * E * I)
    #         elif x[i] > a:
    #             #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #             dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         dy = 0 
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction

    # if radio_button_group.active == 1:   
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                 #the free end and the concentrated load.
    #     for i in range(0,resol):
            
    #         #UNCOMMENT FOR DEFLECTION
    #         # if x[i] < a:
    #         #     #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         #     dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         # elif x[i] == a:
    #         #     dy = ( p * (b**3) ) / (3 * E * I)
    #         # elif x[i] > a:
    #         #     #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #         #     dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )

    #         dy = 0
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction
 
    # if radio_button_group.active == 2:   
    #     ynew = []
    #     a = xf - b;     #The a for cantilever is the distance between
    #                 #the free end and the concentrated load.
    #     for i in range(0,resol):
    #         # if x[i] < a:
    #         #     #dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )
    #         #     dy = (  ( p * (b**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - b )
    #         # elif x[i] == a:
    #         #     dy = ( p * (b**3) ) / (3 * E * I)
    #         # elif x[i] > a:
    #         #     #dy = (  ( p * (a**2) ) / (6 * E * I)  ) * ( (3*xf) - (3*x[i]) - a )
    #         #     dy = (  ( p * ( ( xf - x[i])**2 ) ) / (6 * E * I) ) * ( (3*b) - xf + x[i] )

    #         dy = 0
    #         ynew.append(dy)

    #     return list(reversed(ynew))     #need to reverse because x is calculated in the opposite direction

