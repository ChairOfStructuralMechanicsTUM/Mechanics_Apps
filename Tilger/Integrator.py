from Mass import *

class Integrator:
    def __init__(self,listOfMasses,ForceList):
        try:
            # save masses and forces applied at each step
            self.n=len(listOfMasses)
            self.masses=listOfMasses
            self.forces=ForceList
        except TypeError:
            # if there is only one mass then stock it in a vector so there are no list index errors
            self.n=1
            self.masses=[listOfMasses]
            self.forces=[ForceList]
    
    # Velocity Verlet method
    def evolve(self,dt):
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
            self.masses[i].move(Disp[i],dt)
            # apply force that will be applied at next timestep
            self.masses[i].applyForce(Coord(0,self.forces[i]),None)
        for i in range(0,self.n):
            # save forces to allow getVelAcc function to be able to use them
            self.masses[i].FreezeForces()
            # find current velocity and acceleration
            temp=self.masses[i].getVelAcc()
            # update velocity v=v+0.5*dt*(a_t+a_{t+1})
            self.masses[i].v+=0.5*dt*(Acc[i]+temp[1])
