from Parameters import *

class Being:
    def __init__(self,Master,position,speed,vision,hearing,strength,agility):
        self.Master=Master
        self.position=position      # (x,y) for position in pixels
        self.cell=(int(position[0]),int(position[1]))                  # The cell the being is in
        self.speed=speed                # (vr,vteta) vr is the norm and vteta the angle of the speed
        self.vision=vision              #vision distance
        self.hearing=hearing                    #hearing threshold
        self.strength=strength              #physical trait (don't change)
        self.agilty=agility                 #agility trait (don't change)
        self.stop=0                         #countdown when the entity stop moving

    def move(self,t):
        if self.stop==0:                                                            #verif that the entity can move
            self.position[0]+=t*self.speed[0]*np.cos(self.speed[1])                  #new position of the being
            self.position[1]+=t*self.speed[0]*np.sin(self.speed[1])
            self.cell=self.master.which_cell(self.position[0],self.position[1])
        else:                                                                       #decrease by one the countdown
            self.stop-=1

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
        #pas pris en compte hearing et le son en (x,y) ici

class Zombie(Being):
    def __init__(self,Master,position,*z_speed):
        Being.__init__(self,Master,position,z_speed,z_vision,z_hearing,z_strength,z_agility)
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
    def __init__(self,Master,position,speed,strength,agility,morality,coldblood,behavior,group):
        Being.__init__(self,Master,position,speed,h_vision,h_hearing,strength,agility)
        self.morality=morality              #define the morality of the human
        self.coldblood=coldblood          #define how the human endure the stress
        self.behavior=behavior              #define the type of survival (hide,flee,fight,...)
        self.hunger=100                  #hunger (decrease by time) 0=death
        self.energy=100                  #energy (decrease by time) 0=death
        self.stress=0                  #quantity of stress (determine the quality of the decisions)
        self.stamina=100                #stamina (decrease when running) 0=no more running
        self.knowing=False                  #knowing the zombie invasion
        self.group=group                #define the social group of the human

    def info(self):
        x,y=self.cell
        print("Race: Humain, case: x={}, y={}".format(x,y))
    
    def set_group(self,new_group):
        self.group=new_group
    
    def action(self):
        pass

    def zombification(self):
        time.sleep(z_incubation_time*dt)                #waiting for the human to turn into a zombie
        self.Master.Humans.remove(self)              #removing the entity from class human
        self.MasterZombies.append(Zombie(self.Master,self.position,0))             #creating a new zombie

    def fight(self):
        Zstrength=0
        genSound(self.cell[0],self.cell[1],Bruit)
        for Z in Zinrange:
            Zstrength+=Z.stength
        proba=rd.random()                                          #fight system: uniform law.
        if self.strength/(Zstrength+self.strength)<0.5:
            L=self.strength/(2*(Zstrength+self.strength))
        else:
            L=Z.Strength/(2*(Zstrength+self.strength))
        if self.strength/(Zstrength+self.strength)-L>=proba:         #zombie(s) stronger than human
            self.zombification()      #2 cases: eaten or transformed                
        elif self.strength/(Zstrength+self.strength)+L<=proba:        #human stronger than zombie(s)
            for Z in Zincell:
                Z.death()
        else:                                       #human and zombie(s) as strong: human manage to get away
            for Z in Zincell:
                Z.stop=2
