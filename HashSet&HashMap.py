class HashSet:
    __lengths = [5, 11, 23, 47, 97, 397, 797, 1597, 3203, 6421, 12853, 25717, 51437, 102877, 205759, 411527, 823117,
                 1646237, 3292489, 6584983, 13169977, 26339969, 52679969, 105359939, 210719881, 421439783]
    __add_space_const = 0.75
    __remove_space_const = 0.5

    def __init__(self, seq=None):
        self.__length = 0
        self.__count = 0
        self.__new_set = None
        self.__set = [[] for _ in range(self.__lengths[self.__length])]
        if seq:
            for value in seq:
                self.add(value)

    def __str__(self):
        if not self.__count:
            return "{}"
        result = "{"
        for bucket in self.__set:
            for value in bucket:
                result += f"{str(value)}, "
        return result[:-2] + "}"

    def __repr__(self):
        if not self.__count:
            return "{}"
        result = "{"
        for bucket in self.__set:
            for value in bucket:
                result += f"{str(value)}, "
        return result[:-2] + "}"

    def __len__(self):
        return self.__count

    def __iter__(self):
        for bucket in self.__set:
            for value in bucket:
                yield value

    def __contains__(self, value):
        index = hash(value) % len(self.__set)
        return value in self.__set[index]

    def add(self, value):
        if value in self:
            return
        self.__count += 1
        index = hash(value) % len(self.__set)
        self.__set[index].append(value)
        if self.__count > self.__add_space_const * len(self.__set):
            self.__length += 1
            self.__new_set = [[] for _ in range(self.__lengths[self.__length])]
            for bucket in self.__set:
                for value in bucket:
                    index = hash(value) % len(self.__new_set)
                    self.__new_set[index].append(value)
            self.__set = [[value for value in bucket] for bucket in self.__new_set]
            self.__new_set = None

    def remove(self, value):
        if value not in self:
            return
        self.__count -= 1
        index = hash(value) % len(self.__set)
        self.__set[index].remove(value)
        if self.__length and self.__count < self.__remove_space_const * self.__lengths[self.__length - 1]:
            self.__length -= 1
            self.__new_set = [[] for _ in range(self.__lengths[self.__length])]
            for bucket in self.__set:
                for value in bucket:
                    index = hash(value) % len(self.__new_set)
                    self.__new_set[index].append(value)
            self.__set = [[value for value in bucket] for bucket in self.__new_set]
            self.__new_set = None


class Pair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"({self.key}, {self.value})"

    def __repr__(self):
        return f"({self.key}, {self.value})"


class HashMap:
    __lengths = [5, 11, 23, 47, 97, 397, 797, 1597, 3203, 6421, 12853, 25717, 51437, 102877, 205759, 411527, 823117,
                 1646237, 3292489, 6584983, 13169977, 26339969, 52679969, 105359939, 210719881, 421439783]
    __add_space_const = 0.75
    __remove_space_const = 0.5

    def __init__(self, seq=None):
        self.__count = 0
        self.__length = 0
        self.__keys = HashSet()
        self.__new_map = None
        self.__map = [[] for _ in range(self.__lengths[self.__length])]
        if seq:
            for pair in seq:
                self[pair[0]] = pair[1]

    def __setitem__(self, key, value):
        if key in self.__keys:
            index = hash(key) % len(self.__map)
            for pair in self.__map[index]:
                if pair.key == key:
                    pair.value = value
                    break
        else:
            index = hash(key) % len(self.__map)
            pair = Pair(key, value)
            self.__map[index].append(pair)
            self.__keys.add(key)
            self.__count += 1
            if self.__count > self.__add_space_const * len(self.__map):
                self.__length += 1
                self.__new_map = [[] for _ in range(self.__lengths[self.__length])]
                for bucket in self.__map:
                    for pair in bucket:
                        index = hash(pair.key) % len(self.__new_map)
                        self.__new_map[index].append(Pair(pair.key, pair.value))
                self.__map = [[pair for pair in bucket] for bucket in self.__new_map]
                self.__new_map = None

    def __getitem__(self, key):
        if key not in self.__keys:
            return
        index = hash(key) % len(self.__map)
        for pair in self.__map[index]:
            if pair.key == key:
                return pair.value

    def __iter__(self):
        for bucket in self.__map:
            for pair in bucket:
                yield pair.key, pair.value

    def __str__(self):
        if not self.__count:
            return "{}"
        result = "{"
        for bucket in self.__map:
            for pair in bucket:
                result += f"{pair.key}: {pair.value}, "
        return result[:-2] + "}"

    def __repr__(self):
        if not self.__count:
            return "{}"
        result = "{"
        for bucket in self.__map:
            for pair in bucket:
                result += f"{pair.key}: {pair.value}, "
        return result[:-2] + "}"

    def __len__(self):
        return self.__count

    def __contains__(self, key):
        return key in self.__keys

    def get(self, key, default=None):
        if key not in self.__keys:
            return default
        index = hash(key) % len(self.__map)
        for pair in self.__map[index]:
            if pair.key == key:
                return pair.value

    def pop(self, key):
        if key not in self.__keys:
            return
        self.__count -= 1
        self.__keys.remove(key)
        index = hash(key) % len(self.__map)
        for pos in range(len(self.__map[index])):
            if self.__map[index][pos].key == key:
                self.__map[index].pop(pos)
        if self.__length and self.__count < self.__remove_space_const * self.__lengths[self.__length - 1]:
            self.__length -= 1
            self.__new_map = [[] for _ in range(self.__lengths[self.__length])]
            for bucket in self.__map:
                for pair in bucket:
                    index = hash(pair.key) % len(self.__new_map)
                    self.__new_map[index].append(Pair(pair.key, pair.value))
            self.__map = [[pair for pair in bucket] for bucket in self.__new_map]
            self.__new_map = None

    def get_keys(self):
        return self.__keys
