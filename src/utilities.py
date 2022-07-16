import csv
import re
from package import Package
import variables

# strHash is the hash function used in conjunction with the graph hash table.
def strHash(prehash):
    posthash = 1
    for char in prehash:
        posthash ^= ord(char)
    return posthash


# pluckTupleElement() returns a tuple based on a search string from a list. Linear search, O(N) time.
def pluckTupleElement(addrString, tupleList):
    for item in tupleList:
        if item[0] == addrString:
            return item
    pass


# buildMapGraph() constructs the graph (a hash-table of vertexes) from the provided graph.csv file in /data.
def buildMapGraph(routeMap):
    tempVertexList = []
    lineCount = 0
    n = 1
    with open("data/graph.csv", newline=None) as graphfile:
        graphreader = csv.reader(
            graphfile, delimiter=","
        )  # The delivery destinations, in graph form.
        for row in graphreader:
            n = 1
            fromVertex = row[0]
            # Because of the decision to utilize a hash table to quickly find vertices once created and inserted into the Graph list,
            # it is not possible to walk thru the Graph array to figure out what the "to" array is supposed to be.
            # Additional space is allocated, so that the verticies can be accessed according to when they were added.
            routeMap.addVertex(fromVertex)
            tempVertexList.append(fromVertex)
            # Read the distances from the CSV file, and pass that data to addWeightedEdge() to create distance tuples on each vertex.
            while float(row[n]) != None and float(row[n]) != 0:
                toVertex = tempVertexList[n - 1]
                routeMap.addWeightedEdge(
                    fromVertex,
                    toVertex,
                    float(row[n]),
                )
                n += 1
            lineCount += 1
        # Sort vertex distance associations from least distance to greatest distance.
        for vertex in routeMap.totalVertexes:
            if vertex == []:
                continue
            else:
                vertex.relativesTable.sort(key=lambda y: y[1])
        print("Processed", lineCount, "vertexes.")
        variables.totalVertexes = lineCount
        routeMap.addVertex("TRANSIT")


def buildPackageHashTable(routeMap):
    # Takes the CSV-file with the package metadata, and builds the hash-table.
    packages = 0
    with open("data/packages.csv", newline=None) as packagesFile:
        packagesReader = csv.reader(packagesFile, delimiter=",")
        for row in packagesReader:
            delReadyTime = 0
            delDeadline = 0
            pakAffinity = 0
            truckAffinity = 0

            if row[2] != 480:
                delDeadline = int(row[2])
            else:
                delDeadline = 480
            if row[5] != 0:
                delReadyTime = int(row[5])
            else:
                delReadyTime = 0
            if row[6] != "ANY":
                truckAffinity = int(row[6])
            else:
                truckAffinity = "ANY"
            if row[7] != "NONE":
                pakAffinity = row[7]
            else:
                pakAffinity = "NONE"

            currentPackage = Package(
                row[0],  # pakID
                row[1],  # delAddress
                delDeadline,  # delDeadline
                row[3],  # delCity
                row[4],  # delZip
                delReadyTime,  # delReadyTime
                truckAffinity,  # truckAffinity
                pakAffinity,  # pakAffinity
                row[8],  # pakWeight
            )

            if delDeadline != 480:
                variables.priorityQueue.append(currentPackage)

            routeMap.addPackage(currentPackage)
            packages += 1
        variables.priorityQueue.sort(key=lambda pk: pk.delDeadline)
        variables.totalPackages = packages
        print("Processed", packages, "packages.")


# timeTranslator() translates time from human-input 24 hours, to system time (minutes from 0800)
def timeTranslator(timeToTranslate):
    if re.search("\d\d.\d\d", timeToTranslate):
        x = timeToTranslate.split(":")
        y = (int(x[0]) % 24) * 60
        z = int(x[1]) % 60
        q = y + z - 480  # Sets time in minutes from 8:00.
        if q >= 0:
            return q
        else:
            print("Time entered is before 08:00 hours.")
            return None
    else:
        print("Please input time in the format HH:mm, 24 hours.")
        return None


# timeBackTranslator() translates time from system time (minutes from 0800) to human-input 24 hours.
def timeBackTranslator(timeToTranslate):
    timeStr = []
    timeStr.append(str(int(timeToTranslate / 60) + 8))  # hours
    timeStr.append(str(timeToTranslate % 60).zfill(2))  # minutes
    return ":".join(timeStr)


# printSelectPackage() prints a single package.
def printSelectPackage(package):
    print(
        "ID - ADDRESS ------------------------------ DEADLN -- DELTIME - CITY ------------- ZIP -- WEIGHT - STATUS"
    )
    print(
        f"{package.pakID:4} {package.delAddress:38} {timeBackTranslator(package.delDeadline):9} {timeBackTranslator(package.delComplete):9} {package.delCity:18} {package.delZip:6} {package.pakWeight:8} {package.delStatus:8}"
    )


# printPackages() prints all packages in the map hash table.
def printPackages(routeMap):
    allPackages = []
    for vertex in routeMap.totalVertexes:
        if vertex != []:
            for package in vertex.packages:
                allPackages.append(package)
    allPackages.sort(key=lambda pk: int(pk.pakID))
    print(
        "ID - ADDRESS ------------------------------ DEADLN -- DELTIME - CITY ------------- ZIP --- WEIGHT - STATUS"
    )
    for package in allPackages:
        print(
            f"{package.pakID:4} {package.delAddress:38} {timeBackTranslator(package.delDeadline):9} {timeBackTranslator(package.delComplete):9} {package.delCity:18} {package.delZip:6} {package.pakWeight:8} {package.delStatus:8}"
        )
