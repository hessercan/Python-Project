import hashlib
import urllib.request
import os

FILEURL = "http://downloads.ascentops.com/southhills/file.bin"
FILENAME = os.path.split(FILEURL)[1]


try:
    with urllib.request.urlopen(FILEURL) as urlf:
        with open (FILENAME, "wb") as dl:
            data = urlf.read()
            dl.write(data)
            checksum = hashlib.md5()
            checksum.update(data)
            print("File Downloaded to {}".format(FILENAME))
            print("MD5: {}".format(checksum.hexdigest()))
except urllib.error.URLError:
    print("Failed Download")
