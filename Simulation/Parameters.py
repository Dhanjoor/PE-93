mapTxt="Map/Map.txt"
journalTxt="Journal/Journal.txt"
with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
    xSize=len(lines)-1 #last line shows the buildings
    ySize=len(list(lines[0].split()))

Tsimulation=8
dt=1
attenuationPorte=3

nZombies=1
nHumans=1
dInteraction=10

#Zombie parameters
zSpeed=1
zVision=1
zHearing=1
zStrength=1
zAgility=1
zLifespan=5
zIncubationTime=10
zMaxspeed=1

#Human parameters
hVision=1
hHearing=1

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #maxspeed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

pMoralities=[1/4, 1/2, 1/4] #proba of being "evil","neutral","hero"

pBehaviors=[1/3, 1/3, 1/3]  #proba of being using mostly "flee","hide","fight"

pStress=[1/3, 1/3, 1/3] #proba of being "zen","stable","stressed"