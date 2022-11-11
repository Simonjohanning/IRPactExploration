"""
 Module with a number of helper files specific to the structure of the IRPact model jar.
 Encapsulates the IRPact-specific knowledge (save configuration) and format to expose it to the more general interface
"""
import math
import json
import os

import configurationPVact
import random

# TODO data format not final; has data[0] or without

# TODO make less system-specific
def constructInvokationCommand(mode, param):
    """
    Function to construct the command line array used to invoke the model jar based on the mode.
    Provides the invokation command in a form friendly for a 'check_output' call.

    :param mode: specification as to how the command is put together
    :param param: a dictionary of the parameters used in the invokation command
    :return: performance data of the simulation execution
    """
    if(mode == 'PVact_weightedCumulativeAnnualAdoptionDelta'):
        return ['java', '-jar', configurationPVact.modelPath, '-i', param['inputFile'] + '.json', '-o',
         configurationPVact.defaultOutputFile,
         '--noConsole', '--logPath', configurationPVact.defaultLogFile, '--calculatePerformance', 'cumulativeAnnualAdoptionDelta']
    elif(mode == 'PVact_internal'):
        return ['java', '-jar', configurationPVact.modelPath, '-i',  param['inputFile'] + '.json', '-o',
         configurationPVact.defaultOutputFile,
         '--noConsole', '--logPath', configurationPVact.defaultLogFile, '--calculatePerformance',  param['errorDef'], '--gnuplotCommand',
         'C:/Users/mai11dlx/gnuplot/bin/gnuplot.exe']
    elif(mode == 'PVact_weightedCumulativeAnnualAdoptionDelta_external'):
        return ['java', '-jar', configurationPVact.modelPath, '-i', param['inputFile'] + '.json', '-o',
         configurationPVact.defaultOutputFile,
         '--noConsole', '--logPath', configurationPVact.defaultLogFile, '--calculatePerformance', 'cumulativeAnnualAdoptionDelta', '--dataDir',
         param['dataDirPath']]
    elif(mode == 'PVact_external'):
        return ['java', '-jar', configurationPVact.modelPath, '-i', param['inputFile'] + '.json', '-o',
         configurationPVact.defaultOutputFile,
         '--noConsole', '--logPath', configurationPVact.defaultLogFile, '--calculatePerformance', param['errorDef'], '--gnuplotCommand',
         param['gnuPlotPath'], '--dataDir', param['dataDirPath']]

# TODO check that file was written successfully
def prepareJSON(filenamePrefix, inputFile, simulationIT, simulationAT, AP , IP, currentSeed):
    """
    Function to prepare the shipped JSON file to adjust it to individual runs.
    Changes model parameters in the file on the basis of function arguments and returns the name stub to the input file.

    :param filenamePrefix: filename stub before parameters are appended
    :param inputFile: template model scenario that is overwritten with the respective parameters
    :param simulationIT: the interest threshold to be used in the configured json file
    :param simulationAT: the adoption threshold to be used in the configured json file
    :param AP: the number of adopter points derived from communication in the simulation run
    :param IP: the number of adopter points derived from communication in the simulation run
    :param currentSeed: the seed of the random generator used in the simulation run
    :return: the filename of the written file
    """
    templateFile = inputFile if inputFile else configurationPVact.baseInputFile
    f = open(templateFile, "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = int(simulationIT)
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = float(simulationAT)
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_adopterPoints'] = int(AP)
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_interestedPoints'] = int(IP)
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
    fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_seed'] = currentSeed
    fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_innerParallelism'] = 1
    fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_outerParallelism'] = 1
    with open(configurationPVact.runConfigurationPath + filenamePrefix + "-" + str(simulationAT) + "-" + str(
            int(math.floor(simulationIT))) + '-' + str(currentSeed) + ".json", "w") as file:
        json.dump(fileData, file, indent=2)
    return configurationPVact.runConfigurationPath + filenamePrefix + "-" + str(simulationAT) + "-" + str(int(math.floor(simulationIT))) + '-' + str(currentSeed)

# Function to return the relevant analysis data (total number of cumulated adoptions) to the requesting function
# TODO document
def readAnalysisData(analysisDataPath):
    f = open(analysisDataPath, "r")
    fileData = json.loads(f.read())
    return fileData['cumulated']['total']

# TODO ensure that file is actually written
def prepareJSONRand(parameters):
    """
    Function to prepare the shipped JSON file to adjust it to individual runs.
    Changes model parameters in the file on the basis of function arguments and returns the name stub to the input file.
    Function extracts the PVact relevant parameters to prepare the respective file and manipulates the scenario definition to fit the adoption and interest threshold for the desired run.
    The seed of the number generator is generated endogeneously.
    File is saved in the path and prefix specified by the templateFile parameter

    :param parameters: dictionary to contain the required parameters for the function. Default values are loaded for omitted parameters
    :return: the filename of the written file
    """
    AP = int(parameters['AP']) if 'AP' in parameters else configurationPVact.gds_defaults['AP']
    IP = int(parameters['IP']) if 'IP' in parameters else configurationPVact.gds_defaults['IP']
    if ('adoptionThreshold' in parameters and 'interestThreshold'):
        templateFile = parameters['inputFile'] if 'inputFile' in parameters else configurationPVact.baseInputFile
        f = open(templateFile + '.json', "r")
        fileData = json.loads(f.read())
        fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
            'par_InDiracUnivariateDistribution_value'] = int(parameters['interestThreshold'])
        fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
            'par_InDiracUnivariateDistribution_value'] = float(parameters['adoptionThreshold'])
        fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_adopterPoints'] = AP
        fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_interestedPoints'] = IP
        fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
            'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
        fileData['data'][0]['years'][0]['scalars']['sca_InGeneral_seed'] = random.randint(0, 99999)
        print('writing file with AP ' + str(AP) + ' and IP ' + str(IP) + ' and AT ' + str(parameters['adoptionThreshold']) + ' and IT ' + str(parameters['interestThreshold']))
        with open(configurationPVact.runConfigurationPath + templateFile + "-" + str(parameters['adoptionThreshold']) + "-" + str(parameters['interestThreshold']) + ".json", "w") as file:
            json.dump(fileData, file, indent=2)
        return configurationPVact.runConfigurationPath + templateFile + '-' + str(parameters['adoptionThreshold']) + '-' + str(parameters['interestThreshold'])
    else:
        print('error! Missing parameters adoptionThreshold, interestThreshold, AP and/or IP in preparing files for PVact')


def deriveFilePrefixGDS(parameters):
    """
    Helper function to construct the file prefix for gridDepthSearch files based on the parameters or default values

    :param parameters: dictionary that should contain the adopter points (AP) and interest points (IP). Will load default values if parameters are not provide.
    :return: a string for the partial file name
    """
    AP = parameters['AP'] if 'AP' in parameters else configurationPVact.gds_defaults['AP']
    IP = parameters['IP'] if 'IP' in parameters else configurationPVact.gds_defaults['IP']
    return 'src/resources/gridDepthSearch-' + str(AP) + str(IP) + '0-'


def generateRootname(parameters):
    """
    Helper function to generate a root string for file naming in the model PVact.
    Uses the AP, IP and the adoption and interest threshold to generate name stubs

    :param parameters: dictionary of parameters containing at least AP, IP, adoptionThreshold and interestThreshold
    :return: string concatenation separated by hyphens
    """
    if(not ('AP' and parameters and 'IP' in parameters and 'adoptionThreshold' in parameters and 'interestThreshold' in parameters)):
        raise KeyError('No parameter provided for AP, IP, adoptionThreshold or interestThreshold')
    else:
        return str(parameters['AP']) + '-' + str(parameters['IP']) + '-' + str(parameters['adoptionThreshold']) + '-' + str(parameters['interestThreshold'])