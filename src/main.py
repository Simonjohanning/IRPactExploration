import sys
import getopt
import simulationManager
import quickLauncher
import helper
import os

# main function to read in and check the parameters, as well as invoking the optimization (in the simulationManager)
if __name__ == '__main__':
    # navigate to the root folder of the project source
    os.chdir(sys.argv[0][:len(sys.argv[0]) - 7])
    print(os.getcwd())
    argv = sys.argv[1:]
    # TODO include new parameters for MHs
    opts, args = getopt.getopt(argv, 'd:e:msr', ['acceptableDelta=', 'delta=', 'errorDef=', 'maxDepth=', 'scaleFactor=', 'resolution=', 'AT=', 'IT=', 'method=', 'AP=', 'IP=', 'runFile=', 'noRuns=', 'noRepetitions=', 'scenarioList=', 'lowerBoundAT=', 'upperBoundAT=', 'lowerBoundIT=', 'upperBoundIT=', 'inputFile=', 'model=', 'adoptionThreshold=', 'interestThreshold=', 'quickLaunch=', 'parallelExecution='] )
    parameters = helper.setParameters(opts)
    if(('quickLaunch' in parameters) and (parameters['quickLaunch'] == True)):
        quickLauncher.quickLaunch(parameters)
    else:
        if ('errorDef' in parameters and 'method' in parameters and 'model' in parameters):
            print(parameters)
            # invocation of the search
            simulationManager.runSimulations(parameters['model'], parameters['errorDef'], parameters['method'], parameters, True)
        else:
            print('Please provide parameters errorDef, model and method')
