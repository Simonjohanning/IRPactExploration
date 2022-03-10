from subprocess import check_output, CalledProcessError
import json
import sys

# function to run the (repo-based current) version of the model instance with the conversation
# given in the input file
def invokeJar(inputFile, modeParameters):
    try:
        print('attempting to run jar')
        data = check_output(
            ['java', '-jar', 'src/resources/IRPact-1.0-SNAPSHOT-uber.jar', '-i', inputFile + '.json', '-o', 'example-output.json',
             '--noConsole', '--logPath', 'log.log', '--calculatePerformance', modeParameters])
        t = 0, data.decode('utf-8').rstrip()
        print('jar call successful')
        return data
    except CalledProcessError as e:
        print('ran into exception for jar call')
        print(e)
        sys.exit()

# mock function to test the rest of the module
def mockInvokeJar(AT, IT):
    if(AT > 0):
        return (1/(AT*IT))
    else:
        return 999999

# function that manipulates the scenario definition to fit the adoption and interest threshold for the desired run
# file is saved in the path and prefix specified by the templateFile parameter
def prepareJson(templateFile, adoptionThreshold, interestThreshold):
    f = open('src/resources/example-input.json', "r")
    fileData = json.loads(f.read())
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['INTEREST_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = interestThreshold
    fileData['data'][0]['years'][0]['sets']['set_InDiracUnivariateDistribution']['ADOPTION_THRESHOLD'][
        'par_InDiracUnivariateDistribution_value'] = adoptionThreshold
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