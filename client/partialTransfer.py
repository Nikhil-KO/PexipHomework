import os
import hashlib
import pathlib

CHUNK_SIZE = 1048576

# reference https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python
# needed to implement a soft rolling checksum https://rsync.samba.org/tech_report/node3.html
'''
This class is designed to be given to each file, it stores the hash of each ~1MB block of data, and on change the check function should be run
It computes the new hash's and when a block's data has changed it should be returned
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
                    changed_blocks.append((block, data))
                    self.file_hash[block] = hash
                block += 1
        return changed_blocks, CHUNK_SIZE

def recreate(path : pathlib.Path, changes, chunk_size):
    with open(path, 'wb') as f:
        for change in changes:
            position = change[0] * chunk_size
            f.seek(position)
            f.write(change[1])

# Testing
if __name__ == "__main__":
    listenFile = pathlib.Path('listen/partialTestSource.txt')
    source = PartialTransfer(listenFile)
    print("------ BREAKPOINT HERE -------")
    changes, chunk_size = source.check()
    destFile = pathlib.Path('listen/partialTestDest.txt')
    recreate(destFile, changes, chunk_size)