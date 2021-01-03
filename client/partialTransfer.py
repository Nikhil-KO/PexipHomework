import os
import hashlib
import pathlib

CHUNK_SIZE = 1048576

# reference https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
'''
This class is designed to be given to each file, it stores the hash of each ~1MB block of data, and on change the check function should be run
It computes the new hashs and when a block's data has changed it should be returned
'''
class PartialTransfer:

    @staticmethod
    # Read file by ~1MB chunks
    def read_chunks(file, chunk_size=CHUNK_SIZE):
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data

    def __init__(self, path : pathlib.Path) -> None:
        self.path = path
        self.file_hash =[]
        with open(path, 'rb') as f:
            for data in self.read_chunks(f):
                hash = hashlib.md5(data).hexdigest()
                self.file_hash.append(hash)
                print(hash)    

    def check(self):
        block = 0
        changed_blocks = []
        with open(self.path, 'rb') as f:
            for data in self.read_chunks(f):
                hash = hashlib.md5(data).hexdigest()
                if block >= len(self.file_hash) or self.file_hash[block] != hash:
                    print("Block ", block, " has changed!")
                    changed_blocks.append(block)
                    self.file_hash[block] = hash
                block += 1
        return changed_blocks, CHUNK_SIZE
    
# Testing
if __name__ == "__main__":
    path = pathlib.Path('listen/ok.txt')
    t = PartialTransfer(path)
    print("------ BREAKPOINT HERE -------")
    t.check()
