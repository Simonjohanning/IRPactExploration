"""
    File to store model-specific defaults and data for the PVact model.
"""

baseInputFile = 'resources/scenarios/scenario-dresden-partial'
modelPath = 'resources/PVact.jar'
defaultOutputFile = 'resources/simulationFiles/example-output.json'
defaultLogFile = 'resources/simulationFiles/log.log'

gds_defaults = {
    'AP': 5,
    'IP': 1,
}
defaultInterestThreshold = 22

pointListFile = 'resources/pointList'
templateFile = 'modelInputFiles/changedInterest'
defaultInputFile = 'resources/input-scenario-dresden-partial.json'
outputDataFile = 'resources/simulationFiles/images/JaehrlicheKumulierteAdoptionenVergleich-data.csv'
optimizationBounds = {'minAdoptionThreshold': 0.0, 'maxAdoptionThreshold': 1.0, 'minInterestThreshold': 0, 'maxInterestThreshold': 128}

plotSettingsYearlySimulationReferenceData = {
    'xLabel': 'Years',
    'yLabel': 'Installed PV systems'
}

plotSettingsScenarioAnalysis3D = {
    'xLabel': 'Adoption Threshold',
    'yLabel': 'Interest Threshold'
}


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


runConfigurationPath = 'modelInputFiles/'
