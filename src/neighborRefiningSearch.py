# Idea: keep a list of points with their 4 nearest neighbors and their distances.
# Pick the point with the highest distance to a neighbor and calculate a new point lying in between the two
# For each point, calculate whether it would be new neighbor (closer than the maxDistance) and potentially integrate in neighbor list


import simulationRunner
from operator import attrgetter
import configuration

def evaluateNextPoint(AT, IT):
    simulationRunner.prepareJson('newPoint', AT, IT)
    data = simulationRunner.invokeJar("src/modelInputFiles/newPoint-" + str(AT)[2:len(str(AT))] + "-" + str(IT))
    protoPoint = Point(float(data), 0, AT, IT, [])
    return protoPoint

def addEvaluatedPoint(point):
    with open(configuration.pointListFile, "a") as file:
        file.write(str(point))

def retrieveFurthestNeighbor(respectivePoint):
    distances = []
    for neighbor in respectivePoint.neighbors:
        distances.append(pointDistance(respectivePoint, neighbor))
    maxDistance = max(distances)
    for neighbor in respectivePoint.neighbors:
        if(pointDistance(respectivePoint, neighbor)== maxDistance): return  neighbor

def pointDistance(a, b):
    return abs(a.AT - b.AT) + abs(a.IT - b.IT)

def findNeighbors(newPoint, currentPoints):
    # calculate distances to new point
    for existingPoint in currentPoints:
        existingPoint.distance = abs(newPoint.AT - existingPoint.AT) + abs(newPoint.IT - existingPoint.IT)
    lowerATlowerITPoints = []
    lowerAThigherITPoints = []
    higherATlowerITPoints = []
    higherIThigherITPoints = []
    # separate them into four lists
    for existingPoint in currentPoints:
        if(existingPoint.AT < newPoint.AT and existingPoint.IT < newPoint.IT): lowerATlowerITPoints.append(existingPoint)
        elif(existingPoint.AT < newPoint.AT and existingPoint.IT >= newPoint.IT): lowerAThigherITPoints.append(existingPoint)
        elif(existingPoint.AT >= newPoint.AT and existingPoint.IT < newPoint.IT): higherATlowerITPoints.append(existingPoint)
        else: higherIThigherITPoints.append(existingPoint)
    # from each list, pick the closest point
    distanceGetter = attrgetter('distance')
    newPoint.neighbors.append(distanceGetter(lowerAThigherITPoints))
    newPoint.neighbors.append(distanceGetter(lowerATlowerITPoints))
    newPoint.neighbors.append(distanceGetter(higherATlowerITPoints))
    newPoint.neighbors.append(distanceGetter(higherIThigherITPoints))
    for neighbor in newPoint.neighbors:
        if(pointDistance(neighbor, newPoint) > newPoint.maxDistance): newPoint.maxDistance = pointDistance(neighbor, newPoint)
    return newPoint

def refineNeighbors(points, newCandidate):
    # For all neighbors of all points, check if the new candidate would be a better neighbor
    for point in points:
        for neighbor in point.neighbors:
            # if the new point would be a better neighbor, override the coordinates and make it the new neighbor
            if(pointDistance(point, newCandidate) < pointDistance(point, neighbor)):
                neighbor.AT = newCandidate.AT
                neighbor.IT = newCandidate.IT
        # recalculate max distance
        point.maxDistance = 0
        for neighbor in point.neighbors:
            if(pointDistance(point, neighbor) > point.maxDistance): point.maxDistance = pointDistance(point, neighbor)

def refineList(currentPoints):
    mostUnrefinedPoint = max(currentPoints, key=attrgetter("maxDistance"))
    furthestNeighbor = retrieveFurthestNeighbor(mostUnrefinedPoint)
    newPoint = evaluateNextPoint((mostUnrefinedPoint.AT + furthestNeighbor.AT) / 2, (mostUnrefinedPoint.IT + furthestNeighbor.IT) / 2)
    addEvaluatedPoint(newPoint)
    findNeighbors(newPoint, currentPoints)
    refineNeighbors(currentPoints, newPoint)
    refineList(currentPoints.append(newPoint))

class Point:

    def __init__(self, error, maxDistance, AT, IT, neighbors):
        self.error = error
        self.maxDistance = maxDistance
        self.AT = AT
        self.IT = IT
        self.neighbors = neighbors

class ReducedPoint:
    def __init__(self, AT, IT):
        self.AT = AT
        self.IT = IT