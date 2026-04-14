from datetime import timedelta

def run_simulation(trucks, address_to_id, distance_matrix, capacity):
    deadline_violations = 0
    refrig_violations = 0
    total_fleet_mileage = 0

    for truck in trucks:
        truck.mileage = 0
        print(f'Truck {truck.truck_id}:')
        for package in truck.packages:
            if package.delay_time is not None:
                if package.delay_time > truck.departure_time:
                    truck.departure_time = package.delay_time

        print(f'Departure_time: {truck.departure_time}')
        print(f'Capacity: {len(truck.packages)} / {capacity}')

        current_location = truck.current_location
        current_time = truck.departure_time

        for package in truck.packages:
            location_index = address_to_id[current_location]
            address_index = address_to_id[package.address]

            distance = distance_matrix[location_index][address_index]
            travel_time = distance / 18.0
            current_time += timedelta(hours=travel_time)
            truck.mileage += distance

            current_location = package.address
            package.delivery_time = current_time

            if package.deadline is not None:
                if package.delivery_time >= package.deadline:
                    deadline_violations += 1
            if package.refrigerated and not truck.refrigerated_capable:
                refrig_violations += 1

            if package.deadline is not None:
                dead = package.deadline.strftime('%I:%M %p')
            else:
                dead = 'N/A'
            if package.delay_time is not None:
                delay = package.delay_time.strftime('%I:%M %p')
            else:
                delay= 'N/A'
            deliv = package.delivery_time.strftime('%I:%M %p')

            print(f'Package {package.package_id}, delayed: {delay}, deadline: {dead}, delivery_time: {deliv}, refrig: {package.refrigerated}, truck: {truck.refrigerated_capable}')

        location_index = address_to_id[current_location]
        distance = distance_matrix[location_index][0]
        travel_time = distance / 18.0
        current_time += timedelta(hours=travel_time)
        truck.mileage += distance
        print(f'Truck mileage: {truck.mileage}, return time: {current_time}')
        total_fleet_mileage += truck.mileage


    print(f'\n{"="*30}')
    print(f'FINAL AUDIT RESULTS')
    print(f'{"="*30}')
    print(f'Total Fleet Mileage: {total_fleet_mileage:.2f}')
    print(f'Total Deadline Violations: {deadline_violations}')
    print(f'Total Refrigeration Violations: {refrig_violations}')