from Parameters import *
import numpy as np
from math import atan

def nearestIndex(L,x,y):
    cible=-1
    dMin=xSize+ySize
    for i in range(len(L)):
        xh,yh=L[i].cell
        d=((x-xh)**2+(y-yh)**2)**0.5
        if d<dMin:
            cible=i
            dMin=d
    return(cible)

class Being:
    def __init__(self,Master,position,maxspeed,vision,hearing,strength,agility):
        self.Master=Master
        self.position=position      # (x,y) for position in pixels
        self.cell=[int(position[0]),int(position[1])]                  # The cell the being is in
        self.speed=[0,0]                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving
        self.maxspeed=maxspeed              #maximal speed

    def move(self,t,volume):
        if self.stop==0:                                                            #verif that the entity can move
            self.position[0]+=t*self.speed[0]                 #new position of the being
            self.position[1]+=t*self.speed[1]
            self.cell=(int(self.position[0]),int(self.position[1]))
            self.Master.genSound(self.cell[0], self.cell[1], volume)
        else:                                                                       #decrease by one the countdown
            self.stop-=1

    def zProximity(self):
        n,m=self.cell
        L=[]
        for Z in self.Master.Zombies:
            if abs(Z.cell[0]-n)+abs(Z.cell[1]-m)<=dInteraction:
                L.append(Z)
        return L

    def hProximity(self):
        n,m=self.cell
        L=[]
        for H in self.Master.Humans:
            if abs(H.cell[0]-n)+abs(H.cell[1]-m)<=dInteraction:
                L.append(H)
        return L

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
        x,y=self.cell
        hVision=self.hProximity()

        cible=nearestIndex(hVision,x,y)
        if cible!=-1:
            xh,yh=hVision[cible].cell
            self.speed=[xh-x,yh-y]
            self.move(dt,1)
            return("human in sight")

        xSound, ySound=self.detectSound()
        if (xSound**2+ySound**2)**0.5>self.hearing:
            self.speed=[xSound, ySound]
            self.move(dt,1)
            return("sound heard")

        zVision=self.zProximity()
        cible=nearestIndex(zVision,x,y)
        if cible!=-1:
            xz,yz=zVision[cible].cell
            self.speed=[xz-x,yz-y]
            self.move(dt,1)
            return("zombie in sight")

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
        genSound(self.cell[0],self.cell[1],Bruit)
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
    def pathfinding(self,xd,yd): # xh,yh position of human, xd,yd position of door
        
        # We create a table of cells that can be passed through
        m=max(xSize,ySize)**2
        Access=[[m for _ in range(ySize)] for _ in range(xSize)]
        for i in range(xSize):
            for j in range(ySize):
                if self.Master.Map[i][j].content:
                    Access[i][j] = -1
        for zombie in self.Master.Zombies :
            x,y=zombie.cell
            Access[x][y] = -1
            
        # All possible Moves to a neighbor cell, list of cells to visit, final path
        Moves=[(1,0),(0,1),(-1,0),(0,-1)]
        Tovisit=[(self.position[0],self.position[1])]
        Access[self.position[0]][self.position[1]]=0
        
        # BFS
        fini=False
        while len(Tovisit)>0 and not(fini):
            x,y=Tovisit.pop()
            n=Access[x][y]
            for dx,dy in Moves:
                x2,y2=x+dx,y+dy
                if (0<=x2 and x2<xSize and 0<=y2 and y2<ySize and Access[x2][y2]>n+1):
                    Tovisit.insert(0,(x2,y2))
                    Access[x2][y2]=n+1
                if (x2,y2)==(xd,yd):
                    fini=True
                    break
                
        # Extraction of the path
        if fini:
            Path,x,y,n=[(xd,yd)],xd,yd,Access[xd][yd]
            while n>0:
                for dx,dy in Moves:
                    if (0<=x+dx and x+dx<=xSize-1 and 0<=y+dy and y+dy<=ySize-1 and Access[x+dx][y+dy]==n-1):
                        x,y,n=x+dx,y+dy,n-1
                        Path.insert(0,(x,y))
                        break
            return Path
        else:
            return ([])
