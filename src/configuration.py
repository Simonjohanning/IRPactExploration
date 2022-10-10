gds_defaults = {
    'maxDepth':  2,
    'scaleFactor': 2,
    'resolution': 1,
    'acceptableDelta': 1.2,
    'AP': 5,
    'IP': 1,
    'inputFile': 'resources/scenario-dresden-full.json'
}

harmony_defaults = {
    'maximum_attempt': 25000,
    'pitch_adjusting_range': 100,
    'harmony_search_size': 20,
    'harmony_memory_acceping_rate': 0.95,
    'pitch_adjusting_rate': 0.7
}

firefly_defaults = {
    'number_of_fireflies': 10,
    'maximum_generation': 10,
    'randomization_parameter_alpha': 0.2,
    'absorption_coefficient_gamma': 1.0
}

spso_defaults = {
    'number_of_particles': 20,
    'number_of_iterations': 15,
    'social_coefficient': 0.5,
    'random_variable_coefficient': 0.2
}

simulatedAnnealing_defaults = {
    'temperature': 1.0,
    'minimal_temperature': 1e-10,
    'maximum_number_of_rejections': 2500,
    'maximum_number_of_runs': 500,
    'maximum_number_of_acceptances':15,
    'bolzmann_constant': 1,
    'cooling_factor': 0.95,
    'energy_norm': 1e-8,
    'standard_deviation_for_estimation': 1,
    'ratio_of_energy_delta_over_evaluation_delta': 1
}

geneticAlgorithm_default = {
    'population_size': 20,
    'maximum_number_of_generations': 100,
    'number_of_mutation_sites': 2,
    'crossover_probability': 0.95,
    'mutation_probability': 0.05
}

optimizationBounds = {
    'minY': 1,
    'maxY': 128,
    'minX': 0,
    'maxX': 1.0
}

optimizationStartValues = {
    'X': 0.8,
    'Y': 12
}

defaultInterestThreshold = 22

pointListFile = 'src/resources/pointList'
templateFile = 'src/modelInputFiles/changedInterest'
defaultInputFile = 'src/resources/input-scenario-dresden-partial.json'
shellFlag = False
number_of_variables = 2


testScenarioData = [[{46: {'Dresden_optimistic': 411,
                                                                  'Dresden_pessimistic': 640},
                                                             150: {'Dresden_optimistic': 372,
                                                                   'Dresden_pessimistic': 614}}, {
                                                                112: {'Dresden_optimistic': 370,
                                                                      'Dresden_pessimistic': 609},
                                                                142: {'Dresden_optimistic': 385,
                                                                      'Dresden_pessimistic': 628}}, {
                                                                192: {'Dresden_optimistic': 271,
                                                                      'Dresden_pessimistic': 457},
                                                                105: {'Dresden_optimistic': 225,
                                                                      'Dresden_pessimistic': 361}}], [{208: {
                'Dresden_optimistic': 125, 'Dresden_pessimistic': 151}, 61: {'Dresden_optimistic': 128,
                                                                             'Dresden_pessimistic': 204}}, {69: {
                'Dresden_optimistic': 36, 'Dresden_pessimistic': 53}, 3: {'Dresden_optimistic': 37,
                                                                          'Dresden_pessimistic': 43}}, {141: {
                'Dresden_optimistic': 47, 'Dresden_pessimistic': 90}, 169: {'Dresden_optimistic': 32,
                                                                            'Dresden_pessimistic': 41}}], [{22: {
                'Dresden_optimistic': 5, 'Dresden_pessimistic': 25}, 183: {'Dresden_optimistic': 2,
                                                                           'Dresden_pessimistic': 10}}, {174: {
                'Dresden_optimistic': 4, 'Dresden_pessimistic': 13}, 138: {'Dresden_optimistic': 11,
                                                                           'Dresden_pessimistic': 18}}, {78: {
                'Dresden_optimistic': 9, 'Dresden_pessimistic': 15}, 117: {'Dresden_optimistic': 8,
                                                                           'Dresden_pessimistic': 9}}]]