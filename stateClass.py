import numpy as np

from entityClass import genRandEntities, entity
from func import gmc, xMax, yMax, oneHot


class state:
    def __init__(self, l=None):
        if(l==None):l = genRandEntities()
        self.entities = l

    def validate(self) -> bool:
        e: entity
        for e in self.entities:
            if gmc(e.pos) == " ": return False
            if(e.turnt and not e.vuln):return False
            if e.name=="y":
                for e2 in [x for x in self.entities if x != e]:
                    if e.pos==e2.pos:return False
        return True
    def getInput(self):
        out = []
        for entity in self.entities:
            out.append([entity.name,entity.pos])
        return out
    def step(self):
        out = []
        e: entity
        for e in self.entities:
            if(e.name=="y"):self.pac = e
            if(e.name=="b"):self.blue = e
        for e in self.entities:
            out.append([e.name,e.step(self.pac.pos,self.pac.dir,self.blue.pos)])
        return out


class stateHolder:
    def __init__(self,s=None):
        if(s==None):s= state()
        self.input = {}
        for entity in s.entities:
            self.input[entity.name] = entity.pos
        self.output = {}
        step = s.step()
        for entry in step:
            if entry[0] != 'y':
                self.output[entry[0]] = entry[1]
    def __str__(self):
        out = ""
        for key in self.input.keys():
            out+= key+":"+str(self.input[key])+"|"
        out += "["
        for key in self.output.keys():
            out+= key+":"+self.output[key]+"|"
        out +="]"
        return out
    def inMatrix(self):
        val = []
        for x in self.input.values():
            position = x.asArr()
            position[0] /= xMax
            position[1] /= yMax
            val.append(position)
        return val
    def outMatrix(self):
        val = []
        for x in self.output.values():
            val.append(x)
        return np.array(oneHot(val))