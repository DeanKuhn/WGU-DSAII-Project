# timedelta is needed for datetime conversion
import datetime
from datetime import timedelta

from status import Status
from truck import Truck

def load_trucks(ht):
    # retrieve package array from ht object
    package_array = ht.get_array()
    truck1_array = []
    truck2_array = []
    truck3_array = []

    # IMPORTANT FOR OTHER COMPANIES:
    # These truck arrays are hard-coded to fit the WGUPS constraints.  For
    # your own company's packaging and delivery needs, a sorting algorithm
    # that balances package special needs with deadline restrictions would be
    # efficient.  A sorting algorithm was attempted for WGUPS, but
    # certain packages that were both delayed and had deadlines were not being
    # received on time in simulation runs, so hard-coding each truck's package
    # array was decided upon.
    # Additionally, other companies may have more or less trucks to load up
    # with packages.  For WGUPS specifically, three trucks are used, with
    # two drivers.
    truck1_ids = [13, 14, 15, 16, 10, 31, 34, 37, 40, 2, 4, 19, 7, 39, 8, 30]
    truck2_ids = [3, 18, 36, 38, 5, 20, 1, 29]
    truck3_ids = [6, 25, 28, 32, 9, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35, 11]

    for package in package_array:
        # skip array indeces with no/deleted packages
        if package is None or package == 'Deactivated':
            continue
        if package.package_id in truck1_ids:
            truck1_array.append(package)
        elif package.package_id in truck2_ids:
            truck2_array.append(package)
        elif package.package_id in truck3_ids:
            truck3_array.append(package)

    # create truck objects, add their respective package arrays
    truck1 = Truck(
        truck1_array,                       # assign truck array
        'Western Governors University',     # assign starting location
        0,                                  # assign starting mileage
        datetime(8, 0),        # assign current time
        datetime(2038, 1, 19, 8, 0)         # assign departure time
        )

    truck2 = Truck(
        truck2_array,
        '4001 South 700 East',
        0,
        datetime(8, 0),
        datetime(8, 0)
        )

    truck3 = Truck(
        truck3_array,
        '4001 South 700 East',
        0,
        None,
        None
        )

    # return trucks to be used by nearest neighbor
    return truck1, truck2, truck3

def nearest_neighbor(truck, locations, distances, starting_time):
    # if truck 3, assign current time and departure time to starting time
    if truck.current_time is None:
        truck.current_time = starting_time
        truck.departure_time = starting_time

    # initialize truck location
    current_index = 0
    package_index = 0

    ### print(f"Truck starting at {truck.current_time}\n")

    # IMPORTANT FOR OTHER COMPANIES:
    # This specific nearest neighbor algorithm loops through each of the
    # truck's arrays once per package.  This assumes that no packages have
    # been delivered upon starting the nearest neighbor algorithm.
    # Please take this into consideration when implementing this algorithm
    # in your own trucking routes.
    for _ in range(len(truck.packages)):
        # find current location in locations matrix
        for location in locations:
            if location[2] == truck.current_location:
                current_index = location[0]

        ### print(f"Current location: {truck.current_location}")

        minimum_distance = float('inf')

        # IMPORTANT FOR OTHER COMPANIES:
        # WGUPS packages have three deadlines: 9:00 AM, 10:30 AM, or 'EOD'
        # (end of day).  Your packages may have different deadlines, as well
        # as a much larger amount of different deadlines.  To take these
        # constraints into consideration, it may be helpful to compare package
        # deadline times with general times, such as comparing if a deadline
        # is BEFORE 9:00 AM instead of is the deadline EQUALS 9:00 AM.  These
        # three arrays could hold, for example:
        #   morning_deadline_array = all packages with deadlines < 10:00 AM
        #   afternoon_deadline_array = all packages with deadline < 1:00 PM
        #   eod_deadline_array = all remaining packages to be delivered < EOD
        nine_deadline_array = []
        ten_deadline_array = []
        no_deadline_array = []

        for package in truck.packages:
            if package.deadline == '9:00 AM' and package.status != Status.DELIVERED:
                nine_deadline_array.append(package)
        for package in truck.packages:
            if package.deadline == '10:30 AM' and package.status != Status.DELIVERED:
                ten_deadline_array.append(package)
        for package in truck.packages:
            if package.deadline == 'EOD' and package.status != Status.DELIVERED:
                no_deadline_array.append(package)

        # =====================================================================
        # IMPORTANT FOR OTHER COMPANIES:
        # WGUPS only had one 9:00 AM package to deliver on date 2038-01-19,
        # so there was no reason to compare distances with other 9:00 AM
        # deadlined packages.  You may want to take this into consideration
        # when using this algorithm for your own delivery system.
        if nine_deadline_array:
            # loop through packages
            for package in nine_deadline_array:
                for location in locations:
                    if package.address == location[2]:
                        # no need to choose nearest; there is only one
                        package_index = location[0]
                        package_distance = distances[current_index][package_index]
                        chosen_package = package
                        minimum_distance = package_distance
        # =====================================================================
        elif ten_deadline_array:
            for package in ten_deadline_array:
                for location in locations:
                    if package.address == location[2]:
                        # assign the package index to it's location index
                        package_index = location[0]
                        # check the distance of this package's index from the
                        # current location, and if it's the smallest distance
                        # yet, assign it as the minimum distance
                        package_distance = distances[current_index][package_index]
                        if package_distance < minimum_distance:
                            chosen_package = package
                            minimum_distance = package_distance
        # =====================================================================
        elif no_deadline_array:
            for package in no_deadline_array:
                for location in locations:
                    if package.address == location[2]:
                        package_index = location[0]
                        package_distance = distances[current_index][package_index]
                        if package_distance < minimum_distance:
                            chosen_package = package
                            minimum_distance = package_distance
        # =====================================================================
        # calculate time to deliver package
        hours = minimum_distance / 18
        ### print(f"Distance to cover: {minimum_distance}")

        # calculate mileage
        truck.mileage += minimum_distance
        # add calculated time to current time
        truck.current_time += timedelta(hours = hours)
        # update current location to the package address location
        truck.current_location = chosen_package.address
        # update package status to delivered
        chosen_package.status = Status.DELIVERED
        # update package delivery time
        chosen_package.delivery_time = truck.current_time

        ### print(
        ### f"Package: {chosen_package.package_id} | "
        ### f"Address: {chosen_package.address} | "
        ### f"Deadline: {chosen_package.deadline} | "
        ### f"Delivery Time: {chosen_package.delivery_time}\n"
        ### )

    # IMPORTANT FOR OTHER COMPANIES:
    # in our distances matrix, the HUB distance from any other distance is
    # always col[0].  Please adjust accordingly for your own company's HUB.
    distance_home = distances[current_index][0]
    hours = distance_home / 18
    truck.current_time += timedelta(hours = hours)
    truck.current_location = '4001 South 700 East'
    truck.mileage += distance_home

    # update departure time for the next truck
    departure_time = truck.current_time

    ### print(f"Truck back at HUB, time: {truck.current_time}\n")
    return departure_time, truck.mileage#