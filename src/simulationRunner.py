from subprocess import check_output, CalledProcessError
import json
import sys
import os

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
def invokeJar(inputFile, modeParameters, shelLFlag):
    try:
        if(modeParameters == 'weightedCumulativeAnnualAdoptionDelta'):
            data = check_output(
                ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o',
                 'example-output.json',
                 '--noConsole', '--logPath', 'log.log', '--calculatePerformance', 'cumulativeAnnualAdoptionDelta'],
                shell=shelLFlag).decode('utf-8').rstrip()
            return aggregateData(data, 'weightedCumulativeAnnualAdoptionDelta')
        else:
            print('using file ' + inputFile)
            data = check_output(
                ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o', 'example-output.json',
                 '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters, '--gnuplotCommand', 'C:/Users/mai11dlx/gnuplot/bin/gnuplot.exe'], shell=shelLFlag).decode('utf-8').rstrip()
            if (len(data.split('{')) > 1):
                return aggregateData(data)
            else:
                return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()

# mock function to test the rest of the module
def mockInvokeJar(AT, IT):
    if(AT > 0 and IT > 0):
        return (1/(AT*IT))
    else:
        return 999999

# function that manipulates the scenario definition to fit the adoption and interest threshold for the desired run
# file is saved in the path and prefix specified by the templateFile parameter
def prepareJson(templateFile, adoptionThreshold, interestThreshold, AP, IP):
    navigateToTop()
    f = open('src/resources/example-input.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_adopterPoints'] = int(AP)
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_interestedPoints'] = int(IP)
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
    print('writing file with AP ' + str(AP) + ' and IP ' + str(IP) + ' and AT ' + str(adoptionThreshold) + ' and IT ' + str(interestThreshold))
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file, indent=2)

def prepareJsonDefaultIT(templateFile, adoptionThreshold, interestThreshold):
    f = open('src/resources/example-input_old.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file)