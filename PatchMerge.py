#from SP_Util import message
from SP_Util import Utils
from SP_Util import Files

sp = Utils.SPVar()
#sp.NewDateStamp("20240319-")
basedir   = f'c:/Users/wdempsey/OSS/Customers/FBU'



ansiblecsvfile   = f'{basedir}/Patching/20240306-Ansible.csv'
#AnsibleCSV   = f'{basedir}/Patching/{sp.DateStamp}Ansible.csv'
#AnsibleCSV = "2024-03-06.patch.csv"

azurecsvfile   = f'{basedir}/Gather/Compute/{sp.DateStamp}Compute-AZ.csv'

gcpcsvfile   = f'{basedir}/Gather/Inventory/{sp.DateStamp}GCPInventory.csv'
gcplinuxcsvfile   = f'{basedir}/Patching/{sp.DateStamp}GCPInventory-Linux.csv'
#GCPLinuxCSV = "../Gather/GCPInventory/20240305-GCPInventory-Linux.csv"

inventorycsvfile   = f'{basedir}/Gather/Compute/{sp.DateStamp}Compute-InvDB.csv'
inventorylinuxcsvfile   = f'{basedir}/Patching/{sp.DateStamp}InvDB-Linux.csv'
#InventoryCSV  = "20240312-InvDB.csv"

PatchCSV   = f'{basedir}/Patching/{sp.DateStamp}Patch.csv'
#PatchCSV = "20240306b-Patch.csv"

tenablecsvfile   = f'{basedir}/Gather/Compute/{sp.DateStamp}Compute-Tenable.csv'
tenablelinuxcsvfile   = f'{basedir}/Patching/{sp.DateStamp}Tenable-Linux.csv'
#TenableCSV = "../Gather/TenableInventory/20240305-Tenable-Linux.csv"


mm = Utils.Logger("Test")
mm.SetLevel(mm.INFO)
mm.debug(sp.StartTime)

#--------------------------------------------------------------------
# Prepare Ansible file

ANS = Files.CSVFile(logger=mm)
ANS.ReadCSVFile(ansiblecsvfile)
ANS.BuildHeaders()
ANS.lookup = "DNSName"

#--------------------------------------------------------------------
# Prepare Azure ARC file

mm.SetLevel(mm.DEBUG)
AZ = Files.CSVFile(logger=mm)
AZ.ReadCSVFile(azurecsvfile)
AZ.BuildHeaders()
AZ.lookup = "name"
mm.SetLevel(mm.INFO)

mm.info(f'Removing non-linux operating systems from Azure ARC content')
newcontent = AZ.GrepCol("osSku","^.*ub|^.*sol|^.*ux")
AZ.content = newcontent
mm.info(f'AZ {len(AZ.content)} entries remain in Azure ARC content')

#--------------------------------------------------------------------
# Prepare GCP file
mm.info(f'Reading GCP Inventory File {gcpcsvfile}')
GCP = Files.CSVFile(logger=mm)
GCP.ReadCSVFile(gcpcsvfile)
GCP.BuildHeaders()
#GCP.AddHeaders(["Source","Collected"])
GCP.lookup = "DNSName"
mm.info(f'Removing Windows hosts from GCP Inventory File {gcpcsvfile}')
linuxhosts = GCP.GrepCol("OS Type","^(?!windows)")
GCP.content = linuxhosts
GCP.headers = []
GCP.AddHeaders(["Hostname", "DNSName", "OS Type", "OS Name", "Kernel Release", "Kernel Version", "Tags", "Project", "Zone", "IP Addresses", "State", "Source", "Collected"])
for row in GCP.content:
    row.update({"DNSName": row["Hostname"] + ".sap.fbu.com"})
mm.info(f'Writing Linux GCP Inventory File {gcplinuxcsvfile}')
GCP.WriteCSVFile(gcplinuxcsvfile)
GCP.filename = gcplinuxcsvfile


#--------------------------------------------------------------------
# Prepare InventoryDB file

INV = Files.CSVFile(logger=mm)
INV.ReadCSVFile(inventorycsvfile)
INV.BuildHeaders()
INV.lookup = "DNSName"
mm.info(f'Inv content includes {len(INV.content)} entries')

#mm.info(f'Removing status "Decommissioned" hosts from InventoryDB content')
#newcontent = INV.GrepCol("Status","^(?!decommissioned)")
#INV.content = newcontent
#mm.info(f'Inv {len(INV.content)} entries remain in INV content')

#mm.info(f'Removing hosts not supported by us from InventoryDB content')
#newcontent = INV.GrepCol("ResponsibleSupportTeam","^tech ops|^gt-cloud")
#INV.content = newcontent
#mm.info(f'Inv  {len(INV.content)} entries remain in INV content')

mm.info(f'Removing non linux hosts from InventoryDB content')
newcontent = INV.GrepCol("OperatingSystem","^.*ub|^.*sol|^.*ux")
INV.content = newcontent
mm.info(f'Inv  {len(INV.content)} entries remain')

mm.info(f'Removing Sun VRay hosts from InventoryDB content')
newcontent = INV.GrepCol("DNSName","(?!^.*vray)")
INV.content = newcontent
mm.info(f'Inv  {len(INV.content)} entries remain in INV content')

INV.WriteCSVFile(inventorylinuxcsvfile)
INV.filename = inventorylinuxcsvfile


#--------------------------------------------------------------------
# Prepare Patching file
PATCH = Files.CSVFile(logger=mm)
PATCH.filename = PatchCSV
#PATCH.ReadCSVFile(PatchCSV)
PATCH.AddHeaders(["Hostname","DNSName","OperatingSystem","Kernel","IPAddress","PatchPhase","ResponsibleSupportTeam","Category","ApplicationService","Status","Source","Collected"])
PATCH.lookup = "DNSName"

#--------------------------------------------------------------------
# Prepare Tenable file
TEN = Files.CSVFile(logger=mm)
TEN.ReadCSVFile(tenablecsvfile)
TEN.BuildHeaders()
TEN.lookup = "fqdns"

mm.info(f'Removing non-linux operating systems from Tenable content')
newcontent = TEN.GrepCol("operating_systems","^.*ub|^.*sol|^.*ux")
TEN.content = newcontent
mm.info(f'Inv  {len(TEN.content)} entries remain in Tenable content')

newcontent = TEN.SortCol("updated_at",rev=True)
TEN.content = newcontent

mm.info(f'Removing non-unique fqdns from Tenable content')
newcontent = TEN.UniqueCol("fqdns")
TEN.content = newcontent
mm.info(f'Inv  {len(TEN.content)} entries remain in Tenable content')

mm.info(f'Removing Sun VRay hosts from Tenable content')
newcontent = TEN.GrepCol("fqdns","(?!^.*vray)")
TEN.content = newcontent
mm.info(f'Inv  {len(TEN.content)} entries remain in Tenable content')

TEN.WriteCSVFile(tenablelinuxcsvfile)

#--------------------------------------------------------------------
#
mm.info(f'Merging {PATCH.filename} with {INV.filename}')
INVComp = Files.Compare(PATCH,INV,logger=mm)
INVComp.AddMaps({
    "Hostname": "AssetName",
    "DNSName": "DNSName", 
    "IPAddress": "IPAddress", 
    "PatchPhase": "PatchPhase", 
    "ResponsibleSupportTeam": "ResponsibleSupportTeam", 
    "Category": "Category", 
    "ApplicationService": "ApplicationService", 
    "Status": "Status", 
    "Source": "Source",
    "Collected": "Collected"})
INVComp.logger.debug(f'maps are: {INVComp.mapping}')
INVComp.Match(action="merge")

#--------------------------------------------------------------------
#
mm.info(f'Merging {PATCH.filename} with Ansible file {ANS.filename}')
ANSComp = Files.Compare(PATCH,ANS,logger=mm)
ANSComp.AddMaps({
    "DNSName": "DNSName", 
    "OperatingSystem": "OSType", 
    "Kernel": "Kernel", "Source": 
    "Source","Collected": "Collected"})
ANSComp.logger.debug(f'maps are: {ANSComp.mapping}')
ANSComp.Match(action="merge")

#--------------------------------------------------------------------
#
mm.info(f'Merging {PATCH.filename} with Azure ARC file {AZ.filename}')
PATCH.lookup = "Hostname"
AZComp = Files.Compare(PATCH,AZ,logger=mm)
AZComp.AddMaps({
    "Hostname": "name",
    "DNSName": "dnsFqdn", 
    "OperatingSystem": "osSku",
    "Kernel": "osVersion",
    "Source": "Source",
    "Collected": "Collected"})
AZComp.logger.debug(f'maps are: {AZComp.mapping}')
AZComp.Match(action="merge")
PATCH.lookup = "DNSName"

#--------------------------------------------------------------------
#


mm.info(f'Merging {PATCH.filename} with GCP file {GCP.filename}')
GCPComp = Files.Compare(PATCH,GCP,logger=mm)
GCPComp.AddMaps({
    "DNSName": "DNSName",
    "IPAddress": "IPAddresses", 
    "OperatingSystem": "OS Name", 
    "Kernel": "Kernel Release",
    "Source": "Source",
    "Collected": "Collected"})
GCPComp.logger.debug(f'maps are: {GCPComp.mapping}')
GCPComp.Match(action="merge")

#--------------------------------------------------------------------
#
mm.info(f'Merging {PATCH.filename} with Tenable {TEN.filename}')
TENComp = Files.Compare(PATCH,TEN,logger=mm)
TENComp.AddMaps({
    "Hostname": "hostnames",
    "DNSName": "fqdns", 
    "IPAddress": "ipv4s", 
    "Kernel": "operating_systems", 
    "Source": "Source",
    "Collected": "Collected"})
TENComp.logger.debug(f'maps are: {TENComp.mapping}')

#--------------------------------------------------------------------
#
mm.info(f'Filling gaps in {PATCH.filename} from InventoryDB {INV.filename}')
INVComp.RemoveMaps()
INVComp.AddMaps({
    "Hostname": "AssetName",
    "DNSName": "DNSName", 
    "IPAddress": "IPAddress", 
    "OperatingSystem": "OperatingSystem", 
    "Source": "Source", 
    "Collected": "Collected"})
INVComp.logger.debug(f'maps are: {INVComp.mapping}')
INVComp.Match(action="merge")

mm.info(f'Writing {PATCH.filename}')
INVComp.originalfile.WriteCSVFile(PatchCSV)


#csv1.ReadCSVFile(csvfile)
#mm.info(f"Row 0: {csv1.content[0]}")
#csv1.SetIndex("FWRuleName")
#csv1.SetLookup("FWRuleName")
#mm.info(f"CSV: index = {csv1.index}, lookup = {csv1.lookup}, rows = {len(csv1.content)}")