from subprocess import check_output, CalledProcessError
import json
import numpy as np

def invokeJar(inputFile, modeParameters):
    # print(inputFile)
    # print(modeParameters)
    try:
        data = str(check_output(
            ['java', '-jar', 'src/ressources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o', 'example-output.json',
             '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters], shell=True), 'UTF=8')
        t = 0, data
        return data
    except CalledProcessError as e:
        t = e.returncode, e.message


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
def calculateGrid(minAT, maxAT, minIT, maxIT, startingIndex):
    currentIndex = startingIndex
    list = [[0 for col in range(resolution)] for row in range(resolution)]
    for row in range(resolution):
        for col in range(resolution):
            currentAT = minAT + ((maxAT-minAT)/(resolution-1))*row
            currentIT = round(minIT + ((maxIT-minIT)/(resolution-1))*col)
            print('calculating for IT '+str(currentIT)+' and AT '+str(currentAT))
            prepareJson('src/modelInputFiles/changedInterest', currentAT, currentIT)
            list[col][row] = invokeJar("src/modelInputFiles/changedInterest-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(currentIT), mode)
            currentIndex += 1
            performanceEvaluation["run "+str(currentIndex)] = {
                "adoptionThreshold": currentAT,
                "interestThreshold": currentIT,
                str(mode): list[col][row]
            }
    return list

# Searches
def patternSearch(acceptableDelta, maxAttempts, currentDelta, lowerBoundAT, upperBoundAT, lowerBoundIT, upperBoundIT):
    print('CurrentAttempts: '+str(runIndex))
    print(performanceEvaluation)
    if (currentDelta <= acceptableDelta or runIndex >= maxAttempts):
        return currentDelta, runIndex
    else:
        gridResultList = np.array(calculateGrid(lowerBoundAT, upperBoundAT, lowerBoundIT, upperBoundIT, runIndex))
        # Finding the index with the lowest error, adapted from https://devenum.com/find-min-value-index-in-numpy-array/
        minvalInCols = np.amin(gridResultList, axis=0)
        minvalInRows = np.amin(gridResultList, axis=1)
        index = np.where(gridResultList == np.amin(gridResultList))
        listofIndices = list(zip(index[0], index[1]))
        # Make more elegant
        minInd = listofIndices[0]
        correspondingAT = lowerBoundAT + ((upperBoundAT-lowerBoundAT)/(resolution-1))*minInd[0]
        correspondingIT = round(lowerBoundIT + ((upperBoundIT-lowerBoundIT)/(resolution-1))*minInd[1])
        print('Best index found at ' + str(minInd) + ' with AT ' + correspondingAT + ' and IT ' + correspondingIT)
        newATRadius = (upperBoundAT - lowerBoundAT)/(scaleFactor*2)
        newITRadius = (upperBoundIT - lowerBoundIT) / (scaleFactor * 2)
        print('new search in the bound of [' + str(correspondingAT-newATRadius) + ', '+ str(correspondingAT+newATRadius)+'] (AT) and [' + str(correspondingIT-newITRadius) + ', '+ str(correspondingIT+newITRadius)+']  (IT)')
        return patternSearch(acceptableDelta, maxAttempts, gridResultList[minInd], correspondingAT-newATRadius, correspondingAT+newATRadius, correspondingIT-newITRadius, correspondingIT+newITRadius)

if __name__ == '__main__':
    global mode
    mode = 'RMSD'
    global resolution
    resolution = 2
    global scaleFactor
    scaleFactor = 2
    global performanceEvaluation
    performanceEvaluation = {}
    global runIndex
    runIndex = 0
    patternSearch(2, 12, 9999999, 0, 1.0, 1, 64)

    # performance = invokeJar("modelInputFiles/changedInterest-5-13", 'RMSD')
    # print(performance)
    # performanceEvaluation['run0'] = {
    #             "adoptionThreshold": 0.5,
    #             "interestThreshold": 13,
    #             'RMSD': float(performance)
    # }
    # print(performanceEvaluation)




