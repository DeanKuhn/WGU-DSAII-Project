import csv
from datetime import datetime

from package import Package
from status import Status
from hash_table import HashTable

def load_csvs():
    status = None
    delivery_time = None
    deadline = None

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

            if row['Delivery Deadline'] == 'EOD':
                deadline = datetime(2038, 1, 19, 17, 0)
            else:
                deadline = datetime.strptime(row['Delivery Deadline'], "%I:%M %p")
                deadline = deadline.replace(2038, 1, 19)

            # same as this:
            # result = []
            # for x in ['REFRIG', 'SIG', '']
            #   if x:
            #       result.append(x)
            constraints = set(x for x in row['Constraints'].split('|') if x)

            # create package object based on the package attributes in csv file
            package = Package(
                int(row['Package ID']), # important to make package_id an integer
                row['Address'],
                row['City'],
                row['State'],
                row['Zip'],
                deadline,
                row['Weight KILO'],
                row['Weight Class'],
                constraints,
                row['Special Notes'],
                status,
                delivery_time
                )

            # insert package into the HashTable object's table
            ht.insert(package)

    num_addresses = 87
    distances_matrix = [[None for _ in range(num_addresses)] for _ in range(num_addresses)]
    locations_matrix = [[None for _ in range(3)] for _ in range(num_addresses)]

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
                distances_matrix[row_num][col_num] = float(distance)
                col_num += 1
            row_num += 1

    # return the HashTable object just created, as well as the locations
    # and distances matrices that our routing program will need
    return ht, locations_matrix, distances_matrix