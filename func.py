import pickle
import mazeReader
import numpy as np

maze = mazeReader.read()

xMax = 18
yMax = 19
oneKey = {'u':0,'l':1,'d':2,'r':3}

def oneHot(values):
    val = [0 for x in range(16)]
    for x in range(len(values)):
        val[x*4+oneKey.get(values[x])] = 1
    return val

#from stateClass import stateHolder

def saveStateRange(r:int,s:str):
    objList = []
    i=0
    for _ in range(r):
        h = stateHolder()
        objList.append([h.inMatrix(),h.outMatrix()])
        if i%1000==0:
            print(r-i)
        i+=1
    fh = open(s,"wb")
    pickle.dump(objList,fh,protocol=4)
    fh.close()
def readStateRange(s:str):
    fh = open(s,"rb")
    obj = pickle.load(fh)
    return obj
def seperate(inList:list):
    oL = []
    oLL = []
    for entry in inList:
        oL.append(entry[0])
        oLL.append(entry[1])
    return np.array(oL),np.array(oLL)
retrain = False
if retrain:
    saveStateRange(10000,"dataout.txt")
    saveStateRange(10000,"testout.txt")
#print(readStateRange("dataout.txt")[0][1])