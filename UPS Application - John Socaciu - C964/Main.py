######################################################
# Author: John Socaciu                               #
# Student ID: 011511992                              #
# Title: C964 UPS ROUTING PROGRAM IMPLEMENTATION     #
######################################################

import Package
import datetime
import csv
import Truck
from HashTable import HashTable
from Package import Package

hashTable = HashTable() # Create hash map object

with open("Data/Packages.csv") as packageFile: # Read the data inside Packages CSV
    packageCSV = csv.reader(packageFile)
    packageCSV = list(packageCSV)

with open("Data/Addresses.csv") as addressesFile: # Read the data inside Addresses CSV 
    AddressesCSV = csv.reader(addressesFile)
    AddressesCSV = list(AddressesCSV)
   
with open("Data/Distances.csv") as distancesFile: # Read the data inside Distances CSV 
    distanceCSV = csv.reader(distancesFile)
    distanceCSV = list(distanceCSV)

# package 20 'Must be delivered with 13, 15'

# package 16 'Must be delivered with 13, 19'
    
# package 14 'Must be delivered with 15, 19'

# Creating the object for first truck -- Starting at 8 AM 
firstTruck = Truck.Truck([1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", # packages listed in ascending order
                     datetime.timedelta(hours = 8, minutes = 0, seconds = 0), 16, 25)

# package 6... 'Delayed on flight... will not arrive to depot until 9:05 am'

# package 32 28, 25... 'Delayed on flight... will not arrive to depot until 9:05 am'

# Creating the object for third truck -- Starting at 9:05 AM 
thirdTruck = Truck.Truck([2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours = 9, minutes = 5, seconds = 0), 16, 25)

# package 38 & 36 'Can only be on truck #2'

# package 3... 'Can only be on truck #2'

# Creating the object for second truck -- starting at 10:20 AM
secondTruck = Truck.Truck([3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, "4001 South 700 East", 
                     datetime.timedelta(hours = 10, minutes = 20, seconds = 0), 16, 25)
 
def receiveAddress(address): # Time-complexity is O(n)... converting string to integer
     for column in AddressesCSV:
        if address in column[2]:
            return int(column[0])
        
def distanceBetween(currentLocation, destination): # function for find the distance between the current and the desired destination 
    distanceTwoLocations = distanceCSV[currentLocation][destination] # The Time-complexity is O(1) because a constant amount of operations are done regardless of input
    if not distanceTwoLocations:
        distanceTwoLocations = distanceCSV[destination][currentLocation]

    return float(distanceTwoLocations)
        
def packageData(fileName, hashTable): # Create package objects from the CSV package file... insert package objects into the hashTable
    with open(fileName) as packageAssociatedData: # time-complexity: O(n)
        packageInformation = csv.reader(packageAssociatedData) # used for iteration in packages.csv file 
        for package in packageInformation:
                packageID = int(package[0])  # identifying information from the Package.csv file and setting them equal to the correlating variable
                packageAddress = package[1]
                packageCity = package[2]
                packageState = package[3]
                packageZipcode = package[4]
                packageDeadline = package[5]
                packageWeight = package[6]
                packageStatus = "N/A"

                packageObject = Package(packageID, packageAddress, packageCity, packageState,  # Creation of the packageObject using the Package class
                                packageZipcode, packageDeadline, packageWeight, packageStatus)
                
                hashTable.insert(packageObject.ID, packageObject) #insert into the hash-table

packageData("Data/Packages.csv", hashTable) # load packages into package object... used later for lookup 

def loadTruck(truckNumber): # function that utilizes the nearest-neighbor algorithm... The time complexity of this code is O(n^2)
    undeliveredArray = [hashTable.lookup(packageID) for packageID in truckNumber.packages]
    while undeliveredArray:
        nextAddress = float(100000) # float number that acts as positive infinity 
        nextPackage = None # declare null

        for package in undeliveredArray: # Iteration through the undelivered packages array
            packageAddress = receiveAddress(package.address) # Get address for current package

            if packageAddress is not None: # check if the package actually exists (not null)
                distance = distanceBetween(receiveAddress(truckNumber.address), packageAddress)
            if distance <= nextAddress: # less than or equal positive infinity
                nextAddress = distance # update the netAddress with the new minimum distance
                nextPackage = package # Current package is the next package to be delivered 

        if nextPackage is not None: # not null
            nextPackage.departureTime = truckNumber.leaveingHub
            truckNumber.packages.append(nextPackage.ID) # Adds next closest package ID
            undeliveredArray.remove(nextPackage) # Removing The Same Package From The undelivered Array
            truckNumber.mileage += nextAddress # add mileage to the next addresses mileage to the current mileage for the truck
            truckNumber.time += datetime.timedelta(hours = nextAddress / 25) # Updates the time it took for the truck to drive to the nearest package (25 miles per hour)
            truckNumber.address = nextPackage.address # Updates truck's current address attribute to the package it drove to
            nextPackage.deliveryTime = truckNumber.time
        else:
            print("There is a problem between line 77 and line 111...")
            break

loadTruck(firstTruck) # Put the trucks through the loading process
loadTruck(secondTruck)
thirdTruck.leaveingHub = min(firstTruck.time, secondTruck.time) #third truck leaves last and only two trucks can be on the road at the same time... 
loadTruck(thirdTruck) 

class Main: # time-complexity is O(1) -- onlying performing constant operations...The User Interface in the console
    print("UPS Parcel Service...The Total Mileage For The Current Route Is:")
    print("Total Mileage: " + str(firstTruck.mileage + secondTruck.mileage + thirdTruck.mileage) + " miles") # Prints total mileage for all trucks
    print("Individual Mileages: ")
    print("first truck mileage: " + str(round(firstTruck.mileage, 3)) + " miles")
    print("second truck mileage: " + str(secondTruck.mileage) + " miles")
    print("third truck mileage: " + str(thirdTruck.mileage) + " miles")
    initialUserInput = input("To start please type the word 'confirm': ") # execution will start when the user types 'confirm'
    # If the user doesn't type "leave" the program will ask for a specific time in regard to checking packages
    if initialUserInput == "confirm": # any invalid input will cause the program to quit 
            userTime = input("Please enter a time to check status of package(s). Use the following format, HH:MM:SS: ") # asking the the user to input their desired time
            changeTime = datetime.timedelta(
            hours = int(userTime.split(":")[0]),
            minutes = int(userTime.split(":")[1]),
            seconds = int(userTime.split(":")[2]))
            secondUserInput = input("To look up an individual package, type 'one'. For a rundown of all packages please type 'all': ")
            if secondUserInput == "one": #package ID
                    packageIDNumber = input("Please Enter The Package ID To Look-up A specific Package: ") # The user will be asked to input a package ID..
                    package = hashTable.lookup(int(packageIDNumber))
                    package.packageStatus(changeTime)
                    print(str(package))
            elif secondUserInput == "all": 
                    for packageID in range(1, 41, 1): #prints all Package Status' along with other associated data and increments by 1 
                        package = hashTable.lookup(packageID)
                        package.packageStatus(changeTime)
                        print(str(package))
            else:
                exit()
    else:
        exit()
