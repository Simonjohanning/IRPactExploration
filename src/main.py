import sys
import getopt
import simulationManager
import simulationRunner
import quickLauncher
import helper

# main function to read in and check the parameters, as well as invoking the optimization (in the simulationManager)
if __name__ == '__main__':
    simulationRunner.navigateToTop()
    argv = sys.argv[1:]
    # TODO include new parameters for MHs
    opts, args = getopt.getopt(argv, 'd:e:msr', ['acceptableDelta=', 'delta=', 'errorDef=', 'maxDepth=', 'scaleFactor=', 'resolution=', 'AT=', 'IT=', 'method=', 'AP=', 'IP=', 'runFile=', 'noRuns=', 'noRepetitions=', 'scenarioList=', 'lowerBoundAT=', 'upperBoundAT=', 'lowerBoundIT=', 'upperBoundIT=', 'inputFile='] )
    parameters = helper.setParameters(opts)
    quickLauncher.quickLaunch(parameters)
    # TODO make safe
    if ('errorDef' in parameters and 'method' in parameters):
        print(parameters)
        # invokation of the search
        simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, True)
    else:
        print('Please provide parameters errorDef and method')
