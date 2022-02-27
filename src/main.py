import gridDepthSearch
import sys

# module to initialize the optimization process and set the parameters.
# Serves to isolate the functionality of the individual optimization methods from the data

# function to manage the execution of the optimization by the chosen mode
def runOptimization(acceptableDelta, errorDefinition, optimizationMethod):
    if (optimizationMethod == 'gridDepthSearch'):
        # the grid depth search iteratively samples smaller / finer regions of the parameter space
        # equidistantly until close enough to the reference time series or a given number of iterations are reached
        # parameters are the acceptableDelta, maxDepth, scaleFactor, resolution and errorDefinition;
        # see function for further documentation
        print(gridDepthSearch.iterateGridDepthSearch(acceptableDelta, 5, 2, 3, errorDefinition))

# main method to set up the logging and invoke the optimization management method function
if __name__ == '__main__':
    log_file = open("message.log", "w")
    sys.stdout = log_file
    # invokation of the search
    runOptimization(0.15, 'RMSD', 'gridDepthSearch')
    log_file.close()



