import gridDepthSearch
import sys
import getopt
import configuration
import simulationRunner

# module to initialize the optimization process and set the parameters.
# Serves to isolate the functionality of the individual optimization methods from the data

# function to manage the execution of the optimization by the chosen mode
def runOptimization(acceptableDelta, errorDefinition, optimizationMethod, parameters):
    if (optimizationMethod == 'gridDepthSearch'):
        # the grid depth search iteratively samples smaller / finer regions of the parameter space
        # equidistantly until close enough to the reference time series or a given number of iterations are reached
        # parameters are the acceptableDelta, maxDepth, scaleFactor, resolution and errorDefinition;
        # see function for further documentation
        maxDepth = parameters['maxDepth'] if ('maxDepth' in parameters) else configuration.defaults['maxDepth']
        scaleFactor = parameters['scaleFactor'] if ('scaleFactor' in parameters) else configuration.defaults['scaleFactor']
        resolution = parameters['resolution'] if ('resolution' in parameters) else configuration.defaults['resolution']
        print(gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition))

# main method to set up the logging and invoke the optimization management method function
if __name__ == '__main__':
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, 'd:e:msr', ['delta=', 'errorDef=', 'maxDepth=', 'scaleFactor=', 'resolution=', 'AT=', 'IT='])
    parameters = {}
    for o, a in opts:
        if o == '--delta':
            parameters['delta'] = a
        elif o == '--errorDef':
            parameters['errorDef'] = a
        elif o == '--maxDepth':
            parameters['maxDepth'] = a
        elif o == '--scaleFactor':
            parameters['scaleFactor'] = a
        elif o == '--resolution':
            parameters['resolution'] = a
        elif o == '--AT':
            parameters['AT'] = a
        elif o == '--IT':
            parameters['IT'] = a
        else:
            print('unrecognized parameter ' + str(a))
    if ('AT' in parameters and 'IT' in parameters):
        baseInputFile = 'src/modelInputFiles/changedInterest'
        simulationRunner.prepareJson(baseInputFile, parameters['AT'], parameters['IT'])
        simulationRunner.invokeJar(baseInputFile + '-' + str(parameters['AT'])[2:len(str(parameters['AT']))]  + '-' + str(parameters['IT']), parameters['errorDef'])
    # TODO make safe
    elif ('delta' in parameters and 'errorDef' in parameters):
        print(parameters)
        log_file = open("message.log", "w")
        sys.stdout = log_file
        # invokation of the search
        runOptimization(parameters['delta'], parameters['errorDef'], 'gridDepthSearch', parameters)
        log_file.close()
    else:
        print('Please provide parameters delta and errorDef')


