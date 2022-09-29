import math
import numpy as np

import gridDepthSearch
import configuration
import simulationRunner
import neighborRefiningSearch
import IRPactValWrapper
import dataVisualization
from metaheuristic_algorithms.harmony_search import HarmonySearch
from metaheuristic_algorithms.firefly_algorithm import FireflyAlgorithm
from metaheuristic_algorithms.simplified_particle_swarm_optimization import SimplifiedParticleSwarmOptimization
from metaheuristic_algorithms.simulated_annealing import SimulatedAnnealing
from metaheuristic_algorithms.genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import random

# TODO package a bunch of more concrete stuff here in a library and separate setup and execution

# module to initialize the optimization process and set the parameters.
# Serves to isolate the functionality of the individual optimization methods from the data

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
            print('unrecognized parameter ' + str(o))
    return parameters


# Function that runs the parameter optimization based on the specified parameters.
# Individual simulations will be evaluated based on the errorDefinition with given parameters
# and are optimized based on the specified optimizationMethod.
# If the plotFlag is set, optimization methods using it will plot results between runs.
# Implemented optimization methods include:
# gridDepthSearch,
# multipleRuns,
# plotRuns,
# neighborRefiningSearch,
# harmonySearch (from the metaheuristic algorithm package),
# firefly (from the metaheuristic algorithm package),
# SimplifiedParticleSwarmOptimization (from the metaheuristic algorithm package),
# simulatedAnnealing (from the metaheuristic algorithm package),
# geneticAlgorithm (from the metaheuristic algorithm package).
def runOptimization(errorDefinition, optimizationMethod, parameters, plotFlag):
    number_of_variables = 2
    objective = "minimization"
    optimizationWrapper = None
    if parameters['errorDef'] == 'MAE':
        optimizationWrapper = IRPactValWrapper.IRPactValWrapperMAE()
    elif parameters['errorDef'] == 'RMSD':
        optimizationWrapper = IRPactValWrapper.IRPactValWrapperRMSE()
    # include https://pypi.org/project/metaheuristic-algorithms-python/
    if (optimizationMethod == 'gridDepthSearch'):
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
        lowerBoundAT = parameters['lowerBoundAT'] if ('lowerBoundAT' in parameters) else configuration.optimizationBounds['minAdoptionThreshold']
        upperBoundAT = parameters['upperBoundAT'] if ('upperBoundAT' in parameters) else configuration.optimizationBounds['maxAdoptionThreshold']
        lowerBoundIT = parameters['lowerBoundIT'] if ('lowerBoundIT' in parameters) else configuration.optimizationBounds['minInterestThreshold']
        upperBoundIT = parameters['upperBoundIT'] if ('upperBoundIT' in parameters) else configuration.optimizationBounds['maxInterestThreshold']
        optimizationResult = gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition, AP, IP, inputFile, lowerBoundAT, upperBoundAT, lowerBoundIT, upperBoundIT)
        print(optimizationResult)
        saveAndPlotEvaluationData(optimizationResult['evaluationData'], 'src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-', errorDefinition, plotFlag)
    # TODO check if only for debugging purposes / specific code
    elif (optimizationMethod == 'pvactval'):
        if ('noRepetitions' in parameters and 'scenarioList' in parameters and 'resolution' in parameters and 'lowerBoundAT' in parameters and 'upperBoundAT' in parameters and 'lowerBoundIT' in parameters and 'upperBoundIT' in parameters and 'AP' in parameters and 'IP' in parameters):
            scenarioFiles = parameters['scenarioList'].split(',')
            print('reading ' + str(len(scenarioFiles)) + ' scenarios files ')
            #createForwardRuns(scenarioFiles, float(parameters['noRepetitions']), int(parameters['resolution']), parameters['errorDef'], float(parameters['lowerBoundAT']), float(parameters['upperBoundAT']), float(parameters['lowerBoundIT']), float(parameters['upperBoundIT']), parameters['AP'], parameters['IP'])
            analyseScenarioPerformance([[{46: {'Dresden_optimistic': 411, 'Dresden_pessimistic': 640}, 150: {'Dresden_optimistic': 372, 'Dresden_pessimistic': 614}}, {112: {'Dresden_optimistic': 370, 'Dresden_pessimistic': 609}, 142: {'Dresden_optimistic': 385, 'Dresden_pessimistic': 628}}, {192: {'Dresden_optimistic': 271, 'Dresden_pessimistic': 457}, 105: {'Dresden_optimistic': 225, 'Dresden_pessimistic': 361}}], [{208: {'Dresden_optimistic': 125, 'Dresden_pessimistic': 151}, 61: {'Dresden_optimistic': 128, 'Dresden_pessimistic': 204}}, {69: {'Dresden_optimistic': 36, 'Dresden_pessimistic': 53}, 3: {'Dresden_optimistic': 37, 'Dresden_pessimistic': 43}}, {141: {'Dresden_optimistic': 47, 'Dresden_pessimistic': 90}, 169: {'Dresden_optimistic': 32, 'Dresden_pessimistic': 41}}], [{22: {'Dresden_optimistic': 5, 'Dresden_pessimistic': 25}, 183: {'Dresden_optimistic': 2, 'Dresden_pessimistic': 10}}, {174: {'Dresden_optimistic': 4, 'Dresden_pessimistic': 13}, 138: {'Dresden_optimistic': 11, 'Dresden_pessimistic': 18}}, {78: {'Dresden_optimistic': 9, 'Dresden_pessimistic': 15}, 117: {'Dresden_optimistic': 8, 'Dresden_pessimistic': 9}}]], float(parameters['lowerBoundAT']), float(parameters['upperBoundAT']), float(parameters['lowerBoundIT']), float(parameters['upperBoundIT']), scenarioFiles)
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
    elif (optimizationMethod == 'multipleRuns'):
        if ('AT' in parameters and 'IT' in parameters and 'noRuns' in parameters):
            for index in range(int(parameters['noRuns'])):
                runAndPlot({'adoptionThreshold': parameters['AT'], 'interestThreshold': parameters['IT']}, parameters, errorDefinition, 'run' + str(index))
                print('written out in file plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(parameters['IP']) + '-' + str(parameters['AP']) + '-' + str(parameters['IT']) + '-runError-' + str(index) + '.png')
    elif (optimizationMethod == 'plotRuns'):
        if ('runFile' in parameters):
            # go through all runs in file and do single runs with consecutive plot
            with open('src/' + parameters['runFile'], 'r') as file:
                for line in file:
                    runAndPlot(eval(line), parameters, errorDefinition, '')
    elif (optimizationMethod == 'neighborRefiningSearch'):
        neighborRefiningSearch.neighborRefining(errorDefinition, parameters['inputFile'])
    elif (optimizationMethod == 'harmonySearch'):
        if optimizationWrapper is None:
            pass
        else:
            harmony_search = HarmonySearch(optimizationWrapper, number_of_variables, objective)
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
    elif (optimizationMethod == 'firefly'):
        if optimizationWrapper is None:
            pass
        else:
            firefly = FireflyAlgorithm(optimizationWrapper, number_of_variables, objective)
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
    elif (optimizationMethod == 'spso'):
        if optimizationWrapper is None:
            pass
        else:
            spso = SimplifiedParticleSwarmOptimization(optimizationWrapper, number_of_variables, objective)
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
    elif (optimizationMethod == 'simulatedAnnealing'):
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
    elif (optimizationMethod == 'geneticAlgorithm'):
        if optimizationWrapper is None:
            pass
        else:
            ga = GeneticAlgorithm(optimizationWrapper, number_of_variables, objective)
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
    else:
        print('method ' + optimizationMethod + ' is not known. Please provide a valid method')

# Function to save the specified data into a file given by the prefix and the chosen error definition.
# Will append to the specified file and plot the data if the plotFlag is set.
def saveAndPlotEvaluationData(evaluationData, filePrefix, errorDefinition, plotFlag):
    print('saving and plotting')
    file = open(filePrefix + errorDefinition, "w")
    for i in range(len(evaluationData)):
        for j in range(len(evaluationData[i])):
            file.write(str(evaluationData[i][j])+'\n')
    file.close()
    if(plotFlag):
        dataVisualization.visualizeData('trisurf', filePrefix + errorDefinition)

# Function to execute a single run and to plot the results based on the cumulated adoptions
# for the simulation and the reference data for the simulated years.
# TODO tidy up, make more abstract and name properly
def runAndPlot(runDict, parameters, errorDefinition, nameAppend):
    baseInputFile = 'src/resources/scenario-dresden-full'
    print('running with configuration AP: ' + str(runDict['adoptionThreshold']) + ', IP: ' + str(
        runDict['interestThreshold']) + ', AP: ' + str(parameters['AP']) + ', IP: ' + str(
        parameters['IP']))
    # ToDo change back or make more elegant (randomness)
    simulationRunner.prepareJsonRand(baseInputFile, runDict['adoptionThreshold'], runDict['interestThreshold'],
                                 parameters['AP'],
                                 parameters['IP'])
    returnData = simulationRunner.invokeJar(
        baseInputFile + '-' + str(runDict['adoptionThreshold'])[2:len(str(runDict['adoptionThreshold']))] + '-' + str(
            runDict['interestThreshold']),
        parameters['errorDef'], True)
    print('finished run with configuration AP: ' + str(runDict['adoptionThreshold']) + ', IP: ' + str(
        runDict['interestThreshold']) + ', AP: ' + str(parameters['AP']) + ', IP: ' + str(parameters['IP']) + ' and error ' + str(returnData))
    simulationRunner.navigateToTop()
    with open('images/JaehrlicheKumulierteAdoptionenVergleich-data.csv', 'r') as adoptionsFile:
        years = []
        modelResults = []
        realAdoptions = []
        i = 0
        for yearlyData in adoptionsFile:
            # print('line ' + str(yearlyData))
            if (i > 0):
                dataArray = yearlyData.split(';')
                # print(str(dataArray) + ' with length ' + str(len(dataArray)))
                # print('year ' + str(int(dataArray[0])) + ', model: ' + str(float(dataArray[1])) + ', real: ' + str(
                #     float(dataArray[2].strip())) + ', i: ' + str(i))
                years.append(int(dataArray[0]))
                modelResults.append(float(dataArray[1]))
                realAdoptions.append(float(dataArray[2].strip()))
                # print(str(years))
                # print(str(modelResults))
                # print(str(realAdoptions))
                # print('year ' + str(years[i-1]) + ', model: ' + str(modelResults[i-1]) + ', real: ' + str(realAdoptions[i-1]) + ', i: ' + str(i))
                i += 1
            else:
                i = 1
        # print(str(years))
        # print(str(modelResults))
        # print(str(realAdoptions))
        simulation = plt.plot(years, modelResults, label="Simulation results", color="#b02f2c")
        realData = plt.plot(years, realAdoptions, label="Actual adoptions", color="#8ac2d1")
        plt.ylabel('Installed PV systems')
        plt.xlabel('Years')
        plt.legend(handles=[simulation[0], realData[0]])
        # plt.show()
        plt.savefig('plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(
            parameters['IP']) + '-' + str(runDict['adoptionThreshold']) + '-' + str(
            runDict['interestThreshold']) + '-' + str(returnData) + '-' + nameAppend + '.png', bbox_inches='tight')
        plt.clf()

# Function to schedule, run and analyse a set of runs based on the parameters and scenarios provided
# @TODO clean up and generalize
def createForwardRuns(scenarioFiles, noRepetitions, granularity, errorDef, lowBoundAT, highBoundAT, lowBoundIT, highBoundIT, AP, IP):
    print('creating runs')
    seedSet = set()
    parameterPerformance = [[{} for col in range(granularity)] for row in range(granularity)]
    for l in range(int(noRepetitions * math.pow(granularity, 2))):
        currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        while(currentSeed in seedSet):
            currentSeed = random.randint(0, int(math.pow(noRepetitions, 2) * math.pow(granularity, 3) * 2))
        seedSet.add(currentSeed)
        #print('AT index ' + str(math.floor(l/noRepetitions) % granularity), 'IT index ' + str(math.floor(l/(noRepetitions * granularity))))
        indexAT = (math.floor(l/noRepetitions) % granularity)
        indexIT = (math.floor(l/(noRepetitions * granularity)))
        currentAT = lowBoundAT + (indexAT * (highBoundAT - lowBoundAT) / (granularity - 1))
        currentIT = lowBoundIT + (indexIT * (highBoundIT - lowBoundIT) / (granularity - 1))
        scenarioPerformance = {}
        for currentScenario in scenarioFiles:
            print('generating input file for scenario ' + currentScenario + ', seed ' + str(currentSeed) + ' and (AT, IT)=(' + str(currentAT) + ',' + str(currentIT) + ')')
            f = open('src/resources/' + currentScenario + '.json', "r")
            fileData = json.loads(f.read())
            fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
                'par_InDiracUnivariateDistribution_value'] = int(currentIT)
            fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
                'par_InDiracUnivariateDistribution_value'] = float(currentAT)
            fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
                'par_InCommunicationModule3_actionnode3_adopterPoints'] = int(AP)
            fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
                'par_InCommunicationModule3_actionnode3_interestedPoints'] = int(IP)
            fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
                'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
            fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_seed'] = currentSeed
            fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_innerParallelism'] = 1
            fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_outerParallelism'] = 1
            with open('src/modelInputFiles/' + currentScenario + "-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(int(math.floor(currentIT))) + '-' + str(currentSeed) + ".json", "w") as file:
                json.dump(fileData, file, indent=2)
            simulationRunner.invokeJarExternalData('src/modelInputFiles/' + currentScenario + "-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(int(math.floor(currentIT))) + '-' + str(currentSeed), errorDef, True, 'src/resources/dataFiles/')
            # do something with the results
            scenarioPerformance[currentScenario] = extractData('images/AdoptionAnalysis.json')
            print(str(scenarioPerformance))
        parameterPerformance[indexAT][indexIT][currentSeed] = scenarioPerformance
        print(str(parameterPerformance[indexAT][indexIT]))
    analyseScenarioPerformance(parameterPerformance, lowBoundAT, highBoundAT, lowBoundIT, highBoundIT, scenarioFiles)

# Helper function to extract the total number of cumulated adoptions from the provided file
# @TODO make more general
def extractData(path):
    f = open(path, "r")
    fileData = json.loads(f.read())
    return fileData['cumulated']['total']

# Function to analyse the performance of different scenarios by a set of metrics
# TODO generalize and package away
def analyseScenarioPerformance(parameterPerformance, lowBoundAT, highBoundAT, lowBoundIT, highBoundIT, scenarios):
    #print('performance for ' + str(len(parameterPerformance)) + 'ATs and ' + str(len(parameterPerformance[0])) + ' ITs with entries like ' + str(parameterPerformance[0][0]))
    scenarioDeltaAverages = open('src/resources/scenarioDeltaAverages', 'w')
    scenarioDeltaMinSpread = open('src/resources/scenarioDeltaMinSpread', 'w')
    scenarioDeltaMaxSpread = open('src/resources/scenarioDeltaMaxSpread', 'w')
    scenarioDeltaAnalysis = open('src/resources/scenarioDeltaAnalysis', 'w')
    scenarioAverages = open('src/resources/scenarioAverages', 'w')
    print(str(parameterPerformance))
    analysisData = []
    for indexAT in range(len(parameterPerformance)):
        for indexIT in range(len(parameterPerformance[indexAT])):
            runningTally = 0
            minEntry = 9999999999
            maxEntry = 0
            refCaseTally = 0
            instrumentCaseTally = 0
            #TODO make it work with more than two entries
            for entry in parameterPerformance[indexAT][indexIT]:
                currentEntry = parameterPerformance[indexAT][indexIT][entry][scenarios[1]] - parameterPerformance[indexAT][indexIT][entry][scenarios[0]]
                runningTally += currentEntry
                refCaseTally += parameterPerformance[indexAT][indexIT][entry][scenarios[0]]
                instrumentCaseTally += parameterPerformance[indexAT][indexIT][entry][scenarios[1]]
                if (currentEntry < minEntry):
                    minEntry = currentEntry
                if (currentEntry > maxEntry):
                    maxEntry = currentEntry
            average = runningTally/len(parameterPerformance[indexAT][indexIT])
            relativeMax = average/maxEntry
            relativeMin = average/minEntry
            correspondingAT = lowBoundAT + (indexAT * (highBoundAT - lowBoundAT) / (len(parameterPerformance) - 1))
            correspondingIT = lowBoundIT + (indexIT * (highBoundIT - lowBoundIT) / (len(parameterPerformance[indexAT]) - 1))
            analysisEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'average': average, 'maxSpread': maxEntry, 'minSpread': minEntry, 'maxSpreadRelative': maxEntry/average, 'minSpreadRelative': minEntry/average, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexAT][indexIT]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexAT][indexIT])}
            analysisData.append(analysisEntry)
            scenarioDeltaAnalysis.write(str(analysisEntry))
            averageEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': average}
            scenarioDeltaAverages.write(str(averageEntry) + '\n')
            minSpread = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': minEntry}
            scenarioDeltaMinSpread.write(str(minSpread) + '\n')
            maxSpread = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'performance': maxEntry}
            scenarioDeltaMaxSpread.write(str(maxSpread) + '\n')
            scenarioAverageEntry = {'adoptionThreshold': correspondingAT, 'interestThreshold': correspondingIT, 'baseCaseAverage': refCaseTally/len(parameterPerformance[indexAT][indexIT]), 'instrumentCaseAverage': instrumentCaseTally/len(parameterPerformance[indexAT][indexIT])}
            scenarioAverages.write(str(scenarioAverageEntry) + '\n')
            print(str(analysisEntry))
    print(str(analysisData))
    scenarioDeltaAverages.close()
    scenarioDeltaMinSpread.close()
    scenarioDeltaMaxSpread.close()
    scenarioDeltaAnalysis.close()
    plotRunStatistics(analysisData, 'relative')


# Function to plot different stats over several runs on three-dimensional surfaces based on different modes.
# The data to plot is represented as a list of dictionaries containing the values of the independent variabels (x and y)
# while the value of the dependent variables depends on the mode and provides certain statistics of different runs.
# Modes and required values for the statistics are as follows:
#   absolute: expresses the absolute differences between simulation runs
#       average: the average difference between different runs of the respective parameters
#       minSpread: the minimal difference between different runs of the respective parameters
#       maxSpread: the maximal difference between different runs of the respective parameters
#   relative: expresses the relative differences between simulation runs for each parameter combination
#       minSpread: the minimal difference between different runs of the respective parameters
#       maxSpread: the maximal difference between different runs of the respective parameters
#   averageCases: expresses the averaged differences between two compared scenarios
#       baseCaseAverage: the reference case data for the dependent variable
#       instrumentCaseAverage: the investigated case data for the dependent variable
#   averageCasesRelative: expresses the averaged differences between two compared scenarios
#       average: the average number of adoptions in the cases
#       baseCaseAverage: the reference case data for the dependent variable
#       instrumentCaseAverage: the investigated case data for the dependent variable
# TODO make more general regarding the dimensions and package somewhere else
def plotRunStatistics(analysisData, mode):
    n = len(analysisData)
    cd_x = np.zeros(n, dtype=float)
    cd_y = np.zeros(n, dtype=float)
    cd_z1 = np.zeros(n, dtype=float)
    cd_z2 = np.zeros(n, dtype=float)
    cd_z3 = np.zeros(n, dtype=float)
    i = 0
    for pointDict in analysisData:
        cd_x[i] = pointDict['adoptionThreshold']
        cd_y[i] = pointDict['interestThreshold']
        if(mode == 'absolute'):
            cd_z1[i] = pointDict['average']
            cd_z2[i] = pointDict['minSpread']
            cd_z3[i] = pointDict['maxSpread']
        elif(mode == 'relative'):
            cd_z1[i] = 1.0
            cd_z2[i] = pointDict['minSpreadRelative']
            cd_z3[i] = pointDict['maxSpreadRelative']
        elif(mode == 'averageCases'):
            cd_z1[i] = 0.0
            cd_z2[i] = pointDict['baseCaseAverage']
            cd_z3[i] = pointDict['instrumentCaseAverage']
        elif (mode == 'averageCasesRelative'):
            cd_z2[i] = pointDict['average'] / pointDict['baseCaseAverage']
            cd_z3[i] = pointDict['average'] / pointDict['instrumentCaseAverage']
            cd_z1[i] = (cd_z2[i] + cd_z3[i]) / 2.0
        i += 1
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if(mode == 'relative'):
        colormap = cm.Greys
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
        colormap = cm.inferno
        ax.plot_trisurf(cd_x, cd_y, cd_z2, cmap=colormap)
        colormap = cm.cividis
        ax.plot_trisurf(cd_x, cd_y, cd_z3, cmap=colormap)
    elif(mode == 'absolute'):
        colormap = cm.RdYlGn_r
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
    elif(mode == 'averageCases' or mode == 'averageCasesRelative'):
        colormap = cm.Greys
        ax.plot_trisurf(cd_x, cd_y, cd_z1, cmap=colormap)
        colormap = cm.RdYlGn_r
        ax.plot_trisurf(cd_x, cd_y, cd_z2, cmap=colormap)
        ax.plot_trisurf(cd_x, cd_y, cd_z3, cmap=colormap)
    ax.set_xlabel('Adoption Threshold')
    ax.set_ylabel('Interest Threshold')
    if(mode == 'absolute'):
        ax.set_zlabel('Average Adoption Difference')
    elif(mode == 'relative'):
        ax.set_zlabel('Spread between Runs')
    elif(mode == 'averageCases'):
        ax.set_zlabel('Average Scenario Adoption')
    elif (mode == 'averageCasesRelative'):
        ax.set_zlabel('Relative Av. Scenario Adoption')
    plt.show()