class Truck:
    def __init__(self, packages, mileage, address, leaveingHub, capacity, milesPerHour): #non-default constructor
        self.capacity = capacity
        self.milesPerHour = milesPerHour
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.leaveingHub = leaveingHub
        self.time = leaveingHub