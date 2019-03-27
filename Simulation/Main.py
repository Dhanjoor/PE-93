from Parameters import *
from Cell import *
from CreateBeing import *
from random import randint

class Master:
    def __init__(self):
        self.Map=[]
        self.Humans=[]
        self.Zombies=[]

    def genSound(self,x0,y0,volume):
        if x0<0 or x0>=xSize or y0<0 or y0>=ySize or self.Map[x0][y0].content==2:
            print("error")
            return()

        self.Map[x0][y0].sound+=volume
        if volume==1:
            return()
        moves=[(0,1), (0,-1), (1,0), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
        suivants=[(x0,y0,volume)]

        visited=[[False for _ in range(2*volume+1)] for _ in range(2*volume+1)]
        visited[volume][volume]=True

        while suivants:
            new=[]
            for a,b,M in suivants:
                for dx,dy in moves:
                    x,y=a+dx,b+dy
                    value=M-(dx**2+dy**2)**(1/2)
                    if x>=0 and x<xSize and y>=0 and y<ySize and self.Map[x][y].content!=2 and not(visited[x-x0+volume][y-y0+volume]) and value>0.5:
                        if self.Map[x][y].content==1:
                            value-=attenuationPorte
                            if value<=0.5:
                                continue
                        self.Map[x][y].sound+=round(value)
                        visited[x-x0+volume][y-y0+volume]=True
                        new.append((x,y,value))
            suivants=new[:]

Master=Master()

#Map creation
Master.Map=[[Cell(i,j) for j in range(ySize)] for i in range(xSize)]
Buildings=[]

with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
for i in range(xSize):
    line=list(lines[i].split())
    for j in range(ySize):
        cell=list(line[j].split("/"))
        Master.Map[i][j].idBuilding=int(cell[0])
        Master.Map[i][j].sound=int(cell[1])
        Master.Map[i][j].content=int(cell[2])

for _ in range(nZombies):
    Master.Zombies.append(createZombie(Master))

for _ in range(nHumans):
    Master.Humans.append(createHuman(Master))

#Simulation
t=9
events=[(randint(0, xSize-1),randint(0,ySize-1),5)]
with open(saveTxt,"w") as f:
    pass

while t<=Tsimulation:
    print("======== Tour {} ========".format(t))

    for x in range(xSize):
        for y in range(ySize):
            if Master.Map[x][y].sound>0:
                Master.Map[x][y].sound-=1

    for nh in range(len(Master.Humans)-1, -1, -1):
        h=Master.Humans[nh]
        h.action()
        h.info()
    print()
    for nz in range(len(Master.Zombies)-1,-1,-1):
        z=Master.Zombies[nz]
        print(z.action())
        z.info()
        print(z.lifespan)
    print()

    #Decrease the lifespan of the zombies
    for nz in range(len(Master.Zombies)-1,-1,-1):
        if Master.Zombies[nz].lifespan==1:
            Master.Zombies[nz].death()
        else:
            Master.Zombies[nz].lifespan-=1

    #Sauvegarde
    with open(saveTxt, "a") as f:
        if t>1:
            f.write("***\n")
        f.write(str(len(Master.Humans)))
        f.write("\n")
        for h in Master.Humans:
            x,y=round(h.position[0],2), round(h.position[1],2)
            vr,vtheta=round(h.speed[0],2), round(h.speed[1],2)
            f.write("{}/{}/{}/{}/{}/{}/{}/{}".format(x,y,vr,vtheta,h.hunger,h.energy,h.stress,h.stamina))
            f.write("\n")
        f.write(str(len(Master.Zombies)))
        f.write("\n")
        for z in Master.Zombies:
            x,y=round(z.position[0],2), round(z.position[1],2)
            vr,vtheta=round(z.speed[0],2), round(z.speed[1],2)
            f.write("{}/{}/{}/{}/{}".format(x,y,vr,vtheta,z.lifespan))
            f.write("\n")
        f.write(str(len(events)))
        f.write("\n")
        for x,y,M in events:
            f.write("{}/{}/{}".format(x,y,M))
            f.write("\n")
    t+=dt
    events=[]