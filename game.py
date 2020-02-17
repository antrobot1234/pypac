import pygame as pg
import func
from entityClass import entity
from posClass import opp,pos
from random import  getrandbits
import numpy as np
isModel = bool(getrandbits(1))
isModel = True
if isModel:
    from tensorflow import keras
    model = keras.models.load_model("model.h5")
scaleFac = 32

win = pg.display.set_mode(((func.xMax+1)*scaleFac,(func.yMax+2)*scaleFac))
pg.display.set_caption("pac man")

clock = pg.time.Clock()
def drawSquare(surf, x, y, scale=scaleFac, size=scaleFac, color=(255, 255, 255)):
    sf = scale - size
    hsf = sf/2
    pg.draw.rect(surf,color,(x*scale+hsf,y*scale+hsf,scale-sf,scale-sf))
def drawCross(surf,x,y,scale=scaleFac,color=(255,255,255)):
    pg.draw.line(surf,color,(x*scale,y*scale),((x+1)*scale,(y+1)*scale),2)
    pg.draw.line(surf, color, ((x+1) * scale, y * scale), ((x * scale, (y + 1) * scale)),2)

def drawMap(surf,map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            c = map[y][x]
            if(c==" "):drawSquare(surf,x,y,color=(0,0,255))
            elif(c=="1"):drawSquare(surf,x,y,size=4)
            elif(c=="2"):drawSquare(surf,x,y,size=16)
            elif(c=="3" or c=="4"):drawSquare(surf,x,y,size=8,color=(100,100,100))
def readMap(map):
    i = 0
    for list in map:
        for c in list:
            if c=="1":
                i+=1
    return i
pellets = readMap(func.maze)
pac = []
ghosts = []
def getEntities(map):
    ghostNames = ["r","p","o","b"]
    i = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            c = map[y][x]
            if(c=="4"or c=="3"):
                tempGhost = entity(x,y,ghostNames[i],"x")
                tempDir = opp(tempGhost.getValid(blank=True)[0])
                tempGhost.dir = tempDir
                ghosts.append(tempGhost)
                i+=1
            elif(c=="5"):
                pac.append(entity(x,y,"y","r"))
getEntities(func.maze)
pac = pac[0]
pacWantDir = "u"
maxPow = 15
powerTimer = 0
def dev(imp):
    out = imp
    out[0] = out[0] / func.xMax
    out[1] = out[1]/ func.yMax
    return out
def toOutput():
    out = []
    out.append(dev(pac.pos.asArr()))
    for ent in ghosts:
        out.append(dev(ent.pos.asArr()))
    out = np.array(out)
    return np.expand_dims(out,0)
def fromInput(input):
    input = np.array(input[0])
    key = ["u","l","d","r"]
    l = ["r","p","o","b"]
    out = {}
    temp = np.split(input,4)
    bigI = 0
    for list in temp:
        ind = 0
        i = 0
        max = 0
        for item in list:
            if item >= max:
                max = item
                ind = i
            i+=1
        out[l[bigI]] = key[ind]
        bigI+=1
    return out
def getModelDirs():
    return fromInput(model.predict(toOutput()))
def waka(map):
    global powerTimer
    global pellets
    poc = pac.pos
    c = map[poc.y][poc.x]
    if c== "1":
        map[poc.y][poc.x] = "0"
        pellets -= 1
    if c == "2":
        map[poc.y][poc.x] = "0"
        powerTimer = maxPow
def getXY(pos,dir,offset):
    x = pos.x
    y = pos.y
    if dir=="u":y-=offset
    elif dir=="d":y+=offset
    elif dir=="l":x-=offset
    elif dir=="r":x+=offset
    return x,y
def drawPos(surf,pos,col,siz=32):
    drawSquare(surf,pos.x,pos.y,color=col,size=siz)
def drawEntity(surf,ent,col,offset=0.0):
    x,y=getXY(ent.pos,ent.dir,offset)
    drawSquare(surf,x,y,color=col)
def getCol(n,alpha = 255):
    if(n=="r"):return (255,0,0,alpha)
    elif(n=="o"):return (255,165,0,alpha)
    elif(n=="b"):return (0,170,255,alpha)
    elif (n == "p"):return (255,80,255,alpha)
def drawEntities(surf,offset=0.0):
    drawEntity(surf,pac,(255,255,0),offset)
    for ent in ghosts:
        if ent.vuln:
            col = (0, 0, 200)
        elif ent.gobbled:
            col = (100,100,100)
        else:
            col = getCol(ent.name)
        drawEntity(surf,ent,col,offset)
def drawEntityDirs(surf,showOthers=True):
    drawPos(surf,pac.pos.dirSum(pac.dir),(255,255,0),siz=4)
    if showOthers:
        for ent in ghosts:
            drawPos(surf,ent.pos.dirSum(ent.dir),getCol(ent.name),siz=4)
def drawEntityWants(surf,doDrawPos = True,doOthers=True):
    drawPos(surf,pac.pos.dirSum(pacWantDir),(255,255,0),16)
    if doOthers:
        red = None
        for ent in ghosts:
            if ent.name == "r":red = ent
        for ent in ghosts:
            col = getCol(ent.name,alpha=0)
            position = ent.getPos(pac.pos,pac.dir,red.pos)
            if doDrawPos:
                drawCross(surf,position.x,position.y,color=getCol(ent.name))
            direct = ent.getDir(position)
            drawPos(surf,ent.pos.dirSum(direct),getCol(ent.name),16)
run = True
while(run):
    clock.tick(60)
    for ent in ghosts:
        if ent.name == "r":red = ent.pos
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_x:
                pac.pacMove(pacWantDir)
                waka(func.maze)
                dirs = None
                if isModel:
                    dirs = getModelDirs()
                for ent in ghosts:
                    if(ent.turnt):ent.turnt = False
                    if powerTimer == maxPow:
                        ent.vuln = True
                        ent.turnt = True
                    elif powerTimer == 0 and ent.vuln:
                        ent.vuln = False
                        ent.turnt = True
                    if not isModel:
                        wd = None
                    else:
                        wd = dirs.get(ent.name)
                    ent.move(pac.pos,pac.dir,red,wantDir=wd)
                    if(ent.isCollide(pac)):
                        if(ent.vuln):
                            ent.vuln = False
                            ent.gobbled = True
                        elif(not ent.gobbled):
                            print("you lose!")
                            run = False

                if(powerTimer > 0):powerTimer-=1

            elif event.key == pg.K_a:
                pacWantDir = "l"
            elif event.key == pg.K_s:
                pacWantDir = "d"
            elif event.key == pg.K_d:
                pacWantDir = "r"
            elif event.key == pg.K_w:
                pacWantDir = "u"
    win.fill((0,0,0))
    drawMap(win,func.maze)
    drawEntities(win)
    drawEntityDirs(win,False)
    drawEntityWants(win,False,False)
    pg.display.update()
    if(pellets <= 0):
        print("you win!")
        run = False
pg.quit()
quit()