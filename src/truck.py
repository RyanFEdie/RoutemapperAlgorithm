from mapHashTable import Vertex
from utilities import pluckTupleElement
import variables


class devTruck:
    lastLocation = None
    currentLocation = None
    nextLocation = None
    truckID = 0
    stopList = []
    totalMileage = 0
    currentLeg = 0
    embarkTime = 0
    truckPackages = 0

    def __init__(self, truckID, routeMap):
        self.truckID = truckID
        self.currentLocation = routeMap.searchByAddress("4001 South 700 East")
        self.stopList = []
        self.totalMileage = 0
        self.embarkTime = 0
        variables.activeTrucks += 1

    def buildRoute(self, routeMap):
        tryVertex = 0
        affinityPackageVertexes = []
        # Loop until we handle all packages. If this function is called, and all packages are either delivered or on a truck, do nothing.
        if variables.packagesOut == True:
            return None
        while (
            self.truckPackages < variables.truckCapacity
            and variables.totalPackagesScheduled + variables.totalPackagesDelivered
            < variables.totalPackages
        ):
            # 1. Check Priority Queue. If it has packages, and the truck doesn't have a proportion of them, set destination to the most urgent one, 
            # then pop the entry. If not, revert to greedy search.
            if (
                variables.priorityQueue != []
                and self.truckPackages <= variables.truckCapacity / variables.activeTrucks
            ):
                destinationVertex = routeMap.searchByAddress(
                    variables.priorityQueue.pop(0).delAddress
                )
            else:
                # If there are no packages in the priority queue, revert to greedy search.
                # Crawl down the sorted list of the current vertexes relations to find the next vertex to try. 
                # The list is sorted, from smallest to greatest distance.
                # Data is stored as a list of tuples within the vertex object. 
                destinationVertexTuple = self.currentLocation.relativesTable[tryVertex]
                destinationVertex = routeMap.searchByAddress(destinationVertexTuple[0])

            # 2. Check to see if the vertex has been visited, if it has no packages, 
            # or if the packages at destination would put the truck over limit. 
            # If so, increment the attempt index, and try again.
            if destinationVertex.visited == True:
                tryVertex += 1
                continue
            if affinityPackageVertexes.count(destinationVertex) != 0:
                tryVertex += 1
                continue
            if destinationVertex.packages == []:
                tryVertex += 1
                continue
            if len(destinationVertex.packages) + self.truckPackages > variables.truckCapacity:
                tryVertex += 1
                continue

            # 3. Check package and truck affinity for packages in bucket. Check package for delivery status.
            # Grab the buckets that contain packages that have affinity with packages in the current bucket.

            for package in destinationVertex.packages:
                if int(package.delReadyTime) > variables.currentTime:
                    tryVertex += 1
                if package.delStatus != "At Hub":
                    tryVertex += 1
                    break
                if (
                    package.truckAffinity != "ANY"
                    and package.truckAffinity != self.truckID
                ):
                    tryVertex += 1
                    break
                if package.pakAffinity == "NONE":
                    pass
                else:
                    for pakID in package.pakAffinity.split():
                        # If a package DOES have other packages that must be delivered with it, search the routeMap for those packages.
                        affinityPackage = routeMap.searchByPakID(pakID)
                        # Get the vertex associated with those packages.
                        affinityPackageVertex = routeMap.searchByAddress(
                            affinityPackage.delAddress
                        )
                        if self.stopList.count(affinityPackageVertex) == 0 and affinityPackageVertexes.count(affinityPackageVertex) == 0:
                            #Verify that the stop does not already exist in either the current stop list, or as an affinity for another package.
                            for package in affinityPackageVertex.packages:
                                package.delStatus == "En Route"
                                self.truckPackages += 1
                                variables.totalPackagesScheduled += 1
                            # Add the vertex to a list of packages, to be added to the Stop List after we are sure this truck's proportion of the priority queue
                            # has been taken.    
                            affinityPackageVertexes.append(affinityPackageVertex)

                package.delStatus = "En Route"
            
            # If all other checks pass, add the stop to the stopList.
            self.stopList.append(destinationVertex)
            self.truckPackages += len(destinationVertex.packages)
            variables.totalPackagesScheduled += len(destinationVertex.packages)
            self.currentLocation = destinationVertex
            self.currentLocation.visited = True

            if (
                variables.totalPackagesScheduled + variables.totalPackagesDelivered
                == variables.totalPackages
            ):
                # To be tripped when all packages are either delivered, or on trucks.
                # Set to prevent trucks from racking up useless miles during the takeStep() function.
                variables.packagesOut = True
            tryVertex = 0

        # Affinity packages are added as stops to the truck after priority items have been scheduled and loaded.
        for vertex in affinityPackageVertexes:
            self.stopList.append(vertex)
            vertex.visited = True
        # Set current location to the hub to facilitate predictable behaviour during takeStep()
        self.currentLocation = routeMap.searchByAddress("4001 South 700 East")

    # takeStep allows the truck to move. Handles four states: leaving HUB, arriving HUB, arriving STOP, empty. 
    # Increments the truck's total mileage, and is responsible
    # for tracking the decrement in distance on each leg of the journey.
    # If all packages are scheduled or deliveredA, and the truck is empty, do nothing.
    def takeStep(self, routeMap):
        if len(self.stopList) == 0 and variables.packagesOut == True:
            return None
        if variables.currentTime >= self.embarkTime:
            if self.currentLeg <= 0:  # Indicates arrival at a node.
                if (
                    self.currentLocation.label == "4001 South 700 East"
                ):  # Indicates departure from HUB.
                    self.nextLocation = self.stopList[0]  # Fetch next location.
                    nextLocationTuple = pluckTupleElement(
                        self.nextLocation.label,
                        self.currentLocation.relativesTable,  # Grab the distance to the next stop
                    )
                    self.currentLeg = nextLocationTuple[
                        1
                    ]  # Set the distance to the next stop.
                    self.lastLocation = (
                        self.currentLocation
                    )  # Sets last location to the HUB. Used for indexing.
                    self.currentLocation = routeMap.searchByAddress(
                        "TRANSIT"
                    )  # Truck is now between vertexes.
                elif (
                    self.nextLocation.label == "4001 South 700 East"
                ):  # Indicates arrival at HUB.
                    self.stopList.clear()  # Clear all packages from the truck's manifest
                    if variables.totalPackagesScheduled == variables.totalPackages:
                        return None
                    self.truckPackages = 0  # Set delivered packages to 0 at the beginning of a delivery loop
                    self.currentLocation = (
                        self.nextLocation
                    )  # Set the current location to the HUB
                    self.buildRoute(routeMap)  # Build a new route
                elif (
                    self.lastLocation.label != "4001 South 700 East"
                    and self.stopList.index(self.lastLocation) == len(self.stopList) - 1
                ):  # Checks for the end of the package list. Sets next location to the hub.
                    self.nextLocation = routeMap.searchByAddress("4001 South 700 East")
                    nextLocationTuple = pluckTupleElement(
                        self.nextLocation.label, self.currentLocation.relativesTable
                    )
                    self.currentLeg = nextLocationTuple[1]
                    self.lastLocation = self.currentLocation
                    self.currentLocation = routeMap.searchByAddress("TRANSIT")
                else:  # Truck has arrived at a stop on the list.
                    self.currentLocation = (
                        self.nextLocation
                    )  # Update truck's current location.
                    for (
                        package
                    ) in (
                        self.currentLocation.packages
                    ):  # Set all packages at the arrived location to "delivered". Mark time.
                        package.delComplete = variables.currentTime
                        package.delStatus = "Delivered"
                        variables.totalPackagesDelivered += 1
                        variables.totalPackagesScheduled -= 1
                    if (
                        self.stopList.index(self.currentLocation)
                        == len(self.stopList) - 1  # End of the stoplist.
                    ):
                        self.nextLocation = routeMap.searchByAddress(
                            "4001 South 700 East"
                        )
                        return None  # Break from the step if there is no 'next index', return, allow Condition 2 to build the list.
                    else:  # Additional stops are in the stoplist.
                        self.nextLocation = self.stopList[
                            self.stopList.index(self.currentLocation) + 1
                        ]  # Fetch next location.
                        nextLocationTuple = pluckTupleElement(
                            self.nextLocation.label, self.currentLocation.relativesTable
                        )
                        self.currentLeg = nextLocationTuple[1]
                        self.lastLocation = self.currentLocation
                        self.currentLocation = routeMap.searchByAddress("TRANSIT")

            self.currentLeg -= variables.tickStep
            self.totalMileage += variables.tickStep
