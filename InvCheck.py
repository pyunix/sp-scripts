from SP_Util import message
from SP_Util import stats
from SP_Util import files

sp = stats.stats()
sp.NewDateStamp("20240220-")
csvfile = sp.DateStamp + "FWRules-GCP.csv"
jsonfile = sp.DateStamp + "FWRules-GCP.json"


mm = message.new("Test")
mm.SetLevel(mm.DEBUG)

mm.debug(sp.StartTime)

manifest = files.JSONFile()
manifest.debug = mm
manifest.ReadJSONFile("manifest.json")

for i in manifest.content:
    mm.debug(f'Entry: {i}')

if "InvDB" in manifest.raw.keys():
    manifest.content = manifest.raw["InvDB"]
    mm.info(f'Content = {manifest.content}')
    if "filename" in manifest.content.keys():
      manifest.filename = manifest.content["filename"]
      mm.debug(f"setting filename to {manifest.filename}")
    if "lookup" in manifest.content.keys():
        manifest.lookup = manifest.content["lookup"]
        mm.debug(f"setting lookup to {manifest.lookup}")
        
INVFile = files.CSVFile()
INVFile.debug = mm
INVFile.ReadCSVFile(manifest.filename)
INVFile.BuildHeaders()
INVFile.lookup = manifest.lookup

        
#if "headers" in manifest.content.keys():
#    CSV1.AddHeaders(manifest.content["headers"])
#    mm.debug(f"setting headers to {manifest.headers}")
#mm.debug(f'Headers = {CSV1.headers}')

if "GCPInventory" in manifest.raw.keys():
    manifest.content = manifest.raw["GCPInventory"]
    mm.info(f'Content = {manifest.content}')
    if "filename" in manifest.content.keys():
        manifest.filename = manifest.content["filename"]
        mm.debug(f"setting filename to {manifest.filename}")
    if "lookup" in manifest.content.keys():
        manifest.lookup = manifest.content["lookup"]
        mm.debug(f"setting lookup to {manifest.lookup}")

GCPFile = files.CSVFile()
GCPFile.debug = mm
GCPFile.ReadCSVFile(manifest.filename)
GCPFile.BuildHeaders()
GCPFile.lookup = manifest.lookup

xx = files.Compare(INVFile,GCPFile)
xx.debug = mm

if "InvDB-GCPInventory" in manifest.raw.keys():
    xx.AddMaps(manifest.raw["InvDB-GCPInventory"]["mapping"])


mm.debug(f'maps are: {xx.mapping}')

xx.Match(action="merge")
xx.originalfile.WriteCSVFile("xx.csv")


#csv1.ReadCSVFile(csvfile)
#mm.info(f"Row 0: {csv1.content[0]}")
#csv1.SetIndex("FWRuleName")
#csv1.SetLookup("FWRuleName")
#mm.info(f"CSV: index = {csv1.index}, lookup = {csv1.lookup}, rows = {len(csv1.content)}")