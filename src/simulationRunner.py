import helper
import PVactModelHelper
from subprocess import check_output, CalledProcessError
import json
import sys
import os

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
        print('hasntAttr')
        print(dictData)

def invokeJar(inputFile, modeParameters, model, shellFlag):
    """
    Function to invoke a jar-based model file based on the parameters provided.
    Selects the file and creates the invokation command based on the model specified.
    Returns the performance of the run and aggregates it if necessary

    :param inputFile: the file specifying the configuration of the respective simulation run as required by the model
    :param modeParameters: additional parameters required for the run of the respective model
    :param model: the model to execute the simulation for
    :param shellFlag: the shellFlag for the execution of the jar
    :return: the performance of the model run
    """
    try:
        if(modeParameters == 'weightedCumulativeAnnualAdoptionDelta' and model == 'PVact'):
            data = check_output(PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta', {'inputFile': inputFile}),
                shell=shellFlag).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        elif(model == 'PVact'):
            print('using file ' + inputFile)
            data = check_output(PVactModelHelper.constructInvokationCommand('PVact_internal', {'inputFile': inputFile, 'modeParameters': modeParameters}), shell=shellFlag).decode('utf-8').rstrip()
            print(data)
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()

def invokeJarExternalData(inputFile, modeParameters, shellFlag, dataDirPath):
    """
    Function to invoke a jar-based model file with an external data directory based on the parameters provided.
    Selects the file and creates the invocation command based on the model specified.
    Returns the performance of the run and aggregates it if necessary.
    For the PVact_external mode, the path to GNU plot must be provided (as gnuPlotPath in the modeParameters)

    :param inputFile: the file specifying the configuration of the respective simulation run as required by the model
    :param modeParameters: additional parameters required for the run of the respective model
    :param model: the model to execute the simulation for
    :param shellFlag: the shellFlag for the execution of the jar
    :param dataDirPath: path to the external data directory to be used
    :return: the performance of the model run
    """
    try:
        if(modeParameters == 'weightedCumulativeAnnualAdoptionDelta'):
            data = check_output( PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta_external', {'dataDirPath': dataDirPath})
               ,
                shell=shellFlag).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        else:
            print('using file ' + inputFile)
            # modeParameter needs to contain the gnuFilePath in order for this to work
            data = check_output(
               PVactModelHelper.constructInvokationCommand('PVact_external', {'inputFile': inputFile, 'dataDirPath': dataDirPath, **modeParameters}), shell = shellFlag).decode('utf-8').rstrip()
            print(data)
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()


# function that manipulates the scenario definition to fit the adoption and interest threshold for the desired run
# file is saved in the path and prefix specified by the templateFile parameter
# TODO Adjust description and document
def prepareJson(templateFile, model, modeParameters, inputFile):
    if(model == 'PVact'):
        if(modeParameters['interestThreshold'] and modeParameters['adoptionThreshold'] and modeParameters['AP'] and modeParameters['IP'] and modeParameters['currentSeed']):
            returnFile = PVactModelHelper.prepareJSON(templateFile, inputFile, modeParameters['interestThreshold'], modeParameters['adoptionThreshold'], modeParameters['AP'], modeParameters['IP'], modeParameters['currentSeed'])
            print('Run configuration data written in file ' + returnFile + '.')
            return returnFile
        else:
            helper.printMissingParameters(modeParameters, ['interestThreshold', 'adoptionThreshold', 'AP', 'IP', 'currentSeed'])

# TODO consolidate with TODO in IRPactValWrapper about missing parameter hack
def prepareJsonDefaultIT(templateFile, adoptionThreshold, interestThreshold):
    f = open('src/resources/example-input_old.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file)