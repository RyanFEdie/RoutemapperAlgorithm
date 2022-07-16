# Ryan Edie, ID 001228294,
from utilities import (
    buildMapGraph,
    buildPackageHashTable,
    timeTranslator,
    printPackages,
    printSelectPackage,
)
from mapHashTable import Graph
from truck import devTruck
import variables

routeMap = Graph()

buildMapGraph(routeMap)
buildPackageHashTable(routeMap)

devTruck1 = devTruck(1, routeMap)
devTruck2 = devTruck(2, routeMap)

devTruck1.buildRoute(routeMap)
devTruck2.buildRoute(routeMap)

option = input(
    "Please select an option: r (run to completion), t (run to timestamp), s (search package)\n"
)

if option == "r":
    while variables.totalPackagesDelivered != variables.totalPackages:
        devTruck1.takeStep(routeMap)
        devTruck2.takeStep(routeMap)
        variables.currentTime += 1
    printPackages(routeMap)
    print("Simulation complete. All packages delivered.\n")
    print("Delivery Truck 1 total mileage: ", int(devTruck1.totalMileage))
    print("Delivery Truck 2 total mileage: ", int(devTruck2.totalMileage))
elif option == "t":
    timeLimit = input(
        "Please enter a time, in the format HH:mm, 24 hour time. Include leading zero. (eg: 09:35)\n"
    )
    translatedTimeLimit = timeTranslator(timeLimit)
    while (
        variables.totalPackagesDelivered != variables.totalPackages
        and variables.currentTime < translatedTimeLimit
    ):
        devTruck1.takeStep(routeMap)
        devTruck2.takeStep(routeMap)
        variables.currentTime += 1
    printPackages(routeMap)
    print("Simulation complete. Time limit reached.\n")
    print("Delivery Truck 1 total mileage: ", int(devTruck1.totalMileage))
    print("Delivery Truck 2 total mileage: ", int(devTruck2.totalMileage))
elif option == "s":
    selectPak = int(input("Please enter a package ID.\n"))
    timeLimit = input(
        "Please enter a target time, in the format HH:mm, 24 hours. Include leading zero. (eg: 09:35)\n"
    )
    translatedTimeLimit = timeTranslator(timeLimit)
    if translatedTimeLimit == None:
        exit
    returnPak = routeMap.searchByPakID(str(selectPak))
    while (
        variables.totalPackagesDelivered != variables.totalPackages
        and variables.currentTime < translatedTimeLimit
    ):
        devTruck1.takeStep(routeMap)
        devTruck2.takeStep(routeMap)
        variables.currentTime += 1
    printSelectPackage(returnPak)
