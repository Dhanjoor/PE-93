from random import random, randint
from Parameters import *
from Being import *

def createZombie(Master):
    x,y=randint(2, xSize-3), randint(2, ySize-3)
    while Master.Map[x][y].content!=0 or Master.Map[x][y].idBuilding!=0:
        x,y=randint(2, xSize-3), randint(2, ySize-3)
    #x,y=x+random(),y+random()

    return(Zombie(Master, [x,y]))

def createHuman(Master):
    ability=random()
    if ability<=pAbilities[0]:
        ability=weak
    elif ability<=pAbilities[1]+pAbilities[0]:
        ability=casual
    else:
        ability=strong

    morality=random()
    if morality<=pMoralities[0]:
        morality="evil"
    elif morality<=pMoralities[1]+pMoralities[0]:
        morality="neutral"
    else:
        morality="hero"

    behavior=random()
    if behavior<=pBehaviors[0]:
        behavior="flee"
    elif behavior<=pBehaviors[1]+pBehaviors[0]:
        behavior="hide"
    else:
        behavior="fight"

    coldblood=random()
    if coldblood<=pColdblood[0]:
        coldblood="zen"
    elif coldblood<=pColdblood[1]+pColdblood[0]:
        coldblood="stable"
    else:
        coldblood="stressed"

    x,y=randint(2, xSize-3), randint(2, ySize-3)
    while Master.Map[x][y].content!=0:
        x,y=randint(2, xSize-3), randint(2, ySize-3)
    #x,y=x+random(),y+random()

    return(Human(Master, [x,y],ability[0], ability[1], ability[2], coldblood, morality, behavior))