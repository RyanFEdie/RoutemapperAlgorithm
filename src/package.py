class Package:
    pakID = 0
    delAddress = "Unassigned"
    delDeadline = 480
    delCity = "Unassigned"
    delZip = 0
    pakWeight = 0
    delStatus = "At Hub"
    delReadyTime = 0
    truckAffinity = 0 # For any truck preferences.
    pakAffinity = [] # For the IDs of other packages that MUST be delivered with this package.
    delComplete = 0 # For the time of delivery completion in minutes from 8:00 AM.

    def __init__(
        self,
        pakID,
        delAddress,
        delDeadline,
        delCity,
        delZip,
        delReadyTime,
        truckAffinity,
        pakAffinity,
        pakWeight,
    ):
        self.pakID = pakID
        self.delAddress = delAddress
        self.delDeadline = delDeadline
        self.delCity = delCity
        self.delZip = delZip
        # delStatus will always be set by the Truck, and will always init 'At Hub'
        self.delReadyTime = delReadyTime  # May not be relevant.
        self.truckAffinity = truckAffinity  # May not be relevant.
        self.pakAffinity = pakAffinity  # May not be relevant.
        self.pakWeight = pakWeight
