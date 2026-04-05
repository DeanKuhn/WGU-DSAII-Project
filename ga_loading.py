import random
import datetime
from collections import defaultdict

from status import Status

def generate_population(pop_size, packages, trucks):
    num_trucks = len(trucks)
    refrig_trucks = []
    non_refrig_trucks = []

    for i, truck in enumerate(trucks):
        if truck.refrigerated_capable:
            refrig_trucks.append(i)
        else:
            non_refrig_trucks.append(i)

    population = []
    # generate pop_size chromosomes
    for _ in range(pop_size):
        chromosome = []

        # one gene per package = randomly assign it to a truck
        # but make sure it's refrigerated, a little bit of a "nudge"
        for p in packages:
            if p.refrigerated:
                gene = random.choice(refrig_trucks)
            else:
                gene = random.randint(0, num_trucks-1)
            chromosome.append(gene)

        population.append(chromosome)
    return population, refrig_trucks

def fitness(chromosome, packages, trucks, cluster_map):
    # this function scores a chromosome - higher is better
    # scored on four constraints
    #   1. Hard constraints (capacity, refrigeration, delayed packages)
    #   2. Deadlines (penalize trucks overloaded with early deadlines)
    #   3. Weight balance (reward even distribution across trucks)
    #   4. Geography (reward packages in the same cluster on the same truck)

    score = 0

    # in order to know which packages end up on each truck (that is what we
    # are scoring), we need to use defaultdict(list), which allows us to access
    # a key that doesn't exist yet
    # automatically creates an empty list for it rather than throwing an error

    truck_packages = defaultdict(list)

    for package_index in range(len(chromosome)):
        # gene at this position tells us which truck this package goes on
        truck_index = chromosome[package_index]
        # assign package to truck's list
        truck_packages[truck_index].append(packages[package_index])

    # score the trucks now
    for truck_index in range(len(trucks)):
        truck = trucks[truck_index]
        package_list = truck_packages[truck_index]

        # constraint: capacity
        if len(package_list) > truck.capacity:
            score -= 30000

        # constraint: delayed packages
        for p in package_list:
            if p.delay_time is not None:
                if truck.departure_time < p.delay_time:
                    score -= 5000

        # constraint: deadlines
        tier1 = []  # 9:00 - 9:30
        tier2 = []  # 10:00 - 10:30
        tier3 = []  # 11:00 - 13:30
        tier4 = []  # BZHRS / 17:00 / EOD

        for p in package_list:
            if p.deadline is None:
                continue
            deadline = p.deadline
            if deadline <= datetime.time(9, 30):
                tier1.append(p)
            elif deadline <= datetime.time(10, 30):
                tier2.append(p)
            elif deadline <= datetime.time(13, 30):
                tier3.append(p)
            elif deadline <= datetime.time(17, 0):
                tier4.append(p)

        score -= (len(tier1) ** 2) * 100
        score -= (len(tier2) ** 2) * 50
        score -= (len(tier3) ** 2) * 20
        score -= len(tier4) * 5

        # new penalty... early deadline on delayed truck
        has_delay = any(p.delay_time is not None for p in package_list)
        if has_delay:
            for p in package_list:
                if p.deadline is not None:
                    if p.deadline <= datetime.time(10, 30):
                        score -= 8000

        # constraint: weight
        total_weight = 0.0
        for p in package_list:
            total_weight += p.weight

        all_weight = 0.0
        for p in packages:
            all_weight += p.weight
        average_weight = all_weight / len(trucks)

        score -= abs(total_weight - average_weight) * 10

        # constraint: geography
        if len(package_list) > 0:
            cluster_ids = []
            for p in package_list:
                cluster_id = cluster_map[p.package_id]
                cluster_ids.append(cluster_id)

            cluster_counts = defaultdict(int)
            for c in cluster_ids:
                cluster_counts[c] += 1

            dominant_cluster = None
            dominant_count = 0
            for cluster_id, count in cluster_counts.items():
                if count > dominant_count:
                    dominant_cluster = cluster_id
                    dominant_count = count

            score += dominant_count * 150
    # another constraint: delayed packages on more than one truck
    delayed_trucks = 0
    for truck in trucks:
        for p in truck_packages[trucks.index(truck)]:
            if p.delay_time is not None:
                delayed_trucks += 1
                break
    if delayed_trucks > 1:
        score -= (delayed_trucks - 1) * 3000

    return score

def tournament_select(population, fitnesses, k=3):
    # randomly choose three from the population to compare
    contestants = []
    indices = random.sample(range(len(population)), k)


    for index in indices:
        chromosome = population[index]
        fitness_score = fitnesses[index]
        contestants.append((chromosome, fitness_score))

    best_chromosome = None
    best_score = float('-inf')

    for chromosome, fitness_score in contestants:
        if fitness_score > best_score:
            best_score = fitness_score
            best_chromosome = chromosome

    return best_chromosome

def crossover(parent1, parent2):
    # combines two parent chromosomes into one child chromosome
    # pick a random 'crossover' point
    # child gets everything from the left from parent1, and everything from
    # the right from parent2

    crossover_point = random.randint(1, len(parent1) - 1)

    child = parent1[:crossover_point]
    child = child + parent2[crossover_point:]

    return child

def mutate(chromosome, num_trucks, packages, refrig_trucks, mutation_rate=0.05):
    # random gene reassignment, keeps diversity
    # without mutation, the algorithm can get stuck
    # like copying error in DNA; usually harmful, but occasionally brilliant

    mutated_chromosome = []
    for i, gene in enumerate(chromosome):
        roll = random.random()
        if roll < mutation_rate:
            if packages[i].refrigerated:
                # stay within refrigerated trucks only
                new_gene = random.choice(refrig_trucks)
            else:
                new_gene = random.randint(0, num_trucks - 1)
            mutated_chromosome.append(new_gene)
        else:
            mutated_chromosome.append(gene)
    return mutated_chromosome

def run_ga(packages, trucks, cluster_map, generations=300,
           pop_size=50, mutation_rate=0.05, k=3):
    # basic function loop:
    #   1. Generate a random starting population
    #   2. Score every chromosome with the fitness function
    #   3. Build a new population by selecting parents and breeding children
    #   4. Repeat for generations=300
    #   5. Return the single best chromosome found across all generations

    num_trucks = len(trucks)
    # step 1:
    population, refrig_trucks = generate_population(pop_size, packages, trucks)
    best_chromosome = None
    best_score = float('-inf')

    # step 2:
    for generation in range(generations):
        fitnesses = []
        for chromosome in population:
            score = fitness(chromosome, packages, trucks, cluster_map)
            fitnesses.append(score)

        # check for best score
        for i in range(len(population)):
            if fitnesses[i] > best_score:
                best_score = fitnesses[i]
                # store a copy so future mutations don't alter it
                # need list() since it is immutable
                best_chromosome = list(population[i])

        # step 3
        new_population = []
        # elitism
        new_population.append(list(best_chromosome))

        # fill the rest of the population with children
        while len(new_population) < pop_size:
            parent1 = tournament_select(population, fitnesses, k)
            parent2 = tournament_select(population, fitnesses, k)
            child = crossover(parent1, parent2)
            child = mutate(child, num_trucks, packages, refrig_trucks, mutation_rate)
            new_population.append(child)

        population = new_population

        # progress indicator
        if generation % 50 == 0:
            print(f"Generation {generation} - best score so far: \
                  {best_score}")

    print(f"GA complete.  Final best score: {best_score}")
    return best_chromosome

def load_chromosome(best_chromosome, packages, trucks):
    for package_index in range(len(best_chromosome)):
        truck_index = best_chromosome[package_index]
        package = packages[package_index]
        truck = trucks[truck_index]
        truck.packages.append(package)
        package.status = Status.EN_ROUTE

    # handle delayed packages
    for truck in trucks:
        latest_delay = datetime.time(8, 0)

        for package in truck.packages:
            if package.delay_time is not None:
                if package.delay_time > latest_delay:
                    latest_delay = package.delay_time
        truck.departure_time = latest_delay

    # handle refrigerated packages, flag any incorrectly managed packages
    for truck in trucks:
        for package in truck.packages:
            if package.refrigerated and not truck.refrigerated_capable:
                print(f"WARNING: Package {package.package_id} is refrigerated "
                      f"but assigned to non-refrigerated Truck {truck.truck_id}")
    return trucks