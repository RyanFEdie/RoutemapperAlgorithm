global currentTime
global tickStep
global totalVertexes
global totalPackages
global totalPackagesScheduled
global totalPackagesDelivered
global packagesOut
global priorityQueue
global activeTrucks
global truckCapacity

currentTime = 0  # Time as expressed in minutes from 8:00 AM.
truckCapacity = 16
averageSpeed = 18  # Average speed of a given truck.
tickStep = averageSpeed / 60  # The distance travelled in a single minute.
totalPackages = 0
totalPackagesScheduled = 0
totalPackagesDelivered = 0
totalVertexes = 0
packagesOut = False
priorityQueue = []
activeTrucks = 0
