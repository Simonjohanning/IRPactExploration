# Idea: keep a list of points with their 4 nearest neighbors and their distances.
# Pick the point with the highest distance to a neighbor and calculate a new point lying in between the two
# For each point, calculate whether it would be new neighbor (closer than the maxDistance) and potentially integrate in neighbor list


import simulationRunner
from operator import attrgetter
import configuration

def evaluateNextPoint(AT, IT, inputFile):
    print('Evaluating point ' + str(AT) + ', ' + str(IT))
    simulationRunner.prepareJson('src/modelInputFiles/newPoint', AT, IT, inputFile)
    data = simulationRunner.invokeJar("src/modelInputFiles/newPoint-" + str(AT)[2:len(str(AT))] + "-" + str(IT), mode)
    #data = simulationRunner.mockInvokeJar(AT, IT)
    print(data)
    protoPoint = Point(float(data), 0, AT, IT, None, None, None, None)
    return protoPoint

def fileAppendPoint(point, file):
    outString = '{"AT": ' + str(point.AT) + ', "IT": ' + str(point.IT) + ', "error": ' + str(point.error) + ', "maxDistance": ' + str(point.maxDistance)
    if (hasattr(point, 'neighborQ1') and not point.neighborQ1 is None):
        outString += ', "neighborQ1": { "AT": ' + str(point.neighborQ1.AT) + ', "IT": ' + str(point.neighborQ1.IT) + '}'
    if (hasattr(point, 'neighborQ2') and not point.neighborQ2 is None):
        outString += ',  "neighborQ2": { "AT": ' + str(point.neighborQ2.AT) + ', "IT": ' + str(point.neighborQ2.IT) + '}'
    if (hasattr(point, 'neighborQ3') and not point.neighborQ3 is None):
        outString += ', "neighborQ3": { "AT": ' + str(point.neighborQ3.AT) + ', "IT": ' + str(point.neighborQ3.IT) + '}'
    if (hasattr(point, 'neighborQ4') and not point.neighborQ4 is None):
        outString += ', "neighborQ4": { "AT": ' + str(point.neighborQ4.AT) + ', "IT": ' + str(point.neighborQ4.IT) + '}'
    outString += '}\n'
    # print('writing string to file: \n' + writeString)
    file.write(outString)

def rewritePointFile(newPointList):
    file = open(configuration.pointListFile, "w")
    file.close()
    appendFile = open(configuration.pointListFile, "a")
    # print('point list: ' + str(newPointList))
    for point in newPointList:
      #  print('about to save point ' + str(point))
        fileAppendPoint(point, appendFile)
    appendFile.close()

def retrieveFurthestNeighbor(respectivePoint):
    print('printing neighbors:')
    respectivePoint.printNeighbors()
    if (hasattr(respectivePoint, 'neighborQ1')):
        if (pointDistance(respectivePoint, respectivePoint.neighborQ1) == respectivePoint.maxDistance):
            return respectivePoint.neighborQ1
    if (hasattr(respectivePoint, 'neighborQ2')):
        if (pointDistance(respectivePoint, respectivePoint.neighborQ2) == respectivePoint.maxDistance):
            return respectivePoint.neighborQ2
    if (hasattr(respectivePoint, 'neighborQ3')):
        if (pointDistance(respectivePoint, respectivePoint.neighborQ3) == respectivePoint.maxDistance):
            return respectivePoint.neighborQ3
    if (hasattr(respectivePoint, 'neighborQ4')):
        if (pointDistance(respectivePoint, respectivePoint.neighborQ4) == respectivePoint.maxDistance):
            return respectivePoint.neighborQ4

def pointDistance(a, b):
    return abs(a.AT - b.AT) + (abs(a.IT - b.IT) / configuration.optimizationBounds['maxInterestThreshold'])

def findNeighbors(newPoint, currentPoints):
    # calculate distances to new point
   # print('in findNeighbors: ' + str(currentPoints))
    print('finding neighbors for new point')
    newPoint.printPoint()
    pointRelationsQ1 = []
    pointRelationsQ2 = []
    pointRelationsQ3 = []
    pointRelationsQ4 = []
    for existingPoint in currentPoints:
        respectivePointRelation = PointRelation(existingPoint, abs(newPoint.AT - existingPoint.AT) + abs(newPoint.IT - existingPoint.IT))
        # Sort point into respective quadrant
        if (existingPoint.AT < newPoint.AT and existingPoint.IT < newPoint.IT):
            pointRelationsQ3.append(respectivePointRelation)
        elif (existingPoint.AT < newPoint.AT and existingPoint.IT >= newPoint.IT):
            pointRelationsQ2.append(respectivePointRelation)
        elif (existingPoint.AT >= newPoint.AT and existingPoint.IT < newPoint.IT):
            pointRelationsQ4.append(respectivePointRelation)
        else:
            pointRelationsQ1.append(respectivePointRelation)
    #    print(str(existingPoint) + ' of ' + str(currentPoints))
    # from each list, pick the closest point
    # print(pointRelationsQ1)
    # print(min(pointRelationsQ1, key=attrgetter('distance')))
    # print(type(min(pointRelationsQ1, key=attrgetter('distance'))))
    # print(min(pointRelationsQ1, key=attrgetter('distance')).point)
    if(len(pointRelationsQ1) > 0):
        newPoint.neighborQ1 = min(pointRelationsQ1, key=attrgetter('distance')).point
    if (len(pointRelationsQ2) > 0):
        newPoint.neighborQ2 = min(pointRelationsQ2, key=attrgetter('distance')).point
    if (len(pointRelationsQ3) > 0):
        newPoint.neighborQ3 = min(pointRelationsQ3, key=attrgetter('distance')).point
    if (len(pointRelationsQ4) > 0):
        newPoint.neighborQ4 = min(pointRelationsQ4, key=attrgetter('distance')).point
    newPoint.recalculatedMaxDistance()
    print('point distance of new point is ' + str(newPoint.maxDistance))
    #print(str(currentPoints))
    return newPoint

def refineNeighbors(points, newCandidate):
    # For all neighbors of all points, check if the new candidate would be a better neighbor
    neighborsRefined = False
    for point in points:
        # find out what quadrant the new candidate lies wrt the point and check respective neighbor if the new candidate would be a better match
        if(newCandidate.AT < point.AT and newCandidate.IT < point.IT):
            if (not hasattr(point, 'neighborQ3')):
                point.neighborQ3 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ3)):
                point.neighborQ3 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif(newCandidate.AT < point.AT and newCandidate.IT >= point.IT):
            if (not hasattr(point, 'neighborQ2')):
                point.neighborQ2 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ2)):
                point.neighborQ2 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif (newCandidate.AT >= point.AT and newCandidate.IT < point.IT):
            if (not hasattr(point, 'neighborQ4')):
                point.neighborQ4 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ4)):
                point.neighborQ4 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif (newCandidate.AT >= point.AT and newCandidate.IT >= point.IT):
            if (not hasattr(point, 'neighborQ1')):
                point.neighborQ1 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ1)):
                point.neighborQ1 = ReducedPoint(newCandidate.AT, newCandidate.IT)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        else:
            print('ERROR. This case should not occur')
    return neighborsRefined

def refineList(currentPoints, inputFile):
    # for point in currentPoints:
    #     point.printPoint()
    #     point.printNeighbors()
    mostUnrefinedPoint = max(currentPoints, key=attrgetter("maxDistance"))
    print('most unrefined point: ')
    mostUnrefinedPoint.printPoint()
    furthestNeighbor = retrieveFurthestNeighbor(mostUnrefinedPoint)
    print('its furtherst neighbor is ' + furthestNeighbor.generatePointString())
    newPoint = evaluateNextPoint((mostUnrefinedPoint.AT + furthestNeighbor.AT) / 2, (mostUnrefinedPoint.IT + furthestNeighbor.IT) / 2, inputFile)
    findNeighbors(newPoint, currentPoints)
    if refineNeighbors(currentPoints, newPoint):
        print('neighbors refined')
        currentPoints.append(newPoint)
        rewritePointFile(currentPoints)
    else:
        appendFile = open(configuration.pointListFile, "a")
        print('no neighbor refinement found necessary')
        fileAppendPoint(newPoint, appendFile)
        currentPoints.append(newPoint)
    refineList(currentPoints, inputFile)

def neighborRefining(errorMode, scenarioFile):
    global mode
    mode = errorMode
    pointList = []
    print('reading file ' + configuration.pointListFile)
    with open(configuration.pointListFile, 'r') as file:
        for line in file:
         #   print('reading line ' + line)
            pointDict = eval(line)
            #print(pointDict['neighbors'])
        #    print(type(pointDict['neighbors']))
            neighborQ1 = None
            neighborQ2 = None
            neighborQ3 = None
            neighborQ4 = None
            if ('neighborQ1' in pointDict):
                neighborQ1Dict = pointDict['neighborQ1']
                neighborQ1 = ReducedPoint(neighborQ1Dict['AT'], neighborQ1Dict['IT'])
            if ('neighborQ2' in pointDict):
                neighborQ2Dict = pointDict['neighborQ2']
                neighborQ2 = ReducedPoint(neighborQ2Dict['AT'], neighborQ2Dict['IT'])
            if ('neighborQ3' in pointDict):
                neighborQ3Dict = pointDict['neighborQ3']
                neighborQ3 = ReducedPoint(neighborQ3Dict['AT'], neighborQ3Dict['IT'])
            if ('neighborQ4' in pointDict):
                neighborQ4Dict = pointDict['neighborQ4']
                neighborQ4 = ReducedPoint(neighborQ4Dict['AT'], neighborQ4Dict['IT'])
            currentPoint = Point(pointDict['error'], pointDict['maxDistance'], pointDict['AT'], pointDict['IT'], neighborQ1, neighborQ2, neighborQ3, neighborQ4)
            pointList.append(currentPoint)
    print(pointList)
    refineList(pointList, scenarioFile)

class Point:

    def __init__(self, error, maxDistance, AT, IT, neighborQ1, neighborQ2, neighborQ3, neighborQ4):
        self.error = error
        self.maxDistance = maxDistance
        self.AT = AT
        self.IT = IT
        if(neighborQ1): self.neighborQ1 = neighborQ1
        if(neighborQ2): self.neighborQ2 = neighborQ2
        if(neighborQ3): self.neighborQ3 = neighborQ3
        if(neighborQ4): self.neighborQ4 = neighborQ4

    def generatePointString(self):
        return '(' + str(self.AT) + ', ' + str(self.IT) + ')'

    def printPoint(self):
        print('Point (' + str(self.AT) + ', ' + str(self.IT) + ') has distance ' + str(self.maxDistance))

    def printNeighbors(self):
        if(hasattr(self, 'neighborQ1')): print('(' + str(self.neighborQ1.AT) + ', ' + str(self.neighborQ1.IT) + ') with distance ' + str(pointDistance(self, self.neighborQ1)))
        if(hasattr(self, 'neighborQ2')): print('(' + str(self.neighborQ2.AT) + ', ' + str(self.neighborQ2.IT) + ') with distance ' + str(
            pointDistance(self, self.neighborQ2)))
        if(hasattr(self, 'neighborQ3')): print('(' + str(self.neighborQ3.AT) + ', ' + str(self.neighborQ3.IT) + ') with distance ' + str(
            pointDistance(self, self.neighborQ3)))
        if(hasattr(self, 'neighborQ4')): print('(' + str(self.neighborQ4.AT) + ', ' + str(self.neighborQ4.IT) + ') with distance ' + str(
            pointDistance(self, self.neighborQ4)))

    def recalculatedMaxDistance(self):
        self.maxDistance = 0
        if(hasattr(self, 'neighborQ1')):
            if (pointDistance(self, self.neighborQ1) > self.maxDistance): self.maxDistance = pointDistance(self, self.neighborQ1)
        if(hasattr(self, 'neighborQ2')):
            if (pointDistance(self, self.neighborQ2) > self.maxDistance): self.maxDistance = pointDistance(self, self.neighborQ2)
        if(hasattr(self, 'neighborQ3')):
            if (pointDistance(self, self.neighborQ3) > self.maxDistance): self.maxDistance = pointDistance(self, self.neighborQ3)
        if(hasattr(self, 'neighborQ4')):
            if (pointDistance(self, self.neighborQ4) > self.maxDistance): self.maxDistance = pointDistance(self, self.neighborQ4)

class ReducedPoint:
    def __init__(self, AT, IT):
        self.AT = AT
        self.IT = IT

    def printReducedPoint(self):
        print(str(self.AT) + ', ' + str(self.IT) + ')')

    def generatePointString(self):
        return '(' + str(self.AT) + ', ' + str(self.IT) + ')'

class PointRelation:
    def __init__(self, point, distance):
        self.point = point
        self.distance = distance

