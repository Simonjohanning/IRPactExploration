
#
# TODO generalize and document
def analyseScenarioPerformance(parameterPerformance, lowBoundX, highBoundX, lowBoundY, highBoundY, scenarios):
    """
    Function to analyse the performance of different scenarios by a set of metrics.
    Analysed performance metrics are averages, min/max spread and ...
    The analysis is done on the basis of data for the analysed scenarios in an equally spaced parameter grid delimited
    by the parameters provided.
    Analysed parameters are:
     - parameter values x and y
     - average difference & scenario averages
     - absolute spread (scenario-wide max/min), relative spread (scenario-wide max/min normalized by parameter average)
     All data is written in the scenarioDeltaAnalysis file,
     whereas averages and spreads for all paramters are written in individual files

    :param parameterPerformance: A two-dimensional array of entries that comprise comparable runs.
    Comparable runs are indexed with the seed they were initialized with and are dictionaries of the scenarios and
    the results under the used metric for each simulated parameter pair
    :param lowBoundX: The minimal parameter value for the X dimension of the parameter grid
    :param highBoundX: The maximal parameter value for the X dimension of the parameter grid
    :param lowBoundY: The minimal parameter value for the Y dimension of the parameter grid
    :param highBoundY: The maximal parameter value for the Y dimension of the parameter grid
    :param scenarios: The list of simulated scenarios
    :return:
    """
    #print('performance for ' + str(len(parameterPerformance)) + 'Xs and ' + str(len(parameterPerformance[0])) + ' Ys with entries like ' + str(parameterPerformance[0][0]))
    scenarioDeltaAverages = open('src/resources/scenarioDeltaAverages', 'w')
    scenarioDeltaMinSpread = open('src/resources/scenarioDeltaMinSpread', 'w')
    scenarioDeltaMaxSpread = open('src/resources/scenarioDeltaMaxSpread', 'w')
    scenarioDeltaAnalysis = open('src/resources/scenarioDeltaAnalysis', 'w')
    scenarioAverages = open('src/resources/scenarioAverages', 'w')
    print(str(parameterPerformance))
    # list to store the results of the analysis
    analysisData = []
    for indexX in range(len(parameterPerformance)):
        for indexY in range(len(parameterPerformance[indexX])):
            # TODO check in how far this can be done with numpy more elegantly
            # parameterPerformance[indexX][indexY] contains the results of several runs with the same parameters
            # Analysis integrates over these runs and derives metrics
            # Performance is assumed to be non-negative
            # Variables to determine the min/max of runs between scenarios and runs
            minEntry = 9999999999
            maxEntry = 0
            # The tallies aggregate the results over several runs with the same parameter combination
            # the running tally sums over the difference between the scenarios, whereas the other tallys do so over the different scenarios
            runningTally = 0
            refCaseTally = 0
            instrumentCaseTally = 0
            #TODO make it work with more than two entries
            for entry in parameterPerformance[indexX][indexY]:
                currentEntry = parameterPerformance[indexX][indexY][entry][scenarios[1]] - parameterPerformance[indexX][indexY][entry][scenarios[0]]
                runningTally += currentEntry
                refCaseTally += parameterPerformance[indexX][indexY][entry][scenarios[0]]
                instrumentCaseTally += parameterPerformance[indexX][indexY][entry][scenarios[1]]
                if (currentEntry < minEntry):
                    minEntry = currentEntry
                if (currentEntry > maxEntry):
                    maxEntry = currentEntry
            # construct entries and write to files
            average = runningTally/len(parameterPerformance[indexX][indexY])
            correspondingX = lowBoundX + (indexX * (highBoundX - lowBoundX) / (len(parameterPerformance) - 1))
            correspondingY = lowBoundY + (indexY * (highBoundY - lowBoundY) / (len(parameterPerformance[indexX]) - 1))
            analysisEntry = {'x': correspondingX, 'y': correspondingY, 'average': average, 'maxSpread': maxEntry, 'minSpread': minEntry, 'maxSpreadRelative': maxEntry/average, 'minSpreadRelative': minEntry/average, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexX][indexY]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexX][indexY])}
            analysisData.append(analysisEntry)
            scenarioDeltaAnalysis.write(str(analysisEntry))
            averageEntry = {'x': correspondingX, 'y': correspondingY, 'performance': average}
            scenarioDeltaAverages.write(str(averageEntry) + '\n')
            minSpread = {'x': correspondingX, 'y': correspondingY, 'performance': minEntry}
            scenarioDeltaMinSpread.write(str(minSpread) + '\n')
            maxSpread = {'x': correspondingX, 'y': correspondingY, 'performance': maxEntry}
            scenarioDeltaMaxSpread.write(str(maxSpread) + '\n')
            scenarioAverageEntry = {'x': correspondingX, 'y': correspondingY, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexX][indexY]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexX][indexY])}
            scenarioAverages.write(str(scenarioAverageEntry) + '\n')
            print(str(analysisEntry))
    print(str(analysisData))
    scenarioAverages.close()
    scenarioDeltaAverages.close()
    scenarioDeltaMinSpread.close()
    scenarioDeltaMaxSpread.close()
    scenarioDeltaAnalysis.close()
    return analysisData



