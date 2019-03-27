#content : 0 rien, 1 porte, 2 mur

def genSound(x0,y0,volume):
    if x0<0 or x0>=xSize or y0<0 or y0>=ySize or carte[x0][y0].content==2:
        print("error")
        return()

    carte[x0][y0].sound+=volume
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
                if x>=0 and x<xSize and y>=0 and y<ySize and carte[x][y].content!=2 and not(visited[x-x0+volume][y-y0+volume]) and value>0.5:
                    if carte[x][y].content==1:
                        value-=attenuationPorte
                        if value<=0.5:
                            continue
                    carte[x][y].sound+=round(value)
                    visited[x-x0+volume][y-y0+volume]=True
                    new.append((x,y,value))
        suivants=new[:]


if __name__=="__main__":
    class Case():
        def __init__(self, content):
            self.sound=0
            self.content=content

        def __str__(self):
            if self.content==2:
                return("#")
            if self.content==1 and self.sound==0:
                return("|")
            if self.sound==0:
                return(".")
            return(str(self.sound))

    attenuationPorte=2
    xSize,ySize=10,10
    carte=[[Case(0) for _ in range(ySize)] for _ in range(xSize)]
    for k in range(4):
        carte[k][2].content=2
    carte[1][2].content=1
    carte[4][1].content=2

    genSound(0,0,6)
    genSound(8,8,2)
    genSound(6,7,2)

    for x in range(xSize):
        for y in range(ySize):
            print(carte[x][y], end=" ")
        print("\n")