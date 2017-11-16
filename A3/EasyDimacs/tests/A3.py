#WalkSat

"""To Do:

-Parse a file


To hold info after parse:

-vArr (An array to hold the boolean of each variable:
    vArr[1]=1 means x_1 is true

-cArr (An array to hold clauses)
    cArr[3]=[-1,3,4,-5]

-tCls (Array for currently true clauses)
    -numT (Array of variable in all of the true clauses)
         [0,3,0,4,2,1,0,1,5]
         Each variable is an int representing number of
         occurences in all clauses
-fCls (Array for currently false clauses)
    -numF (same as above, for false)

Pseudo:

Parse file
Assign random values to variables
Check each clause and push into corresponding T-F array
While fCls is not empty
    Some probability of picking random variable flip
    (from false clause variables)
    Else:
        if numT contains a 0 (at least one variable doesn't
                              occur in any currently true clauses)
            Flip first variable not in numT
            Check false clauses
            Transfer newly true clauses
        else:
            Flip var with min in numT and max in numF (max difference?)
            Check all clauses
            Sort
"""

import random,time

"""Parses file and returns two lists containing variable states
    and clauses"""
def parseFile(fileName):
    fin = open(fileName,'r')
    line = fin.readline()
    line = line.split()
    numVars = int(line[2])
    numClau = int(line[3])
    vArr = initVars(numVars)
    cArr = []
    for line in fin:
        lArr = line.split()
        if lArr[0] == 'c':
            break
        cls = []
        for i in range(len(lArr)-1):
            cls.append(int(lArr[i]))
        cArr.append(cls)
    return (vArr,cArr)

"""Helper function to randomize variables"""
def initVars(numVars):
    Vars = []
    for i in range(numVars):
        Vars.append(random.randint(0,1))
    return Vars

"""Performs walksat on given file"""
def WalkSat():

    #Get variables and clauses
    vArr,cArr = parseFile('10.40.160707067.cnf')

    #init and fill true and false clause arrays
    tCls,fCls = checkAll(vArr,cArr) 

    print("vars = ",vArr)
    print("tCls")
    for i in tCls:
        print(i)
    print("fCls")
    for i in fCls:
        print(i)

    #Collect variable occurences and differences
    numT,numF,diff = getOcc(tCls,fCls,len(vArr))

    print("numT = ",numT)
    print("numF = ",numF)
    print("diff = ",diff)

    while(len(fCLs)>0):
        if 0 in numT:
            print("0 occured. restart.")
            return
        else:
            if vArr[(diff.index(max(diff))+1)] == 1:
                vArr[(diff.index(max(diff))+1)] -= 1
            else:
                vArr[(diff.index(max(diff))+1)] += 1

            tCls,fCls = checkAll(vArr,cArr)

"""Function to check all clauses"""
def checkAll(vArr,cArr):
    tCls = []
    fCls = []
    for i in cArr:
        if(testClause(vArr,i)):
            tCls.append(i)
        else:
            fCls.append(i)
    return(tCls,fCls)

"""Helper function to test truth of clauses"""
def testClause(vArr,clause):

    for i in clause:
        #If both true or both false
        if ((i<0)&(~vArr[abs(i)-1]))|((i>0)&(vArr[abs(i)-1])):
            return(True)
    #If all conflicting
    return(False)

"""Gets the number of occurences of variables in the sets of
    true and false clauses. Also the respective differences"""
def getOcc(tCls,fCls,numVars):
    numT = [0 for x in range(numVars)]
    numF = [0 for x in range(numVars)]
    diff = [0 for x in range(numVars)]

    for i in tCls:
        for j in i:
            numT[abs(j)-1] += 1
    for i in fCls:
        for j in i:
            numF[abs(j)-1] += 1

    for i in range(len(diff)):
        diff[i] = numF[i] - numT[i]

    return (numT,numF,diff)
    

def main():
    startTime = time.time()
    WalkSat()
    print("Execution time: ",time.time()-startTime," seconds.")

main()
