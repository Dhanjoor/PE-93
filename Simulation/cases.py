from math import floor

def cases(x1,y1,x2,y2):
    if x1>x2:
        x1,y1,x2,y2=x2,y2,x1,y1 #x1<=x2

    if floor(x1)==floor(x2):
        ym,yM=min(y1,y2), max(y1,y2)
        return([(floor(x1),y) for y in range(floor(ym),floor(yM)+(1-(yM%1==0)))])
    if y1==y2:
        return([(x,floor(y1)) for x in range(floor(x1),floor(x2)+1-(x2%1==0))])

    reverse=False
    if y1>y2:
        reverse=True
        y2=2*y1-y2 #x1<x2 and y1<y2

    L=[(floor(x1),floor(y1))]

    a=(y2-y1)/(x2-x1) #y=ax +y1
    x,y=x1,y1

    if x2%1==0:
        cond1=lambda x: abs(x-x2)>10**-10 and floor(x)!=floor(x2)
    else:
        cond1=lambda x: floor(x)!=floor(x2)

    if y2%1==0:
        cond2=lambda y: abs(y-y2)>10**-10 and floor(y)!=floor(y2)
    else:
        cond2=lambda y: floor(y)!=floor(y2)

    while cond1(x) or cond2(y):
       xNew=floor(x)+1
       yNew=y+a*(xNew-x)
       if yNew<floor(y)+1: #we didnt cross the top frontier of the cell
           x,y=xNew,yNew
           L.append((xNew,floor(y)))
       else: #we crossed the top frontier of the cell
           yNew=floor(y)+1
           xNew=x+(yNew-y)/a
           x,y=xNew,yNew
           L.append((floor(xNew),y))

    if reverse:
        L=[(x,2*y1-y-1) for x,y in L]
    if x2%1==0 or y2%1==0:
        L.pop()
    return(L)
if __name__=="__main__":
    x1,y1=0,0
    x2,y2=2,3.5
    print(cases(x1,y1,x2,y2))