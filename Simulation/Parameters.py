mapTxt="Map/ecl.txt"
journalTxt="Journal/ecl_food.txt"
with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
    xSize=len(lines)-1 #last line shows the buildings
    ySize=len(list(lines[0].split()))

Tsimulation=1000
dt=1
attenuationPorte=10
foodPerCell=10
restPerCell=10

moveVolume=0
shoutVolume=0
fightVolume=0

nZombies=1
nHumans=100
dInteraction=2
nZombieAware=2 #number of zombie to see in the same place to become aware

#Zombie parameters
zSpeed=1
zVision=100
zHearing=100
zStrength=2
zAgility=1
zLifespan=200000000
zIncubationTime=10
zMaxspeed=1

#Human parameters
hVision=100
hHearing=100
cosVisionAngle=0 #ANGLE IGNORE
maxHunger=500
maxEnergy=50000

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #maxspeed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

pMoralities=[1/4, 1/2, 1/4] #proba of being "evil","neutral","hero"

pBehaviors=[3/7, 4/7, 0/7]  #proba of being using mostly "flee","hide","fight"

pColdblood=[1/3, 1/3, 1/3] #proba of being "zen","stable","stressed"

pCharisma=[1/10, 8/10, 1/10] #proba of being "solitary", "casual", "leader"