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

def setParameters(opts):
    print(opts)
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
        elif o == '--method':
            parameters['method'] = a
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
        else:
            print('unrecognized parameter ' + str(a))
    return parameters


# module to initialize the optimization process and set the parameters.
# Serves to isolate the functionality of the individual optimization methods from the data

def runOptimization(errorDefinition, optimizationMethod, parameters):
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
        print(
            gridDepthSearch.iterateGridDepthSearch(acceptableDelta, maxDepth, scaleFactor, resolution, errorDefinition))
    elif (optimizationMethod == 'singleRun'):
        if ('AT' in parameters and 'IT' in parameters):
            baseInputFile = 'src/modelInputFiles/changedInterest'
            simulationRunner.prepareJson(baseInputFile, parameters['AT'], parameters['IT'])
            simulationRunner.invokeJar(
                baseInputFile + '-' + str(parameters['AT'])[2:len(str(parameters['AT']))] + '-' + str(parameters['IT']),
                parameters['errorDef'])
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
                                    maximum_generation=maximum_generation,
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
            result = spso.search(number_of_particles=number_of_particles,
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
            simulatedAnnealing = SimulatedAnnealing(optimizationWrapper, number_of_variables, objective)
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
                                               standard_deviation_for_estimation=standard_deviation_for_estimation,
                                               ratio_of_energy_delta_over_evaluation_delta=ratio_of_energy_delta_over_evaluation_delta)
            print(result["best_decision_variable_values"][0])  # x value: Example: 1.0112
            print(result["best_decision_variable_values"][1])  # y value: Example: 0.9988
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