import numpy as np
import math
import simulationRunner
import configuration
import os

# function to set up the simulation runs of the current iteration level
# calculates the parameters for equidistant sampling in the respective parameter region
# number of samples is given by the resolution (entry in searchParameters dictionary),
# region is defined through the min and max of the AT and IT parameters
def calculateGrid(searchParameters, minX, maxX, minY, maxIT, model):
    list = [[0 for col in range(searchParameters['resolution'])] for row in range(searchParameters['resolution'])]
    performanceEvaluation = [0 for run in range(int(math.pow(searchParameters['resolution'], 2)))]
    # prepare the grid for the simulation errors (2D list entries)
    for row in range(searchParameters['resolution']):
        for col in range(searchParameters['resolution']):
            # parameters for entries are calculated equidistantly (currentX = respective run)
            currentAT = minX + ((maxX-minX)/(searchParameters['resolution']-1))*row
            currentIT = round(minY + ((maxIT-minY)/(searchParameters['resolution']-1))*col)
            if(searchParameters['printFlag']): print('calculating for IT '+str(currentIT)+' and AT '+str(currentAT))
            simulationRunner.prepareJsonRand('src/modelInputFiles/changedInterest', currentAT, currentIT, searchParameters['AP'], searchParameters['IP'], searchParameters['inputFile'])
            # add the performance of the run to the list
            list[col][row] = float(simulationRunner.invokeJar(os.getcwd() + "\src\modelInputFiles\changedInterest-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(currentIT), searchParameters['errorDefinition'], model, configuration.shellFlag))
            #if(searchParameters['printFlag']): print('Calculating for index ' + str(row*searchParameters['resolution']+col) + ' with row ' + str(row) + ' and column ' + str(col))
    #        list[col][row] = mockInvokeJar(currentAT, currentIT)
            if(searchParameters['printFlag']): print('Performance of run ' + str(row*searchParameters['resolution']+col) + ': ' + str(list[col][row]))
            # evaluation of a single run is recorded in parameters and performance
            performanceEvaluation[row*searchParameters['resolution']+col] = {
                "adoptionThreshold": currentAT,
                "interestThreshold": currentIT,
                "performance": list[col][row]
            }
    return list, performanceEvaluation

# Evaluates a grid-based pattern in evenly spaced points in two dimensions
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
#   printFlag: whether evaluated data should be printed during the process
#   errorDefinition: the error mode used for IRPact
# search state:
#   currentDelta: deviation of the last run from the validated time series
#   currentRecursionDepth: number of recursion steps made before
#   evaluationData: performance and information of the previous runs; entries are lists for each sample in the iteration
#   lowerBoundX: the low end of the x dimension to search in
#   upperBoundX: the high end of the x dimension to search in
#   lowerBoundY: the low end of the y dimension to search in
#   upperBoundY: the high end of the y dimension to search in
def nextDepthSearchIteration(searchParameters, searchState):
    # if the last results are close enough to quality standards or 'too many' iterations have been performed, the search terminates
    if (searchState['currentDelta'] <= searchParameters['acceptableDelta'] or searchState['currentRecursionDepth'] >= searchParameters['maxDepth']):
        return searchState
    else:
        if(searchParameters['printFlag']):
            print('In next search iteration. State is \n')
            print(searchState)
        # results and information on the
        gridResults, resultDic = calculateGrid(searchParameters, searchState['lowerBoundX'], searchState["upperBoundX"], searchState["lowerBoundY"], searchState["upperBoundY"])
        gridResultList = np.array(gridResults)
        # Finding the index with the lowest error, adapted from https://devenum.com/find-min-value-index-in-numpy-array/
        if(searchParameters['printFlag']): print(gridResultList)
        index = np.where(gridResultList == np.amin(gridResultList))
        listofIndices = list(zip(index[0], index[1]))
        print(listofIndices)
        # TODO list of several optima, make it so that all process
        # TODO think through and compare with previous code
        for currentMinIndex in listofIndices:
            correspondingX = searchState['lowerBoundX'] + ((searchState['upperBoundX'] - searchState['lowerBoundX']) / (searchParameters['resolution'] - 1)) * currentMinIndex[0]
            if(configuration.optimizationBounds['minX'] > correspondingX):
                correspondingX = configuration.optimizationBounds['minX']
            if(configuration.optimizationBounds['maxX'] < correspondingX):
                correspondingX = configuration.optimizationBounds['maxX']
            correspondingY = round(searchState['lowerBoundY'] + ((searchState['upperBoundY'] - searchState['lowerBoundY']) / (searchParameters['resolution'] - 1)) * currentMinIndex[1])
            if (configuration.optimizationBounds['minY'] > correspondingY):
                correspondingY = configuration.optimizationBounds['minY']
            if (configuration.optimizationBounds['maxY'] < correspondingY):
                correspondingY = configuration.optimizationBounds['maxY']
        print('optimal area assumed in [' + str(minX) + ', ' + str(maxX) + '] x [ ' + str(minY) + ', ' + str(maxY) + ']')
        newXRadius = (searchState['upperBoundX'] - searchState['lowerBoundX'])/(searchParameters['scaleFactor']*2)
        newYRadius = (searchState['upperBoundY'] - searchState['lowerBoundY']) / (searchParameters['scaleFactor'] * 2)
        # TODO differentiate between continuous and discrete
        newLowerBoundX = max(correspondingX-newXRadius, configuration.optimizationBounds['minX'])
        newUpperBoundX = min(correspondingX+newXRadius, configuration.optimizationBounds['maxX'])
        newLowerBoundY = math.floor(max(minY-newYRadius, configuration.optimizationBounds['minY']))
        newUpperBoundY = math.ceil(min(maxY+newYRadius, configuration.optimizationBounds['maxY']))
        print('new search in the bound of [' + str(newLowerBoundX) + ', '+ str(newUpperBoundX)+'] (X) and [' + str(newLowerBoundY) + ', '+ str(newUpperBoundY)+']  (Y)')
        print('search state is ' + str(searchState))
        print('with evaluation data ' + str(searchState['evaluationData']))
        print('resultDic is ' + str(resultDic))
        searchState['evaluationData'].append(resultDic)
        print('appended version ' + str(searchState['evaluationData']))
        return nextDepthSearchIteration(searchParameters, {
            'currentDelta': gridResultList[currentMinIndex],
            'currentRecursionDepth': searchState['currentRecursionDepth'] + 1,
            "evaluationData": searchState['evaluationData'],
            "lowerBoundX": newLowerBoundX,
            "upperBoundX": newUpperBoundX,
            "lowerBoundY": newLowerBoundY,
            "upperBoundY": newUpperBoundY
        })

# the grid depth search iteratively samples smaller / finer regions of the parameter space
# equidistantly until close enough to the reference time series or a given number of iterations are reached
# initializes the first call with relatively broad parameters
# returns the state of the iteration that terminates the search
# TODO document the parameters
def iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition, specificSearchParameters, inputFile, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY):
    print(f"Running simulation with parameters \n acceptableDelta: {acceptableDelta} \n maxDepth {maxDepth} \n scaleFactor {scaleFactor} \n resolution {resolution} \n errorDefinition {errorDefinition} \n lowerBoundAT {lowerBoundAT} \n upperBoundAT {upperBoundAT} \n lowerBoundIT {lowerBoundIT} \n upperBoundIT {upperBoundIT} ")
    # clean the folder of former modelInputFiles
    #check_output(['rm', 'src/modelInputFiles/*.json', '-r'], shell=True)
    searchParameters = specificSearchParameters
    searchParameters['acceptableDelta']: float(acceptableDelta)
    searchParameters['maxDepth']: int(maxDepth)
    searchParameters['scaleFactor']: float(scaleFactor)
    searchParameters['resolution']: int(resolution)
    searchParameters['printFlag']: True
    searchParameters['errorDefinition']: errorDefinition
    searchParameters['inputFile']: inputFile
    return nextDepthSearchIteration(searchParameters,
        {
        'currentDelta': 999999,
        'currentRecursionDepth': 0,
        "evaluationData": [],
        "lowerBoundX": lowerBoundX,
        "upperBoundX": upperBoundX,
        "lowerBoundY": lowerBoundY,
        "upperBoundY": upperBoundY }
    )
