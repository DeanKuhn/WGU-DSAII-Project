from datetime import datetime

from status import Status
from truck import Truck
from driver import Driver

def load_trucks(ht):
    # retrieve packages array from ht object
    package_array = ht.get_array()

    # create truck objects, add their respective package arrays
    truck1 = Truck(
        'Western Governors University',     # assign starting location
        0,                                  # assign starting mileage
        datetime(2038, 1, 19, 8, 0),        # assign departure time
        False                               # assign refrigerated_capable
        )

    truck2 = Truck(
        '4001 South 700 East',
        0,
        datetime(2038, 1, 19, 8, 0),
        False
        )

    truck3 = Truck(
        '4001 South 700 East',
        0,
        datetime(2038, 1, 19, 8, 0),
        False
        )

    truck4 = Truck(
        '4001 South 700 East',
        0,
        None,
        False
        )

    # create driver objects

    driver1 = Driver(
        1,
        truck1,
        datetime(2038, 1, 19, 8, 0)
    )

    driver2 = Driver(
        2,
        truck2,
        datetime(2038, 1, 19, 8, 0)
    )

    driver3 = Driver(
        3,
        truck3,
        datetime(2038, 1, 19, 8, 0)
    )

    # assign refrigeration-capable trucks
    # this is one area of the code that is hard-coded
    truck1.refrigerated_capable = True
    truck3.refrigerated_capable = True

    trucks = [truck1, truck2, truck3, truck4]
    refrig_trucks_list = [truck for truck in trucks if truck.refrigerated_capable]


    # self-loading loop
    for package in package_array:
        if package is None or package == 'Deactivated':
            continue
        if 'REFRIG' in package.constraints:
            min(refrig_trucks_list, key = lambda truck: len(truck.truck_array)).truck_array.append(package)
        # important note: REFRIG items will never be delayed
        if 'DELAY:09:05' in package.constraints:
            truck4.truck_array.append(package)

    # return trucks to be used by nearest neighbor
    return truck1, truck2, truck3, truck4, driver1, driver2, driver3