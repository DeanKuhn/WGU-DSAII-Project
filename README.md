# WGUPS Routing Program
A package delivery routing system built for WGU's C950 Data Structures & Algorithms II.

## Features
- Custom hash table implementation with linear probing
- KMeans geographic clustering via MDS distance matrix conversion
- Genetic algorithm for smart truck loading
- Truck delivery simulation with dynamic departure times
- CLI with colorama

## Planned Improvements
- [ ] Routing GA or nearest neighbor for stop ordering
- [ ] Hash table optimization
- [ ] Dijkstra's/A* preprocessing for distance matrix
- [ ] Multi-criteria package sorting (deadline + proximity)
- [ ] Role-based CLI (user vs. supervisor access)
- [ ] Address-based package lookup

## Changelog

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