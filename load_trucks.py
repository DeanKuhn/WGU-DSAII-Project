import datetime
from truck import Truck
from ga_loading import run_ga

def load_trucks(num_trucks, num_refrig, num_capacity):
    # retrieve packages array from ht object
    trucks = []
    for i in range(num_trucks):
        truck_id = i + 1
        refrig = (i < num_refrig)

        is_last = (i == num_trucks - 1)
        truck = Truck(
            truck_id=truck_id,
            current_location='4001 South 700 East',
            mileage=0.0,
            departure_time=datetime.time(8, 0),
            refrigerated_capable=refrig,
            capacity=num_capacity
            )
        trucks.append(truck)
    return trucks


    # ga runs here
    # fix departure times based on what each truck ended up with
    for truck in trucks:
        truck.departure_time = calculate_departure_time(truck)
    refrig_trucks_list = [truck for truck in trucks if truck.refrigerated_capable]

def calculate_departure_time(truck):
    None


    # # self-loading loop
    # for package in package_array:
    #     if package is None or package == 'Deactivated':
    #         continue
    #     if 'REFRIG' in package.constraints:
    #         min(refrig_trucks_list, key = lambda truck: len(truck.packages)).packages.append(package)
    #     # important note: REFRIG items will never be delayed
    #     if 'DELAY:09:05' in package.constraints:
    #         truck4.packages.append(package)


