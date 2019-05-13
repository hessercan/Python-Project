import hashlib

with open("download.pdf", "rb") as f:
    checksum = hashlib.md5()
    data = f.read()
    checksum.update(data)
    print(checksum.hexdigest())
