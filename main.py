# Student ID: 012897237

# =============================================================================
# Welcome to the WGUPS programming system!  To use this program, you will
# need three csv files:
#   1. A list of packages
#   2. A list of locations
#   3. A condensed distance matrix based on the locations from
#   the location list
#
#  What this program does:
#   1. Loads in the csv files.  This loader:
#       a. Creates a package object for each package that store's the
#       package's important attributes, such as its address, deadline,
#       special notes, and delivery time
#       b. Creates a locations matrix from the locations list
#       c. Creates a complete distance matrix from the condensed distance
#       matrix, where each index matches up with the indeces in the
#       locations matrix
#
#   2. Creates a hash table object from a self-made HashTable class, which:
#       a. Uses a hashing function on the package IDs to insert the package
#       objects into the hash table
#       b. Includes a lookup function for quick and efficient access to each
#       package object
#
#   3. Loads each package into three truck objects, taking into account
#   multiple constraints, such as:
#       a. There are 40 packages, yet only 16 can fit on each truck at a time
#       b. Only two drivers are available, so one driver will have to return
#       to the HUB after delivering their truck's packages, and then deliver
#       the packages on the third truck
#       c. Some packages contain deadlines, such as 9:00 AM or 10:30 AM
#       d. Some packages are delayed and won't arrive at the HUB until 9:05
#       AM (trucks can leave as early as 8:00 AM)
#       e. Some packages contain special notes, such as being delivered with
#       other packages, being on a certain truck, or having the wrong address
#       until a certain time
#
#   4. Uses a customized nearest neighbor algorithm to deliver packages based
#   on deadline priority and nearest distance.  If two packages contain the
#   same deadline, the algorithm will choose the closest package address.
#
#   5. Provides a CLI that allows a customer to:
#       a. Check the status of a package given a package ID and time
#       b. Check the status of all packages given a time
#       c. Check the total truck mileage after delivering all packages
#
# Throughout the program, I have left comments to help those who may want to
# use this program for their own company's package delivery system.  Some
# aspects of this program are specialized solely for the packages delivered
# by WGUPS on the date 2038-01-19.  Keeping that in mind, the comments give
# warnings and ideas for mainstream company use.
#
# *Comments marked with three hashes ### are meant for program testing.
# =============================================================================

from csv_loaders import load_csvs
from routing_program import load_trucks, nearest_neighbor
from hash_table import HashTable
from cli import run_cli

ht = HashTable()

def main():
    # pass empty HashTable object, locations matrix, and distances matrix
    # to the load_csvs() function to be loaded
    ht, locations, distances = load_csvs()
    # pass HashTable object (now full of packages) to load trucks, and return
    # three truck objects, now full of their respecive packages
    truck1, truck2, truck3 = load_trucks(ht)

    # run all three trucks
    ### print("\nTruck 1 starting:\n")
    return_time1, mileage1 = nearest_neighbor(truck1, locations, distances, None)

    ### print("\nTruck 2 starting:\n")
    return_time2, mileage2 = nearest_neighbor(truck2, locations, distances, None)

    # find out which truck returns to the HUB first so that truck 3's
    # departure time can be set
    return_time3 = min(return_time1, return_time2)

    # depart with truck 3
    ### print("\nTruck 3 starting:\n")
    final_time, mileage3 = nearest_neighbor(truck3, locations, distances, return_time3)
    total_mileage = mileage1 + mileage2 + mileage3

    ### print (f"\nTotal mileage: {total_mileage}")
    ### print (f"\nTruck 3 return time: {final_time}")

    # run the interface, inputting all of the data it will need as parameters
    run_cli(total_mileage, ht, truck1, truck2, truck3)

if __name__ == "__main__":
    main()
