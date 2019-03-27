from Parameters import *
import numpy as np
from math import atan

def nearestIndex(L,x,y,self):
    cible=-1
    dMin=xSize+ySize
    for i in range(len(L)):
        if L[i]!=self:
            u,v=L[i].position
            d=((x-u)**2+(y-v)**2)**0.5
            if d<dMin:
                cible=i
                dMin=d
    return(cible)

class Being:
    def __init__(self,Master,position,maxspeed,vision,hearing,strength,agility):
        self.Master=Master
        self.position=position      # (x,y) for position in pixels
        self.cell=[int(position[0]),int(position[1])]                  # The cell the being is in
        self.speed=[0,0]                # vx and vy speeds in direction x and y
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving
        self.maxspeed=maxspeed              #maximal speed

    def move(self,t,volume):
        if self.stop==0:                                                            #verif that the entity can move
            self.position[0]+=t*self.speed[0]*self.maxspeed                 #new position of the being
            self.position[1]+=t*self.speed[1]*self.maxspeed
            self.cell=[int(self.position[0]),int(self.position[1])]
            if volume>0:
                self.Master.genSound(self.cell[0], self.cell[1], volume)
        else:                                                                       #decrease by one the countdown
            self.stop-=1

    def zProximity(self):
        x,y=self.position
        L=[]
        for Z in self.Master.Zombies:
            if Z!=self and abs(Z.position[0]-x)+abs(Z.position[1]-y)<=dInteraction:
                L.append(Z)
        return(L)

    def hProximity(self):
        x,y=self.position
        L=[]
        for H in self.Master.Humans:
            if H!=self and abs(H.position[0]-x)+abs(H.position[1]-y)<=dInteraction:
                L.append(H)
        return(L)

    def detectSound(self):
        x,y=self.cell
        u,v=0,0
        if x>0:
            u-=self.Master.Map[x-1][y].sound
            if y>0:
                u-=self.Master.Map[x-1][y-1].sound/2**0.5
            if y<ySize-1:
                u-=self.Master.Map[x-1][y+1].sound/2**0.5

        if x<xSize-1:
            u+=self.Master.Map[x+1][y].sound
            if y>0:
                u-=self.Master.Map[x+1][y-1].sound/2**0.5
            if y<ySize-1:
                u-=self.Master.Map[x+1][y+1].sound/2**0.5

        if y>0:
            v-=self.Master.Map[x][y-1].sound
        if y<ySize-1:
            v+=self.Master.Map[x][y+1].sound

        return(u,v)
        # sound in (x,y) and hearing aren't used

class Zombie(Being):
    def __init__(self,Master,position):
        Being.__init__(self,Master,position,zMaxspeed,zVision,zHearing,zStrength,zAgility)
        self.lifespan=zLifespan

    def info(self):
        x,y=self.cell
        print("Race: Zombie, case: x={}, y={}".format(x,y))

    def action(self):
        x,y=self.position
        hVision=self.hProximity()

        cible=nearestIndex(hVision,x,y,self)
        if cible!=-1:
            xh,yh=hVision[cible].position
            r=((x-xh)**2+(y-yh)**2)**0.5
            if r==0:
                self.speed=[0,0]
                return("human on position")
            slow=0
            if r<self.maxspeed:
                r=self.maxspeed
                slow=1
            self.speed=[(xh-x)/r,(yh-y)/r]
            self.move(dt,1-slow)
            return("human in sight")

        xSound, ySound=self.detectSound()
        r=(xSound**2+ySound**2)**0.5
        if r>self.hearing:
            self.speed=[xSound/r, ySound/r]
            self.move(dt,1)
            return("sound heard")

        zVision=self.zProximity()
        cible=nearestIndex(zVision,x,y,self)
        if cible!=-1:
            xz,yz=zVision[cible].position
            r=((x-xz)**2+(y-yz)**2)**0.5
            if r==0:
                self.speed=[0,0]
                return("zombie on position")
            slow=0
            if r<self.maxspeed:
                r=self.maxspeed
                slow=1
            self.speed=[(xz-x)/r,(yz-y)/r]
            self.move(dt,1-slow)
            return("zombie in sight")

        return("nothing detected")

    def death(self):
        self.Master.Zombies.remove(self)

class Human(Being):
    def __init__(self,Master,position,maxspeed,strength,agility,morality,coldblood,behavior):
        Being.__init__(self,Master,position,maxspeed,hVision,hHearing,strength,agility)
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

    def addEnergy(self,e):
        if self.energy+e<0:
            self.energy=0
        else:
            self.energy=min(100,self.energy+e)

    def addHunger(self,h):
        if self.hunger+h<0:
            self.hunger=0
        else:
            self.hunger=min(100,self.hunger+h)

    def setGroup(self,newGroup):
        if self.group !=None:
            self.Master.Groups[self.group].remove(self)
        self.group=newGroup
        self.Master.Groups[newGroup].append(self)

    def action(self):
        pass

    def zombification(self):
        time.sleep(zIncubationTime*dt)                #waiting for the human to turn into a zombie
        self.Master.Humans.remove(self)              #removing the entity from class human
        self.Master.Zombies.append(Zombie(self.Master,self.position))             #creating a new zombie

    def fight(self):
        self.Master.genSound(self.cell[0],self.cell[1],Bruit)
        Zstrength=0
        Zbattle=[]
        for Z in self.zProximity():
            Zbattle.append(Z)
            Zstrength+=Z.stength
        Hstrength=0
        Hbattle=[]
        for H in self.hProximity():
            if H.group==self.group or H.morality=="hero":
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
