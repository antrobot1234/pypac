import math
from random import choice

from func import maze
from posClass import pos, opp, posMap

def gmc(pos: pos)->str:
    return maze[pos.y][pos.x]

class entity:
    def __init__(self, x, y, name:str, d: str, tr=False, vl=False,gl=False):
        self.gobbled = gl
        self.pos = pos(x, y)
        self.name = name
        self.dir = d
        self.turnt = tr
        self.vuln = vl
        self.oldPos = pos
    def __str__(self):
        return self.name+":"+self.dir+" "+str(self.pos)
    def lookDist(self, pos: pos, dir: str) -> float:
        return self.pos.sum(posMap.get(dir)).distance(pos)

    def getDir(self, pos, validDirs=None,wantDir = None):
        if validDirs is None:
            validDirs = self.getValid()
        out = ""
        size = None
        if (self.vuln): return choice(validDirs)
        if wantDir != None:
            if wantDir in validDirs: return wantDir
            elif self.dir in validDirs: return self.dir
            elif(self.name == "y"): return None
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
        elif (self.name == "p"): return pacPos.sum(posMap.get(pacDir).mult(4))
        elif (self.name == "b"): return otPos.flip(pacPos.sum(posMap.get(pacDir).mult(2)))
        elif (self.name == "o"):
            if (math.sqrt(pacPos.distance(self.pos)) > 6.0):
                return pacPos
            else:
                return pos(0, 20)
        else:
            return self.pos.dirSum(self.dir)

    def getValid(self,rand=False,blank=False):
        dirs = ["u", "l", "d", "r"]
        remove = []
        if (gmc(self.pos) == "3"):
            return ["u"]
        if not rand and not blank:
            oppPos = self.pos.dirSum(opp(self.dir))
            if oppPos.inRange() and gmc(oppPos) == ' ': return [""]
        if (self.turnt): return [opp(self.dir)]
        for look in dirs:
            if self.name != "y":
                if (opp(look) == self.dir):
                    remove.append(look)
                    continue
            lookPos = self.pos.dirSum(look)
            if lookPos.inRange() and gmc(lookPos) == ' ': remove.append(look)
        out = [x for x in dirs if x not in remove]
        if len(out) == 0:
            return [opp(self.dir)]
        return out
    def step(self, pacPos: pos, pacDir:str, otPos: pos,wantDir=None):
        return self.getDir(self.getPos(pacPos,pacDir,otPos),wantDir=wantDir)
    def place(self,pos):
        self.oldPos = self.pos
        self.pos = pos
        self.dir = opp(self.getValid(blank=True)[0])
    def move(self,pacPos,pacDir,otPos,wantDir=None):
        self.oldPos = self.pos
        if not self.gobbled:
            direct = self.step(pacPos,pacDir,otPos,wantDir)
        else:
            direct = self.getDir(pos(9,8))
        self.pos = self.pos.dirSum(direct)
        self.pos = self.pos.wrap()
        self.dir = direct
        if self.gobbled:
            if self.pos == pos(9,8): self.gobbled = False
    def pacMove(self,wantDir):
        direct = self.getDir(self.pos.dirSum(wantDir),wantDir=wantDir)
        if direct != None:
            self.oldPos = self.pos
            self.pos = self.pos.dirSum(direct)
            self.pos = self.pos.wrap()
            self.dir = direct
    def isCollide(self,other):
        if(self.pos == other.pos):return True
        return self.pos == other.oldPos and self.oldPos == other.pos



def entityBuild(pos,name:str, d: str, tr=False, vl=False, ch=False,randDir = False):
    if(randDir):
        e = entity(pos.x, pos.y, name, "x", tr, vl)
        e.dir = opp(choice(e.getValid(rand=True)))
        return e;
    return entity(pos.x, pos.y, name, d, tr, vl)


