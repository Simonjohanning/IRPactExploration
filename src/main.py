import sys
import getopt
import simulationManager
import dataVisualization
import simulationRunner

# main method to set up the logging and invoke the optimization management method function
if __name__ == '__main__':
    #dataVisualization.visualizeData('trisurf', 'resources/gridDepthSearch-210-reduced')
    simulationRunner.navigateToTop()
    argv = sys.argv[1:]
    # include new parameters for MHs
    opts, args = getopt.getopt(argv, 'd:e:msr', ['acceptableDelta=', 'delta=', 'errorDef=', 'maxDepth=', 'scaleFactor=', 'resolution=', 'AT=', 'IT=', 'method=', 'AP=', 'IP='])
    print(opts)
    parameters = simulationManager.setParameters(opts)
    # TODO make safe
    if ('errorDef' in parameters and 'method' in parameters):
        print(parameters)
        # log_file = open("message.log", "w")
        # sys.stdout = log_file
        # invokation of the search
        simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters)
        # log_file.close()
    else:
        print('Please provide parameters errorDef and method')
