import json
import os

# Simple helper function to determine the number of (line-based) data points in the specified file
def determineDataPoints(dataPath):
    with open(dataPath, 'r') as file:
        return (len(file.readlines()))

# Helper function to extract the total number of cumulated adoptions from the provided file
# @TODO make more general
def extractData(path):
    f = open(path, "r")
    fileData = json.loads(f.read())
    return fileData['cumulated']['total']


# Function that sets the parameter map based on the inline parameters the script was invoked with.
# The function reads the inline parameters and assigns them to the respective parameter
def setParameters(opts):
    print(opts)
    parameters = {}
    for o, a in opts:
        if o == '--acceptableDelta':
            parameters['acceptableDelta'] = a
        elif o == '--delta':
            parameters['acceptableDelta'] = a
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
        elif o == '--method':
            parameters['method'] = a
        elif o == '--AP':
            parameters['AP'] = a
        elif o == '--IP':
            parameters['IP'] = a
        elif o == '--maximum_attempt':
            parameters['maximum_attempt'] = a
        elif o == '--pitch_adjusting_range':
            parameters['pitch_adjusting_range'] = a
        elif o == '--harmony_search_size':
            parameters['harmony_search_size'] = a
        elif o == '--harmony_memory_acceping_rate':
            parameters['harmony_memory_acceping_rate'] = a
        elif o == '--pitch_adjusting_rate':
            parameters['pitch_adjusting_rate'] = a
        elif o == '--number_of_fireflies':
            parameters['number_of_fireflies'] = a
        elif o == '--maximum_generation':
            parameters['maximum_generation'] = a
        elif o == '--randomization_parameter_alpha':
            parameters['randomization_parameter_alpha'] = a
        elif o == '--absorption_coefficient_gamma':
            parameters['absorption_coefficient_gamma'] = a
        elif o == '--number_of_particles':
            parameters['number_of_particles'] = a
        elif o == '--number_of_iterations':
            parameters['number_of_iterations'] = a
        elif o == '--social_coefficient':
            parameters['social_coefficient'] = a
        elif o == '--random_variable_coefficient':
            parameters['random_variable_coefficient'] = a
        elif o == '--temperature':
            parameters['temperature'] = a
        elif o == '--minimal_temperature':
            parameters['minimal_temperature'] = a
        elif o == '--maximum_number_of_rejections':
            parameters['maximum_number_of_rejections'] = a
        elif o == '--maximum_number_of_runs':
            parameters['maximum_number_of_runs'] = a
        elif o == '--maximum_number_of_acceptances':
            parameters['maximum_number_of_acceptances'] = a
        elif o == '--bolzmann_constant':
            parameters['bolzmann_constant'] = a
        elif o == '--cooling_factor':
            parameters['cooling_factor'] = a
        elif o == '--energy_norm':
            parameters['energy_norm'] = a
        elif o == '--standard_deviation_for_estimation':
            parameters['standard_deviation_for_estimation'] = a
        elif o == '--ratio_of_energy_delta_over_evaluation_delta':
            parameters['ratio_of_energy_delta_over_evaluation_delta'] = a
        elif o == '--population_size':
            parameters['population_size'] = a
        elif o == '--maximum_number_of_generations':
            parameters['maximum_number_of_generations'] = a
        elif o == '--number_of_mutation_sites':
            parameters['number_of_mutation_sites'] = a
        elif o == '--crossover_probability':
            parameters['crossover_probability'] = a
        elif o == '--mutation_probability':
            parameters['mutation_probability'] = a
        elif o == '--runFile':
            parameters['runFile'] = a
        elif o == '--noRuns':
            parameters['noRuns'] = a
        elif o == '--noRepetitions':
            parameters['noRepetitions'] = a
        elif o == '--scenarioList':
            parameters['scenarioList'] = a
        elif o == '--lowerBoundAT':
            parameters['lowerBoundAT'] = a
        elif o == '--upperBoundAT':
         parameters['upperBoundAT'] = a
        elif o == '--lowerBoundIT':
            parameters['lowerBoundIT'] = a
        elif o == '--upperBoundIT':
            parameters['upperBoundIT'] = a
        elif o == '--inputFile':
            parameters['inputFile'] = a
        else:
            raise NotImplementedError('unrecognized parameter ' + str(o))
    return parameters

# TODO make more general
def navigateToTop():
    currentDir = os.getcwd().split('\\')[-1]
    #print(currentDir)
    if (currentDir == 'C:\\'):
        os.chdir('Users\mai11dlx\PycharmProjects\IRPactExploration')
    elif (not currentDir == 'IRPactExploration'):
        print('current dir is ' + os.getcwd() + '; navigating up')
        os.chdir('../')
        navigateToTop()

# TODO document and test
def printMissingParameters(parameterDictionary, parameterArray):
    missingParameters = []
    for parameter in parameterArray:
        if(not parameter in parameterDictionary):
            missingParameters.append(parameter)
    if(len(missingParameters) > 1):
        print('Missing parameters: \n')
        for parameter in missingParameters:
            print(parameter)
    elif(len(missingParameters) == 1):
        print('Parameter ' + missingParameters[0] + ' missing.')

# Method to translate the model-agnostic parameters into the semantics of the model
# TODO document better
def convertGridInMode(X, Y, mode):
    if(mode == 'PVact'):
        return {'AT': X, 'IT': Y}
    else:
        raise NotImplementedError('Mode ' + mode + ' is not implemented')