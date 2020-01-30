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
def posMatrixPrint(matrix:list, arr:list):
    for y in range(len(matrix)):
        str = ""
        for x in range(len(matrix[y])):
            c="nil"
            for entry in arr:
                if(entry[0].equal(x,y)):
                    c=entry[1]
                    break
            if(c=="nil"):c = matrix[y][x]
            else:
                str += c
                continue
            if c == "" or c == " ": str+="█"
            else: str += " "
        print(str)
