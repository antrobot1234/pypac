from random import randrange

from func import maze


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
        return pos(self.x * i, self.y * i)

    def flip(self, mirror):
        return pos(mirror.x - (self.x - mirror.x), mirror.y - (self.y - mirror.y))
    def equal(self,x,y):
        return self.x==x and self.y==y
    def dirSum(self,d:str):
        return self.sum(posMap.get(d))
    def __eq__(self,other):
        return self.x==other.x and self.y == other.y
    def inRange(self):
        return 0 <= self.x <= 18
    def wrap(self):
        if(self.x<0):return pos(18,self.y)
        elif(self.x>18):return pos(0,self.y)
        else:return self
    def asArr(self):
        return [self.x,self.y]

posMap = {"u": pos(0, -1), "d": pos(0, 1), "l": pos(-1, 0), "r": pos(1, 0)}

def genRandPos():
    y = randrange(1,len(maze)-1)
    x=0
    list = maze[y]
    go = True
    while go:
        x=randrange(len(list))
        if list[x]!=" ":go = False
    return pos(x, y)


def opp(d: str):
    if d == "u": return "d"
    if d == "d": return "u"
    if d == "l": return "r"
    if d == "r": return "l"
    else:return d


