class Building():
    def __init__(self,x1,y1,x2,y2,nFood,nRest,doors):
        self.corners=[x1,y1,x2,y2]
        self.nFoodCells=nFood
        self.nRestCells=nRest
        self.doors=doors

    def affiche(self):
        print("corners:",self.corners[0],self.corners[1])
        print("number of food cells:",self.nFoodCells)
        print("number of rest cells:", self.nRestCells)
        print(str(len(self.doors))+" doors:")
        for k in range(len(self.doors)):
            print(str(k+1)+":", self.doors[k])

if __name__=="__main__":
    b=Building(0,1,3,3,1,0,[(0,1), (1,1)])
    b.affiche()