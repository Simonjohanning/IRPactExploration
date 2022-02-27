from subprocess import check_output, CalledProcessError
import json
import numpy as np
import math

def invokeJar(inputFile, modeParameters):
    # print(inputFile)
    # print(modeParameters)
    try:
        data = check_output(
            ['java', '-jar', 'src/ressources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o', 'example-output.json',
             '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters], shell=True)
        t = 0, data.decode('utf-8').rstrip()
        return data
    except CalledProcessError as e:
        t = e.returncode, e.message

def mockInvokeJar(AT, IT):
    if(AT > 0):
        return (1/(AT*IT))
    else:
        return 999999

def prepareJson(templateFile, adoptionThreshold, interestThreshold):
    f = open('src/ressources/example-input.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file)

# calculate an even grid of the respective values for the thresholds in the specified execution
def calculateGrid(searchParameters, minAT, maxAT, minIT, maxIT):
    list = [[0 for col in range(searchParameters['resolution'])] for row in range(searchParameters['resolution'])]
    performanceEvaluation = [0 for run in range(int(math.pow(searchParameters['resolution'], 2)))]
    for row in range(searchParameters['resolution']):
        for col in range(searchParameters['resolution']):
            currentAT = minAT + ((maxAT-minAT)/(searchParameters['resolution']-1))*row
            currentIT = round(minIT + ((maxIT-minIT)/(searchParameters['resolution']-1))*col)
            print('calculating for IT '+str(currentIT)+' and AT '+str(currentAT))
            prepareJson('src/modelInputFiles/changedInterest', currentAT, currentIT)
            list[col][row] = float(invokeJar("src/modelInputFiles/changedInterest-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(currentIT), searchParameters['errorDefinition']))
            print('Calculating for index ' + str(row*searchParameters['resolution']+col) + ' with row ' + str(row) + ' and column ' + str(col))
    #        list[col][row] = mockInvokeJar(currentAT, currentIT)
            print('Performance of run ' + str(row*searchParameters['resolution']+col) + ': ' + str(list[col][row]))
            performanceEvaluation[row*searchParameters['resolution']+col] = {
                "adoptionThreshold": currentAT,
                "interestThreshold": currentIT,
                "error": list[col][row]
            }
    return list, performanceEvaluation

# Evaluates a grid-based pattern in evenly spaced points (dim: interest threshold and adoption threshold)
# and iterates the search in a sub-region containing the best performing points.
# The size of the sub-region depends on the searchParameter scaleFactor (size of current region and next iteration per dimension)
# and the number of points evaluated depends on the resolution
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
#   evaluationData: performance and information of the previous runs
#   lowerBoundAT: the low end of the adoption threshold dimension to search in
#   upperBoundAT: the high end of the adoption threshold dimension to search in
#   lowerBoundIT: the low end of the interest threshold dimension to search in
#   upperBoundIT: the high end of the interest threshold dimension to search in
def nextDepthSearchIteration(searchParameters, searchState):
    if (searchState['currentDelta'] <= searchParameters['acceptableDelta'] or searchState['currentRecursionDepth'] >= searchParameters['maxDepth']):
        return searchState
    else:
        print('In next search iteration. State is \n')
        print(searchState)
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
                "evaluationData": {},
                "lowerBoundAT": newLowerBoundIT,
                "upperBoundAT": newUpperBoundIT,
                "lowerBoundIT": newLowerBoundAT,
                "upperBoundIT": newUpperBoundAT
            })

def iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition):
    return nextDepthSearchIteration({
        'acceptableDelta': acceptableDelta,
        'maxDepth': maxDepth,
        'scaleFactor': scaleFactor,
        'resolution': resolution,
        'printFlag': True,
        'errorDefinition': errorDefinition
    }, {
        'currentDelta': 999999,
        'currentRecursionDepth': 0,
        "evaluationData": [],
        "lowerBoundAT": 0.0,
        "upperBoundAT": 1.0,
        "lowerBoundIT": 1,
        "upperBoundIT": 86
    })
