from Parameters import *
from Cell import *
from CreateBeing import *

class Master:
    def __init__(self):
        self.Map=[]
        self.Humans=[]
        self.Zombies=[]

Master=Master()

#Map creation
Master.Map=[[Cell(i,j) for j in range(ySize)] for i in range(xSize)]
Buildings=[]

with open("Map/"+mapTxt, "r") as f:
    lines=f.read().split("\n")
for i in range(xSize):
    line=list(lines[i].split())
    for j in range(ySize):
        cell=list(line[j].split("/"))
        Master.Map[i][j].idBuilding=int(cell[0])
        Master.Map[i][j].sound=int(cell[1])
        Master.Map[i][j].content=int(cell[2])

for _ in range(nZombies):
    Master.Zombies.append(create_zombie(Master))

for _ in range(nHumans):
    Master.Humans.append(create_human(Master))

#Simulation
t=1
events=[(2,2,6)]
with open("Save.txt","w") as f:
    pass

while t<=Tsimulation:
    print("======== Tour {} ========".format(t))
    for nh in range(len(Master.Humans)-1, -1, -1):
        h=Master.Humans[nh]
        h.action()
        h.info()
    print()
    for nz in range(len(Master.Zombies)-1,-1,-1):
        z=Master.Zombies[nz]
        z.action()
        z.info()
        print(z.lifespan)
    print()

    #Sauvegarde
    with open("Save.txt","a") as f:
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
        f.write("***\n")
    t+=dt
    events=[]