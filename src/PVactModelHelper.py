import math
import json
import configurationPVact
import random
import helper

# Module with a number of helper files specific to the structure of the IRPact model jar.
# Encapsulates the IRPact-specific knowledge and format to expose it to the more general interface


# Function to construct the command line array used to invoke the jar
# TODO document and make less system-specific
def constructInvokationCommand(mode, param):
    if(mode == 'PVact_weightedCumulativeAnnualAdoptionDelta'):
        return ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', param['inputFile'] + '.json', '-o',
         'simulationFiles/example-output.json',
         '--noConsole', '--logPath', 'simulationFiles/log.log', '--calculatePerformance', 'cumulativeAnnualAdoptionDelta']
    elif(mode == 'PVact_internal'):
        return ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i',  param['inputFile'] + '.json', '-o',
         'simulationFiles/example-output.json',
         '--noConsole', '--logPath', 'simulationFiles/log.log', '--calculatePerformance',  param['modeParameters'], '--gnuplotCommand',
         'C:/Users/mai11dlx/gnuplot/bin/gnuplot.exe']
    elif(mode == 'PVact_weightedCumulativeAnnualAdoptionDelta_external'):
        return ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', param['inputFile'] + '.json', '-o',
         'simulationFiles/example-output.json',
         '--noConsole', '--logPath', 'simulationFiles/log.log', '--calculatePerformance', 'cumulativeAnnualAdoptionDelta', '--dataDir',
         param['externalPath']]
    elif(mode == 'PVact_external'):
        return ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', param['inputFile'] + '.json', '-o',
         'simulationFiles/example-output.json',
         '--noConsole', '--logPath', 'simulationFiles/log.log', '--calculatePerformance', param['modeParameters'], '--gnuplotCommand',
         'C:/Users/mai11dlx/gnuplot/bin/gnuplot.exe', '--dataDir', param['externalPath']]

# Function to prepare the shipped JSON file to adjust it to individual runs.
# Changes some parameters in the file and returns the name stub to the input file
# TODO document
def prepareJSON(templateFile, inputFile, currentIT, currentAT, AP , IP, currentSeed):
    helper.navigateToTop()
    f = open(inputFile, "r")
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
    with open(templateFile + "-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(
            int(math.floor(currentIT))) + '-' + str(currentSeed) + ".json", "w") as file:
        json.dump(fileData, file, indent=2)
    return templateFile + "-" + str(currentAT)[2:len(str(currentAT))] + "-" + str(int(math.floor(currentIT))) + '-' + str(currentSeed)

# Function to return the relevant analysis data (total number of cumulated adoptions) to the requesting function
# TODO document
def readAnalysisData(analysisDataPath):
    f = open(analysisDataPath, "r")
    fileData = json.loads(f.read())
    return fileData['cumulated']['total']

# Function to extract the PVact relevant parameters to prepare the respective JSON file
# function that manipulates the scenario definition to fit the adoption and interest threshold for the desired run
# file is saved in the path and prefix specified by the templateFile parameter
# TODO document
def prepareJSONRand(parameters):
    AP = int(parameters['AP']) if 'AP' in parameters else configurationPVact.gds_defaults['AP']
    IP = int(parameters['IP']) if 'IP' in parameters else configurationPVact.gds_defaults['IP']
    if ('adoptionThreshold' in parameters and 'interestThreshold'):
        templateFile = parameters['inputFile'] if 'inputFile' in parameters else configurationPVact.baseInputFile
        helper.navigateToTop()
        f = open(templateFile + '.json', "r")
        fileData = json.loads(f.read())
        fileData['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
            'par_InDiracUnivariateDistribution_value'] = int(parameters['interestThreshold'])
        fileData['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
            'par_InDiracUnivariateDistribution_value'] = float(parameters['adoptionThreshold'])
        fileData['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_adopterPoints'] = AP
        fileData['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_interestedPoints'] = IP
        fileData['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
        fileData['years'][0]['scalars']['sca_InGeneral_seed'] = random.randint(0, 99999)
        print('writing file with AP ' + AP + ' and IP ' + IP + ' and AT ' + parameters['adoptionThreshold'] + ' and IT ' + parameters['interestThreshold'])
        with open(templateFile + "-" + parameters['adoptionThreshold'][2:len(parameters['adoptionThreshold'])] + "-" + parameters['interestThreshold'] + ".json", "w") as file:
            json.dump(fileData, file, indent=2)
        return configurationPVact.baseInputFile + '-' + str(parameters['adoptionThreshold'])[2:len(str(parameters['adoptionThreshold']))] + '-' + str(parameters['interestThreshold'])
    else:
        print('error! Missing parameters adoptionThreshold, interestThreshold, AP and/or IP in preparing files for PVact')

# TODO generalize and document
def deriveFilePrefix(parameters):
    AP = parameters['AP'] if 'AP' in parameters else configurationPVact.gds_defaults['AP']
    IP = parameters['IP'] if 'IP' in parameters else configurationPVact.gds_defaults['IP']
    return 'src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-'