from tkinter import *
import numpy
from Parameters import *

class Visualisator(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Data
        self.ppc=0         # pixel per cell
        self.onclic='w'    # what to do when the user clic on a cell
        self.nclic = 1     # first or second clic for a new wall of line
        self.firstcase = (0,0)     # first clic for a wall of line
        self.grid=[]
        self.canvas=0
        self.timer = 0
        self.nbati=1
        self.batiments=[]
        self.humains=[]
        self.zombies=[]
        self.vitesse_affichage=100
        # Each cell is [x,y,z] where y is noise level and z is wall/not wall

        # Load map
        self.load()

        # Binding
        self.canvas.bind('<Button-1>',self.clic)

    def load(self):
        with open(mapTxt,"r") as f:
            text=f.read()
        lines=text.split('\n')
        batis=lines[-1]
        lines=lines[0:len(lines)-1]
        self.grid=[lines[i].split(' ') for i in range(len(lines))]
        self.ppc=int(min(self.winfo_screenwidth()/ySize,(self.winfo_screenheight()-300)/xSize))
        self.canvas = Canvas(self,width=ySize*self.ppc,height=xSize*self.ppc,bg='white')
        self.timer=Label(self,width=self.ppc,text="Coucou !",font=("Arial",20))
        self.sheet1=Label(self,width=self.ppc,text="Humains ",font=("Arial",12))
        self.sheet2=Label(self,width=self.ppc,text="Zombies ",font=("Arial",12))
        self.canvas.config(width=self.ppc*ySize,height=self.ppc*xSize)
        self.timer.grid(column=0)
        self.sheet1.grid(column=0)
        self.sheet2.grid(column=0)
        self.button=Button(self,text='Ça part',command=self.run).grid()
        self.canvas.grid(column=0)
        self.nbati=2
        for i in range (xSize):
            for j in range (ySize):
                self.grid[i][j]=self.grid[i][j].split('/')
                for k in range (len(self.grid[i][j])):
                    self.grid[i][j][k]=int(self.grid[i][j][k])
                if self.grid[i][j][2]==1:
                    self.color(i,j,'black')
                elif self.grid[i][j][2]==2:
                    self.color(i,j,'blue')
                elif self.grid[i][j][2]==3:
                    self.color(i,j,'yellow')
                elif self.grid[i][j][2]==4:
                    self.color(i,j,'green')
        batims=batis.split(' ')
        self.batiments=([b.split('/') for b in batims])

    def color(self,nx,ny,color):
        #inversion of x/y by Tkinter
        self.canvas.create_rectangle(ny*self.ppc,nx*self.ppc,(ny+1)*self.ppc-1,(nx+1)*self.ppc-1,fill=color,outline=color)

    def genSound(self,x0,y0,volume):
        xMax,yMax=xSize,ySize

        if x0<0 or x0>xMax or y0<0 or y0>yMax:
            print("genSound error")
            return()

        self.grid[x0][y0][1]+=volume
        self.color(x0,y0,self.reform(round(self.grid[x0][y0][1])))
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
                    if x>=0 and x<xMax and y>=0 and y<yMax and (self.grid[x][y][2]==0 or self.grid[x][y][2]==2)  and not(visited[x-x0+volume][y-y0+volume]) and value>0:
                        self.grid[x][y][1]+=round(value)
                        visited[x-x0+volume][y-y0+volume]=True
                        self.color(x,y,self.reform(self.grid[x][y][1]))
                        new.append((x,y,value))
            suivants=new[:]

    def reform(self,n):
        #num=int(500/numpy.pi*numpy.arctan(0.5*n))
        num=int(250*(1-numpy.exp(-n/5)))
        txt=hex(255-num)[2:]
        if len(txt)==1:
            txt='0'+txt
        return('#ff'+txt+txt)

    def plotHumain(self,L):
        d=int(self.ppc/3)
        for oval in self.humains:
            self.canvas.delete(oval)
        self.humains=[]
        for (x,y) in L:
            px,py=int(self.ppc*y),int(self.ppc*x) #inversion of x/y by Tkinter
            self.humains.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#ba4a00'))

    def plotZombie(self,L):
        d=int(self.ppc/4)
        for oval in self.zombies:
            self.canvas.delete(oval)
        self.zombies=[]
        for (x,y) in L:
            px,py=int(self.ppc*y),int(self.ppc*x) #inversion of x/y by Tkinter
            self.zombies.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#4a235a'))

    def plotPath(self,path):
        for x,y in path:
            self.color(x,y,"#aff")

    def clic(self,event):
        #inversion of x/y by Tkinter
        self.genSound(int(event.y/self.ppc),int(event.x/self.ppc),5)

    def run(self):
        with open(journalTxt,"r") as f:
            text=f.read()
        turns=text.split("***\n")
        def go(t):
            #reduce volume after a turn
            for x in range(xSize):
                for y in range(ySize):
                    if self.grid[x][y][1]>0:
                        self.grid[x][y][1]-=1
                        self.color(x,y,self.reform(self.grid[x][y][1]))

            Lh,Lz=[],[]
            lines=turns[t].split("\n")
            self.timer.config(text="Tour "+str(t+1))
            self.sheet1.config(text="Humains : {}".format(len(self.humains)))
            self.sheet2.config(text="Zombies : {}".format(len(self.zombies)))
            debut,fin=1,int(lines[0])+1
            for i in range(debut,fin):
                humain=lines[i].split("/")
                Lh.append((float(humain[0]),float(humain[1])))
            debut,fin=fin+1,fin+1+int(lines[fin])
            for i in range(debut,fin):
                zombie=lines[i].split("/")
                Lz.append((float(zombie[0]),float(zombie[1])))
            debut,fin=fin+1,fin+1+int(lines[fin])
            for i in range(debut,fin):
                sound=lines[i].split("/")
                self.genSound(int(sound[0]),int(sound[1]),int(sound[2])) #inversion of x/y by Tkinter
            self.plotHumain(Lh)
            self.plotZombie(Lz)
            if t<len(turns)-1:
                self.after(self.vitesse_affichage,lambda: go(t+1))
            else:
                self.timer.config(text="C'est fini !")
        go(0)

#Change the first value in self.after (line 162) to fix the time between each turn of the simulation
E=Visualisator()
E.focus_force()
E.mainloop()
