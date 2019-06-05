mapTxt="Map/ecully.txt"
journalTxt="Journal/ecully_stress.txt"
with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
    xSize=len(lines)-1 #last line shows the buildings
    ySize=len(list(lines[0].split()))

Tsimulation=10000
dt=1
attenuationPorte=10
foodPerCell=200
restPerCell=20

moveVolume=50
shoutVolume=50
fightVolume=100

nZombies=1
nHumans=100
dInteraction=2
nZombieAware=5 #number of zombie to see in the same place to become aware

#Zombie parameters
zSpeed=2
zVision=100
zHearing=100
zStrength=2
zAgility=1
zLifespan=500
zIncubationTime=10
zMaxspeed=2

#Human parameters
hVision=100
hHearing=100
cosVisionAngle=0 #ANGLE IGNORE
maxHunger=500
maxEnergy=500

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #maxspeed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

pMoralities=[1/4, 1/4, 1/2] #proba of being "evil","neutral","hero"

pBehaviors=[1/6, 2/3, 1/6]  #proba of being using mostly "flee","hide","fight"

pColdblood=[0, 0, 1] #proba of being "zen","stable","stressed"

pCharisma=[1/10, 8/10, 1/10] #proba of being "solitary", "casual", "leader"