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
import os


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
        else:
            print('unrecognized parameter ' + str(a))
    return parameters


# module to initialize the optimization process and set the parameters.
# Serves to isolate the functionality of the individual optimization methods from the data

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
        optimizationResult = gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition, AP, IP)
        print(optimizationResult)
        saveAndPlotEvaluationData(optimizationResult['evaluationData'], AP, IP, errorDefinition, plotFlag)
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
        neighborRefiningSearch.neighborRefining(errorDefinition)
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

def saveAndPlotEvaluationData(evaluationData, AP, IP, errorDefinition, plotFlag):
    print('saving and plotting')
    file = open('src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-' + errorDefinition, "w")
    for i in range(len(evaluationData)):
        for j in range(len(evaluationData[i])):
            file.write(str(evaluationData[i][j])+'\n')
    file.close()
    if(plotFlag):
        dataVisualization.visualizeData('trisurf', 'src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-' + errorDefinition)

def runAndPlot(runDict, parameters, errorDefinition, nameAppend):
    baseInputFile = 'src/modelInputFiles/changedInterest'
    print('running with configuration AP: ' + str(runDict['adoptionThreshold']) + ', IP: ' + str(
        runDict['interestThreshold']) + ', AP: ' + str(parameters['AP']) + ', IP: ' + str(
        parameters['IP']))
    simulationRunner.prepareJson(baseInputFile, runDict['adoptionThreshold'], runDict['interestThreshold'],
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
        simulation = plt.plot(years, modelResults, label="Simulationsergebnisse", color="#b02f2c")
        realData = plt.plot(years, realAdoptions, label="Tatsächliche Adoptionen", color="#8ac2d1")
        plt.ylabel('Installierte Anlagen')
        plt.xlabel('Jahre')
        plt.legend(handles=[simulation[0], realData[0]])
        # plt.show()
        plt.savefig('plots/' + errorDefinition + '-' + str(parameters['AP']) + '-' + str(
            parameters['IP']) + '-' + str(runDict['adoptionThreshold']) + '-' + str(
            runDict['interestThreshold']) + '-' + str(returnData) + '-' + nameAppend + '.png', bbox_inches='tight')
        plt.clf()