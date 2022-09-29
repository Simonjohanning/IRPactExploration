import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def visualizeData(graphType, dataPath):
    n = determineDataPoints(dataPath)
    if(graphType == 'trisurf'):
        visualizeLinearRepresentationPlot(graphType, dataPath, n)
    elif(graphType == 'barChart'):
        visualize2DRepresentationPlot(graphType, dataPath, n)

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

def determineDataPoints(dataPath):
    with open(dataPath, 'r') as file:
        return (len(file.readlines()))
