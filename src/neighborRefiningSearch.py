# Idea: keep a list of points with their 4 nearest neighbors and their distances.
# Pick the point with the highest distance to a neighbor and calculate a new point lying in between the two
# For each point, calculate whether it would be new neighbor (closer than the maxDistance) and potentially integrate in neighbor list


import simulationRunner
from operator import attrgetter
import configuration
import helper

# TODO document
def evaluateNextPoint(X, Y, model, mode, inputFile):
    print('Evaluating point ' + str(X) + ', ' + str(Y))
    runConfigurationPrefix = simulationRunner.prepareJson('src/modelInputFiles/newPoint', model, helper.convertGridInMode(X, Y, model), inputFile)
    data = simulationRunner.invokeJar(runConfigurationPrefix, mode)
    #data = simulationRunner.mockInvokeJar(X, IT)
    print(data)
    protoPoint = Point(float(data), 0, X, Y, None, None, None, None)
    return protoPoint

# TODO document
def fileAppendPoint(point, file):
    outString = '{"X": ' + str(point.X) + ', "Y": ' + str(point.Y) + ', "error": ' + str(point.error) + ', "maxDistance": ' + str(point.maxDistance)
    if (hasattr(point, 'neighborQ1') and not point.neighborQ1 is None):
        outString += ', "neighborQ1": { "X": ' + str(point.neighborQ1.X) + ', "Y": ' + str(point.neighborQ1.Y) + '}'
    if (hasattr(point, 'neighborQ2') and not point.neighborQ2 is None):
        outString += ',  "neighborQ2": { "X": ' + str(point.neighborQ2.X) + ', "Y": ' + str(point.neighborQ2.Y) + '}'
    if (hasattr(point, 'neighborQ3') and not point.neighborQ3 is None):
        outString += ', "neighborQ3": { "X": ' + str(point.neighborQ3.X) + ', "Y": ' + str(point.neighborQ3.Y) + '}'
    if (hasattr(point, 'neighborQ4') and not point.neighborQ4 is None):
        outString += ', "neighborQ4": { "X": ' + str(point.neighborQ4.X) + ', "Y": ' + str(point.neighborQ4.Y) + '}'
    outString += '}\n'
    # print('writing string to file: \n' + writeString)
    file.write(outString)

# TODO document
def rewritePointFile(newPointList):
    file = open(configuration.pointListFile, "w")
    file.close()
    appendFile = open(configuration.pointListFile, "a")
    # print('point list: ' + str(newPointList))
    for point in newPointList:
      #  print('about to save point ' + str(point))
        fileAppendPoint(point, appendFile)
    appendFile.close()

# TODO document
def retrieveFurthestNeighbor(respectivePoint):
    # print('printing neighbors:')
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
    """Determines the distance between two points a and b in two-dimensional space

    :param a: point to find distance in relation to b
    :type a: Point
    :param b: point to find distance in relation to a
    :type b: Point
    :returns distance between given points
    :rtype float
    """
    return (abs(a.X - b.X) / (configuration.optimizationBounds['maxX'] - configuration.optimizationBounds['minX'])  + (abs(a.Y - b.Y) / (configuration.optimizationBounds['maxY'] - configuration.optimizationBounds['minY'])))

def findNeighbors(newPoint, currentPoints):
    """Finds the closest points (neighbors) for a given point in a set of points and attaches them to the Point

    :param newPoint: the point to find neighbors for
    :type newPoint: Point
    :param currentPoints: the set of points to find neighbors in
    :type currentPoints: List<Point>
    :returns newPoint with its neighbors attached
    :rtype Point
    """

    #newPoint.printPoint()
    pointRelationsQ1 = []
    pointRelationsQ2 = []
    pointRelationsQ3 = []
    pointRelationsQ4 = []
    # calculate distances to new point
    for existingPoint in currentPoints:
        respectivePointRelation = PointRelation(existingPoint, abs(newPoint.X - existingPoint.X) + abs(newPoint.Y - existingPoint.Y))
        # Sort point into respective quadrant
        if (existingPoint.X < newPoint.X and existingPoint.Y < newPoint.Y):
            pointRelationsQ3.append(respectivePointRelation)
        elif (existingPoint.X < newPoint.X and existingPoint.Y >= newPoint.Y):
            pointRelationsQ2.append(respectivePointRelation)
        elif (existingPoint.X >= newPoint.X and existingPoint.Y < newPoint.Y):
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

# TODO document
def refineNeighbors(points, newCandidate):
    # For all neighbors of all points, check if the new candidate would be a better neighbor
    neighborsRefined = False
    for point in points:
        # find out what quadrant the new candidate lies wrt the point and check respective neighbor if the new candidate would be a better match
        if(newCandidate.X < point.X and newCandidate.Y < point.Y):
            if (not hasattr(point, 'neighborQ3')):
                point.neighborQ3 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ3)):
                point.neighborQ3 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif(newCandidate.X < point.X and newCandidate.Y >= point.Y):
            if (not hasattr(point, 'neighborQ2')):
                point.neighborQ2 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ2)):
                point.neighborQ2 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif (newCandidate.X >= point.X and newCandidate.Y < point.Y):
            if (not hasattr(point, 'neighborQ4')):
                point.neighborQ4 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ4)):
                point.neighborQ4 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        elif (newCandidate.X >= point.X and newCandidate.Y >= point.Y):
            if (not hasattr(point, 'neighborQ1')):
                point.neighborQ1 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
            elif (pointDistance(point, newCandidate) < pointDistance(point, point.neighborQ1)):
                point.neighborQ1 = ReducedPoint(newCandidate.X, newCandidate.Y)
                neighborsRefined = True
                point.recalculatedMaxDistance()
        else:
            print('ERROR. This case should not occur')
    return neighborsRefined

#TODO document and make more efficient; check for exit condition
def refineList(currentPoints, model, mode, inputFile):
    # for point in currentPoints:
    #     point.printPoint()
    #     point.printNeighbors()
    mostUnrefinedPoint = max(currentPoints, key=attrgetter("maxDistance"))
    print('most unrefined point: ')
    mostUnrefinedPoint.printPoint()
    furthestNeighbor = retrieveFurthestNeighbor(mostUnrefinedPoint)
    print('its furtherst neighbor is ' + furthestNeighbor.generatePointString())
    newPoint = evaluateNextPoint((mostUnrefinedPoint.X + furthestNeighbor.X) / 2, (mostUnrefinedPoint.Y + furthestNeighbor.Y) / 2, model, mode, inputFile)
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
    refineList(currentPoints, model, mode, inputFile)

# TODO document
def neighborRefining(mode, model,scenarioFile):
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
                neighborQ1 = ReducedPoint(neighborQ1Dict['X'], neighborQ1Dict['Y'])
            if ('neighborQ2' in pointDict):
                neighborQ2Dict = pointDict['neighborQ2']
                neighborQ2 = ReducedPoint(neighborQ2Dict['X'], neighborQ2Dict['Y'])
            if ('neighborQ3' in pointDict):
                neighborQ3Dict = pointDict['neighborQ3']
                neighborQ3 = ReducedPoint(neighborQ3Dict['X'], neighborQ3Dict['Y'])
            if ('neighborQ4' in pointDict):
                neighborQ4Dict = pointDict['neighborQ4']
                neighborQ4 = ReducedPoint(neighborQ4Dict['X'], neighborQ4Dict['Y'])
            currentPoint = Point(pointDict['error'], pointDict['maxDistance'], pointDict['X'], pointDict['Y'], neighborQ1, neighborQ2, neighborQ3, neighborQ4)
            pointList.append(currentPoint)
    print(pointList)
    refineList(pointList, model, mode, scenarioFile)

# TODO document data structures
class Point:

    def __init__(self, error, maxDistance, X, Y, neighborQ1, neighborQ2, neighborQ3, neighborQ4):
        self.error = error
        self.maxDistance = maxDistance
        self.X = X
        self.Y = Y
        if(neighborQ1): self.neighborQ1 = neighborQ1
        if(neighborQ2): self.neighborQ2 = neighborQ2
        if(neighborQ3): self.neighborQ3 = neighborQ3
        if(neighborQ4): self.neighborQ4 = neighborQ4

    def generatePointString(self):
        return '(' + str(self.X) + ', ' + str(self.Y) + ')'

    def printPoint(self):
        print('Point (' + str(self.X) + ', ' + str(self.Y) + ') has distance ' + str(self.maxDistance))

    def printNeighbors(self):
        if(hasattr(self, 'neighborQ1')): print('(' + str(self.neighborQ1.X) + ', ' + str(self.neighborQ1.Y) + ') with distance ' + str(pointDistance(self, self.neighborQ1)))
        if(hasattr(self, 'neighborQ2')): print('(' + str(self.neighborQ2.X) + ', ' + str(self.neighborQ2.Y) + ') with distance ' + str(
            pointDistance(self, self.neighborQ2)))
        if(hasattr(self, 'neighborQ3')): print('(' + str(self.neighborQ3.X) + ', ' + str(self.neighborQ3.Y) + ') with distance ' + str(
            pointDistance(self, self.neighborQ3)))
        if(hasattr(self, 'neighborQ4')): print('(' + str(self.neighborQ4.X) + ', ' + str(self.neighborQ4.Y) + ') with distance ' + str(
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
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def printReducedPoint(self):
        print(str(self.X) + ', ' + str(self.Y) + ')')

    def generatePointString(self):
        return '(' + str(self.X) + ', ' + str(self.Y) + ')'

class PointRelation:
    def __init__(self, point, distance):
        self.point = point
        self.distance = distance

