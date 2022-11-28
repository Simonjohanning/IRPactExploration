"""
Module to manage and setup the execution of the simulation/optimization runs.
Provides a number of functions to invoke different simulation/optimization methods
as well as the interface for other modules to trigger the methods based on parameters.
Module serves to isolate the functionality of the individual optimization methods from the data.
Imported optimization methods are taken from the metaheuristic package https://pypi.org/project/metaheuristic-algorithms-python/
"""

import math
import gridDepthSearch
import configuration
import simulationRunner
import neighborRefiningSearch
import PVactWrapper
from metaheuristic_algorithms.harmony_search import HarmonySearch
from metaheuristic_algorithms.firefly_algorithm import FireflyAlgorithm
from metaheuristic_algorithms.simplified_particle_swarm_optimization import SimplifiedParticleSwarmOptimization
from metaheuristic_algorithms.simulated_annealing import SimulatedAnnealing
from metaheuristic_algorithms.genetic_algorithm import GeneticAlgorithm
import random
import multiprocessing as mp

import simulationPlotter
import simulationAnalyser
import configurationPVact

import PVactModelHelper

# TODO package a bunch of more concrete stuff here in a library and separate setup and execution


# TODO finish arguments documentation
def runSimulations(model, errorDefinition, executionMethod, parameters, plotFlag):
    """
    Function to invoke the simulation execution methods based on the specified execution method.
    Selects and prepares the data for the non-optimization-based execution methods detailed below or invokes the respective optimization method.
    Implemented execution methods not directly bound in optimization are:
       pvactval: generates the data and statistics for several instances of the scenarios based on the scenario list
       multipleRuns: runs simulations for a specified number of repetitions for the same parameters and stores the results
       plotRuns: plotRuns executes and plots single runs specified in the runFile
    The parameters for the respective models are documented in the readme file.

    :param model:
    :param errorDefinition:
    :param executionMethod:
    :param parameters:
    :param plotFlag:
    :return:
    """
    if (executionMethod == 'pvactval'):
        if ('noRepetitions' in parameters and 'scenarioList' in parameters and 'resolution' in parameters and 'lowerBoundAT' in parameters and 'upperBoundAT' in parameters and 'lowerBoundIT' in parameters and 'upperBoundIT' in parameters and 'AP' in parameters and 'IP' in parameters):
            scenarioFiles = parameters['scenarioList'].split(',')
            print('reading ' + str(len(scenarioFiles)) + ' scenarios files ')
            # TODO Make the parallel execution more generic and move parallel/sequential decision into one forwardRun function at the appropriate point
            print('parallelExecution' in parameters and parameters['parallelExecution'])
            if('parallelExecution' in parameters and parameters['parallelExecution']):
                parameterPerformance = createParallelForwardRuns(scenarioFiles, float(parameters['noRepetitions']),
                                                         int(parameters['resolution']), parameters['errorDef'],
                                                         float(parameters['lowerBoundAT']),
                                                         float(parameters['upperBoundAT']),
                                                         float(parameters['lowerBoundIT']),
                                                         float(parameters['upperBoundIT']),
                                                         {'AP': float(parameters['AP']), 'IP': float(parameters['IP'])},
                                                         'PVact')
                # TODO make less hacky and specific here
                analysisData = simulationAnalyser.analyseScenarioPerformance(parameterPerformance,
                                                                             float(parameters['lowerBoundAT']),
                                                                             float(parameters['upperBoundAT']),
                                                                             float(parameters['lowerBoundIT']),
                                                                             float(parameters['upperBoundIT']),
                                                                             scenarioFiles)
            else:
                parameterPerformance = createForwardRuns(scenarioFiles, float(parameters['noRepetitions']), int(parameters['resolution']), parameters['errorDef'], float(parameters['lowerBoundAT']), float(parameters['upperBoundAT']), float(parameters['lowerBoundIT']), float(parameters['upperBoundIT']),  {'AP': float(parameters['AP']), 'IP': float(parameters['IP'])}, 'PVact')
                # TODO make less hacky and specific here
                analysisData = simulationAnalyser.analyseScenarioPerformance(parameterPerformance,
                                                              float(parameters['lowerBoundAT']),
                                                              float(parameters['upperBoundAT']),
                                                              float(parameters['lowerBoundIT']),
                                                              float(parameters['upperBoundIT']), scenarioFiles)
            simulationPlotter.plotRunStatistics(analysisData, 'relative', model)
        else:
            print(parameters)
            print('noRepetitions' in parameters)
            print('scenarioList' in parameters)
            print('resolution' in parameters)
            print('lowerBoundAT' in parameters)
            print('upperBoundAT' in parameters)
            print('lowerBoundIT' in parameters)
            print('upperBoundIT' in parameters)
            print('AP' in parameters)
            print('IP' in parameters)
    elif (executionMethod == 'multipleRuns'):
        for index in range(int(parameters['noRuns'])):
            singleRunAndPlot(parameters, errorDefinition, 'run' + str(index))
            #TODO delete
                # print('written out in file plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(
                # parameters['IP']) + '-' + str(parameters['AP']) + '-' + str(parameters['IT']) + '-runError-' + str(
                # index) + '.png')
    elif (executionMethod == 'plotRuns'):
        if ('runFile' in parameters):
            # go through all runs in file and do single runs with consecutive plot
            with open(parameters['runFile'], 'r') as file:
                for line in file:
                    singleRunAndPlot({**parameters, **eval(line)}, errorDefinition, '')
    elif (executionMethod == 'PVact_forwardRuns'):
        scenarioFiles = parameters['scenarioList'].split(',')
        createForwardRuns(scenarioFiles, float(parameters['noRepetitions']), float(parameters['resolution']), errorDefinition, float(parameters['lowerBoundAT']), float(parameters['upperBoundAT']), float(parameters['lowerBoundIT']), float(parameters['upperBoundIT']), {'AP': float(parameters['AP']), 'IP': float(parameters['IP'])}, 'PVact')
    elif (executionMethod == 'runAndPlot'):
        print('in runAndPlot')
        singleRunAndPlot({**parameters, 'model': model}, errorDefinition, '')
    else:
        runOptimization(errorDefinition, executionMethod, parameters, plotFlag)

def runOptimization(errorDefinition, optimizationMethod, parameters, plotFlag):
    """
    Function that runs the parameter optimization based on the specified parameters.
    Individual simulations will be evaluated based on the errorDefinition with given parameters
    and are optimized based on the specified optimizationMethod with the goal of error minimization
    If the plotFlag is set, optimization methods using it will plot results between runs.
    Implemented optimization methods include:
        gridDepthSearch: optimization method where values are sampled within a grid of regular intervals that gets consecutively finer around the local minimum of the last execution
        neighborRefiningSearch: optimization method in which the investigated parameter grid is surveyed by evaluating points in the grid are added based on the distance to evaluated points and their error term,
        harmonySearch (from the metaheuristic algorithm package),
        firefly (from the metaheuristic algorithm package),
        SimplifiedParticleSwarmOptimization (from the metaheuristic algorithm package),
        simulatedAnnealing (from the metaheuristic algorithm package),
        geneticAlgorithm (from the metaheuristic algorithm package).

    :param errorDefinition: the metric used to evaluate runs
    :param optimizationMethod: the method chosen for parameter optimization
    :param parameters: general and optimization-method specific parameters (see readme)
    :param plotFlag: flag to indicate that the results should be plotted
    :return:
    """
    objective = "minimization"
    optimizationWrapper = None
    if parameters['errorDef'] == 'MAE':
        optimizationWrapper = PVactWrapper.PVactWrapperMAE()
    elif parameters['errorDef'] == 'RMSD':
        optimizationWrapper = PVactWrapper.PVactWrapperRMSE()
    if (optimizationMethod == 'gridDepthSearch'):
        executeGridDepthSearch(errorDefinition, parameters, plotFlag)
    elif (optimizationMethod == 'neighborRefiningSearch'):
        neighborRefiningSearch.neighborRefining(errorDefinition, parameters['model'], parameters['inputFile'])
    elif (optimizationMethod == 'harmonySearch'):
        runHarmonySearch(optimizationWrapper, parameters, objective)
    elif (optimizationMethod == 'firefly'):
        runFirefly(optimizationWrapper, parameters, objective)
    elif (optimizationMethod == 'spso'):
        runSimplifiedParticleSwarmOptimization(optimizationWrapper, parameters, objective)
    elif (optimizationMethod == 'simulatedAnnealing'):
        runSimulatedAnnealing(optimizationWrapper, parameters, objective)
    elif (optimizationMethod == 'geneticAlgorithm'):
        runGeneticAltgorithm(optimizationWrapper, parameters, objective)
    else:
        print('method ' + optimizationMethod + ' is not known. Please provide a valid method')

def executeGridDepthSearch(errorDefinition, parameters, plotFlag):
    """
    This function sets up the GridDepthSearch algorithm and triggers its execution based on the provided 
    error metric and parameters. 
    the grid depth search iteratively samples smaller / finer regions of the parameter space
    equidistantly until close enough to the reference time series or a given number of iterations are reached
    Model-agnostic parameters are the acceptableDelta, maxDepth, scaleFactor and resolution;
    For specific models, bounds, data and the file naming are set. 
    See Readme for further documentation
    :param errorDefinition: a string for the error metric to be used 
    :param parameters: dictionary containing at least the necessary parameters
    :param plotFlag: flag to indicate if the simulation result should be plotted
    :return: 
    """
    if(not 'model' in parameters):
        raise KeyError('Key model not set in parameters for gridDepthSearch')
    else:
        # general parameters
        maxDepth = parameters['maxDepth'] if ('maxDepth' in parameters) else configuration.gds_defaults['maxDepth']
        scaleFactor = parameters['scaleFactor'] if ('scaleFactor' in parameters) else configuration.gds_defaults[
            'scaleFactor']
        resolution = parameters['resolution'] if ('resolution' in parameters) else configuration.gds_defaults[
            'resolution']
        acceptableDelta = parameters['acceptableDelta'] if ('acceptableDelta' in parameters) else \
            configuration.gds_defaults['acceptableDelta']
        # model=specific parameters
        lowerBoundX = None
        upperBoundX = None
        lowerBoundY = None
        upperBoundY = None
        modelPrefix = None
        inputFile = None
        if(parameters['model'] == 'PVact'):
            lowerBoundX = parameters['lowerBoundX'] if ('lowerBoundX' in parameters) else configurationPVact.optimizationBounds[
                'minAdoptionThreshold']
            upperBoundX = parameters['upperBoundX'] if ('upperBoundX' in parameters) else configurationPVact.optimizationBounds[
                'maxAdoptionThreshold']
            lowerBoundY = parameters['lowerBoundY'] if ('lowerBoundY' in parameters) else configurationPVact.optimizationBounds[
                'minInterestThreshold']
            upperBoundY = parameters['upperBoundY'] if ('upperBoundY' in parameters) else configurationPVact.optimizationBounds[
                'maxInterestThreshold']
            modelPrefix = PVactModelHelper.deriveFilePrefixGDS(parameters)
            inputFile = parameters['inputFile'] if ('inputFile' in parameters) else configurationPVact.baseInputFile
        else:
            raise NotImplementedError('model ' + parameters['model'] + ' is not implemented.')
        optimizationResult = gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition, parameters, inputFile, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY)
        print(optimizationResult)
        simulationPlotter.saveAndPlotEvaluationData(optimizationResult['evaluationData'],
                                                    modelPrefix, errorDefinition, plotFlag)

def runHarmonySearch(optimizationWrapper, parameters, objective):
    """
    Function to manage the harmony search metaheuristic from the https://pypi.org/project/metaheuristic-algorithms-python/ package.
    
    :param optimizationWrapper: A model and error metric specific wrapper for the metaheuristic
    :param parameters: A dictionary containing parameters relevant for harmony search 
    :param objective: The optimization objective used in the metaheuristic
    :return: 
    """
    if optimizationWrapper is None:
        pass
    else:
        harmony_search = HarmonySearch(optimizationWrapper, configuration.number_of_variables, objective)
        maximum_attempt = parameters['maximum_attempt'] if ('maximum_attempt' in parameters) else \
            configuration.harmony_defaults['maximum_attempt']
        pitch_adjusting_range = parameters['pitch_adjusting_range'] if ('pitch_adjusting_range' in parameters) else \
            configuration.harmony_defaults['pitch_adjusting_range']
        harmony_search_size = parameters['harmony_search_size'] if ('harmony_search_size' in parameters) else \
            configuration.harmony_defaults['harmony_search_size']
        harmony_memory_acceping_rate = parameters['harmony_memory_acceping_rate'] if (
                'harmony_memory_acceping_rate' in parameters) else configuration.harmony_defaults[
            'harmony_memory_acceping_rate']
        pitch_adjusting_rate = parameters['pitch_adjusting_rate'] if ('pitch_adjusting_rate' in parameters) else \
            configuration.harmony_defaults['pitch_adjusting_rate']
        result = harmony_search.search(maximum_attempt=maximum_attempt,
                                       pitch_adjusting_range=pitch_adjusting_range,
                                       harmony_search_size=harmony_search_size,
                                       harmony_memory_acceping_rate=harmony_memory_acceping_rate,
                                       pitch_adjusting_rate=pitch_adjusting_rate)

        print(result["best_decision_variable_values"][0])  # x value: Example: 1.0112
        print(result["best_decision_variable_values"][1])  # y value: Example: 0.9988
        print(result["best_objective_function_value"])  # f(x,y) value: Example: 0.0563

def runFirefly(optimizationWrapper, parameters, objective):
    """
        Function to manage the firefly metaheuristic from the https://pypi.org/project/metaheuristic-algorithms-python/ package.

        :param optimizationWrapper: A model and error metric specific wrapper for the metaheuristic
        :param parameters: A dictionary containing parameters relevant for the firefly algorithm 
        :param objective: The optimization objective used in the metaheuristic
        :return: 
        """
    if optimizationWrapper is None:
        pass
    else:
        firefly = FireflyAlgorithm(optimizationWrapper, configuration.number_of_variables, objective)
        number_of_fireflies = parameters['number_of_fireflies'] if ('number_of_fireflies' in parameters) else \
            configuration.firefly_defaults['number_of_fireflies']
        maximum_generation = parameters['maximum_generation'] if ('maximum_generation' in parameters) else \
            configuration.firefly_defaults['maximum_generation']
        randomization_parameter_alpha = parameters['randomization_parameter_alpha'] if (
                'randomization_parameter_alpha' in parameters) else configuration.firefly_defaults[
            'randomization_parameter_alpha']
        absorption_coefficient_gamma = parameters['absorption_coefficient_gamma'] if (
                'absorption_coefficient_gamma' in parameters) else configuration.firefly_defaults[
            'absorption_coefficient_gamma']
        result = firefly.search(number_of_fireflies=number_of_fireflies,
                                maximun_generation=maximum_generation,
                                randomization_parameter_alpha=randomization_parameter_alpha,
                                absorption_coefficient_gamma=absorption_coefficient_gamma)
        print(result["best_decision_variable_values"][0])  # x value: Example: 1.0112
        print(result["best_decision_variable_values"][1])  # y value: Example: 0.9988
        print(result["best_objective_function_value"])  # f(x,y) value: Example: 0.0563

def runSimplifiedParticleSwarmOptimization(optimizationWrapper, parameters, objective):
    """
        Function to manage the spso metaheuristic from the https://pypi.org/project/metaheuristic-algorithms-python/ package.

        :param optimizationWrapper: A model and error metric specific wrapper for the metaheuristic
        :param parameters: A dictionary containing parameters relevant for spso 
        :param objective: The optimization objective used in the metaheuristic
        :return: 
        """
    if optimizationWrapper is None:
        pass
    else:
        spso = SimplifiedParticleSwarmOptimization(optimizationWrapper, configuration.number_of_variables, objective)
        number_of_particles = parameters['number_of_particles'] if ('number_of_particles' in parameters) else \
            configuration.spso_defaults['number_of_particles']
        number_of_iterations = parameters['number_of_iterations'] if ('number_of_iterations' in parameters) else \
            configuration.spso_defaults['number_of_iterations']
        social_coefficient = parameters['social_coefficient'] if ('social_coefficient' in parameters) else \
            configuration.spso_defaults['social_coefficient']
        random_variable_coefficient = parameters['random_variable_coefficient'] if (
                'random_variable_coefficient' in parameters) else configuration.spso_defaults[
            'random_variable_coefficient']
        result = spso.search(number_of_particiles=number_of_particles,
                             number_of_iterations=number_of_iterations,
                             social_coefficient=social_coefficient,
                             random_variable_coefficient=random_variable_coefficient)
        print(result["best_decision_variable_values"][0])  # x value: Example: 1.0112
        print(result["best_decision_variable_values"][1])  # y value: Example: 0.9988
        print(result["best_objective_function_value"])  # f(x,y) value: Example: 0.0563

def runSimulatedAnnealing(optimizationWrapper, parameters, objective):
    """
    Function to manage the simulated annealing metaheuristic from the https://pypi.org/project/metaheuristic-algorithms-python/ package.

    :param optimizationWrapper: A model and error metric specific wrapper for the metaheuristic
    :param parameters: A dictionary containing parameters relevant for simulated annealing 
    :param objective: The optimization objective used in the metaheuristic
    :return: 
    """
    if optimizationWrapper is None:
        pass
    else:
        if parameters['errorDef'] == 'MAE':
            optimizationWrapper = PVactWrapper.PVactWrapperMAESingleVariable()
        elif parameters['errorDef'] == 'RMSD':
            optimizationWrapper = PVactWrapper.PVactWrapperRMSESingleVariable()
        simulatedAnnealing = SimulatedAnnealing(optimizationWrapper, 1, objective)
        temperature = parameters['temperature'] if ('temperature' in parameters) else \
            configuration.simulatedAnnealing_defaults['temperature']
        minimal_temperature = parameters['minimal_temperature'] if ('minimal_temperature' in parameters) else \
            configuration.simulatedAnnealing_defaults['minimal_temperature']
        maximum_number_of_rejections = parameters['maximum_number_of_rejections'] if (
                'maximum_number_of_rejections' in parameters) else configuration.simulatedAnnealing_defaults[
            'maximum_number_of_rejections']
        maximum_number_of_runs = parameters['maximum_number_of_runs'] if (
                'maximum_number_of_runs' in parameters) else configuration.simulatedAnnealing_defaults[
            'maximum_number_of_runs']
        maximum_number_of_acceptances = parameters['maximum_number_of_acceptances'] if (
                'maximum_number_of_acceptances' in parameters) else configuration.simulatedAnnealing_defaults[
            'maximum_number_of_acceptances']
        bolzmann_constant = parameters['bolzmann_constant'] if ('bolzmann_constant' in parameters) else \
            configuration.simulatedAnnealing_defaults['bolzmann_constant']
        cooling_factor = parameters['cooling_factor'] if ('cooling_factor' in parameters) else \
            configuration.simulatedAnnealing_defaults['cooling_factor']
        energy_norm = parameters['energy_norm'] if ('energy_norm' in parameters) else \
            configuration.simulatedAnnealing_defaults['energy_norm']
        standard_deviation_for_estimation = parameters['standard_deviation_for_estimation'] if (
                'standard_deviation_for_estimation' in parameters) else \
            configuration.simulatedAnnealing_defaults['standard_deviation_for_estimation']
        ratio_of_energy_delta_over_evaluation_delta = parameters['ratio_of_energy_delta_over_evaluation_delta'] if (
                'ratio_of_energy_delta_over_evaluation_delta' in parameters) else \
            configuration.simulatedAnnealing_defaults['ratio_of_energy_delta_over_evaluation_delta']
        result = simulatedAnnealing.search(temperature=temperature,
                                           minimal_temperature=minimal_temperature,
                                           maximum_number_of_rejections=maximum_number_of_rejections,
                                           maximum_number_of_runs=maximum_number_of_runs,
                                           maximum_number_of_acceptances=maximum_number_of_acceptances,
                                           bolzmann_constant=bolzmann_constant,
                                           cooling_factor=cooling_factor,
                                           energy_norm=energy_norm,
                                           standard_diviation_for_estimation=standard_deviation_for_estimation,
                                           ratio_of_energy_delta_over_evaluation_delta=ratio_of_energy_delta_over_evaluation_delta)
        print(result["best_decision_variable_values"])  # x value: Example: 1.0112
        print(result["best_objective_function_value"])  # f(x,y) value: Example: 0.0563

def runGeneticAltgorithm(optimizationWrapper, parameters, objective):
    """
    Function to manage the genetic algorithm metaheuristic from the https://pypi.org/project/metaheuristic-algorithms-python/ package.

    :param optimizationWrapper: A model and error metric specific wrapper for the metaheuristic
    :param parameters: A dictionary containing parameters relevant for the genetic algorithm 
    :param objective: The optimization objective used in the metaheuristic
    :return: 
    """
    if optimizationWrapper is None:
        pass
    else:
        ga = GeneticAlgorithm(optimizationWrapper, configuration.number_of_variables, objective)
        population_size = parameters['population_size'] if ('population_size' in parameters) else \
            configuration.geneticAlgorithm_default['population_size']
        maximum_number_of_generations = parameters['maximum_number_of_generations'] if (
                'maximum_number_of_generations' in parameters) else configuration.geneticAlgorithm_default[
            'maximum_number_of_generations']
        number_of_mutation_sites = parameters['number_of_mutation_sites'] if (
                'number_of_mutation_sites' in parameters) else configuration.geneticAlgorithm_default[
            'number_of_mutation_sites']
        crossover_probability = parameters['crossover_probability'] if ('crossover_probability' in parameters) else \
            configuration.geneticAlgorithm_default['crossover_probability']
        mutation_probability = parameters['mutation_probability'] if ('mutation_probability' in parameters) else \
            configuration.geneticAlgorithm_default['mutation_probability']
        result = ga.search(population_size=population_size,
                           maximum_number_of_generations=maximum_number_of_generations,
                           number_of_mutation_sites=number_of_mutation_sites,
                           crossover_probability=crossover_probability,
                           mutation_probability=mutation_probability
                           )
        print(result["best_decision_variable_values"][0])  # x value: Example: 1.0112
        print(result["best_decision_variable_values"][1])  # y value: Example: 0.9988
        print(result["best_objective_function_value"])  # f(x,y) value: Example: 0.0563


def singleRunAndPlot(parameters, errorDefinition, plotfileSuffix):
    """
    # Function to execute a single run and to plot the results based on the cumulated adoptions
    # for the simulation and the reference data for the simulated years.
    # Saves the image of the plot in the plot folder with a file name based on the parameters

    :param parameters: dictionary containing at least parameters required for generating JSON & executing the model (see documentation)
    :param errorDefinition: the error definition for the model result
    :param plotfileSuffix: suffix for naming the resulting image file
    :return: -
    """
    # set the required strings by the model based on model requirements
    configurationFile = None
    plotfileRootname = None
    outputDataFile = None
    if (not 'model' in parameters):
        raise KeyError('Key "model" not provided in the parameters')
    elif (parameters['model'] == 'PVact'):
        configurationFile = PVactModelHelper.prepareJSONRand(parameters)
        plotfileRootname = PVactModelHelper.generateRootname(parameters)
        outputDataFile = configurationPVact.outputDataFile
    if(configurationFile and plotfileRootname and outputDataFile):
        returnData = simulationRunner.invokeJar(configurationFile, parameters['errorDef'], parameters['model'], 1)
        simulationPlotter.plotYearlySimulationReferenceData(outputDataFile, '../plots/' + errorDefinition + '-' + plotfileRootname + '-' + str(returnData) + '-' + plotfileSuffix + '.png', parameters['model'])
    else:
        raise NotImplementedError('Mandatory model-specific data has not been set. This might be an omission')


def createForwardRuns(scenarioFiles, noRepetitions, granularity, errorDef, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, modelSpecificParameters, model):
    """
    Function to generate and execute a number of simulation executions over an equally spaced parameter region based on the parameters
    
    :param scenarioFiles: list of the scenarios to execute the simulation runs for
    :param noRepetitions: the number of simulation runs for each parameter combination and scenario
    :param granularity: the number of parameter values to span the grid over for each dimension
    :param errorDef: the error metric to be used
    :param lowerBoundX: the minimum value for the model parameter in the x-dimension
    :param upperBoundX: the maximum value for the model parameter in the x-dimension
    :param lowerBoundY: the minimum value for the model parameter in the y-dimension
    :param upperBoundY: the maximum value for the model parameter in the x-dimension
    :param modelSpecificParameters: simulation execution parameters specific to the model used
    :param model: the model employed for the simuation
    :return: A list containing analysis for every parameter combination between the scenarios comprising the x and y coordinates and the average, maxSpread, minSpread, maxSpreadRelative, minSpreadRelative between the cases as well as the baseCaseAverage and the instrumentCaseAverage
    """
    print('creating runs')
    seedSet = set()
    parameterPerformance = [[{} for col in range(granularity)] for row in range(granularity)]
    # create the number of runs (repetitions of all parameter combinations) by initializing the seeds and calculating the relevant parameters
    for l in range(int(noRepetitions * math.pow(granularity, 2))):
        currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        while(currentSeed in seedSet):
            currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        seedSet.add(currentSeed)
        indexX = (math.floor(l/noRepetitions) % granularity)
        indexY = (math.floor(l/(noRepetitions * granularity)))
        currentX = lowerBoundX + (indexX * (upperBoundX - lowerBoundX) / (granularity - 1))
        currentY = lowerBoundY + (indexY * (upperBoundY - lowerBoundY) / (granularity - 1))
        scenarioPerformance = {}
        # For each scenario calculate and store the results
        for currentScenario in scenarioFiles:
            jarPath = None
            if(model == 'PVact'):
                modeParameters = {'adoptionThreshold': currentX, 'interestThreshold': currentY, 'currentSeed': currentSeed}
                modeParameters['AP'] = int(modelSpecificParameters['AP']) if 'AP' in modelSpecificParameters else configurationPVact.gds_defaults['AP']
                modeParameters['IP'] = int(modelSpecificParameters['IP']) if 'IP' in modelSpecificParameters else configurationPVact.gds_defaults['IP']
                jarPath = simulationRunner.prepareJson(currentScenario, 'PVact', modeParameters, configuration.scenarioPath + currentScenario + '.json')
            if(jarPath):
                # Invoke the simulation run with the respective scenario data (as dataDirPath)
                simulationRunner.invokeJarExternalData(jarPath, errorDef, l, 'resources/dataFiles/')
            else:
                print('Error! No model was set so no configuration file was created for this run')
            if(model == 'PVact'):
                scenarioPerformance[currentScenario] = PVactModelHelper.readAnalysisData('resources/simulationFiles/images/AdoptionAnalysis.json')
            print(str(scenarioPerformance))
        parameterPerformance[indexX][indexY][currentSeed] = scenarioPerformance
        print(str(parameterPerformance[indexX][indexY]))
    # Return the analysis of the data to the invoking function
    return simulationAnalyser.analyseScenarioPerformance(parameterPerformance, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, scenarioFiles)

def createParallelForwardRuns(scenarioFiles, noRepetitions, granularity, errorDef, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, modelSpecificParameters, model):
    """
    Function to generate and execute a number of simulation executions over an equally spaced parameter region in parallel

    :param scenarioFiles: list of the scenarios to execute the simulation runs for
    :param noRepetitions: the number of simulation runs for each parameter combination and scenario
    :param granularity: the number of parameter values to span the grid over for each dimension
    :param errorDef: the error metric to be used
    :param lowerBoundX: the minimum value for the model parameter in the x-dimension
    :param upperBoundX: the maximum value for the model parameter in the x-dimension
    :param lowerBoundY: the minimum value for the model parameter in the y-dimension
    :param upperBoundY: the maximum value for the model parameter in the x-dimension
    :param modelSpecificParameters: simulation execution parameters specific to the model used
    :param model: the model employed for the simuation
    :return: A list containing analysis for every parameter combination between the scenarios comprising the x and y coordinates and the average, maxSpread, minSpread, maxSpreadRelative, minSpreadRelative between the cases as well as the baseCaseAverage and the instrumentCaseAverage
    """
    print('creating parallel runs')
    seedSet = set()
    parameterPerformance = [[{} for col in range(granularity)] for row in range(granularity)]
    print('creating a pool of ' + str(mp.cpu_count()) + ' cores')
    pool = mp.Pool(4)
    # create the number of runs (repetitions of all parameter combinations) by initializing the seeds and calculating the relevant parameters
    for l in range(int(noRepetitions * math.pow(granularity, 2))):
        currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        while (currentSeed in seedSet):
            currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        seedSet.add(currentSeed)
        indexX = (math.floor(l / noRepetitions) % granularity)
        indexY = (math.floor(l / (noRepetitions * granularity)))
        correspondingX = lowerBoundX + (indexX * (upperBoundX - lowerBoundX) / (granularity - 1))
        correspondingY = lowerBoundY + (indexY * (upperBoundY - lowerBoundY) / (granularity - 1))
        def storeSimulationRun(parameters):
            parameterPerformance[parameters['indexX']][parameters['indexY']][parameters['currentSeed']] = parameters['scenarioPerformance']
        print('executing run ' + str(l))
        pool.apply_async(executeSeedRun, args=(scenarioFiles, errorDef, model, correspondingX, correspondingY, indexX, indexY, currentSeed, modelSpecificParameters), callback=storeSimulationRun)
    # After all runs are started, close and join the pool (i.e. wait until all results are done)
    pool.close()
    pool.join()
    print(parameterPerformance)
    return simulationAnalyser.analyseScenarioPerformance(parameterPerformance, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, scenarioFiles)

def executeSeedRun(scenarioFiles, errorDef, model, X, Y, indexX, indexY, seed, modelSpecificParameters):
    """
    Function to run the model with a fixed seed over a range of scenarios

    :param scenarioFiles: list of the scenarios to execute the simulation runs for
    :param errorDef: the error metric to be used
    :param modelSpecificParameters: simulation execution parameters specific to the model used
    :param model: the model employed for the simulation
    :param X: the first variational parameter for the simulation run
    :param Y: the second variational parameter for the simulation run
    :param indexX: the index of the corresponding run in the first variational parameter (pass-through parameter)
    :param indexY: the index of the corresponding run in the first variational parameter (pass-through parameter)
    :param seed: the random seed of the respective run (pass-through parameter)
    :param modelSpecificParameters: dictionary containing parameters specific to the model
        (in the case of PVact containing AP and IP if they should deviate from the configuration default)
    :return: a dictionary containing the passing parameters and the scenarioPerformance
    """
    scenarioPerformance = {}
    # For each scenario calculate and store the results
    for currentScenario in scenarioFiles:
        jarPath = None
        if (model == 'PVact'):
            modeParameters = {'adoptionThreshold': X, 'interestThreshold': Y, 'currentSeed': seed}
            modeParameters['AP'] = int(modelSpecificParameters['AP']) if 'AP' in modelSpecificParameters else \
            configurationPVact.gds_defaults['AP']
            modeParameters['IP'] = int(modelSpecificParameters['IP']) if 'IP' in modelSpecificParameters else \
            configurationPVact.gds_defaults['IP']
            jarPath = simulationRunner.prepareJson(currentScenario, 'PVact', modeParameters,
                                                   configuration.scenarioPath + currentScenario + '.json')
        if (jarPath):
            # Invoke the simulation run with the respective scenario data (as dataDirPath)
            simulationRunner.invokeJarExternalData(jarPath, errorDef, seed, 'resources/dataFiles/')
        else:
            print('Error! No model was set so no configuration file was created for this run')
        if (model == 'PVact'):
            scenarioPerformance[currentScenario] = PVactModelHelper.readAnalysisData(
                'resources/simulationFiles/images/AdoptionAnalysis.json')
    # print(str(scenarioPerformance))
    # print(str((indexX, indexY, seed, scenarioPerformance)))
    return {'indexX': indexX, 'indexY': indexY, 'seed': seed, 'scenarioPerformance': scenarioPerformance}