
import random,copy,time,Queue


def WalkSat(model,clauses,p,maxFlips):
    
    for Flips in range(maxFlips):   
        #If the model satisfies the set of clauses
        if(checkModel(model,clauses)):
            return model,Flips
        
        #Pick a random clause from the set of false clauses
        clause = getFalseClause(model,clauses)
        
        #Flip a random variable in that clause with probability p
        rand = random.uniform(0.0,1.0)
        if rand < p:
            randomFlip(model, clause)
            
        else:
            #Initiate max satisfied clause value, best index holder
            maxSatClauses = 0
            bestIndex = 0
            #For every variable in clause
            for i in clause:
                #Get associated index
                index = abs(i)-1
                #Flip that variable in a copy of the model
                tempModel = copy.deepcopy(model)
                flip(tempModel,index)
                #Count the number of clauses that will be satisfied with flip
                if countSatClauses(tempModel,clauses) > maxSatClauses:
                    bestIndex = index
                    
            #Flip the variable that gives the most satisfied clauses
            flip(model,bestIndex)
            
    #If the maximum number of flips has been reached, return failure
    return False

def GeneticSat(models,clauses,p,maxFlips):
    """It is assumed that len(models) is divisible by ten [this is for calculations in the crossModel function]"""
    
    for Flips in range(maxFlips):
        #For every current model
        for model in models:
            #If the model satisfies the set of clauses
            if(checkModel(model,clauses)):
                return model,Flips
        
        #Select the best models
        que = natSelect(models,clauses)
        
        #For every pair
        while not que.empty():
            #Cross-breed
            model1 = que.get_nowait()[1]
            model2 = que.get_nowait()[1]
            crossModel(model1,model2)
            
        #For every model
        for model in models:
            #Mutate with probability p
            mutate(model,clauses,p)
                
    #If the maximum number of flips has been reached, return failure
    return False

"""Function to mutate model with probability p"""   
def mutate(model,clauses,p):
    
    rand = random.uniform(0.0,1.0)
    if rand < p:
        #Because of the way randomFlip is set up, you have to feed it a clause as well
            #Picking a random clause may throw off the probability distribution of 
            #evenly picking variables to flip if one variable occurs more than another 
            #in the set of clauses, but this difference decreases as the number of clauses
            #and number of variables increase. So we'll ingore this for now.
        #Pick random clause
        clause = random.choice(clauses)
        #Flip random variable
        randomFlip(model,clause)
        
    return True
     
"""Crossbreeds given models"""
def crossModel(model1,model2):
    
    #Assign cut percentage
    percentToCut = 40/100.0
    
    #Define length of cut
    cutLength = int(len(model1)*percentToCut)
    
    #Create a temp list to hold cut of model1
    temp = [0 for x in range(cutLength)]
    
    #Cross the models 
    for i in range(len(temp)):
        temp[i] = model1[i]
        model1[i] = model2[i]
        model2[i] = temp[i]
    
    return   
        
"""Returns a priority que of models based on the number of clauses they satisfy"""
def natSelect(models,clauses):
    
    #Initiate priority que
    PQ = Queue.PriorityQueue()
    
    #For every model
    for model in models:
        #Rank the model based on satisfied clauses
        #Number of satisfied clauses = #of clauses - false clauses
        #False clauses
        falseClauses = 0
        #For every clause
        for clause in clauses:
            #If clause is not satisfied
            if not testClause(model,clause):
                falseClauses += 1
        #Add to queue
        PQ.put_nowait((falseClauses,model))
    
    #Return Queue
    return PQ

"""Function to determine fitness of model for given clauses"""
def checkModel(model,clauses):
    
    #For every clause
    for clause in clauses:
        #If at least one clause reports false
        if(testClause(model,clause)==False):
            return False
    return True

"""Returns a random (deep copied) false clause from the set of all clauses"""
def getFalseClause(model,clauses):
    
    falseClauses = []
    #For every clause
    for i in clauses:
        #If false
        if not testClause(model,i):
            #Add to list
            falseClauses.append(i)
    
    #Pick random clause from the set
    clause = random.choice(falseClauses)
    #Return deep copy
    return copy.deepcopy(clause)  
    
"""Helper function to test truth of clauses"""
def testClause(model,clause):

    for i in range(len(clause)):
        #Checking sign of clause variable and value of corresponding model variable
        if ( (clause[i]>0) and (model[abs(clause[i])-1]) or (clause[i]<0) and (not model[abs(clause[i])-1]) ):
            return(True)
    #If all conflicting
    return(False)

"""Function to randomly flip one variable in the model corresponding to a clause variable"""
def randomFlip(model,clause):
    
    #Get the variable indexes associated with clause
    varIndex = []
    for i in clause:
        varIndex.append(abs(i)-1)
    
    #Pick a random index
    index = random.choice(varIndex)
    #Flip the variable
    flip(model,index)
    
    return True
  
"""Function to flip variable in model with given index"""
def flip(model,index):
    
    if model[index] == 0:
        model[index] = 1
    else:
        model[index] = 0
    
"""Returns the integer value of the number of satisfied clauses for the given model"""
def countSatClauses(model,clauses):
    
    satCount = 0
    #For every clause
    for clause in clauses:
        #If the clause is satisfied
        if testClause(model,clause):
            #Increment
            satCount += 1
    return satCount

"""Function to retrieve random model and clauses from given file""" 
def parseFile(fileName):
    
    #Open the file
    fin = open(fileName,'r')
    
    #Retrieve info from first line
    line = fin.readline()
    line = line.split()
    while line[0] == 'c':
        line = fin.readline()
        line = line.split()
    numVars = int(line[2])
    
    #Initiate clauses and random model
    model = initVars(numVars)
    clauses = []
    
    #Iterate over the lines
    for line in fin:
        splitLine = line.split()
        if splitLine[0] == 'c':
            break
        clause = []
        for var in splitLine:
            #Create clause
            clause.append(int(var))
        #Store clause in list
        clauses.append(clause)
    #Close file
    fin.close()
    
    #Return the random model and clause list
    return model,clauses

"""Helper function to randomize variables"""
def initVars(numVars):
    model = []
    for n in range(numVars):
        model.append(random.randint(0,1))
    return model

"""Function to convert binary string of variables to positive and negative value representation of variables"""
def modelToString(model):
    assignment = []
    for i in range(len(model)):
        if model[i]==0:
            assignment.append(0-(i+1))
        else:
            assignment.append(i+1)
    return assignment

def testWalkSat(fileList):
    
    print "Testing WalkSat...\n\n"
    
    #For every file
    for File in fileList:
        print "Parsing file: ",File
        
        #Initiate sum for average execution time and flips for the same
        sumTime = 0
        sumFlips = 0
        #Do 10 runs
        for run in range(10):
            #Parse file
            model,clauses = parseFile(File)
            maxFlips,p = 10000,0.5
            
            #Time the run
            startTime = time.time()
            assignment = WalkSat(model,clauses,p,maxFlips)
            endTime = time.time()
            if assignment == False:
                print "Max number of flips reached, no solution found."
                sumFlips += maxFlips
            else:
                print "Solved. Variable assignment:"
                print modelToString(assignment[0])
                print "Flips: ",assignment[1]," flips."
                sumFlips += assignment[1]
            exeTime = endTime-startTime
            print "Execution time: ",exeTime," seconds."
            sumTime += exeTime
            
        avgTime = sumTime/10
        avgFlips = sumFlips/10
        print "Average time for ",File,": ",avgTime,"seconds."
        print "Average flips for ",File,": ",avgFlips,"flips.\n\n"
    
def testGeneticSat(fileList):

    print "Testing GeneticSat...\n\n"

    #For every file
    for File in fileList:
        print "Parsing file: ",File
        
        #Initiate sum for average execution time and flips for the same
        sumTime = 0
        sumFlips = 0
        #Do 10 runs
        for run in range(10):
            #Parse file
            model,clauses = parseFile(File)
            numModels = 100
            maxFlips,p = 400,0.1      
            
            #Generate models
            #Best with diversity?
            models = []
            for m in range(numModels):
                #Create a new model
                newModel = initVars(len(model))
                #Add it to models
                models.append(newModel)
                
            #Time the run
            startTime = time.time()
            assignment = GeneticSat(models,clauses,p,maxFlips)
            endTime = time.time()
            if assignment == False:
                print "Max number of flips reached, no solution found."
                sumFlips += maxFlips
            else:
                print "Solved. Variable assignment:"
                print modelToString(assignment[0])
                print "Flips: ",assignment[1]," flips."
                sumFlips += assignment[1]
            exeTime = endTime-startTime
            print "Execution time: ",exeTime," seconds."
            sumTime += exeTime
            
        avgTime = sumTime/10
        avgFlips = sumFlips/10
        print "Average time for ",File,": ",avgTime,"seconds."
        print "Average flips for ",File,": ",avgFlips,"flips.\n"


def main():
    
    easyList = []
    eFile1 = '10.40.160707067.cnf'
    eFile2 = '10.40.967323288.cnf'
    eFile3 = '10.42.1465130262.cnf'
    eFile4 = '10.42.504071595.cnf'
    eFile5 = '10.44.1247388329.cnf'
    eFile6 = '10.44.1667358355.cnf'
    eFile7 = '10.46.183405239.cnf'
    eFile8 = '10.46.623142927.cnf'
    eFile9 = '10.48.1494607484.cnf'
    eFile10 = '10.48.640112774.cnf'
    easyList.append(eFile1)
    easyList.append(eFile2)
    easyList.append(eFile3)
    easyList.append(eFile4)
    easyList.append(eFile5)
    easyList.append(eFile6)
    easyList.append(eFile7)
    easyList.append(eFile8)
    easyList.append(eFile9)
    easyList.append(eFile10)
    
    
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
    fileList.append(file2)
    fileList.append(file3)
    fileList.append(file4)
    fileList.append(file5)
    fileList.append(file6)
    fileList.append(file7)
    fileList.append(file8)
    fileList.append(file9)
    fileList.append(file10)
    fileList.append(file11)
    fileList.append(file12)
    fileList.append(file13)
    fileList.append(file14)
    fileList.append(file15)
    fileList.append(file16)
    fileList.append(file17)
    fileList.append(file18)
    fileList.append(file19)
    fileList.append(file20)
    fileList.append(file21)
    fileList.append(file22)
    fileList.append(file23)
    fileList.append(file24)
    fileList.append(file25)
    fileList.append(file26)
    fileList.append(file27)
    fileList.append(file28)
    fileList.append(file29)
    fileList.append(file30)
    fileList.append(file31)
    fileList.append(file32)

    longFiles = [file17,file18,file19,file20,file21,file22,file23,file24,file25,file26,file27,file28,file29,file30,file31,file32]

    #testWalkSat(easyList)
    testGeneticSat(longFiles)
        
main()