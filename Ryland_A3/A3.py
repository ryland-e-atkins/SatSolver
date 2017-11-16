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
#For genetic alg
import Queue as q
#sys.path.append("/home/ryland/Desktop/A3/EasyDimacs/tests/")

"""Parses file and returns two lists containing variable states
    and clauses"""
def parseFile(fileName):
    fin = open(fileName,'r')
    line = fin.readline()
    line = line.split()
    while line[0] == 'c':
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
    fin.close()
    return (vArr,cArr)

"""Helper function to randomize variables"""
def initVars(numVars):
    Vars = []
    for i in range(numVars):
        Vars.append(random.randint(0,1))
    return Vars

"""Performs walksat on given file"""
def RunSat(model,clauses,p,maxFlips):
    
    for i in range(maxFlips):
        #check number of false clauses
        if (len(checkAll(model,clauses)[1])<0):
            print "False occs: ",getOcc(checkAll(model,clauses)[0],checkAll(model,clauses)[1],len(model))[1]
            print("trying",i,len(checkAll(model,clauses)[1]))
            GeneticSat(model,clauses,p,maxFlips-i)
        if(checkModel(model,clauses)):
            print("Number of Flips:",i)
            return (True,model)
        fClauses = checkAll(model,clauses)[1]
        rand = random.randint(0,len(fClauses)-1)
        clause = clauses[rand]
        rand = random.randint(1,100)/100.0
        if rand < p:
            rand = random.randint(0,len(clause)-1)
            flipOne(model,abs(clause[rand])-1)
        else:
            #count number of satisfied clauses if each variable flipped
            
            #each item in this list corresponds to the number of true clauses that exist if that variable is flipped.
            truNumClauseArr = []
            tempModel = []
            #for every possible flip
            for u in range(len(model)):
                #create a deep copy of array
                for b in model:
                    tempModel.append(b)
                #flip a variable
                flipOne(tempModel,u)
                #add number of flips to truNumArr
                
                truNumClauseArr.append(len(checkAll(tempModel,clauses)[0]))
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                """getOcc(checkAll(tempModel,clauses)[0],checkAll(tempModel,clauses)[1],len(model))[1]"""
                
                """This gives the array that holds number of occurences in false clauses."""
                
                """I want to flip (randomly) one of the non-zero variables in this list."""
                
                
                
                
                
                
                
                
                
                
                
                
                
            #randomly pick one the max occurences
            #store the idexes of the max occurences in an array
            #pick one
            indexArray = []
            maxi = max(truNumClauseArr)
            for m in truNumClauseArr:
                if m == maxi:
                    indexArray.append(truNumClauseArr.index(m))
                    truNumClauseArr.remove(m)
            #find the max of truNumArr and use the index to flip the corresponding model variable 
            print "truNumClauseArr",truNumClauseArr
            print truNumClauseArr.index(max(truNumClauseArr))
            print max(truNumClauseArr)
            
            flipOne(model,truNumClauseArr.index(max(truNumClauseArr)))
    return (False,len(checkAll(model,clauses)[0]))

def WalkSat(model,clauses,p,maxFlips):
    
    for i in range(maxFlips):   
        if(checkModel(model,clauses)):
            print("Number of Flips:",i)
            return (True,model)
        fClauses = checkAll(model,clauses)[1]
        rand = random.randint(0,len(fClauses)-1)
        clause = clauses[rand]
        rand = random.randint(1,100)/100.0
        if rand < p:
            rand = random.randint(0,len(clause)-1)
            flipOne(model,abs(clause[rand])-1)
        else:
            #count number of satisfied clauses if each variable flipped
            truNumArr = []
            tempModel = [0 for x in range(len(model))]
            #for every possible flip
            for u in range(len(tempModel)):
                #create a deep copy of array
                for b in range(len(model)):
                    tempModel[b] = model[b]
                #flip a variable
                flipOne(tempModel,u)
                #add number of flips to truNumArr
                truNumArr.append(len(checkAll(tempModel,clauses)[0]))
            #find the max of truNumArr and use the index to flip the corresponding model variable 
            flipOne(model,truNumArr.index(max(truNumArr)))
    return (False,len(checkAll(model,clauses)[0]))

def flipOne(arr,index):
    if arr[index] == 0:
        arr[index] = 1
    else:
        arr[index] = 0

def flip(locale):
    if locale == 0:
        return 1
    else:
        return 0

def checkModel(model,clauses):
    for i in clauses:
        if(testClause(model,i)==False):
            return False
    return True
 
"""So this was my first attempt at WalkSat... It works for the smaller files, but
    when you move to the larger files it never completes. Hence the name. Even after 30 minutes.
    Soooo.. I took a look back at WalkSat and the pseudo for it, rewrote it, and it 
    works. This is also why I have some very awkward calls in the ActualWalkSat 
    function; they were left over from this attempt."""           
def CrawlSat(fileName):

    #Get variables and clauses
    vArr,cArr = parseFile(fileName)

    #init and fill true and false clause arrays
    tCls,fCls = checkAll(vArr,cArr) 

    print("vars = ",vArr)
    print("Initial clauses:")
    print("True Clauses:")
    for i in tCls:
        print(i)
    print("False Clauses:")
    for i in fCls:
        print(i)

    #Collect variable occurences and differences
    numT,numF,diff = getOcc(tCls,fCls,len(vArr))

    print("numT = ",numT)
    print("numF = ",numF)
    print("diff = ",diff)

    
    while(len(fCls)>0): 
        #Determine random probability
        rand = random.randint(0,1000)
        #flip random
        if rand == 47:
            print "working..."
            ind = random.randint(0,len(vArr)-1)
            #flip it
            if vArr[ind] == 1:
                vArr[ind] = 0
            elif vArr[ind] == 0:
                vArr[ind] = 1
            tCls,fCls = checkAll(vArr,cArr)
        
        else:
            if 0 in numT:
                #flip first variable not in numT
                if vArr[numT.index(0)] == 1:
                    vArr[numT.index(0)] = 0
                else:
                    vArr[numT.index(0)] = 1
                    
                tCls,fCls = checkAll(vArr,cArr)
            else:
                if vArr[diff.index(max(diff))] == 1:
                    vArr[diff.index(max(diff))] = 0
                else:
                    vArr[diff.index(max(diff))] = 1

                tCls,fCls = checkAll(vArr,cArr)
        #print("fCls")
        #for i in fCls:
        #    print(i)
    return(vArr)

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
    
def GeneticSat(model,clauses,p,maxFlips):
    
    #define initial population (# of sets of variables) Should probably be even number
    #Each geneSet has its own set of variables and clauses
    numPop = 40
    geneSetList = []
    #deep copy clauses, leave model the same and let mutation take care of differentiation
    for i in range(numPop):
        
        #for j in model:
        #    passModel = initVars(len(model))
        passClauses = []
        for j in clauses:
            newClause = []
            for k in j:
                newClause.append(k)
            passClauses.append(newClause)
        geneSetList.append(geneSet(model,passClauses))
    geneQ = q.PriorityQueue()
      
    for i in range(maxFlips):
        #print i
        #Compare fitness, que things
        for g in geneSetList:
            fit = g.getFitness()
            geneQ.put_nowait((fit,g))
            
        #Crossbreed each pair
        for i in range(numPop/2):
            first = geneQ.get_nowait()[1]
            fMod = first.getModel()
            second = geneQ.get_nowait()[1]
            sMod = second.getModel()
            
            #Cut up selection and cross-over
            for j in range(int(0.2*numPop)):
                temp = fMod[j]
                fMod[j] = sMod[j]
                sMod[j] = temp
                 
            #Put back in     
            first.setModel(fMod)
            second.setModel(sMod)
            
            #Check for viability
            if (first.isFin()):
                print("Number of Flips:",i)
                return (True,first.getModel())
            if (second.isFin()):
                print("Number of Flips:",i)
                return (True,second.getModel())
            
            #Not viable, Mutate with probability p
            FnS = [first,second]
            for k in FnS:
                rand = random.randint(1,100)/100.0
                if rand < p:
                    ind = random.randint(0,len(k.getModel())-1)
                    k.getModel()[ind] = flip(k.getModel()[ind])
    for g in geneSetList:
        fit = g.getFitness()
        geneQ.put_nowait((fit,g))
    best = geneQ.get_nowait()[1]   
    print("Failure. Closest model: ",best.getModel())   
    return (False,best.getModel())

        
"""Each geneSet contains its own copy of everything."""
class geneSet():
    
    def __init__(self,model,clauses):
        self.model,self.clauses = model,clauses
        
    def getFitness(self):
        #lower is better
        #number of false clauses/number of total clauses
        fitness = len(checkAll(self.model,self.clauses)[1])/len(self.clauses)
        return fitness
    
    def getModel(self):
        return self.model
    
    def setModel(self,newModel):
        for i in range(len(newModel)):
            self.model[i] = newModel[i]
        
    def isFin(self):
        return(len(checkAll(self.model,self.clauses)[1])==0)

def modelToString(model):
    assignment = []
    for i in range(len(model)):
        if model[i]==0:
            assignment.append(0-(i+1))
        else:
            assignment.append(i+1)
    return assignment


def main():
    fileList = []
    file1 = 'f0020-01-s.cnf'
    file2 = 'f0020-01-u.cnf'
    file3 = 'f0020-02-s.cnf'
    file4 = 'f0020-02-u.cnf'
    file5 = 'f0020-03-s.cnf'
    file6 = 'f0020-03-u.cnf'
    file7 = 'f0020-04-s.cnf'
    file8 = 'f0020-04-u.cnf'
    file9 = 'f0020-05-s.cnf'
    file10 = 'f0020-05-u.cnf'
    file11 = 'f0020-06-s.cnf'
    file12 = 'f0020-06-u.cnf'
    file13 = 'f0020-07-s.cnf'
    file14 = 'f0020-07-u.cnf'
    file15 = 'f0020-08-s.cnf'
    file16 = 'f0020-08-u.cnf'
    file17 = 'f0040-01-s.cnf'
    file18 = 'f0040-01-u.cnf'
    file19 = 'f0040-02-s.cnf'
    file20 = 'f0040-02-u.cnf'
    file21 = 'f0040-03-s.cnf'
    file22 = 'f0040-03-u.cnf'
    file23 = 'f0040-04-s.cnf'
    file24 = 'f0040-04-u.cnf'
    file25 = 'f0040-05-s.cnf'
    file26 = 'f0040-05-u.cnf'
    file27 = 'f0040-06-s.cnf'
    file28 = 'f0040-06-u.cnf'
    file29 = 'f0040-07-s.cnf'
    file30 = 'f0040-07-u.cnf'
    file31 = 'f0040-08-s.cnf'
    file32 = 'f0040-08-u.cnf'
    fileList.append(file1)
    #fileList.append(file2)
    fileList.append(file3)
    #fileList.append(file4)
    fileList.append(file5)
    #fileList.append(file6)
    fileList.append(file7)
    #fileList.append(file8)
    fileList.append(file9)
    #fileList.append(file10)
    fileList.append(file11)
    #fileList.append(file12)
    fileList.append(file13)
    #fileList.append(file14)
    fileList.append(file15)
    #fileList.append(file16)
    fileList.append(file17)
    #fileList.append(file18)
    fileList.append(file19)
    #fileList.append(file20)
    fileList.append(file21)
    #fileList.append(file22)
    fileList.append(file23)
    #fileList.append(file24)
    fileList.append(file25)
    #fileList.append(file26)
    fileList.append(file27)
    #fileList.append(file28)
    fileList.append(file29)
    #fileList.append(file30)
    fileList.append(file31)
    #fileList.append(file32)
    
    
    for i in fileList:
        print
        print
        print i
        print
        print
        for j in range(10):
            model,clauses = parseFile(i)
            startTime = time.time()
            assignment = GeneticSat(model,clauses,0.5,100)
            endTime = time.time()
            if (assignment[0] != False):
                print("Solved. Variable assignment:")
                print(modelToString(assignment[1]))
            else:
                print("Hit max flip limit.")
                print("C = ",assignment[1])
            print("Execution time: ",endTime-startTime," seconds.")

    
    
main()
