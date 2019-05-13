import urllib.request
import json

DOGSURL = "http://downloads.ascentops.com/southhills/dogs.json"
# f = urllib.request.urlopen(DOGSURL)
# data = json.load(f)
# print(data)
# f.close()

PDFURL = "https://www.southhills.edu/media/PDF/catalog/catalog_2017-18.pdf"
with urllib.request.urlopen(PDFURL) as f:
    data = f.read()
    with open ("download.pdf", "wb") as dl:
        dl.write(data)
        checksum = hashlib.md5()
        data = dl.read()
        checksum.update(data)
        print(checksum.hexdigest())
