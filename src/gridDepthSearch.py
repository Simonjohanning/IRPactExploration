"""
Module to encapsulate the grid depth search algorithm.
Recursively iterates through finer granularity of the parameter grid until a given error or recursion depth is reached.
"""

import numpy as np
import math
import simulationRunner
import configuration
import PVactModelHelper

def calculateGrid(searchParameters, minX, maxX, minY, maxY):
    """
    Function to set up the simulation runs of the current iteration level.
    Calculates the parameters for equidistant sampling in the respective parameter region;
    number of samples is given by the resolution (entry in searchParameters dictionary),
    region is defined through the min and max of the X and Y parameters

    :param searchParameters: dictionary of parameters for specifying the search
    :param minX: The minimal value in x coordinate dimension of the analysed grid
    :param maxX: The maximum value in x coordinate dimension of the analysed grid
    :param minY: The minimal value in y coordinate dimension of the analysed grid
    :param maxY: The maximum value in y coordinate dimension of the analysed grid
    :return: A pair of data with the first entry a 2D list of model performance (rows and columns in the performance matrix) and a second entry a list of dictionaries describing this data (with coordinates in both parameter dimensions (X,Y) and scalar performance value).
    """
    if(not 'model' in searchParameters):
        raise KeyError('Parameter model not specified for grid calculation')
    model = searchParameters['model']
    list = [[0 for col in range(searchParameters['resolution'])] for row in range(searchParameters['resolution'])]
    performanceEvaluation = [0 for run in range(int(math.pow(searchParameters['resolution'], 2)))]
    # prepare the grid for the simulation errors (2D list entries)
    for row in range(searchParameters['resolution']):
        for col in range(searchParameters['resolution']):
            inputFile = None
            # parameters for entries are calculated equidistantly (currentX = respective run)
            currentX = minX + ((maxX-minX)/(searchParameters['resolution']-1))*row
            currentY = round(minY + ((maxY-minY)/(searchParameters['resolution']-1))*col)
            if(searchParameters['printFlag']): print('calculating for X '+str(currentX)+' and Y '+str(currentY))
            if(model == 'PVact'):
                inputFile = PVactModelHelper.prepareJSONRand({'adoptionThreshold': currentX, 'interestThreshold': currentY, **searchParameters})
            elif(model == None):
                raise KeyError('Error: model not set.')
            else:
                raise NotImplementedError('Model ' + model + ' not implemented.')
            # add the performance of the run to the list
            if(not inputFile == None):
                list[col][row] = float(simulationRunner.invokeJar(inputFile, searchParameters['errorDefinition'], model, configuration.shellFlag))
            else:
                raise NotImplementedError('inputFile not set by the model; most likely the model is invalid or implemented incompletely.')
            #if(searchParameters['printFlag']): print('Calculating for index ' + str(row*searchParameters['resolution']+col) + ' with row ' + str(row) + ' and column ' + str(col))
    #        list[col][row] = mockInvokeJar(currentAT, currentIT)
            if(searchParameters['printFlag']): print('Performance of run ' + str(row*searchParameters['resolution']+col) + ': ' + str(list[col][row]))
            # evaluation of a single run is recorded in parameters and performance
            performanceEvaluation[row*searchParameters['resolution']+col] = {
                "X": currentX,
                "Y": currentY,
                "performance": list[col][row]
            }
    return list, performanceEvaluation

def nextDepthSearchIteration(searchParameters, searchState):
    """
    Evaluates a grid-based pattern in evenly spaced points in two dimensions
    and iterates the search in a sub-region containing the best performing points.
    The size of the sub-region depends on the searchParameter scaleFactor (size of current region and next iteration per dimension)
    and the number of points evaluated depends on the resolution.
    arguments are split in search parameters (that remain constant throughout the iteration)
    and the search state that is individual to each run.
    search parameters:
       acceptableDelta: what error is tolerable to terminate the search
       maxDepth: how many iterations can be made at most
       scaleFactor: how much smaller should the region get (fraction of larger one)
       resolution: how many points to evaluate per dimension
       printFlag: whether evaluated data should be printed during the process
       errorDefinition: the error mode used for the model execution
    search state:
       currentDelta: deviation of the last run from the validated time series
       currentRecursionDepth: number of recursion steps made before
       evaluationData: performance and information of the previous runs; entries are lists for each sample in the iteration
       lowerBoundX: the low end of the x dimension to search in
       upperBoundX: the high end of the x dimension to search in
       lowerBoundY: the low end of the y dimension to search in
       upperBoundY: the high end of the y dimension to search in


    :param searchParameters: Parameter dictionary containing the parameters that remain constant between runs (acceptable data, maxDepth, scaleFactor, resolution, printFLag and errorDefinition) as detailed above
    :param searchState: Parameter dictionary with all state parameters, i.e. those that change between the run (currentDelta, currentRecursionDepth, evaluationData, lowerBoundX, upperBoundX, lowerBoundY and upperBoundY) as detailed above
    :return: the search state after the last iteration with the evaluation data determined by the calculateGrid function (A pair of data with the first entry a 2D list of model performance (rows and columns in the performance matrix) and a second entry a list of dictionaries describing this data (with coordinates in both parameter dimensions (X,Y) and scalar performance value))
    """
    # if the last results are close enough to quality standards or 'too many' iterations have been performed, the search terminates
    if (searchState['currentDelta'] <= float(searchParameters['acceptableDelta']) or searchState['currentRecursionDepth'] >= int(searchParameters['maxDepth'])):
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
        newXRadius = (searchState['upperBoundX'] - searchState['lowerBoundX'])/(searchParameters['scaleFactor']*2)
        newYRadius = (searchState['upperBoundY'] - searchState['lowerBoundY']) / (searchParameters['scaleFactor'] * 2)
        # TODO differentiate between continuous and discrete
        newLowerBoundX = max(correspondingX-newXRadius, configuration.optimizationBounds['minX'])
        newUpperBoundX = min(correspondingX+newXRadius, configuration.optimizationBounds['maxX'])
        newLowerBoundY = math.floor(max(correspondingY-newYRadius, configuration.optimizationBounds['minY']))
        newUpperBoundY = math.ceil(min(correspondingY+newYRadius, configuration.optimizationBounds['maxY']))
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


# TODO improve documentation
def iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition, specificSearchParameters, inputFile, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY):
    """
    the grid depth search iteratively samples smaller / finer regions of the parameter space
    equidistantly until close enough to the reference time series or a given number of iterations are reached
    initializes the first call with relatively broad parameters
    returns the state of the iteration that terminates the search

    :param acceptableDelta: the error delta until which a finer grid will be analysed (search terminates when the performance goes beyond this value)
    :param maxDepth: the maximal number of iterations calculated
    :param scaleFactor: scalar factor how fast the parameter grid should shrink
    :param resolution: search granularity (how many points to evaluate between the parameter extremes
    :param errorDefinition: the error metric used in the model evaluation
    :param specificSearchParameters: additional parameters to be used in the search algorithm
    :param inputFile: the input file for the parameter configuration
    :param lowerBoundX: the minimal parameter value in the analysed area in x coordinate direction
    :param upperBoundX: the maximum parameter value in the analysed area in x coordinate direction
    :param lowerBoundY: the minimal parameter value in the analysed area in y coordinate direction
    :param upperBoundY: the maximum parameter value in the analysed area in y coordinate direction
    :return:
    """
    # clean the folder of former modelInputFiles
    # TODO check if it should be included again
    #check_output(['rm', 'src/modelInputFiles/*.json', '-r'], shell=True)
    return nextDepthSearchIteration({**specificSearchParameters, 'acceptableDelta': float(acceptableDelta), 'maxDepth': int(maxDepth), 'scaleFactor': float(scaleFactor), 'resolution': int(resolution), 'printFlag': True, 'errorDefinition': errorDefinition, 'inputFile': inputFile},
        {
        'currentDelta': 999999,
        'currentRecursionDepth': 0,
        "evaluationData": [],
        "lowerBoundX": lowerBoundX,
        "upperBoundX": upperBoundX,
        "lowerBoundY": lowerBoundY,
        "upperBoundY": upperBoundY }
    )
