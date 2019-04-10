from tkinter import *

def line(x1,y1,x2,y2):

    if x1==x2:
        y1,y2=min(y1,y2),max(y1,y2)
        return([(x1, y) for y in range(y1, y2+1)])
    if y1==y2:
        x1,x2=min(x1,x2),max(x1,x2)
        return([(x, y1) for x in range(x1, x2+1)])

    L=[(x1,y1)]
    x,y=x1,y1
    dx=(x2-x1)//abs(x2-x1)
    inverse=False
    if y2<y1:
        y2=y1+abs(y2-y1)
        inverse=True
    a=(y2-y1)/(x2-x1)
    while x!=x2 or y!=y2:
        if y<=a*(x-x1)+y1:
            y+=1
        else:
            x+=dx
        L.append((x,y))
    if inverse:
        for i in range(len(L)):
            x,y=L[i]
            L[i]=(x,y1-(y-y1))
    return(L)



class Map_editor(Tk):
    def __init__(self):
        Tk.__init__(self)

        # Data
        self.x_size=10    # In cells
        self.y_size=10    # In cells
        self.ppc=int(min((self.winfo_screenwidth()-300)/self.y_size,self.winfo_screenheight()/self.x_size))
        self.onclic='w'    # w : wall, wl : line of wall, b : building, f : food, r : rest
        self.nclic = 1     # first or second clic for a new wall of line
        self.firstcase = (0,0)     # first clic for a wall of line
        self.grid=[[[0,0,0] for _ in range (self.y_size)] for _ in range (self.x_size)]
        self.nbati=1
        self.batiments=[]    # each building is [[topLeftCornerX,topLeftCornerY,bottomRightCornerX,bottomRightCornerY],nbCaseFood,nbCaseRepos,[(porteXi,porteYi)]]
        # Each cell is [x,y,z] where y is noise level and z is wall/not wall

        #Canvas
        self.canvas = Canvas(self,width=self.y_size*self.ppc,height=self.x_size*self.ppc,bg='white')
        self.canvas.grid(row=0,column=0,rowspan=10)

        #Save/Open
        self.frame1 = Frame(self)
        self.filename_label = Label(self.frame1,text='Nom de la carte (no file extension)')
        self.filename_entry = Entry(self.frame1)
        self.frame2 = Frame(self)
        self.finish_button = Button(self.frame2,text='Sauvegarder',command=self.finish)
        self.open_button = Button(self.frame2,text='Ouvrir',command=self.load)
        self.clear_button = Button(self.frame2,text='Nettoyer',command=self.clear)
        self.frame3 = Frame(self)
        self.onclic_label = Label(self.frame3,text='Cliquer pour ajouter un mur')
        self.onclicwall_button = Button(self.frame3,text='Mur au clic',command=lambda: self.setclic('w'))
        self.onclicline_button = Button(self.frame3,text='Ligne au clic',command=lambda: self.setclic('wl'))
        self.onclicbuild_button = Button(self.frame3,text='Batiment au clic',command=lambda: self.setclic('b'))
        self.onclicfood_button = Button(self.frame3,text='Zone food au clic',command=lambda: self.setclic('f'))
        self.onclicrest_button = Button(self.frame3,text='Zone repos au clic',command=lambda: self.setclic('r'))
        self.onclicclear_button= Button(self.frame3,text='Nettoyerbis au clic',command=lambda: self.setclic('clb'))

        #Layout
        self.frame1.grid(row=0,column=1)
        self.filename_label.grid(row=0,column=0)
        self.filename_entry.grid(row=1,column=0)

        self.frame2.grid(row=1,column=1)
        self.finish_button.grid(row=0,column=0)
        self.open_button.grid(row=1,column=0)
        self.clear_button.grid(row=2,column=0)

        self.frame3.grid(row=2,column=1)
        Label(self.frame3,text='------').grid(row=0,column=0)
        self.onclic_label.grid(row=1,column=0)
        self.onclicwall_button.grid(row=2,column=0)
        self.onclicline_button.grid(row=3,column=0)
        self.onclicbuild_button.grid(row=4,column=0)
        self.onclicfood_button.grid(row=5,column=0)
        self.onclicrest_button.grid(row=6,column=0)
        self.onclicclear_button.grid(row=7,column=0)

        # Binding
        self.canvas.bind('<Button-1>',self.clic)
        self.canvas.bind('<Button-3>',self.rclic)
        self.bind('Escape',self.leave)

    def clic(self,event):
        nx,ny=event.x//self.ppc,event.y//self.ppc
        if self.onclic == 'w':
            self.add_wall(ny,nx)
        elif self.onclic == 'wl':
            if self.nclic == 1:
                self.firstcase = (ny,nx)
                self.color(ny,nx,"grey")
                self.nclic+=1
            else:
                self.add_line(self.firstcase[0],self.firstcase[1],ny,nx)
                self.nclic-=1
        elif self.onclic == 'b':
            if self.nclic == 1 and self.isInBati(nx,ny) == -1:
                self.firstcase = (ny,nx)
                self.color(ny,nx,"grey")
                self.nclic+=1
            elif self.nclic == 2 and self.isInBati(nx,ny) == -1:
                self.add_build(self.firstcase[0],self.firstcase[1],ny,nx)
                self.nclic+=1
            else:
                self.adddoor(ny,nx)
        elif self.onclic == 'f':            # food zone on cilc
            i=self.isInBati(ny,nx)
            if i != -1:
                self.grid[ny][nx][2]=3
                self.grid[ny][nx][0]=i
                self.color(ny,nx,'yellow')
                self.batiments[i][1]+=1
        elif self.onclic == 'r':            # rest zone on cilc
            i=self.isInBati(ny,nx)
            if i != -1:
                self.grid[ny][nx][2]=4
                self.grid[ny][nx][0]=i
                self.color(ny,nx,'green')
                self.batiments[i][2]+=1
        elif self.onclic == 'clb':
            self.grid[ny][nx][2]=0
            self.color(ny,nx,'white')

    def rclic(self,event):
        self.nclic = 1
        self.nbati += 1

    def add_line(self,nx1,ny1,nx2,ny2):
        L=line(nx1,ny1,nx2,ny2)
        for case in L:
            self.add_wall(case[0],case[1])

    def add_wall(self,nx,ny):
        self.grid[nx][ny][2]=1
        self.color(nx,ny,'black')

    def add_wallinbati(self,nx,ny):
        self.grid[nx][ny][2]=1
        self.grid[nx][ny][0]=self.nbati
        self.color(nx,ny,'black')

    def adddoor(self,nx,ny):
        if self.grid[nx][ny][0] == self.nbati:
            self.grid[nx][ny][2]=2
            self.color(nx,ny,'blue')
        self.batiments[self.nbati-1][3].append((nx,ny))

    def add_build(self,nx1,ny1,nx2,ny2):
        for nx in range (min(nx1,nx2),max(nx1,nx2)+1):
            self.add_wallinbati(nx,min(ny1,ny2))
            self.add_wallinbati(nx,max(ny1,ny2))
        for ny in range (min(ny1,ny2),max(ny1,ny2)+1):
            self.add_wallinbati(min(nx1,nx2),ny)
            self.add_wallinbati(max(nx1,nx2),ny)
        self.batiments.append([[nx1,ny1,nx2,ny2],0,0,[]])

    def isInBati(self,x,y):
        for i in range(len(self.batiments)):
            [l,a,b,c]=self.batiments[i]
            x1,y1,x2,y2=l
            if (x1<=x) and (x<=x2) and  (y1<=y) and (y<=y2):
                return i
        return -1

    def color(self,nx,ny,color):
        self.canvas.create_rectangle(ny*self.ppc,nx*self.ppc,(ny+1)*self.ppc-1,(nx+1)*self.ppc-1,fill=color,outline=color)

    def finish(self):
        filename='Map/'+self.filename_entry.get()
        if filename != '':
            g=self.grid
            with open(filename+'.txt',"w") as f:
                for i in range(len(g)):
                    for j in range(len(g[0])-1):
                        f.write(str(g[i][j][0])+'/'+str(g[i][j][1])+'/'+str(g[i][j][2])+' ')
                    f.write(str(g[i][len(g[0])-1][0])+'/'+str(g[i][len(g[0])-1][1])+'/'+str(g[i][len(g[0])-1][2])+'\n')
                for i in range (len(self.batiments)):
                    lw,nf,nb,ld=self.batiments[i]
                    txt=str(lw[0])+"_"+str(lw[1])+"-"+str(lw[2])+"_"+str(lw[3])+"/"+str(nf)+"/"+str(nb)+"/"
                    for (x,y) in ld:
                        txt=txt+str(x)+"_"+str(y)+"-"
                    txt=txt[0:-1]
                    f.write(txt)
                    if i!=len(self.batiments)-1:
                        f.write(' ')

    def load(self):
        filename='Map/'+self.filename_entry.get()
        try:
            with open(filename+'.txt',"r") as f:
                text=f.read()
            lines=text.split('\n')
            batis=lines[-1]
            lines=lines[0:len(lines)-1]
            self.grid=[lines[i].split(' ') for i in range(len(lines))]
            self.canvas.delete("all")
            self.canvas.config(width=self.ppc*len(self.grid[0]),height=self.ppc*len(self.grid))
            self.nbati=1
            for i in range (len(self.grid)):
                for j in range (len(self.grid[0])):
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
            self.batiments=[b.split('/') for b in batims]
        except:
            pass

    def clear(self):
        self.grid=[[[0,0,0] for _ in range (self.y_size)] for _ in range (self.x_size)]
        self.nclic=1
        self.onclic = 'w'    # wl for wall line
        self.onclic_label.config(text='Cliquer pour ajouter un mur')
        self.canvas.delete("all")
        self.batiments=[]

    def setclic(self,txt):  # change from one wall per clic to a line of wall per two clics
        self.nclic=1
        if txt == 'w':
            self.onclic = 'w'
            self.onclic_label.config(text='Cliquer pour ajouter un mur')
        elif txt == 'wl':
            self.onclic = 'wl'
            self.onclic_label.config(text='Cliquer deux fois pour \n une ligne de murs')
        elif txt == 'b':
            self.onclic = 'b'
            self.onclic_label.config(text='Cliquer deux fois pour \n un batiment, puis une \n fois pour la porte, \n puis clic droit')
        elif txt == 'f':
            self.onclic = 'f'
            self.onclic_label.config(text='Cliquer pour ajouter \n une case nourriture')
        elif txt == 'clb':
            self.onclic = 'clb'
            self.onclic_label.config(text='Cliquer pour nettoyer un point')
        if txt == 'r':
            self.onclic = 'r'
            self.onclic_label.config(text='Cliquer pour ajouter \n une zone de repos')

    def leave(self,event):
        self.destroy()

#Adapt xsize and ysize in Map_editor class init (line 39) to the size of the map you want to make
E=Map_editor()
E.focus_force()
E.mainloop()