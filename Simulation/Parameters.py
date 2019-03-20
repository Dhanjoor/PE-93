mapTxt="Map.txt"
with open("Map/"+mapTxt, "r") as f:
    lines=f.read().split("\n")
    xSize=len(lines)-1 #last line shows the buildings
    ySize=len(list(lines[0].split()))

Tsimulation=10
dt=1
attenuation_porte=3

nZombies=3
nHumans=3

#Zombie parameters
z_speed=1
z_vision=1
z_hearing=1
z_strength=1
z_agility=1
z_lifespan=5
z_incubation_time=10
z_maxspeed=1

#Human parameters
h_vision=1
h_hearing=1

weak, casual, strong=(1,1,1), (2,2,2), (3,3,3) #speed, strength, agility
pAbilities=[1/4, 1/2, 1/4] #proba for general stats

evil, neutral, hero=0,1,2
pMoralities=[1/4, 1/2, 1/4] #proba

flee,hide,fight=0,1,2
pBehaviors=[1/3, 1/3, 1/3]  #proba

zen,stable,stressed=0,1,2
pStress=[1/3, 1/3, 1/3] #proba
