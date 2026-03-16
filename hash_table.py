# IMPORTANT FOR OTHER COMPANIES:
# This HashTable class does not account for collisions.  Please use the
# alternative class (HashTableV2) in hash_table_vs.py if you are expecting
# to process a larger amount of packages.
class HashTable:
    def __init__(self):
        # 101 is a good array size, as it is prime
        self.array = [None for _ in range(101)]

    def hashing_algorithm(self, package_id):
        # simple hashing algorithm, importantt to % by the array size
        return (package_id * 33) % 101

    def insert(self, package):
        self.array[self.hashing_algorithm(package.package_id)] = package

    def lookup(self, package_id):
        hashed_index = self.hashing_algorithm(package_id)
        return self.array[hashed_index]

    def get_array(self):
        return self.array