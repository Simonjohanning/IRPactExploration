import sys
import getopt
import simulationManager
import dataVisualization
import os
import simulationRunner
import json



def quickCheck():
    f = open('src/resources/example-input_old.json', "r")
    fileData = json.loads(f.read())
    print(fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'])
    print(fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_adopterPoints'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_interestedPoints'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_awarePoints'])
    f = open('src/modelInputFiles/changedInterest-0-33.json', "r")
    fileData = json.loads(f.read())
    print(fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'])
    print(fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_adopterPoints'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_interestedPoints'])
    print(fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_awarePoints'])

def runPlotRunsWithMethod(method, parameters):
    parameters['AP'] = 5
    # parameters['IP'] = 1
    # parameters['runFile'] = 'resources/gridDepthSearch-' + str(parameters['AP']) + str(parameters['IP']) + '0-' + method + '-mini'
    # simulationManager.runOptimization(method, 'plotRuns', parameters, False)
    parameters['IP'] = 2
    parameters['runFile'] = 'resources/gridDepthSearch-' + str(parameters['AP']) + str(parameters['IP']) + '0-' + method + '-mini'
    simulationManager.runOptimization(method, 'plotRuns', parameters, False)
    parameters['AP'] = 3
    parameters['runFile'] = 'resources/gridDepthSearch-' + str(parameters['AP']) + str(parameters['IP']) + '0-' + method + '-mini'
    simulationManager.runOptimization(method, 'plotRuns', parameters, False)
    # parameters['IP'] = 1
    # parameters['runFile'] = 'resources/gridDepthSearch-' + str(parameters['AP']) + str(parameters['IP']) + '0-' + method + '-mini'
    # simulationManager.runOptimization(method, 'plotRuns', parameters, False)

def runPlotRuns(parameters):
    errorMethod = 'cumulativeAnnualAdoptionDelta'
    runPlotRunsWithMethod(errorMethod, parameters)
    errorMethod = 'weightedCumulativeAnnualAdoptionDelta'
    runPlotRunsWithMethod(errorMethod, parameters)
    # errorMethod = 'MAE'
    # runPlotRunsWithMethod(errorMethod, parameters)
    # errorMethod = 'RMSD'
    # runPlotRunsWithMethod(errorMethod, parameters)

def runAll(parameters):
    parameters['errorDef'] = 'MAE'
    parameters['AP'] = 5
    parameters['IP'] = 1
    simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, False)
    parameters['IP'] = 2
    simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, False)
    parameters['AP'] = 3
    simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, False)
    parameters['IP'] = 1
    simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, False)

# main method to set up the logging and invoke the optimization management method function
if __name__ == '__main__':
    #dataVisualization.visualizeData('trisurf', 'resources/gridDepthSearch-210-cumulativeAnnualAdoptionDelta-reduced')
    simulationRunner.navigateToTop()
    #quickCheck()
    argv = sys.argv[1:]
    # include new parameters for MHs
    opts, args = getopt.getopt(argv, 'd:e:msr', ['acceptableDelta=', 'delta=', 'errorDef=', 'maxDepth=', 'scaleFactor=', 'resolution=', 'AT=', 'IT=', 'method=', 'AP=', 'IP=', 'runFile='])
    print(opts)
    parameters = simulationManager.setParameters(opts)
    # TODO make safe
    if ('errorDef' in parameters and 'method' in parameters):
        print(parameters)
        # log_file = open("message.log", "w")
        # sys.stdout = log_file
        # invokation of the search
        simulationManager.runOptimization(parameters['errorDef'], parameters['method'], parameters, True)
        #runPlotRuns(parameters)
        #runAll(parameters)
        # log_file.close()
    else:
        print('Please provide parameters errorDef and method')
