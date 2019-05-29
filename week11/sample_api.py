import urllib.request
import json

with urllib.request.urlopen("https://api.iextrading.com/1.0/stock/amd/company") as f:
    data = f.read().decode('utf-8')
    jdata = json.loads(data)
    print(data)
