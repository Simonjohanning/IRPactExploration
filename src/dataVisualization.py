import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def visualizeData(graphType, dataPath):
    n = determineDataPoints(dataPath)
    cd_x = np.zeros(n, dtype=float)
    cd_y = np.zeros(n, dtype=float)
    cd_z = np.zeros(n, dtype=float)
    i = 0
    with open(dataPath, 'r') as file:
        for line in file:
            pointDict = eval(line)
            cd_x[i] = pointDict['adoptionThreshold']
            cd_y[i] = pointDict['interestThreshold']
            cd_z[i] = pointDict['performance']
            i += 1
    fig = plt.figure()
    colormap = cm.RdYlGn_r
    if(graphType == 'trisurf'):
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(cd_x, cd_y, cd_z, cmap=colormap)
        ax.set_xlabel('Adoption Threshold')
        ax.set_ylabel('Interest Threshold')
        ax.set_zlabel('Error')
        plt.show()


def determineDataPoints(dataPath):
    with open(dataPath, 'r') as file:
        return (len(file.readlines()))