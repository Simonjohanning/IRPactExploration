import math
import gridDepthSearch
import configuration
import simulationRunner
import neighborRefiningSearch
import IRPactValWrapper
from metaheuristic_algorithms.harmony_search import HarmonySearch
from metaheuristic_algorithms.firefly_algorithm import FireflyAlgorithm
from metaheuristic_algorithms.simplified_particle_swarm_optimization import SimplifiedParticleSwarmOptimization
from metaheuristic_algorithms.simulated_annealing import SimulatedAnnealing
from metaheuristic_algorithms.genetic_algorithm import GeneticAlgorithm
import json
import random

import simulationPlotter
import simulationAnalyser

import PVactModelHelper

# TODO package a bunch of more concrete stuff here in a library and separate setup and execution

# module to initialize the optimization process.
# Serves to isolate the functionality of the individual optimization methods from the data.

# Function to invoke the simulation execution methods based on the specified execution method.
# Selects and prepares the data for the non-optimization-based execution methods detailed below or invokes the respective optimization method.
# Implemented execution methods not directly bound in optimization are:
#   pvactval: generates the data and statistics for several instances of the scenarios based on the scenario list
#   multipleRuns: runs simulations for a specified number of repetitions for the same parameters and stores the results
#   plotRuns: plotRuns executes and plots single runs specified in the runFile
def runSimulations(model, errorDefinition, executionMethod, parameters, plotFlag):
    if (executionMethod == 'pvactval'):
        if ('noRepetitions' in parameters and 'scenarioList' in parameters and 'resolution' in parameters and 'lowerBoundAT' in parameters and 'upperBoundAT' in parameters and 'lowerBoundIT' in parameters and 'upperBoundIT' in parameters and 'AP' in parameters and 'IP' in parameters):
            scenarioFiles = parameters['scenarioList'].split(',')
            print('reading ' + str(len(scenarioFiles)) + ' scenarios files ')
            # createForwardRuns(scenarioFiles, float(parameters['noRepetitions']), int(parameters['resolution']), parameters['errorDef'], float(parameters['lowerBoundAT']), float(parameters['upperBoundAT']), float(parameters['lowerBoundIT']), float(parameters['upperBoundIT']), parameters['AP'], parameters['IP'])
            # TODO make less hacky and specific here
            analysisData = simulationAnalyser.analyseScenarioPerformance(configuration.testScenarioData,
                                                          float(parameters['lowerBoundAT']),
                                                          float(parameters['upperBoundAT']),
                                                          float(parameters['lowerBoundIT']),
                                                          float(parameters['upperBoundIT']), scenarioFiles)
            simulationPlotter.plotRunStatistics(analysisData, 'relative')
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
            runAndPlot(model, parameters, errorDefinition, 'run' + str(index))
            #TODO delete print('written out in file plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(
                # parameters['IP']) + '-' + str(parameters['AP']) + '-' + str(parameters['IT']) + '-runError-' + str(
                # index) + '.png')
    elif (executionMethod == 'plotRuns'):
        if ('runFile' in parameters):
            # go through all runs in file and do single runs with consecutive plot
            with open('src/' + parameters['runFile'], 'r') as file:
                for line in file:
                    runAndPlot(eval(line), parameters, errorDefinition, '')
    else:
        runOptimization(errorDefinition, executionMethod, parameters, plotFlag)

# Function that runs the parameter optimization based on the specified parameters.
# Individual simulations will be evaluated based on the errorDefinition with given parameters
# and are optimized based on the specified optimizationMethod.
# If the plotFlag is set, optimization methods using it will plot results between runs.
# Implemented optimization methods include:
# gridDepthSearch: optimization method where values are sampled within a grid of regular intervals that gets consecutively finer around the local minimum of the last execution
# neighborRefiningSearch: optimization method in which the investigated parameter grid is surveyed by evaluating points in the grid are added based on the distance to evaluated points and their error term,
# harmonySearch (from the metaheuristic algorithm package),
# firefly (from the metaheuristic algorithm package),
# SimplifiedParticleSwarmOptimization (from the metaheuristic algorithm package),
# simulatedAnnealing (from the metaheuristic algorithm package),
# geneticAlgorithm (from the metaheuristic algorithm package).
def runOptimization(errorDefinition, optimizationMethod, parameters, plotFlag):
    objective = "minimization"
    optimizationWrapper = None
    if parameters['errorDef'] == 'MAE':
        optimizationWrapper = IRPactValWrapper.IRPactValWrapperMAE()
    elif parameters['errorDef'] == 'RMSD':
        optimizationWrapper = IRPactValWrapper.IRPactValWrapperRMSE()
    # include https://pypi.org/project/metaheuristic-algorithms-python/
    if (optimizationMethod == 'gridDepthSearch'):
        gridDepthSearch(errorDefinition, parameters, plotFlag)
    elif (optimizationMethod == 'neighborRefiningSearch'):
        neighborRefiningSearch.neighborRefining(errorDefinition, parameters['inputFile'])
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

def gridDepthSearch(errorDefinition, parameters, plotFlag):
    # the grid depth search iteratively samples smaller / finer regions of the parameter space
    # equidistantly until close enough to the reference time series or a given number of iterations are reached
    # parameters are the acceptableDelta, maxDepth, scaleFactor, resolution and errorDefinition;
    # see function for further documentation
    maxDepth = parameters['maxDepth'] if ('maxDepth' in parameters) else configuration.gds_defaults['maxDepth']
    scaleFactor = parameters['scaleFactor'] if ('scaleFactor' in parameters) else configuration.gds_defaults[
        'scaleFactor']
    resolution = parameters['resolution'] if ('resolution' in parameters) else configuration.gds_defaults[
        'resolution']
    acceptableDelta = parameters['acceptableDelta'] if ('acceptableDelta' in parameters) else \
        configuration.gds_defaults['acceptableDelta']
    AP = parameters['AP'] if ('AP' in parameters) else configuration.gds_defaults['AP']
    IP = parameters['IP'] if ('IP' in parameters) else configuration.gds_defaults['IP']
    inputFile = parameters['inputFile'] if ('inputFile' in parameters) else configuration.gds_defaults['inputFile']
    lowerBoundAT = parameters['lowerBoundAT'] if ('lowerBoundAT' in parameters) else configuration.optimizationBounds[
        'minAdoptionThreshold']
    upperBoundAT = parameters['upperBoundAT'] if ('upperBoundAT' in parameters) else configuration.optimizationBounds[
        'maxAdoptionThreshold']
    lowerBoundIT = parameters['lowerBoundIT'] if ('lowerBoundIT' in parameters) else configuration.optimizationBounds[
        'minInterestThreshold']
    upperBoundIT = parameters['upperBoundIT'] if ('upperBoundIT' in parameters) else configuration.optimizationBounds[
        'maxInterestThreshold']
    optimizationResult = gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution,
                                                                errorDefinition, AP, IP, inputFile, lowerBoundAT,
                                                                upperBoundAT, lowerBoundIT, upperBoundIT)
    print(optimizationResult)
    simulationPlotter.saveAndPlotEvaluationData(optimizationResult['evaluationData'],
                                                'src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-',
                                                errorDefinition, plotFlag)

def runHarmonySearch(optimizationWrapper, parameters, objective):
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
    if optimizationWrapper is None:
        pass
    else:
        if parameters['errorDef'] == 'MAE':
            optimizationWrapper = IRPactValWrapper.IRPactValWrapperMAESingleVariable()
        elif parameters['errorDef'] == 'RMSD':
            optimizationWrapper = IRPactValWrapper.IRPactValWrapperRMSESingleVariable()
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

# Function to execute a single run and to plot the results based on the cumulated adoptions
# for the simulation and the reference data for the simulated years.
# TODO tidy up, make more abstract and name properly
def runAndPlot(model, parameters, errorDefinition, nameAppend):
    if (model == 'PVact'):
        configurationFile = PVactModelHelper.prepareJSONRand(parameters)


    # ToDo change back or make more elegant (randomness)

    returnData = simulationRunner.invokeJar(configurationFile),
        parameters['errorDef'], True)
    print('finished run with configuration AP: ' + str(parameters['adoptionThreshold']) + ', IP: ' + str(
        parameters['interestThreshold']) + ', AP: ' + str(parameters['AP']) + ', IP: ' + str(parameters['IP']) + ' and error ' + str(returnData))
    simulationRunner.navigateToTop()
    simulationPlotter.plotCumulatedAdoptions('images/JaehrlicheKumulierteAdoptionenVergleich-data.csv', 'plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(
            parameters['IP']) + '-' + str(parameters['adoptionThreshold']) + '-' + str(parameters['interestThreshold']) + '-' + str(returnData) + '-' + nameAppend + '.png')

# Function to schedule, run and analyse a set of runs based on the parameters and scenarios provided
def createForwardRuns(scenarioFiles, noRepetitions, granularity, errorDef, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, specificParameters):
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
            f = open('src/resources/' + currentScenario + '.json', "r")
            fileData = json.loads(f.read())
            if(specificParameters['model'] == 'PVact'):
                jarPath = PVactModelHelper.prepareJSON(fileData, currentX, currentY, currentSeed, currentScenario, specificParameters['AP'], specificParameters['IP'])
            if(jarPath):
                simulationRunner.invokeJarExternalData(jarPath, errorDef, True, 'src/resources/dataFiles/')
            else:
                print('Error! No model was set so no configuration file was created for this run')
            if(specificParameters['model'] == 'PVact'):
                scenarioPerformance[currentScenario] = PVactModelHelper.readAnalysisData('images/AdoptionAnalysis.json')
            print(str(scenarioPerformance))
        parameterPerformance[indexX][indexY][currentSeed] = scenarioPerformance
        print(str(parameterPerformance[indexX][indexY]))
    # Return the analysis of the data to the invoking function
    return simulationAnalyser.analyseScenarioPerformance(parameterPerformance, lowerBoundX, upperBoundX, lowerBoundY, upperBoundY, scenarioFiles)

