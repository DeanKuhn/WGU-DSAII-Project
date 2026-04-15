# WGUPS Routing Program
A package delivery routing system improved from the original submission for WGU's C950 Data Structures & Algorithms II capstone project.

## Why improve?
Originally, the program was not fit for real-world implication. For example:
- **Randomness:** The algorithm ran on an unchanged package CSV file.  In the real world, package counts, delays, and deadlines change day to day.  The new algorithm must be able to handle this randomness.
- **Flexibility:** Package-to-truck assignment was hard-coded.  In a real-world application, there is not enough time to find an optimized truck-loading sequence.  The improved algorithm must not only deliver packages efficiently but also load them optimally.
- **Scale:** Package and truck count were constant.  The algorithm only worked if there were exactly 40 packages and exactly three trucks.  The new algorithm must be able to scale to meet increased company demand.

## New features
- **Genetic Algorithm Implementation:** The previous algorithm's K Nearest Neighbor algorithm was completely replaced by a Genetic Algorithm that simultaneously optimized package-to-truck assignment while finding efficient package delivery routes for each truck.
- **Package/Truck Generation:** To account for day-to-day uncertainty and company scalability, packages are generated randomly for each GA run.  Trucks are then generated to scale based on the package load automatically.
- **Custom Constraints:** Because different businesses may have different constraints, truck capacity and refrigeration capabilities are customizable via the CLI.  Additionally, the GA's parameters are customizable.  This gives companies the ability to (1) run quick and cheap GA runs if time is a constraint, or (2) run computationally expensive GA runs if they have the resources and time to do so.

## Changelog
### v4.0 - Finalized & Operational Program
#### *GA Improvements*
**Bundling Implementation:** A pre-processing layer was added to the GA that groups packages with the same addresses into bundles.  This bundle is then checked to ensure that `max(delay_times) + buffer < min(deadlines)`.  This ensures that the timing within this bundle is physically possible (for example, a package with a `delay_time` of 9:30 am cannot go in the same bundle as a package with a `deadline` of 9:00 am).  By bundling packages, the GA's search space is reduced, increasing the likelihood of earlier convergence.

**Bug Reductions:** An error was identified within the GA's fitness function where `Truck` objects were maintaining state across GA generations.  This resulted in every truck leaving at the latest possible `delay_time`.  By fixing this issue, the GA was able to better load trucks based on package delay times.

**Precise Penalty Scoring:** The GA's fitness function was updated with a `minutes_late * multiplier` penalty.  This creates a gradient descent, allowing the GA to see the difference between a package being five minutes late versus five hours late.

**Improving Computational Efficiency:** The previous chromosome sentinels (`'|1|'`) were replaced with numeric sentinels (`-1`), allowing computationally expensive sentinel checks (`isinstance(gene, str)`) to be replaced with computationally light numerical comparison checks (`if gene < 0`).  Comparing a number to zero is the fastest possible comparison in Python.  This lightens the load of the already expensive GA just a bit, but makes a meaningful difference across thousands of generations.

**Adaptive Mutation:** If the GA's best score doesn't improve within 50 generations, the mutation rate doubles to 'heat' the population, hopefully allowing the GA to escape local optima.  Crucially, a reset to the baseline mutation rate was implemented once a new best score was found, allowing the algorithm to 'cool down' and refine a discovery.

**Scramble & Inversion Mutation:** The mutation function was improved to include both scramble and inversion mutation.  These contributions allow the GA to explore the search space better while avoiding early convergence.

**Early Return:** If the GA's best score doesn't improve within 500 generations, the GA will terminate early and return the best score.  This allows a user to run the GA to its limit by specifying an astronomically high generation parameter and waiting for it to return once an optimal chromosome has been found.

#### *CLI Enhancements*
**Custom CLI Implementation:** A configurable interface was developed that allows the user to test the GA's hyperparameters in real time with a custom number of packages and deadline/delay/refrigeration requirements.  The user can enter the number of packages to generate, the percentage of those packages with deadlines, delays, and refrigeration requirements, choose the number of trucks, determine truck capacity/refrigeration capabilities, and set the parameters for the GA function, including `pop_size`, `generations`, and `mutation_rate`.

**Lookup Functions:** The CLI was updated with lookup functions allowing the user to see a package's delivery status, delivery time, delay, and deadline by entering either the package's ID or address.  If multiple packages are assigned to an address, the CLI will list each package's information.  The package statistics shown are based on the most recent GA run, allowing users to see the performance of individual packages for their customized GA iteration.

### v3.0 - Complete Project Overhaul
#### *Architectural drifts*
**Removal of Custom Structures:** Custom Hash Tables were replaced with Python dictionaries.  While the original C950 submission did not allow the use of Python dictionaries, it was determined that this constraint was unnecessary and hindered the program's development.

**Simplicity:** It was decided to remove K-Means, MDS clustering, K Nearest Neighbors, and 2-opt. While these algorithms contributed to a seemingly more 'advanced' algorithm, they added unnecessary complexity and detracted from the program's interpretability.  The system now uses a single GA to solve the package placement and truck delivery order.

#### *GA Evolution*
**Sentinel-Based Chromosome Organization:** The chromosome's makeup was redone.  Originally, the chromosome did not factor in delivery order; it only determined which packages went on which truck.  Now, chromosomes include the delivery order for all trucks, with sentinels (e.g., `|1|`) serving as boundaries between truck routes.

**Capacity-Aware Population Generation:** Originally, packages and sentinels were seeded randomly within the chromosome.  Now, the population generation function generates package placement based on truck capacity, giving the GA a slight 'nudge' in the right direction.

**Improved Fitness Scoring:** Scoring weights were rebalanced and organized into groups, such as `distance_score`, `num_capacity_over`, and `refrig_violations`.  This way, the fitness function can be fine-tuned with greater precision.

- **Return to HUB Incorporation:** The GA's fitness model penalizes trucks that end their route farther away from the HUB by adding the return trip's distance to the overall distance score.

- **Sentinel-Aware Ordered Crossover:** The GA's crossover function was modified so that sentinel positions are not accidentally swapped with package elements.

- **Multiple Mutation Strategies:** The mutation function now combines package swapping with sentinel shifting to ensure that the GA is allowed to adjust truck capacity.  Otherwise, the population generation's sentinel encoding would be permanent.

### v2.0 - Genetic Algorithm Loading (in progress)
- Replaced hard-coded truck loading with a genetic algorithm
- Implemented K-Means geographic pre-clustering using MDS to convert the distance matrix into approximate 2D coordinates
- The GA chromosome encodes each truck's package assignments as a flat index list
- Fitness function scores chromosomes across multiple weighted areas:
  - Hard constraints: capacity, delayed packages
  - Deadlines: exponential penalty for too many early deadlines on one truck
  - Weight balance: penalizes uneven weight distribution across trucks
  - Geography: rewards closer packages on the same truck (used the KMeans clustering)
  - Delay grouping: penalizes delayed packages spread across trucks
- Smart population seeding makes sure refrigerated packages are on refrigerated-capable trucks from generation zero
- Mutation keeps refrigeration constraints during random reassignment
- Elitism preserves the best chromosome across generations
- Departure times are calculated dynamically based on the actual time of the package delays
- Truck count scales automatically with math.ceil(packages / capacity) (not added yet)

### v1.0 - WGU Submission
- Initial submission with nearest neighbor routing
- Custom hash table
- Three-truck static loading
- Colorama/tabulate CLI

## Potential Improvements
**Heuristic Seeding:** To improve population generation, 10% of the starting population could be initialized using a Nearest Neighbor algorithm instead of pure randomness.  The GA will be provided with a rational baseline immediately, allowing it to spend generations refining a good route rather than fixing a chaotic one.

**Dynamic Hub Reassignment:** A mutation operator could be added to move a delayed bundle from one truck to another.  This will help trucks that may be bottlenecked by a single delayed bundle (in addition to bundle swapping).

**Physical Limit Audit:** An audit will be performed pre-GA to check if `delay_time + (distance_to_hub / speed) > deadline`.  This will automatically flag unsolvable packages, preventing the GA from wasting cycles on the impossible.

**Route Visualization:** A coordinate-based plot will be created to audit delivery paths and identify potential routing inefficiencies visually.