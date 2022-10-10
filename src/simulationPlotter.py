import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import helper

# TODO document
def visualizeData(graphType, dataPath):
    n = helper.determineDataPoints(dataPath)
    if(graphType == 'trisurf'):
        visualizeLinearRepresentationPlot(graphType, dataPath, n)
    elif(graphType == 'barChart'):
        visualize2DRepresentationPlot(graphType, dataPath, n)

# TODO document and generalize
def visualize2DRepresentationPlot(graphType, dataPath, n):
    adoptionKeys = set()
    interestKeys = set()
    dataDictionary = []
    with open(dataPath, 'r') as file:
        for line in file:
            pointDict = eval(line)
            if(not pointDict['adoptionThreshold'] in adoptionKeys):
                adoptionKeys.add(pointDict['adoptionThreshold'])
                #print('at' + str(pointDict['adoptionThreshold']))
            if (not pointDict['interestThreshold'] in interestKeys):
                interestKeys.add(pointDict['interestThreshold'])
                #print('it' + str(pointDict['interestThreshold']))
            dataDictionary.append(pointDict)
        adoptionIndices = {}
        interestIndices = {}
        for index in range(len(adoptionKeys)):
            adoptionIndices[adoptionKeys.pop()] = index
        for index in range(len(interestKeys)):
            interestIndices[interestKeys.pop()] = index
        print(len(adoptionIndices))
        print(','.join(adoptionKeys))
        print(len(interestIndices))
        print(list(interestKeys))
        cd_x = np.zeros(len(adoptionIndices), dtype=float)
        cd_y = np.zeros(len(interestIndices), dtype=float)
        cd_z = np.zeros(len(adoptionIndices) * len(interestIndices), dtype=float)
        print(str(len(cd_z)))
        print(str(len(cd_x)))
        print(str(len(cd_y)))
        #cd_z.reshape((len(cd_x), len(cd_y)))
        cd_z.reshape((10, 13))
        print(str(len(cd_z)))
        print(str(cd_z))
        for dataIndex in dataDictionary:
            print(str(dataIndex))
            cd_x[adoptionIndices[dataIndex['adoptionThreshold']]] = dataIndex['adoptionThreshold']
            print('AT ' + str(dataIndex['adoptionThreshold']) + ' is associated with index ' + str(adoptionIndices[dataIndex['adoptionThreshold']]))
            cd_y[interestIndices[dataIndex['interestThreshold']]] = dataIndex['interestThreshold']
            print('IT ' + str(dataIndex['interestThreshold']) + ' is associated with index ' + str(adoptionIndices[dataIndex['interestThreshold']]))
            cd_z[adoptionIndices[dataIndex['adoptionThreshold']]][interestIndices[dataIndex['interestThreshold']]] = dataIndex['performance']
            print('performance at [' + str(adoptionIndices[dataIndex['adoptionThreshold']]) + '][' + str([interestIndices[dataIndex['interestThreshold']]]) + ' set to ' + str(dataIndex['performance']))
    #
    # colormap = cm.RdYlGn_r
    #     print(str(cd_x))
    #     print(str(cd_y))
    #     print(str(cd_z))
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.plot_surface(cd_x, cd_y, cd_z, cmap=colormap)
    #     ax.set_xlabel('Adoption Threshold')
    #     ax.set_ylabel('Interest Threshold')
    #     ax.set_zlabel('Error')
    #     plt.show()

# TODO document and generalize
def visualizeLinearRepresentationPlot(graphType, dataPath, n):
    cd_x = np.zeros(n, dtype=float)
    cd_y = np.zeros(n, dtype=float)
    cd_z = np.zeros(n, dtype=float)
    print(n)
    i = 0
    with open(dataPath, 'r') as file:
        for line in file:
            pointDict = eval(line)
            print(str(pointDict))
            cd_x[i] = pointDict['adoptionThreshold']
            cd_y[i] = pointDict['interestThreshold']
            cd_z[i] = pointDict['performance']
            i += 1
    fig = plt.figure()
    if(graphType == 'trisurf'):
        colormap = cm.RdYlGn_r
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(cd_x, cd_y, cd_z, cmap=colormap)
    ax.set_xlabel('Adoption Threshold')
    ax.set_ylabel('Interest Threshold')
    ax.set_zlabel('Error')
    plt.show()



# Function to plot different stats over several runs on three-dimensional surfaces based on different modes.
# The data to plot is represented as a list of dictionaries containing the values of the independent variabels (x and y)
# while the value of the dependent variables depends on the mode and provides certain statistics of different runs.
# Modes and required values for the statistics are as follows:
#   absolute: expresses the absolute differences between simulation runs
#       average: the average difference between different runs of the respective parameters
#       minSpread: the minimal difference between different runs of the respective parameters
#       maxSpread: the maximal difference between different runs of the respective parameters
#   relative: expresses the relative differences between simulation runs for each parameter combination
#       minSpread: the minimal difference between different runs of the respective parameters
#       maxSpread: the maximal difference between different runs of the respective parameters
#   averageCases: expresses the averaged differences between two compared scenarios
#       baseCaseAverage: the reference case data for the dependent variable
#       instrumentCaseAverage: the investigated case data for the dependent variable
#   averageCasesRelative: expresses the averaged differences between two compared scenarios
#       average: the average number of adoptions in the cases
#       baseCaseAverage: the reference case data for the dependent variable
#       instrumentCaseAverage: the investigated case data for the dependent variable
# TODO make more general regarding the dimensions and package somewhere else
def plotRunStatistics(analysisData, mode):
    n = len(analysisData)
    cd_x = np.zeros(n, dtype=float)
    cd_y = np.zeros(n, dtype=float)
    cd_z1 = np.zeros(n, dtype=float)
    cd_z2 = np.zeros(n, dtype=float)
    cd_z3 = np.zeros(n, dtype=float)
    i = 0
    for pointDict in analysisData:
        cd_x[i] = pointDict['adoptionThreshold']
        cd_y[i] = pointDict['interestThreshold']
        if(mode == 'absolute'):
            cd_z1[i] = pointDict['average']
            cd_z2[i] = pointDict['minSpread']
            cd_z3[i] = pointDict['maxSpread']
        elif(mode == 'relative'):
            cd_z1[i] = 1.0
            cd_z2[i] = pointDict['minSpreadRelative']
            cd_z3[i] = pointDict['maxSpreadRelative']
        elif(mode == 'averageCases'):
            cd_z1[i] = 0.0
            cd_z2[i] = pointDict['baseCaseAverage']
            cd_z3[i] = pointDict['instrumentCaseAverage']
        elif (mode == 'averageCasesRelative'):
            cd_z2[i] = pointDict['average'] / pointDict['baseCaseAverage']
            cd_z3[i] = pointDict['average'] / pointDict['instrumentCaseAverage']
            cd_z1[i] = (cd_z2[i] + cd_z3[i]) / 2.0
        i += 1
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if(mode == 'relative'):
        colormap = cm.Greys
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
        colormap = cm.inferno
        ax.plot_trisurf(cd_x, cd_y, cd_z2, cmap=colormap)
        colormap = cm.cividis
        ax.plot_trisurf(cd_x, cd_y, cd_z3, cmap=colormap)
    elif(mode == 'absolute'):
        colormap = cm.RdYlGn_r
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
    elif(mode == 'averageCases' or mode == 'averageCasesRelative'):
        colormap = cm.Greys
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
        colormap = cm.RdYlGn_r
        ax.plot_trisurf(cd_x, cd_y, cd_z2, cmap=colormap)
        ax.plot_trisurf(cd_x, cd_y, cd_z3, cmap=colormap)
    ax.set_xlabel('Adoption Threshold')
    ax.set_ylabel('Interest Threshold')
    if(mode == 'absolute'):
        ax.set_zlabel('Average Adoption Difference')
    elif(mode == 'relative'):
        ax.set_zlabel('Spread between Runs')
    elif(mode == 'averageCases'):
        ax.set_zlabel('Average Scenario Adoption')
    elif (mode == 'averageCasesRelative'):
        ax.set_zlabel('Relative Av. Scenario Adoption')
    plt.show()

# TODO document and generalize
def plotCumulatedAdoptions(adoptionFilePath, saveFile):
    with open(adoptionFilePath, 'r') as adoptionsFile:
        years = []
        modelResults = []
        realAdoptions = []
        i = 0
        for yearlyData in adoptionsFile:
            # print('line ' + str(yearlyData))
            if (i > 0):
                dataArray = yearlyData.split(';')
                # print(str(dataArray) + ' with length ' + str(len(dataArray)))
                # print('year ' + str(int(dataArray[0])) + ', model: ' + str(float(dataArray[1])) + ', real: ' + str(
                #     float(dataArray[2].strip())) + ', i: ' + str(i))
                years.append(int(dataArray[0]))
                modelResults.append(float(dataArray[1]))
                realAdoptions.append(float(dataArray[2].strip()))
                # print(str(years))
                # print(str(modelResults))
                # print(str(realAdoptions))
                # print('year ' + str(years[i-1]) + ', model: ' + str(modelResults[i-1]) + ', real: ' + str(realAdoptions[i-1]) + ', i: ' + str(i))
                i += 1
            else:
                i = 1
        # print(str(years))
        # print(str(modelResults))
        # print(str(realAdoptions))
        simulation = plt.plot(years, modelResults, label="Simulation results", color="#b02f2c")
        realData = plt.plot(years, realAdoptions, label="Actual adoptions", color="#8ac2d1")
        plt.ylabel('Installed PV systems')
        plt.xlabel('Years')
        plt.legend(handles=[simulation[0], realData[0]])
        # plt.show()
        plt.savefig(saveFile, bbox_inches='tight')
        plt.clf()

# Function to save the specified data into a file given by the prefix and the chosen error definition.
# Will append to the specified file and plot the data if the plotFlag is set.
# TODO document
def saveAndPlotEvaluationData(evaluationData, filePrefix, errorDefinition, plotFlag):
    print('saving and plotting')
    file = open(filePrefix + errorDefinition, "w")
    for i in range(len(evaluationData)):
        for j in range(len(evaluationData[i])):
            file.write(str(evaluationData[i][j])+'\n')
    file.close()
    if(plotFlag):
        visualizeData('trisurf', filePrefix + errorDefinition)