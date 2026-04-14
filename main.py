from loaders import generate_packages, load_csvs, load_trucks
from genetic_algorithm import genetic_algorithm, load_chromosome
from simulation import run_simulation

from datetime import timedelta
if __name__ == "__main__":
    # generate packages and load csv data for the address list and distance
    # matrix data
    num_addresses, address_to_id, id_to_address, distance_matrix = \
        load_csvs()
    packages = generate_packages(id_to_address, num_addresses)

    # get basic questions
    print("Capacity?")
    capacity = int(input())
    print("Number of trucks?")
    num_trucks = int(input())
    print("Number of refrigerated trucks?")
    num_refrig_trucks = int(input())

    trucks = load_trucks(num_trucks, num_refrig_trucks, capacity)

    best_chromosome = genetic_algorithm(packages, num_trucks, trucks, capacity, address_to_id, distance_matrix)
    load_chromosome(best_chromosome, packages, trucks)

    # run final simulation with optimal chromosome
    run_simulation(trucks, address_to_id, distance_matrix, capacity)