from Parameters import *
import numpy as np

class Being:
    def __init__(self,Master,position,maxspeed,vision,hearing,strength,agility):
        self.Master=Master
        self.position=position      # (x,y) for position in pixels
        self.cell=(int(position[0]),int(position[1]))                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving
        self.maxspeed=maxspeed              #maximal speed
        self.speed=(0,0)

    def move(self,t):
        if self.stop==0:                                                            #verif that the entity can move
            self.position[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
            self.position[1]+=t*self.speed[0]*np.sin(self.speed[1])
            self.cell=self.master.which_cell(self.position[0],self.position[1])
        else:                                                                       #decrease by one the countdown
            self.stop-=1

    def Z_proximity(self):
        n,m=self.cell
        L=[]
        for Z in self.Master.Zombies:
            if abs(Z.cell[0]-n)+abs(Z.cell[1]-m)<=D_interaction:
                L.append(Z)
        return L

    def H_proximity(self):
        n,m=self.cell
        L=[]
        for H in self.Master.Humans:
            if abs(H.cell[0]-n)+abs(H.cell[1]-m)<=D_interaction:
                L.append(H)
        return L

    def detectSound(self):
        x,y=self.cell
        u,v=0,0
        if x>0:
            u-=self.Master.Map[x-1][y].sound
            if y>0:
                u-=self.Master.Map[x-1][y-1].sound/2**0.5
            if y<ySize:
                u-=self.Master.Map[x-1][y+1].sound/2**0.5

        if x<xSize-1:
            u+=self.Master.Map[x+1][y].sound
            if y>0:
                u-=self.Master.Map[x+1][y-1].sound/2**0.5
            if y<ySize:
                u-=self.Master.Map[x+1][y+1].sound/2**0.5

        if y>0:
            v-=self.Master.Map[x][y-1].sound
        if y<ySize:
            v+=self.Master.Map[x][y+1].sound

        return(u,v)
        # sound in (x,y) and hearing aren't used

    def seeHuman(self):
        x,y=self.cell
        H=[]
        for h in self.master.Humains:
            if h.cell[0]-x==0 and h.cell[1]-y==0:
                if ((h.cell[0]-x)**2+(h.cell[1]-y)**2)**0.5<self.vision and abs(2*atan((h.cell[1]-y)/((h.cell[0]-x)+((h.cell[0]-x)**2+(h.cell[1]-y)**2)**0.5)))<60:
                    H.append(h)
        return H

    def seeZombie(self):
        x,y=self.cell
        Z=[]
        for z in self.master.Zombies:
            if z.cell[0]-x==0 and z.cell[1]-y==0:
                if ((z.cell[0]-x)**2+(z.cell[1]-y)**2)**0.5<self.vision and abs(2*atan((z.cell[1]-y)/((z.cell[0]-x)+((z.cell[0]-x)**2+(z.cell[1]-y)**2)**0.5)))<60:
                    Z.append(z)
        return Z

class Zombie(Being):
    def __init__(self,Master,position):
        Being.__init__(self,Master,position,z_maxspeed,z_vision,z_hearing,z_strength,z_agility)
        self.lifespan=z_lifespan

    def info(self):
        x,y=self.cell
        print("Race: Zombie, case: x={}, y={}".format(x,y))

    def action(self):

        self.lifespan-=1
        if self.lifespan==0:
            self.death()

    def death(self):
        self.Master.Zombies.remove(self)

class Human(Being):
    def __init__(self,Master,position,maxspeed,strength,agility,morality,coldblood,behavior):
        Being.__init__(self,Master,position,maxspeed,h_vision,h_hearing,strength,agility)
        self.morality=morality              #define the morality of the human
        self.coldblood=coldblood          #define how the human endure the stress
        self.behavior=behavior              #define the type of survival (hide,flee,fight,...)
        self.hunger=100                  #hunger (decrease by time) 0=death
        self.energy=100                  #energy (decrease by time) 0=death
        self.stress=0                  #quantity of stress (determine the quality of the decisions)
        self.stamina=100                #stamina (decrease when running) 0=no more running
        self.knowing=False                  #knowing the zombie invasion
        self.group=None                #define the social group of the human

    def info(self):
        x,y=self.cell
        print("Race: Humain, case: x={}, y={}".format(x,y))

    def add_energy(self,e):
        if self.energy+e<0:
            self.energy=0
        else:
            self.energy=min(100,self.energy+e)

    def add_hunger(self,h):
        if self.hunger+h<0:
            self.hunger=0
        else:
            self.hunger=min(100,self.hunger+h)

    def set_group(self,new_group):
        if self.group !=None:
            self.Master.Groups[self.group].remove(self)
        self.group=new_group
        self.Master.Groups[new_group].append(self)

    def action(self):
        pass

    def zombification(self):
        time.sleep(z_incubation_time*dt)                #waiting for the human to turn into a zombie
        self.Master.Humans.remove(self)              #removing the entity from class human
        self.Master.Zombies.append(Zombie(self.Master,self.position))             #creating a new zombie

    def fight(self):
        genSound(self.cell[0],self.cell[1],Bruit)
        Zstrength=0
        Zbattle=[]
        for Z in self.Z_proximity():
            Zbattle.append(Z)
            Zstrength+=Z.stength
        Hstrength=0
        Hbattle=[]
        for H in self.H_proximity():
            if H.group==self.group or H.morality==hero:
                Hbattle.append(H)
                Hstrength+=H.strength                                          #fight system: uniform law.
                L=Hstrength/(2*(Zstrength+Hstrength))
            else:
                L=Zstrength/(2*(Zstrength+Hstrength))
        if Hstrength/(Zstrength+Hstrength)-L>=proba:         #zombie(s) stronger than human
            for H in Hbattle:
                H.zombification()
        elif Hstrength/(Zstrength+Hstrength)+L<=proba:        #human stronger than zombie(s)
            for Z in Zbattle:
                Z.death()
        else:                                       #human and zombie(s) as strong: human manage to get away
            for Z in Zbattle:
                Z.stop=2
