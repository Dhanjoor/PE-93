mapTxt="Map/test.txt"
journalTxt="Journal/Journal.txt"
with open(mapTxt, "r") as f:
    lines=f.read().split("\n")
    xSize=len(lines)-1 #last line shows the buildings
    ySize=len(list(lines[0].split()))

Tsimulation=100
dt=1
attenuationPorte=3
foodPerCell=10
restPerCell=10

shoutVolume=0
fightVolume=3
uneVariable=0
unSeuil=0.5

nZombies=1
nHumans=100
dInteraction=2

#Zombie parameters
zSpeed=1
zVision=20
zHearing=1
zStrength=2
zAgility=1
zLifespan=900
zIncubationTime=1
zMaxspeed=1

#Human parameters
hVision=20
hHearing=1
cosVisionAngle=0 #ANGLE IGNORE
maxHunger=86400
maxEnergy=259200

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #maxspeed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

pMoralities=[1/4, 1/2, 1/4] #proba of being "evil","neutral","hero"

pBehaviors=[1/3, 1/3, 1/3]  #proba of being using mostly "flee","hide","fight"

pColdblood=[1/3, 1/3, 1/3] #proba of being "zen","stable","stressed"

pCharisma=[1/10, 8/10, 1/10] #proba of being "solitary", "casual", "leader"