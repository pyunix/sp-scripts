# stolen from Ash's script to list servers from opstatusDB

# Imports
import requests
from sys import argv
import json
from datetime import datetime

now = datetime.now()
DateStamp = now.strftime("%Y%m%d-")

# API documentation:
# http://dcsydusrvdoc01.fbu.com:8192

#uxlist = requests.get('http://dcsydusrvdoc01.fbu.com:8191//system/list/custom/fuzzy/OperatingSystem/ux')
list = requests.get('http://dcsydusrvdoc01.fbu.com:8191//system/list')
print(f"Found {len(list.json())} hosts\n")
data = list.json()
rawoutput = requests.get('http://dcsydusrvdoc01.fbu.com:8191//system/bulk',json=data)
print(f"Status = {rawoutput.status_code}\n")

with open(f"{DateStamp}Compute-InvDB.json","w") as JSONOut:
    json.dump(rawoutput.json(),JSONOut,indent=4)
