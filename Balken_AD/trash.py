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
