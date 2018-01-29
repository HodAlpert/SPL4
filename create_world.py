import sys
import os
def readFile(filename):
    filehandle = open(filename)
    for line in filehandle:
        newLine=line.split(',')
        newLine[-1]=newLine[-1].replace('\n','')
        print (newLine)
    print (filehandle.read())
    filehandle.close()




if __name__ == '__main__':
    filename = os.path.abspath(os.path.realpath(sys.argv[1]))
    readFile(filename)


