# instead of loading the entire file into memory, this import loads the
# file in row by row, which allows for more efficient data parsing
import csv

from package import Package
from status import Status
from hash_table import HashTable

status = None
delivery_time = None

# IMPORTANT FOR OTHER COMPANIES:
# Your number of addresses may be different than WGUPS's.  Adjust accordingly.
num_addresses = 27
distances_matrix = [[None for _ in range(num_addresses)] for _ in range(num_addresses)]
locations_matrix = [[None for _ in range(3)] for _ in range(num_addresses)]

def load_csvs():
    ht = HashTable()    # create HashTable object upon csv load

    with open('data/packages.csv', 'r') as packages:
        # DictReader to read column names instead of indeces
        csv_reader = csv.DictReader(packages, delimiter = ',')
        for row in csv_reader:
            # check if package can be marked delayed or at hub
            if row['Special Notes'] == 'Delayed on flight---will not arrive to depot until 9:05 am':
                status = Status.DELAYED
            else:
                status = Status.AT_HUB
            # create package class based on the package attributes in csv file
            package = Package(
                int(row['Package ID']), # important to make package_id an integer
                row['Address'],
                row['City'],
                row['State'],
                row['Zip'],
                row['Delivery Deadline'],
                row['Weight KILO'],
                row['Special Notes'],
                status,
                delivery_time
                )

            # insert package into the HashTable object's table
            ht.insert(package)

    # load locations
    with open('data/locations.csv', 'r') as locations:
        csv_reader = csv.DictReader(locations, delimiter = ',')
        row_num = 0
        for row in csv_reader:
            # insert locations into locations matrix
            locations_matrix[row_num] = (int(row['Index']), row['Name'], row['Address'])
            row_num += 1

    # load distances
    with open('data/distances.csv', 'r') as distances:
        csv_reader = csv.reader(distances, delimiter = ',')
        # insert distances into distances matrix
        row_num = 0
        for row in csv_reader:
            col_num = 0
            for distance in row:
                # see note at top of function def
                distances_insert(row_num, col_num, float(distance))
                col_num += 1
            row_num += 1

    # return the HashTable object just created, as well as the locations
    # and distances matrices that our routing program will need
    return ht, locations_matrix, distances_matrix

# IMPORTANT FOR OTHER COMPANIES:
# If you use a full distance matrix instead of a condensed distance matrix,
# this step is not necessary
def distances_insert(row, col, distance):
    distances_matrix[row][col] = distance

    # do this so that we have a full matrix, not just half
    distances_matrix[col][row] = distance