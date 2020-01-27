def read():
    file = open("maze.txt","r")
    list = file.readlines()
    out = []
    for string in list:
        out.append([char for char in string if char!="\n"])
    return out
def matrixPrint(matrix):
    for l in matrix:
        str = ""
        for c in l:
            if c == "" or c == " ": str+="█"
            else: str += " "
        print(str)