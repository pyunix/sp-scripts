from SP_Util import message
from SP_Util import Utils
from SP_Util import Files

import re


sp = Utils.SPVar()
#sp.NewDateStamp("20240319-")
basedir   = f'c:/Users/wdempsey/OSS/Customers/FBU'
jsonfile  = f'{basedir}/Gather/Compute/{sp.DateStamp}Compute-AZ.json'
csvfile   = f'{basedir}/Gather/Inventory/{sp.DateStamp}AZInventory.csv'

header1 = ['name','dnsFqdn','location','osSku','osVersion','resourceGroup','tags','type','vmId','vmUuid','lastStatusChange','status']

#jsonfile = f'{basedir}/Gather/{sp.DateStamp}Tenable.json'

mm = message.new("AZComputeCSV")
mm.SetLevel(mm.INFO)

mm.debug(sp.StartTime)
mm.debug(f"{sp.DateStamp} starting")

JSONFile = Files.JSONFile(logger=mm)
JSONFile.ReadJSONFile(jsonfile)
JSONFile.BuildHeaders()
JSONFile.lookup = "name"

CSVFile = Files.CSVFile(logger=mm)
#CSVFile.JSON2CSV(JSONFile.content,csvfile)
CSVFile.AddHeaders(header1 + ['Source', 'Collected','ProvisioningState','AutoUpgradeMinorVersion','EnableAutomaticUpgrade', 'StatusCode', 'StatusLevel', 'StatusMessage'])
CSVFile.lookup = "name"
CSVFile.content = []

for row in JSONFile.content:
    line = {}
    for word in header1:
        line.update({word: row[word]})
    mm.info(f'Processing {line}')
        
    line.update({
        'Source': 'AzureArc',
        'Collected': sp.DateStamp[0:8],
        'AutoUpgradeMinorVersion': "None",
        'EnableAutomaticUpgrade': "None",
        'StatusCode': "None",
        'StatusLevel': "None",
        'ProvisioningState': "None",
        'StatusMessage': "None"
    })
        
    for resource in row["resources"]:

        if re.match("^MDE\.",resource["name"]):
            mm.debug(f'status for {line["name"]}={resource["properties"]["instanceView"]}')
            line.update({
                'AutoUpgradeMinorVersion': resource["properties"]["autoUpgradeMinorVersion"], 
                'EnableAutomaticUpgrade': resource["properties"]["enableAutomaticUpgrade"], 
                'ProvisioningState': resource["properties"]["provisioningState"]
            })
            if resource["properties"]["instanceView"]["status"]:
                line.update({
                    'StatusCode': resource["properties"]["instanceView"]["status"]["code"],
                    'StatusLevel': resource["properties"]["instanceView"]["status"]["level"],
                    'StatusMessage': resource["properties"]["instanceView"]["status"]["message"]
                })    
            mm.debug(f'Found MDE extension . Line is {line}')
#        exit(0)
    CSVFile.AddRow(line)
    
#for row in CSVFile.content:
#    for word in row:
#        row.update({word: re.sub('[\[\]",]| *$','',row[word]).lower()})
#        x = row[CSVFile.lookup].split(".")[0]
#        row.update({CSVFile.lookup: x})

CSVFile.logger.info(f'Removing blank lookup field ({CSVFile.lookup})')
#CSVFile.GrepCol("name","(?!^$)")

# remove rows that don't have a useful hostname or other than type=microsoft.hybridcompute/machines
#rowcount = len(CSVFile.content)
#counter = 0
#while counter < rowcount:
#
#    row = CSVFile.content[counter]
#    if row[CSVFile.lookup] == "" or row["type"] != 'microsoft.hybridcompute/machines':
#        CSVFile.RemoveRow(row)
#    else:
#        counter += 1
#    rowcount = len(CSVFile.content)

    
CSVFile.WriteCSVFile(csvfile)
