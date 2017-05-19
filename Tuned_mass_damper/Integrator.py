from Mass import *
from math import cos

class Integrator:
    def __init__(self,listOfMasses,oscAmp,listOfDashpots):
        self.oscAmp=oscAmp
        try:
            # save masses and forces applied at each step
            self.n=len(listOfMasses)
            self.masses=listOfMasses
        except TypeError:
            # if there is only one mass then stock it in a vector so there are no list index errors
            self.n=1
            self.masses=[listOfMasses]
        try:
            # save masses and forces applied at each step
            self.d=len(listOfDashpots)
            self.dashpots=listOfDashpots
        except TypeError:
            # if there is only one mass then stock it in a vector so there are no list index errors
            self.d=1
            self.dashpots=[listOfDashpots]
    
    # Velocity Verlet method
    def evolve(self,dt,oscForceAngle,omega):
        self.Verlet(dt,oscForceAngle,omega)
        #self.Symplectic3(dt,oscForceAngle,omega)
        #self.RK4(dt,oscForceAngle,omega)
    
    def Verlet(self,dt,oscForceAngle,omega):
        # prepare vectors to save values needed across loops
        Disp=[]
        Acc=[]
        for i in range(0,self.n):
            # save all forces to allow movements without acceleration being changed
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            # calculate new position s=s+v*dt+0.5*a*dt*dt
            Disp.append(temp[0]*dt+0.5*dt*dt*temp[1])
            # save current acceleration
            Acc.append(temp[1])
        for i in range(0,self.n):
            # once all forces have been saved, move by previously calculated displacement
            self.masses[i].move(Disp[i])
            # apply force that will be applied at next timestep
            self.masses[i].applyForce(Coord(0,self.oscAmp*cos(oscForceAngle+omega*dt)),None)
        for i in range(0,self.d):
            self.dashpots[i].assertForces(dt)
        for i in range(0,self.n):
            # save forces to allow getVelAcc function to be able to use them
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            # update velocity v=v+0.5*dt*(a_t+a_{t+1})
            self.masses[i].v+=0.5*dt*(Acc[i]+temp[1])
    
    def RK4(self,dt,oscForceAngle,omega):
        # !!!!! Not Symplectic !!!!!
        
        
        # prepare vectors to save values needed across loops
        K=[]
        for i in range(0,self.n):
            # save all forces to allow movements without acceleration being changed
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            # save current acceleration
            K.append([temp])
        for i in range(0,self.n):
            # once all forces have been saved, move by previously calculated displacement
            self.masses[i].move(K[i][0][0]*dt/2.0)
            self.masses[i].v+=K[i][0][1]*dt/2.0
            # apply force that will be applied at next timestep
            self.masses[i].applyForce(Coord(0,self.oscAmp*cos(oscForceAngle+omega*dt/2.0)),None)
        for i in range(0,self.n):
            # save forces to allow getVelAcc function to be able to use them
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            K[i].append(temp)
        for i in range(0,self.n):
            # once all forces have been saved, move by previously calculated displacement
            # 2 steps for dashpot
            self.masses[i].move(-K[i][0][0]*dt/2.0)
            self.masses[i].move(K[i][1][0]*dt/2.0)
            self.masses[i].v+=(K[i][1][1]-K[i][0][1])*dt/2.0
            # apply force that will be applied at next timestep
            self.masses[i].applyForce(Coord(0,self.oscAmp*cos(oscForceAngle+omega*dt/2.0)),None)
        for i in range(0,self.n):
            # save forces to allow getVelAcc function to be able to use them
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            K[i].append(temp)
        for i in range(0,self.n):
            # once all forces have been saved, move by previously calculated displacement
            # 2 steps for dashpot
            self.masses[i].move(-K[i][1][0]*dt/2.0)
            self.masses[i].move(K[i][2][0]*dt)
            self.masses[i].v+=(K[i][2][1]-K[i][1][1]/2.0)*dt
            # apply force that will be applied at next timestep
            self.masses[i].applyForce(Coord(0,self.oscAmp*cos(oscForceAngle+omega*dt)),None)
        for i in range(0,self.n):
            # save forces to allow getVelAcc function to be able to use them
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            K[i].append(temp)
        for i in range(0,self.n):
            # once all forces have been saved, move by previously calculated displacement
            # 2 steps for dashpot
            self.masses[i].move(-K[i][2][0]*dt)
            self.masses[i].move((K[i][0][0]+2.0*(K[i][1][0]+K[i][2][0])+K[i][3][0])*dt/6.0)
            self.masses[i].v+=((K[i][0][1]+2.0*(K[i][1][1]+K[i][2][1])+K[i][3][1])/6.0-K[i][3][1])*dt
