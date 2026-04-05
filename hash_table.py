class HashTable:
    def __init__(self):
        self.size = 101
        self.array = [None for _ in range(self.size)]
        self.slots_used = 0
        # primes for hash table size
        self.primes = [101, 211, 431, 863, 1741]

    def hashing_algorithm(self, package_id):
        return (package_id * 33) % self.size

    def insert(self, package):
        # load benchmark is 75%
        if ((float(self.slots_used) / float(self.size)) >= 0.75):
            self.array = self.resize()

        hashed_index = self.hashing_algorithm(package.package_id)
        closed = True

        while (closed):
            if self.array[hashed_index] is None:
                self.slots_used += 1
                closed = False
            elif self.array[hashed_index] == 'Deactivated':
                closed = False
            else:
                hashed_index = (hashed_index + 1) % self.size

        self.array[hashed_index] = package

    def resize(self):
        old_array = self.array

        if len(self.primes) > 1:
            self.primes.pop(0)
            self.size = self.primes[0]
        else:
            # if the hash table runs out of primes
            self.size = (self.size * 2) + 1

        # reset current array, since we have saved it as 'old_array'
        self.array = [None for _ in range(self.size)]
        # reset slots_used variable
        self.slots_used = 0

        for package in old_array:
            # important that we do not copy 'Deactivated' tombstone slots
            if package is not None and package != 'Deactivated':
                self.insert(package)

        return self.array

    def lookup(self, package_id):
        hashed_index = self.hashing_algorithm(package_id)
        elements_checked = 0

        # prevents infinite loops
        while elements_checked < self.size:
            current_item = self.array[hashed_index]

            if current_item is None:
                return 'Package not found.'
            if current_item != 'Deactivated' and\
                current_item.package_id == package_id:
                return current_item

            # this only happens if the slot is a tombstone slot
            hashed_index = (hashed_index + 1) % self.size
            elements_checked += 1

        # this only happens if the entire array is iterated over
        return 'Package not found.'

    def delete(self, package_id):
        hashed_index = self.hashing_algorithm(package_id)

        elements_checked = 0

        while elements_checked < self.size:
            current_item = self.array[hashed_index]
            if self.array[hashed_index] is None:
                return "\nPackage not found."
            if current_item != 'Deactivated' and\
                current_item.package_id == package_id:
                self.array[hashed_index] = 'Deactivated'
                print("\nYour package has been deleted.")

                # Notice that slots_used is not decremented upon deletion.
                # By not decrementing slots_used in the delete() function,
                # it ensures that a table full of 'Deactivated' tombstone
                # slots is eventually resized and ridded of these slots,
                # as too many tombstone slots makes both the insertion and
                # lookup functions inefficient, and takes up a lot of memory.
                return

            hashed_index = (hashed_index + 1) % self.size
            elements_checked += 1

        return 'Package not found.'

    def get_array(self):
        return self.array