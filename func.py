import math as m

import mazeReader
from random import choice
import math

maze = mazeReader.read()


class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "{" + str(self.x) + "," + str(self.y) + "}"

    def distance(self, other):
        return (abs(other.x - self.x) ** 2) + (abs(other.y - self.y) ** 2)

    def sum(self, other):
        return pos(self.x + other.x, self.y + other.y)

    def mult(self, i: int):
        return pos(self.x * i.x, self.y * i)

    def flip(self, mirror):
        return pos(mirror.x - (self.x - mirror.x), mirror.y - (self.y - mirror.y))
    def equal(self,other):
        return self.x==other.x and self.y==other.y


posMap = {"u": pos(0, -1), "d": pos(0, 1), "l": pos(-1, 0), "r": pos(1, 0)}


def gmc(pos: pos):
    return maze[pos.y][pos.x]


def opp(dir: str):
    if dir == "u": return "d"
    if dir == "d": return "u"
    if dir == "l": return "r"
    if dir == "r": return "l"


class entity:
    def __init__(self, x, y, n, d: str, tr: bool, vl: bool, ch: bool):
        self.pos = pos(x, y)
        self.name = n
        self.dir = d
        self.turnt = tr
        self.vuln = vl
        self.chomped = False

    def lookDist(self, pos: pos, dir: str) -> float:
        return self.pos.sum(posMap.get(dir)).distance(pos)

    def getDir(self, pos: pos, validDirs: list):
        out = ""
        size = None
        if (self.vuln): return choice(list)
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
        if (self.name == "b"): return otPos.flip(pacPos.sum(posMap.get(pacDir).pacPos.mult(2)))
        if (self.name == "o"):
            if (math.sqrt(pacPos.distance(self.pos)) > 8.0):
                return pacPos
            else:
                return pos(0, 20)
        else:
            return self.pos.sum(posMap.get(self.dir))

    def getValid(self):
        dirs = ["u", "l", "d", "r"]
        remove = []
        if gmc(self.pos.sum(posMap.get(opp(self.dir)))) == ' ': return [""]
        if (self.turnt): return [].append(opp(self.dir))
        for look in dirs:
            if (opp(look) == self.dir):
                remove.append(look)
                continue
            if gmc(self.pos.sum(posMap.get(look))) == ' ': remove.append(look)
        return [x for x in dirs if x not in remove]


class state:
    def __init(self, list):
        self.entities = list

    def validate(self) -> bool:
        e: entity
        for e in self.entities:
            if gmc(e.pos) == " ": return False
            if(e.turnt and not e.vuln):return False
            if e.type=="y":
                for e2 in [x for x in self.entities if x != e]:
                    if e.pos.equal(e2.pos):return False