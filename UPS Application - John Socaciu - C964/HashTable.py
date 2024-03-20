class HashTable:  # hashtables have a worse case of O(n)
    def __init__(self, initialCapacity = 40):
        self.buckets = [[] for someNumber in range(initialCapacity)] # each hash table array element is a bucket

    def insert(self, key, package): # time-complexity is O(n) 
        indexofBucket = hash(key) % len(self.buckets)
        bucket = self.buckets[indexofBucket]
        pairOfKeys = [key, package] # insert the item to the end of the bucket array
        bucket.append(pairOfKeys)

    def lookup(self, key): # time-complexity is O(1) 
        hashCode = hash(key) # find the hash code for the chosen key
        index = hashCode % len(self.buckets) # find the index of the bucket, a location where the key could be located
        if index < len(self.buckets) and key in dict(self.buckets[index]): # check if the calculated index is within the array of buckets
            return dict(self.buckets[index])[key] # if the key is found, return it
    
    def remove(self, key): # time-complexity is O(n)
        indexOfBucket = hash(key) % len(self.buckets) # calculate the index of the bucket where is key could be located
        bucket = self.buckets[indexOfBucket] # get the bucket that correctly corresponds to the index
        for pair in bucket:  # Iterate through each key pair in the bucket.
            if pair[0] == key:  # Check if the current key matches the target key for removal.
                bucket.remove(pair) # if the pair is found, remove it from the bucket entirely 