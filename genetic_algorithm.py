import random
from datetime import timedelta

def create_population(packages, num_trucks, pop_size):
    population = []
    package_ids = list(packages.keys())

    for _ in range(pop_size):
        random.shuffle(package_ids)
        chromosome = []

        # this evenly places sentinels to give the GA a better starting chance
        average_load = len(package_ids) // num_trucks
        for i in range(num_trucks):
            start = i * average_load
            # else handles any remainders in the division
            end = (i + 1) * average_load if i < num_trucks - 1 \
                else len(package_ids)
            chromosome.extend(package_ids[start:end])
            # add sentinel if not last truck
            if i < num_trucks - 1:
                chromosome.append(f'|{i+1}|')
        population.append(chromosome)
    return population

def fitness(chromosome, trucks, capacity, packages, address_to_id,
            distance_matrix):
    distance_score = 0
    num_late_packages = 0
    num_capacity_over = 0
    refrig_violations = 0

    # first, find different routes
    routes = []
    current_route = []
    for gene in chromosome:
        if isinstance(gene, str):
            routes.append(current_route)
            current_route = []
        else:
            current_route.append(gene)
    routes.append(current_route)

    for i, route in enumerate(routes):
        if i >= len(trucks): break

        curr_truck = trucks[i]

        # constraint: capacity
        if len(route) > capacity:
            num_capacity_over += (len(route) - capacity)

        # find delay time
        departure_time = curr_truck.departure_time
        for package_id in route:
            package = packages[package_id]
            if package.delay_time and \
                package.delay_time > curr_truck.departure_time:
                curr_truck.departure_time = package.delay_time

        # assign time and location
        current_time = curr_truck.departure_time
        current_location = curr_truck.current_location

        # simulated route execution
        for package_id in route:
            package = packages[package_id]
            location_index = address_to_id[current_location]
            address_index = address_to_id[package.address]

            distance = distance_matrix[location_index][address_index]

            # distance score
            distance_score += distance

            travel_time = distance / 18.0
            current_time += timedelta(hours=travel_time)

            if package.deadline and current_time > package.deadline:
                    num_late_packages += 1

            if package.refrigerated and not curr_truck.refrigerated_capable:
                refrig_violations += 1

            current_location = package.address

        # return to the HUB, score based on how far
        location_index = address_to_id[current_location]
        distance_score += distance_matrix[location_index][0]

    # scoring constraints, easy to fine-tune
    score = (distance_score +
             (num_late_packages * 500) +
             (num_capacity_over * 1000) +
             (refrig_violations * 1000))

    return score

def get_population_fitness(population, trucks, capacity, packages,
                           address_to_id, distance_matrix):
    scored_population = []
    for chromosome in population:
        score = fitness(chromosome, trucks, capacity, packages,
                        address_to_id, distance_matrix)
        scored_population.append((score, chromosome))
    return scored_population

def tournament_selection(scored_population):
    k = 3
    selection = random.sample(scored_population, k)
    selection.sort(key=lambda x: x[0])
    winner = selection[0][1]
    return winner.copy()

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    child = [None] * size

    # find sentinel positions
    sentinel_indices = \
        [i for i, gene in enumerate(parent1) if isinstance(gene, str)]
    for index in sentinel_indices:
        # keep sentinel positions of parent 1
        child[index] = parent1[index]

    p1_sentinels = set([parent1[i] for i in sentinel_indices])
    p2_packages = [gene for gene in parent2 if not isinstance(gene, str)]

    p2_index = 0
    for i in range(size):
        if child[i] is None:
            child[i] = p2_packages[p2_index]
            p2_index += 1

    return child

def mutate(chromosome):
    mutation_rate = 0.05
    if random.random() < mutation_rate:
        # mutation type 1, package swap
        package_indices = \
            [i for i, g in enumerate(chromosome) if not isinstance(g, str)]
        i, j = random.sample(package_indices, 2)
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

    if random.random() < (mutation_rate):
        # mutation type 2, sentinal shift
        sentinel_indices = \
            [i for i, g in enumerate(chromosome) if isinstance(g, str)]
        index = random.choice(sentinel_indices)

        shift = random.choice([-1, 1])
        new_index = index + shift

        if 0 <= new_index < len(chromosome) \
            and not isinstance(chromosome[new_index], str):

            chromosome[index], chromosome[new_index] = \
                chromosome[new_index], chromosome[index]

def genetic_algorithm(packages, num_trucks, trucks, capacity,
                      address_to_id, distance_matrix):

    # create initial population
    pop_size = 500
    population = create_population(packages, num_trucks, pop_size)

    generations = 2000
    for generation in range(generations):
        # get the overall population fitness for each chromosome
        scored_pop = get_population_fitness(population, trucks, capacity,
                                    packages, address_to_id, distance_matrix)

        # sort by the highest scorers
        scored_pop.sort(key=lambda x: x[0])
        if generation % 50 == 0:
            print(f"Gen {generation}: Best Score = {scored_pop[0][0]}")
            sentinel_positions = [i for i, gene in enumerate(scored_pop[0][1])
                                  if isinstance(gene, str)]
            print(sentinel_positions)

        # start creating new population
        new_population = []
        # append the best scorer
        new_population.append(scored_pop[0][1].copy())
        new_population.append(scored_pop[1][1].copy())
        new_population.append(scored_pop[2][1].copy())

        # run two tournaments, each parent being the winner
        while len(new_population) < pop_size:
            p1 = tournament_selection(scored_pop)
            p2 = tournament_selection(scored_pop)

            # potentially create a child from these parents
            if random.random() < 0.8:
                child = ordered_crossover(p1, p2)
            else:
                child = p1.copy()
            # potentially mutate the child
            mutate(child)
            # add to the new population
            new_population.append(child)
        population = new_population

    # get the score of the final population
    scored_pop = get_population_fitness(population, trucks, capacity, packages,
                                        address_to_id, distance_matrix)

    # sort and find the best chromosome
    scored_pop.sort(key=lambda x: x[0])
    print(f"Final Gen, Best Score = {scored_pop[0][0]}")
    best_chromosome = scored_pop[0][1]
    return best_chromosome

# creates package arrays for each truck
def load_chromosome(best_chromosome, packages, trucks):
    routes = []
    current_route = []
    for gene in best_chromosome:
        if isinstance(gene, str):
            routes.append(current_route)
            current_route = []
        else:
            current_route.append(gene)
    routes.append(current_route)

    for i, route in enumerate(routes):
        if i >= len(trucks): break
        truck = trucks[i]
        truck.packages = []
        for package_id in route:
            package = packages[package_id]
            truck.packages.append(package)