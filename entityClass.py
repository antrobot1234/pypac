import math
from random import choice

from func import posMap, gmc
from posClass import pos, genRandPos, opp


class entity:
    def __init__(self, x, y, name:str, d: str, tr=False, vl=False):
        self.pos = pos(x, y)
        self.name = name
        self.dir = d
        self.turnt = tr
        self.vuln = vl
    def __str__(self):
        return self.name+":"+self.dir+" "+str(self.pos)
    def lookDist(self, pos: pos, dir: str) -> float:
        return self.pos.sum(posMap.get(dir)).distance(pos)

    def getDir(self, pos, validDirs=None):
        if validDirs is None:
            validDirs = self.getValid()
        out = ""
        size = None
        if (self.vuln): return choice(validDirs)
        for look in validDirs:
            if size is None:
                size = self.lookDist(pos, look)
                out = look
                continue
            elif size > self.lookDist(pos, look):
                size = self.lookDist(pos, look)
                out = look
        return out

    def getPos(self, pacPos: pos, pacDir: str, otPos: pos) -> pos:
        if (self.name == "r"): return pacPos
        if (self.name == "p"): return pacPos.sum(posMap.get(pacDir).mult(4))
        if (self.name == "b"): return otPos.flip(pacPos.sum(posMap.get(pacDir).mult(2)))
        if (self.name == "o"):
            if (math.sqrt(pacPos.distance(self.pos)) > 8.0):
                return pacPos
            else:
                return pos(0, 20)
        else:
            return self.pos.dirSum(self.dir)

    def getValid(self,rand=False):
        dirs = ["u", "l", "d", "r"]
        remove = []
        if (gmc(self.pos) == "3"):
            return ["u"]
        if not rand:
            oppPos = self.pos.dirSum(opp(self.dir))
            if oppPos.inRange() and gmc(oppPos) == ' ': return [""]
        if (self.turnt): return [opp(self.dir)]
        for look in dirs:
            if (opp(look) == self.dir):
                remove.append(look)
                continue
            lookPos = self.pos.dirSum(look)
            if lookPos.inRange() and gmc(lookPos) == ' ': remove.append(look)
        out = [x for x in dirs if x not in remove]
        if len(out) == 0:
            return [opp(self.dir)]
        return out
    def step(self, pacPos: pos, pacDir:str, otPos: pos):
        return self.getDir(self.getPos(pacPos,pacDir,otPos),self.getValid())


def entityBuild(pos,name:str, d: str, tr=False, vl=False, ch=False,randDir = False):
    if(randDir):
        e = entity(pos.x, pos.y, name, "x", tr, vl)
        e.dir = opp(choice(e.getValid(rand=True)))
        return e;
    return entity(pos.x, pos.y, name, d, tr, vl)


def genRandEntities():
    nameList = ["r","p","o","b"]
    objList = []
    objList.append(entityBuild(genRandPos(), "y", "x", randDir=True))
    for name in nameList:
        exit = False
        pos = None
        while not exit:
            pos = genRandPos()
            if(pos!=objList[0].pos):exit=True
        objList.append(entityBuild(pos, name, "x", randDir=True))
    return objList