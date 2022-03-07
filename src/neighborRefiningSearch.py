# Idea: keep a list of points with their 4 nearest neighbors and their distances.
# Pick the point with the highest distance to a neighbor and calculate a new point lying in between the two
# For each point, calculate whether it would be new neighbor (closer than the maxDistance) and potentially integrate in neighbor list


import simulationRunner
from operator import attrgetter
import configuration

def evaluateNextPoint(AT, IT):
    simulationRunner.prepareJson('src/modelInputFiles/newPoint', AT, IT)
    data = simulationRunner.invokeJar("src/modelInputFiles/newPoint-" + str(AT)[2:len(str(AT))] + "-" + str(IT), mode)
    print(data)
    protoPoint = Point(float(data), 0, AT, IT, [])
    return protoPoint

def fileAppendPoint(point, file):
    outstring = '{"AT": ' + str(point.AT) + ', "IT": ' + str(point.IT) + ', "error": ' + str(point.error) + ', "maxDistance": ' + str(point.maxDistance) + ', "neighbors": [ '
    for neighborEntry in point.neighbors:
        outstring += '{"AT": ' + str(neighborEntry.AT) + ', "IT": ' + str(neighborEntry.IT) + '}, '
    writeString = outstring[:-2] + ']}\n'
    print('writing string to file: \n' + writeString)
    file.write(writeString)

def rewritePointFile(newPointList):
    file = open(configuration.pointListFile, "w")
    file.close()
    appendFile = open(configuration.pointListFile, "a")
    print('point list: ' + str(newPointList))
    for point in newPointList:
        print('about to save point ' + str(point))
        fileAppendPoint(point, appendFile)
    appendFile.close()

def retrieveFurthestNeighbor(respectivePoint):
    distances = []
    for neighbor in respectivePoint.neighbors:
        distances.append(pointDistance(respectivePoint, neighbor))
    maxDistance = max(distances)
    for neighbor in respectivePoint.neighbors:
        if(pointDistance(respectivePoint, neighbor)== maxDistance): return neighbor

def pointDistance(a, b):
    return abs(a.AT - b.AT) + (abs(a.IT - b.IT) / configuration.maxInterestThreshold)

def findNeighbors(newPoint, currentPoints):
    # calculate distances to new point
    print('in findNeighbors: ' + str(currentPoints))
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
        print(str(existingPoint) + ' of ' + str(currentPoints))
    # from each list, pick the closest point
    # print(pointRelationsQ1)
    # print(min(pointRelationsQ1, key=attrgetter('distance')))
    # print(type(min(pointRelationsQ1, key=attrgetter('distance'))))
    # print(min(pointRelationsQ1, key=attrgetter('distance')).point)
    if(len(pointRelationsQ1) > 0):
        newPoint.neighbors.append(min(pointRelationsQ1, key=attrgetter('distance')).point)
    if (len(pointRelationsQ2) > 0):
        newPoint.neighbors.append(min(pointRelationsQ2, key=attrgetter('distance')).point)
    if (len(pointRelationsQ3) > 0):
        newPoint.neighbors.append(min(pointRelationsQ3, key=attrgetter('distance')).point)
    if (len(pointRelationsQ4) > 0):
        newPoint.neighbors.append(min(pointRelationsQ4, key=attrgetter('distance')).point)
    for neighbor in newPoint.neighbors:
        if(pointDistance(neighbor, newPoint) > newPoint.maxDistance): newPoint.maxDistance = pointDistance(neighbor, newPoint)
    print('point distance of new point is '  + str(newPoint.maxDistance))
    print(str(currentPoints))
    return newPoint

def refineNeighbors(points, newCandidate):
    # For all neighbors of all points, check if the new candidate would be a better neighbor
    neighborsRefined = False
    for point in points:
        for neighbor in point.neighbors:
            # if the new point would be a better neighbor, override the coordinates and make it the new neighbor
            if(pointDistance(point, newCandidate) < pointDistance(point, neighbor)):
                neighbor.AT = newCandidate.AT
                neighbor.IT = newCandidate.IT
                neighborsRefined = True
        # recalculate max distance
        point.maxDistance = 0
        for neighbor in point.neighbors:
            if(pointDistance(point, neighbor) > point.maxDistance): point.maxDistance = pointDistance(point, neighbor)
    return neighborsRefined

def refineList(currentPoints):
    mostUnrefinedPoint = max(currentPoints, key=attrgetter("maxDistance"))
    furthestNeighbor = retrieveFurthestNeighbor(mostUnrefinedPoint)
    newPoint = evaluateNextPoint((mostUnrefinedPoint.AT + furthestNeighbor.AT) / 2, (mostUnrefinedPoint.IT + furthestNeighbor.IT) / 2)
    findNeighbors(newPoint, currentPoints)
    if refineNeighbors(currentPoints, newPoint):
        currentPoints.append(newPoint)
        rewritePointFile(currentPoints)
    else:
        appendFile = open(configuration.pointListFile, "a")
        fileAppendPoint(newPoint, appendFile)
        currentPoints.append(newPoint)
    refineList(currentPoints)

def neighborRefining(errorMode):
    global mode
    mode = errorMode
    pointList = []
    print('reading file ' + configuration.pointListFile)
    with open(configuration.pointListFile, 'r') as file:
        for line in file:
            print('reading line ' + line)
            pointDict = eval(line)
            #print(pointDict['neighbors'])
            print(type(pointDict['neighbors']))
            currentPoint = Point(pointDict['error'], pointDict['maxDistance'], pointDict['AT'], pointDict['IT'], pointDict['neighbors'])
            pointList.append(currentPoint)
    print(pointList)
    refineList(pointList)

class Point:

    def __init__(self, error, maxDistance, AT, IT, neighbors):
        self.error = error
        self.maxDistance = maxDistance
        self.AT = AT
        self.IT = IT
        neighborList = []
        for entry in neighbors:
            reducedPoint = ReducedPoint(entry['AT'], entry['IT'])
            neighborList.append(reducedPoint)
        self.neighbors = neighborList

class ReducedPoint:
    def __init__(self, AT, IT):
        self.AT = AT
        self.IT = IT

class PointRelation:
    def __init__(self, point, distance):
        self.point = point
        self.distance = distance