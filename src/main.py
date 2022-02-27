import gridDepthSearch
import sys


def runOptimization(acceptableDelta, errorDefinition, optimizationMethod):
    if (optimizationMethod == 'gridDepthSearch'):
        gridDepthSearch.iterateGridDepthSearch(acceptableDelta, 5, 2, 3, errorDefinition)

if __name__ == '__main__':
    log_file = open("message.log", "w")
    sys.stdout = log_file
    runOptimization(0.15, 'RMSD', 'gridDepthSearch')
    log_file.close()



