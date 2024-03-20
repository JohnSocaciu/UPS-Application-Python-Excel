# Create class for packages
import datetime
from colors import colors

color = colors()
    
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status): #non-default constructor
        self.deliveryTime = None
        self.departureTime = None
        self.ID = ID
        self.address = address
        self.state = state
        self.zipcode = zipcode
        self.city = city
        self.weight = weight
        self.status = status
        self.deadline = deadline

    def __str__(self): # for displaying variables in console
        return f"Package Number: {self.ID}, {self.address}, {self.zipcode}, {self.city}, {self.state}, Deadline: {self.deadline}, Weight: {self.weight}, Load Truck At: {self.departureTime}, Delivery Time: {self.deliveryTime}"

    # time-complexity is O(1)
    def packageStatus(self, changeTime): # Status update for packages, check if null, if not then continue and print status to console
        self.deliveryTime = self.deliveryTime if self.deliveryTime is not None else datetime.timedelta()
        self.departureTime = self.departureTime if self.departureTime is not None else datetime.timedelta()

        if self.deliveryTime < changeTime:
            self.status = print(f"{color.green}Status: [delivered]")
        elif self.departureTime > changeTime:
            self.status = print( f"{color.blue}Status: [en Route]")
        else:
            self.status = print(f"{color.red}Status: [at the hub]")