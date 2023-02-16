"""
Module to prepare and execute single model runs as well as processing output data
"""

import helper
import PVactModelHelper
from subprocess import check_output, CalledProcessError
import sys
import configuration

# TODO remove specificity and inconsistency in the code
def aggregateData(data, specialMode=None):
    """
    Helper function to aggregate data provided as a series by a model run into a scalar.
    Implements different weighting for the different entries.

    :param data: the data as output by the simulation run (as time series)
    :param specialMode: parameter to indicate a weighting function. If none is provided, the average is calculated
    :return: A single scalar to describe the performance of the simulation.
    """
    dictData = eval(data)
    if(specialMode):
        if(specialMode == 'weightedCumulativeAnnualAdoptionDelta'):
            # Weight terms by the index, by how often they appear in the error cumulation); penalizes later deviations more strongly, making sure the series is matched decently early enough
            error = 0
            index = 0
            # print('weightedCumulativeAnnualAdoptionDelta')
            # print(str(dictData['cumulativeAnnualAdoptionDelta']))
            for entry in dictData['cumulativeAnnualAdoptionDelta']:
                # print('error at ' + str(index) + ' is ' + str(entry))
                # print('weighted to ' + str(entry * index / (len(dictData['cumulativeAnnualAdoptionDelta']))))
                error += abs(entry) * index / (len(dictData['cumulativeAnnualAdoptionDelta']) - index)
                index += 1
            return error / len(dictData['cumulativeAnnualAdoptionDelta'])
    elif ('cumulativeAnnualAdoptionDelta' in dictData):
        return abs(sum(dictData['cumulativeAnnualAdoptionDelta']) / float(len(dictData['cumulativeAnnualAdoptionDelta'])))
    else:
        print(dictData)
        raise NotImplementedError('No method provided for the aggregation mode.')


# TODO Make consistent in exception handling with rest of the code base
def invokeJar(inputFile, errorDef, model, logID):
    """
    Function to invoke a jar-based model file based on the parameters provided.
    Selects the file and creates the invocation command based on the model specified.
    Returns the performance of the run and aggregates it if necessary

    :param inputFile: the file specifying the configuration of the respective simulation run as required by the model
    :param errorDef: the definition of the errorMetric
    :param model: the model to execute the simulation for
    :param logID: An ID for the log file to be created for the run
    :return: the performance of the model run
    """
    try:
        if(errorDef == 'weightedCumulativeAnnualAdoptionDelta' and model == 'PVact'):
            data = check_output(PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta', {'inputFile': inputFile}),
                shell=False).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        elif(model == 'PVact'):
            #print('using file ' + inputFile)
            data = check_output(PVactModelHelper.constructInvokationCommand('PVact_internal', {'inputFile': inputFile, 'errorDef': errorDef, 'logFile': 'log' + str(logID) + '.log'}), shell=False).decode('utf-8').rstrip()
            print(data)
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()

# TODO Make consistent in exception handling with rest of the code base
def invokeJarExternalData(inputFile, errorMode, logID, dataDirPath):
    """
    Function to invoke a jar-based model file with an external data directory based on the parameters provided.
    Selects the file and creates the invocation command based on the model specified.
    Returns the performance of the run and aggregates it if necessary.

    :param inputFile: the file specifying the configuration of the respective simulation run as required by the model
    :param errorMode: the mode to weigh the errors in the jar
    :param model: the model to execute the simulation for
    :param shellFlag: the shellFlag for the execution of the jar
    :param dataDirPath: path to the external data directory to be used
    :return: the performance of the model run
    """
    try:
        if(errorMode == 'weightedCumulativeAnnualAdoptionDelta'):
            data = check_output( PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta_external', {'dataDirPath': dataDirPath})
               ,
                shell=False).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        else:
            print('using file ' + inputFile)
            # modeParameter needs to contain the gnuFilePath in order for this to work
            # TODO rename logID that is abused now
            data = check_output(
               PVactModelHelper.constructInvokationCommand('PVact_external', {'inputFile': inputFile, 'dataDirPath': dataDirPath, 'gnuPlotPath': configuration.gnuPlotPath, 'errorDef': errorMode, 'logFile': 'log' + str(logID) + '.log', 'outputFolder': 'output' + str(logID)}), shell = False).decode('utf-8').rstrip()
            print(data)
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()


# TODO Adjust description and document
# TODO fix calls from neighbourhood search and Wrapper since parameters changed (check simulationManager for reference)
def prepareJson(filenamePrefix, model, modeParameters, inputFile):
    """
    Function to manipulate a json-based scenario definition file to fit the parameters for the desired run.
    The file is saved in the path and prefix specified by the templateFile parameter.

    :param filenamePrefix: file name stub before scenario-specific parameters are attached
    :param model: the model to be executed
    :param modeParameters: parameter dictionary that contains the model-specific parameters for the execution
    :param inputFile: json scenario file that is changed for the specific run
    :return: the filename of the written json file
    """
    if(model == 'PVact'):
        if(('interestThreshold' in modeParameters) and ('adoptionThreshold' in modeParameters) and ('AP' in modeParameters) and ('IP' in modeParameters) and ('currentSeed' in modeParameters) and ('communicationFlag' in modeParameters)):
            print('communicationFlag is ' + str(modeParameters['communicationFlag']))
            returnFile = PVactModelHelper.prepareJSON(filenamePrefix, inputFile, modeParameters['interestThreshold'], modeParameters['adoptionThreshold'], modeParameters['AP'], modeParameters['IP'], modeParameters['currentSeed'], modeParameters['communicationFlag'])
            print('Run configuration data written in file ' + returnFile + '.')
            return returnFile
        else:
            helper.printMissingParameters(modeParameters, ['interestThreshold', 'adoptionThreshold', 'AP', 'IP', 'currentSeed'])
    else:
        raise NotImplementedError('JSON preparation for model ' + model + ' not implemented.')