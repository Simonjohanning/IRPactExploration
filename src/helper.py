import json

# Simple helper function to determine the number of (line-based) data points in the specified file
def determineDataPoints(dataPath):
    with open(dataPath, 'r') as file:
        return (len(file.readlines()))

# Helper function to extract the total number of cumulated adoptions from the provided file
# @TODO make more general
def extractData(path):
    f = open(path, "r")
    fileData = json.loads(f.read())
    return fileData['cumulated']['total']

