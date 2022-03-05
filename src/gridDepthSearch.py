import numpy as np
import math
import simulationRunner

# function to set up the simulation runs of the current iteration level
# calculates the parameters for equidistant sampling in the respective parameter region
# number of samples is given by the resolution (entry in searchParameters dictionary),
# region is defined through the min and max of the AT and IT parameters
def calculateGrid(searchParameters, minAT, maxAT, minIT, maxIT):
    list = [[0 for col in range(searchParameters['resolution'])] for row in range(searchParameters['resolution'])]
    performanceEvaluation = [0 for run in range(int(math.pow(searchParameters['resolution'], 2)))]
    # prepare the grid for the simulation errors (2D list entries)
    for row in range(searchParameters['resolution']):
        for col in range(searchParameters['resolution']):
            # parameters for entries are calculated equidistantly (currentX = respective run)
            currentAT = minAT + ((maxAT-minAT)/(searchParameters['resolution']-1))*row
            currentIT = round(minIT + ((maxIT-minIT)/(searchParameters['resolution']-1))*col)
            if(searchParameters['printFlag']): print('calculating for IT '+str(currentIT)+' and AT '+str(currentAT))
            simulationRunner.prepareJson('src/modelInputFiles/changedInterest', currentAT, currentIT)
            # add the performance of the run to the list
            list[col][row] = float(simulationRunner.invokeJar("src/modelInputFiles/changedInterest-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(currentIT), searchParameters['errorDefinition']))
            if(searchParameters['printFlag']): print('Calculating for index ' + str(row*searchParameters['resolution']+col) + ' with row ' + str(row) + ' and column ' + str(col))
    #        list[col][row] = mockInvokeJar(currentAT, currentIT)
            if(searchParameters['printFlag']): print('Performance of run ' + str(row*searchParameters['resolution']+col) + ': ' + str(list[col][row]))
            # evaluation of a single run is recorded in parameters and performance
            performanceEvaluation[row*searchParameters['resolution']+col] = {
                "adoptionThreshold": currentAT,
                "interestThreshold": currentIT,
                "performance": list[col][row]
            }
    return list, performanceEvaluation

# Evaluates a grid-based pattern in evenly spaced points (dim: interest threshold and adoption threshold)
# and iterates the search in a sub-region containing the best performing points.
# The size of the sub-region depends on the searchParameter scaleFactor (size of current region and next iteration per dimension)
# and the number of points evaluated depends on the resolution.
# arguments are split in search parameters (that remain constant throughout the iteration)
# and the search state that is individual to each run.
# search parameters:
#   acceptableDelta: what error is tolerable to terminate the search
#   maxDepth: how many iterations can be made at most
#   scaleFactor: how much smaller should the region get (fraction of larger one)
#   resolution: how many points to evaluate per dimension
#   printFlag: whether evalutated data should be printed during the process
#   errorDefinition: the error mode used for IRPact
# search state:
#   currentDelta: deviation of the last run from the validated time series
#   currentRecursionDepth: number of recursion steps made before
#   evaluationData: performance and information of the previous runs; entries are lists for each sample in the iteration
#   lowerBoundAT: the low end of the adoption threshold dimension to search in
#   upperBoundAT: the high end of the adoption threshold dimension to search in
#   lowerBoundIT: the low end of the interest threshold dimension to search in
#   upperBoundIT: the high end of the interest threshold dimension to search in
def nextDepthSearchIteration(searchParameters, searchState):
    # if the last results are close enough to quality standards or 'too many' iterations have been performed, the search terminates
    if (searchState['currentDelta'] <= searchParameters['acceptableDelta'] or searchState['currentRecursionDepth'] >= searchParameters['maxDepth']):
        return searchState
    else:
        if(searchParameters['printFlag']):
            print('In next search iteration. State is \n')
            print(searchState)
        # results and information on the
        gridResults, resultDic = calculateGrid(searchParameters, searchState['lowerBoundAT'], searchState["upperBoundAT"], searchState["lowerBoundIT"], searchState["upperBoundIT"])
        gridResultList = np.array(gridResults)
        # Finding the index with the lowest error, adapted from https://devenum.com/find-min-value-index-in-numpy-array/
        if(searchParameters['printFlag']): print(gridResultList)
        index = np.where(gridResultList == np.amin(gridResultList))
        listofIndices = list(zip(index[0], index[1]))
        print(listofIndices)
        # Make more elegant
        for currentMinIndex in listofIndices:
            print(currentMinIndex)
            correspondingAT = searchState['lowerBoundAT'] + ((searchState['upperBoundAT']-searchState['lowerBoundAT'])/(searchParameters['resolution']-1))*currentMinIndex[0]
            correspondingIT = round(searchState['lowerBoundIT'] + ((searchState['upperBoundIT']-searchState['lowerBoundIT'])/(searchParameters['resolution']-1))*currentMinIndex[1])
            print('Best index found at ' + str(currentMinIndex) + ' with AT ' + str(correspondingAT) + ' and IT ' + str(correspondingIT))
            newATRadius = (searchState['upperBoundAT'] - searchState['lowerBoundAT'])/(searchParameters['scaleFactor']*2)
            newITRadius = (searchState['upperBoundIT'] - searchState['lowerBoundIT']) / (searchParameters['scaleFactor'] * 2)
            newLowerBoundAT = max(correspondingAT-newATRadius, 0)
            newUpperBoundAT = min(correspondingAT+newATRadius, 1)
            newLowerBoundIT = math.floor(max(correspondingIT-newITRadius, 0))
            newUpperBoundIT = math.ceil(min(correspondingIT+newITRadius, 128))
            print('new search in the bound of [' + str(newLowerBoundAT) + ', '+ str(newUpperBoundAT)+'] (AT) and [' + str(newLowerBoundIT) + ', '+ str(newUpperBoundIT)+']  (IT)')
            return nextDepthSearchIteration(searchParameters, {
                'currentDelta': gridResultList[currentMinIndex],
                'currentRecursionDepth': searchState['currentRecursionDepth'] + 1,
                "evaluationData": searchState['evaluationData'].append(resultDic),
                "lowerBoundAT": newLowerBoundAT,
                "upperBoundAT": newUpperBoundAT,
                "lowerBoundIT": newLowerBoundIT,
                "upperBoundIT": newUpperBoundIT
            })

# the grid depth search iteratively samples smaller / finer regions of the parameter space
# equidistantly until close enough to the reference time series or a given number of iterations are reached
# initializes the first call with relatively broad parameters
# returns the state of the iteration that terminates the search
def iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition):
    print(f"Running simulation with parameters \n acceptableDelta: {acceptableDelta} \n maxDepth {maxDepth} \n scaleFactor {scaleFactor} \n resolution {resolution} \n errorDefinition {errorDefinition} ")
    # clean the folder of former modelInputFiles
    #check_output(['rm', 'src/modelInputFiles/*.json', '-r'], shell=True)
    return nextDepthSearchIteration({
        'acceptableDelta': float(acceptableDelta),
        'maxDepth': int(maxDepth),
        'scaleFactor': float(scaleFactor),
        'resolution': int(resolution),
        'printFlag': True,
        'errorDefinition': errorDefinition
    }, {
        'currentDelta': 999999,
        'currentRecursionDepth': 0,
        "evaluationData": [],
        "lowerBoundAT": 0.5,
        "upperBoundAT": 0.8,
        "lowerBoundIT": 1,
        "upperBoundIT": 86
    })
