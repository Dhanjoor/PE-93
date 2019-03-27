from tkinter import *
import numpy

class Visualisator(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Data
        self.x_size=0   # In cells
        self.y_size=0    # In cells
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
        # Each cell is [x,y,z] where y is noise level and z is wall/not wall

        # Load map
        self.load()
        self.plotPath([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (2, 9), (2, 8), (2, 7), (3, 7), (4, 7), (5, 7), (5, 6), (5, 5)])
        
        # Binding
        self.canvas.bind('<Button-1>',self.clic)

    def load(self):
        with open('Map/Map.txt',"r") as f:
            text=f.read()
        lines=text.split('\n')
        batis=lines[-1]
        lines=lines[0:len(lines)-1]
        self.grid=[lines[i].split(' ') for i in range(len(lines))]
        self.x_size=len(self.grid)
        self.y_size=len(self.grid[0])
        self.ppc=int(min(self.winfo_screenwidth()/self.y_size,(self.winfo_screenheight()-300)/self.x_size))
        self.canvas = Canvas(self,width=self.y_size*self.ppc,height=self.x_size*self.ppc,bg='white')
        self.timer=Label(self,width=self.ppc,text="COUCOU",font=("Arial",20))
        self.canvas.config(width=self.ppc*self.y_size,height=self.ppc*self.x_size)
        self.timer.grid(column=0)
        Button(self,text='launch',command=self.run).grid()
        self.canvas.grid(column=0)
        self.nbati=2
        for i in range (self.x_size):
            for j in range (self.y_size):
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
        self.canvas.create_rectangle(ny*self.ppc,nx*self.ppc,(ny+1)*self.ppc-1,(nx+1)*self.ppc-1,fill=color,outline=color)

    def genSound(self,x0,y0,volume):
        xMax,yMax=self.x_size,self.y_size
        if x0<0 or x0>xMax or y0<0 or y0>yMax:
            print("error")
            return
        self.grid[x0][y0][1]+=volume
        self.color(x0,y0,self.reform(round(self.grid[x0][y0][1])))
        if volume==1:
            return
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
        d=int(self.ppc/3.5)
        for oval in self.humains:
            self.canvas.delete(oval)
        self.humains=[]
        for (x,y) in L:
            px,py=int(self.ppc*x),int(self.ppc*y)
            self.humains.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#ba4a00'))

    def plotZombie(self,L):
        d=int(self.ppc/3.5)
        for oval in self.zombies:
            self.canvas.delete(oval)
        self.zombies=[]
        for (x,y) in L:
            px,py=int(self.ppc*x),int(self.ppc*y)
            self.zombies.append(self.canvas.create_oval(px-d,py-d,px+d,py+d,fill='#4a235a'))
                                                        
    def plotPath(self,path):
        for x,y in path:
            self.color(x,y,"#aff")

    def clic(self,event):
        self.genSound(int(event.y/self.ppc),int(event.x/self.ppc),5)

    def run(self):
        with open("Journal/Sauvegarde.txt","r") as f:
            text=f.read()
        turns=text.split("***\n")
        def go(t):
            Lh,Lz=[],[]
            lines=turns[t].split("\n")
            self.timer.config(text=str(t))
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
                self.genSound(int(sound[0]),int(sound[1]),int(sound[2]))
            self.plotHumain(Lh)
            self.plotZombie(Lz)
            if t<len(turns)-1:
                self.after(1000,lambda: go(t+1))
        go(0)

E=Visualisator()
E.focus_force()
E.mainloop()