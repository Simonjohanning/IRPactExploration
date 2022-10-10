
# Function to analyse the performance of different scenarios by a set of metrics
# TODO generalize and document
def analyseScenarioPerformance(parameterPerformance, lowBoundAT, highBoundAT, lowBoundIT, highBoundIT, scenarios):
    #print('performance for ' + str(len(parameterPerformance)) + 'ATs and ' + str(len(parameterPerformance[0])) + ' ITs with entries like ' + str(parameterPerformance[0][0]))
    scenarioDeltaAverages = open('src/resources/scenarioDeltaAverages', 'w')
    scenarioDeltaMinSpread = open('src/resources/scenarioDeltaMinSpread', 'w')
    scenarioDeltaMaxSpread = open('src/resources/scenarioDeltaMaxSpread', 'w')
    scenarioDeltaAnalysis = open('src/resources/scenarioDeltaAnalysis', 'w')
    scenarioAverages = open('src/resources/scenarioAverages', 'w')
    print(str(parameterPerformance))
    analysisData = []
    for indexAT in range(len(parameterPerformance)):
        for indexIT in range(len(parameterPerformance[indexAT])):
            runningTally = 0
            minEntry = 9999999999
            maxEntry = 0
            refCaseTally = 0
            instrumentCaseTally = 0
            #TODO make it work with more than two entries
            for entry in parameterPerformance[indexAT][indexIT]:
                currentEntry = parameterPerformance[indexAT][indexIT][entry][scenarios[1]] - parameterPerformance[indexAT][indexIT][entry][scenarios[0]]
                runningTally += currentEntry
                refCaseTally += parameterPerformance[indexAT][indexIT][entry][scenarios[0]]
                instrumentCaseTally += parameterPerformance[indexAT][indexIT][entry][scenarios[1]]
                if (currentEntry < minEntry):
                    minEntry = currentEntry
                if (currentEntry > maxEntry):
                    maxEntry = currentEntry
            average = runningTally/len(parameterPerformance[indexAT][indexIT])
            relativeMax = average/maxEntry
            relativeMin = average/minEntry
            correspondingAT = lowBoundAT + (indexAT * (highBoundAT - lowBoundAT) / (len(parameterPerformance) - 1))
            correspondingIT = lowBoundIT + (indexIT * (highBoundIT - lowBoundIT) / (len(parameterPerformance[indexAT]) - 1))
            analysisEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'average': average, 'maxSpread': maxEntry, 'minSpread': minEntry, 'maxSpreadRelative': maxEntry/average, 'minSpreadRelative': minEntry/average, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexAT][indexIT]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexAT][indexIT])}
            analysisData.append(analysisEntry)
            scenarioDeltaAnalysis.write(str(analysisEntry))
            averageEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': average}
            scenarioDeltaAverages.write(str(averageEntry) + '\n')
            minSpread = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': minEntry}
            scenarioDeltaMinSpread.write(str(minSpread) + '\n')
            maxSpread = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': maxEntry}
            scenarioDeltaMaxSpread.write(str(maxSpread) + '\n')
            scenarioAverageEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexAT][indexIT]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexAT][indexIT])}
            scenarioAverages.write(str(scenarioAverageEntry) + '\n')
            print(str(analysisEntry))
    print(str(analysisData))
    scenarioDeltaAverages.close()
    scenarioDeltaMinSpread.close()
    scenarioDeltaMaxSpread.close()
    scenarioDeltaAnalysis.close()
    return analysisData



