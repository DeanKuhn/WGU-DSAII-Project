# WGUPS Routing Program

A package delivery routing system built for WGU's C950 Data Structures & Algorithms II.

## Features

- Genetic algorithm for smart truck loading and routing

## Planned Improvements
- **Dynamic Fleet Scaling:** Implement math.ceil(total_packages / capacity) to automatically scale the truck count based on load.

- **Adaptive Mutation Rates:** Implement "Simulated Annealing" logic where the mutation rate increases if the population stagnates (local optima escape).

- **Route Visualization:** Export delivery paths to a coordinate-based plot to visually audit "zigzag" inefficiencies.

**Address-Based Lookup:** Finalize the CLI integration for real-time package status queries during the simulation run.

## Changelog

### v3.0 - Complete Project Overhaul
#### *Architectural drifts*
**Deprioritization of Custom Structures:** Removed custom Hash Table implementations in favor of native Python dictionaries to reduce overhead and focus on algorithmic optimization.

**Unified Optimization:** Evaluated and subsequently removed K-Means, MDS clustering, and 2-opt local search. The system now utilizes a **Pure Genetic Algorithm (PGA)** that solves the partitioning problem (which packages go on which truck) and the TSP (delivery order) simultaneously.

#### *GA Evolution*
**Sentinel-Based Chromosome Encoding:** Implemented a single-chromosome string using unique string sentinels (e.g., `|1|`) to act as "moveable fences" between truck routes.

**Deterministic Population Seeding:**  Replaced random initialization with a capacity-aware partitioner to ensure Gen-0 begins with physically valid solutions.

**Multi-Objective Fitness Scoring (Linear Penalty Scaling):** Re-balanced weights to create a smooth fitness gradient, preventing hard-constraint "eclipsing."

- **Temporal Synchronization:** Fitness now accounts for "Hub Standstill" delays, ensuring trucks wait at the depot until all assigned cargo is available.

- **Distance Logic:** Implemented mandatory Hub-return scoring to prevent "open-loop" distance cheating.

**Evolutionary Mechanics (Tournament Selection):** Implemented size-3 selection to maintain genetic diversity and prevent premature convergence.

- **Sentinel-Aware Ordered Crossover (OX):** Modified crossover to preserve truck structures while evolving delivery sequences.

- **Dual-Mode Mutation:** Combined standard Package Swaps (route optimization) with Sentinel Shifting (load balancing) to break "hard-coded" partition limits.

### v2.0 - Genetic Algorithm Loading (in progress)
- Replaced hard-coded truck loading with a genetic algorithm
- Implemented KMeans geographic pre-clustering using MDS to convert distance matrix into approximate 2D coordinates
- GA chromosome encodes each truck's package assignments as a flat index list
- Fitness function scores chromosomes across multiple weighted areas:
  - Hard constraints: capacity, delayed packages
  - Deadlines: exponential penalty for too many early deadlines on one truck
  - Weight balance: penalizes uneven weight distribution across trucks
  - Geography: rewards closer packages on the same truck (used the KMeans clustering)
  - Delay grouping: penalizes delayed packages spread across trucks
- Smart population seeding makes sure refrigerated packages are on refrigerated-capable trucks from generation zero
- Mutation keeps refrigeration constraints during random reassignment
- Elitism preserves best chromosome across generations
- Departure times calculated dynamically based on the actual time of the package delays
- Truck count scales automatically with math.ceil(packages / capacity) (not added yet)

### v1.0 - WGU Submission

- Initial submission with nearest neighbor routing
- Custom hash table
- Three-truck static loading
- Colorama/tabulate CLI