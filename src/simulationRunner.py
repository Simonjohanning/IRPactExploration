from subprocess import check_output, CalledProcessError
import json
import sys
import os


def navigateToTop():
    currentDirArray = os.getcwd().split('\\')
    currentSubDir = currentDirArray[-1]
    if (currentSubDir == 'PycharmProjects'):
        os.chdir('./IRPactAutomizer')
        print('change to ' + os.getcwd())
    elif (not currentSubDir == 'IRPactAutomizer'):
        print('current dir is ' + os.getcwd() + '; navigating up')
        os.chdir('../')

# function to run the (repo-based current) version of the model instance with the conversation
# given in the input file
def invokeJar(inputFile, modeParameters, shelLFlag):
    try:
        if(shelLFlag):
            data = check_output(
                ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o', 'example-output.json',
                 '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters], shell=True)
            t = 0, data.decode('utf-8').rstrip()
            return data
        else:
            data = check_output(
                ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o',
                 'example-output.json',
                 '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters])
            t = 0, data.decode('utf-8').rstrip()
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
        'par_InCommunicationModule3_actionnode3_adopterPoints'] = AP
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_interestedPoints'] = IP
    fileData['data'][0]['years'][0]['sets']['set_InCommunicationModule3_actionnode3']['COMMU_ACTION'][
        'par_InCommunicationModule3_actionnode3_awarePoints'] = 0
    print('writing file with AP ' + str(AP) + ' and IP ' + str(IP))
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file)

def prepareJsonDefaultIT(templateFile, adoptionThreshold, interestThreshold):
    f = open('src/resources/example-input.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
    with open(templateFile+"-"+str(adoptionThreshold)[2:len(str(adoptionThreshold))]+"-"+str(interestThreshold)+".json", "w") as file:
        json.dump(fileData, file)