from Parameters import *
from Cell import *
from CreateBeing import *
from Buildings import *
from random import randint

class Master:
    def __init__(self):
        self.Map=[]
        self.Humans=[]
        self.Zombies=[]
        self.Buildings=[]
        self.Events=[]
        self.Turn=1

    def showMap(self):
        for i in range(xSize):
            for j in range(ySize):
                print(Master.Map[i][j].content, end=" ")
            print()

    def showBeing(self):
        L=[[0 for _ in range(ySize)] for _ in range(xSize)]
        for h in self.Humans:
            x,y=h.cell
            L[x][y]="h"
        for z in self.Zombies:
            x,y=z.cell
            L[x][y]="z"

        for i in range(xSize):
            for j in range(ySize):
                print(L[i][j], end=" ")
            print()

    def genSound(self,x0,y0,volume):
        self.Events.append((x0,y0,volume))
        if x0<0 or x0>=xSize or y0<0 or y0>=ySize or (self.Map[x0][y0].content in [1,2]):
            print("genSound error")
            return()

        self.Map[x0][y0].sound+=volume
        if volume<=1:
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
                    if x>=0 and x<xSize and y>=0 and y<ySize and self.Map[x][y].content!=1 and not(visited[x-x0+volume][y-y0+volume]) and value>0.5:
                        if self.Map[x][y].content==2:
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

with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
for i in range(xSize):
    line=list(lines[i].split())
    for j in range(ySize):
        cell=list(line[j].split("/"))
        Master.Map[i][j].idBuilding=int(cell[0])
        Master.Map[i][j].sound=int(cell[1])
        Master.Map[i][j].content=int(cell[2])
        if int(cell[2])==3:
            Master.Map[i][j].quantity=foodPerCell
        elif int(cell[2])==4:
            Master.Map[i][j].quantity=restPerCell

buildings=lines[-1].split()
idBuilding=1
for b in buildings:
    elements=b.split("/")
    corners=elements[0].split("-")
    x1,y1=map(int, corners[0].split("_"))
    x2,y2=map(int, corners[1].split("_"))
    for i in range(min(x1,x2), max(x1,x2)+1):
        for j in range(min(y1,y2), max(y1,y2)+1):
            Master.Map[i][j].idBuilding=idBuilding
    nFood, nRest=int(elements[1]), int(elements[2])
    building=Building(x1,y1,x2,y2,nFood,nRest,[])
    doors=elements[3].split("-")
    for door in doors:
        xd,yd=map(int, door.split("_"))
        building.doors.append((xd,yd))
    Master.Buildings.append(building)
    idBuilding+=1

for _ in range(nZombies):
    Master.Zombies.append(createZombie(Master))

for _ in range(nHumans):
    Master.Humans.append(createHuman(Master))

""" Debug
Master.showMap()
print()
Master.showBeing()
print()
print("Ça part")"""


#Simulation
with open(journalTxt,"w") as f:
    pass

while Master.Turn<=Tsimulation and Master.Humans and Master.Zombies:

    print("======== Tour {} ========".format(Master.Turn))

    nh=len(Master.Humans)-1
    while nh>=0:
        if nh>=len(Master.Humans):
            nh-=1
            continue
        h=Master.Humans[nh]
        h.action()
        #h.info()
        nh-=1
    #print()
    nz=len(Master.Zombies)-1
    while nz>=0:
        if nz>=len(Master.Zombies):
            nz-=1
            continue
        z=Master.Zombies[nz]
        z.action()
        #z.info()
        nz-=1
    #print()

    #Sauvegarde
    with open(journalTxt, "a") as f:
        if Master.Turn>1:
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
            vx,vy=round(z.speed[0],2), round(z.speed[1],2)
            f.write("{}/{}/{}/{}/{}".format(x,y,vx,vy,z.lifespan))
            f.write("\n")
        f.write(str(len(Master.Events)))
        f.write("\n")
        for x,y,M in Master.Events:
            f.write("{}/{}/{}".format(x,y,M))
            f.write("\n")

    #reduce the sound
    for x in range(xSize):
        for y in range(ySize):
            if Master.Map[x][y].sound>0:
                Master.Map[x][y].sound-=1

    #Decrease the lifespan of the zombies
    for nz in range(len(Master.Zombies)-1,-1,-1):
        Master.Zombies[nz].addLifespan(-1)

    Master.Turn+=1
    Master.Events=[]

#Save the parameters
with open("Parameters.py", "r") as f:
    parameters=f.read()
with open(journalTxt.split("/")[0]+"/"+"parameters_"+journalTxt.split("/")[1], "w") as f:
    f.write(parameters)


print("Humans remaining :", len(Master.Humans), "Zombies remaining :", len(Master.Zombies))
results={"strong":0, "casual":0, "weak":0, "zen":0, "stable":0, "stressed":0, "evil":0, "neutral":0, "hero":0, "flee":0, "hide":0, "fight":0}
for h in Master.Humans:
    results[h.morality]+=1
    results[h.behavior]+=1
    results[h.coldblood]+=1
    if h.agility==1:
        results["weak"]+=1
    elif h.agility==2:
        results["casual"]+=1
    else:
        results["strong"]+=1
print(results)

""" Debug
for h in Master.Humans:
    h.info()
for z in Master.Zombies:
    z.info()

Master.showMap()
Master.showBeing()"""