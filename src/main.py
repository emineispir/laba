
class SSTable:
    def __init__(self, max_size=30):
        self.max_size = max_size
        self.storage = {}

    def insert(self, key, value):
        if len(self.storage) < self.max_size:
            self.storage[key] = value
        else:
            print("SSTable is full. Consider compaction.")

    def get(self, key):
        return self.storage.get(key, "Not found")

    def update(self, key, value):
        if key in self.storage:
            self.storage[key] = value
        else:
            print("Key not found.")

    def delete(self, key):
        if key in self.storage:
            del self.storage[key]
        else:
            print("Key not found.")

class LSMTree:
    def __init__(self, max_size=30):
        self.max_size = max_size
        self.memtable = SSTable(max_size)
        self.sstables = []

    def insert(self, key, value):
        if len(self.memtable.storage) >= self.max_size:
            self._compact()
        self.memtable.insert(key, value)

    def get(self, key):
        result = self.memtable.get(key)
        if result == "Not found":
            for sstable in reversed(self.sstables):
                result = sstable.get(key)
                if result != "Not found":
                    return result
        return result

    def update(self, key, value):
        self.insert(key, value)

    def delete(self, key):
        self.insert(key, None)

    def _compact(self):
        self.sstables.append(self.memtable)
        self.memtable = SSTable(self.max_size)

# Ana program akışını tanımlayalım.
if __name__ == "__main__":
    lsm_tree = LSMTree()
    lsm_tree.insert("key1", "value1")
    print(f"key1 için değer: {lsm_tree.get('key1')}")
    lsm_tree.update("key1", "updated_value1")
    print(f"key1 için güncellenmiş değer: {lsm_tree.get('key1')}")
    lsm_tree.delete("key1")
    print(f"key1 silindikten sonra değer: {lsm_tree.get('key1')}")
