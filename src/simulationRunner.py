import helper
import PVactModelHelper
from subprocess import check_output, CalledProcessError
import json
import sys
import os

# TODO document
def aggregateData(data, specialMode=None):
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


# function to run the (repo-based current) version of the model instance with the conversation
# given in the input file
# TODO adjust doumentation
def invokeJar(inputFile, modeParameters, model, shellFlag):
    try:
        if(modeParameters == 'weightedCumulativeAnnualAdoptionDelta' and model == 'PVact'):
            data = check_output(PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta', {'inputFile': inputFile}),
                shell=shellFlag).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        elif(model == 'PVact'):
            print('using file ' + inputFile)
            data = check_output(
                PVactModelHelper.constructInvokationCommand('PVact_internal', {'inputFile': inputFile}, modeParameters), shell=shellFlag).decode('utf-8').rstrip()
            print(data)
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()


# function to run the (repo-based current) version of the model instance with the conversation
# given in the input file
def invokeJarExternalData(inputFile, modeParameters, shellFlag, externalPath):
    try:
        if(modeParameters == 'weightedCumulativeAnnualAdoptionDelta'):
            data = check_output( PVactModelHelper.constructInvokationCommand('PVact_weightedCumulativeAnnualAdoptionDelta_external', {'externalPath': externalPath})
               ,
                shell=shellFlag).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        else:
            print('using file ' + inputFile)
            data = check_output(
               PVactModelHelper.constructInvokationCommand('PVact_external', {'inputFile': inputFile, 'externalPath': externalPath, 'modeParameters': modeParameters}), shell = shellFlag).decode('utf-8').rstrip()
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
# TODO Adjust description
def prepareJson(templateFile, mode, modeParameters, inputFile):
    if(mode == 'PVact'):
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