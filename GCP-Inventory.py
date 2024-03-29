#--------------------------------------------------------------------------------------------------------------------------------
# Python script: Inventory_DC_GCP.py
# Author: Warren Dempsey
# Company OSS Group NZ
#
# Modification History:
# 20230926 WD - Start conversion from ps1
#
# Usage: Run this script to build a list of DC inventory (Projects) for GCP based on the filter pattern specified
from SP_Util import Files,Utils

import csv
import json
#import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime

sp = Utils.SPVar()

#----------------------------------------------------------------------------------------------------------------------------------
# Setup some debugging and command line args  
SPLog = Utils.Logger("GCPInventory")
SPLog.SetLevel(SPLog.INFO)
  


# For testing we may want to have multiple BIN directories. Look at where the script was called from for the "right" helper scripts.
OSSBinDir = sys.argv[0]
ScriptName = OSSBinDir
#OSS_Dir = split-path -path $OSSBinDir
OSSVersion = "20240312"
now = datetime.now()

DCType = "Google Cloud Project"
if os.environ.get("DateStamp") == None:
    DateStamp = ""
else:
    DateStamp = os.environ.get("DateStamp")
    
SPLog.info(f"Generating GCP Inventory file: {DateStamp}GCPInventory.csv")

if os.environ.get("GCPProjectFilter") == None:
    GCPProjectFilter = "^fbu|int"
    SPLog.debug(f"GCPProjectFilter is not set")
else:
    GCPProjectFilter = os.environ.get("GCPProjectFilter")

SPLog.debug(f"GCPProjectFilter {GCPProjectFilter}")

DCType = "gcloud-project"
HostFile = f"..\Compute\{DateStamp}Compute-GCP.csv"
GCPOutputJSON = ""
#--------------------------------------------------------------------------------------------------------------------------------
# Helper functions
def read_csv_file(csv_file_name):
    # Open the CSV file and create a reader object
    with open(csv_file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)



#--------------------------------------------------------------------------------------------------------------------------------
Headers = ["Hostname","OS Type","Kernel Release","Backups Needed","BootDisk SnapCount","BootDisk SnapLast","CPU Insight","Memory Insight","LastUpdate","Application Label","Environment Label","Tier Label","NessusAgent Version","OSConfigAgent Version","OpsAgent Version","Project","Zone","Instance","IP Addresses","Tags","State","GCP Hostname","Kernel Version","OS Name","Udsagent Version","GPG2 Version","wget Version","sapconf Version","aide Version","systemd Version","openssl Version","BootDisk Name","Source","Collected"]

OSHeaders = [         "OS Type","Kernel Release",                                                                                         "LastUpdate",                                                     "NessusAgent Version","OSConfigAgent Version","OpsAgent Version",                                                        "GCP Hostname","Kernel Version","OS Name","Udsagent Version","GPG2 Version","wget Version","sapconf Version","aide Version","systemd Version","openssl Version"]
ComputeHeaders = [                                                                                                                                                                                                                                                            "Project","Zone","Instance","IP Addresses","Tags","State"]
CPUInsightHeaders = [                                                                                      "CPU Insight"]
MemoryInsightHeaders = [                                                                                                 "Memory Insight"]
SnapHeaders = [                                                  "BootDisk SnapCount","BootDisk SnapLast" ]
BootDiskHeaders = ["BootDisk Name"]

#--------------------------------------------------------------------------------------------------------------------------------
# Go grab some stuff!
#OSFile = open(f"..\OperatingSystem\{DateStamp}OperatingSystem-GCP.csv","r")
#OSIn = csv.DictReader(OSFile, delimiter=',', quotechar='"')
OSIn = read_csv_file(f"..\OperatingSystem\{DateStamp}OperatingSystem-GCP.csv")

CPUInsightFile = open(f"..\FinOps\{DateStamp}CPU-GCP.csv","r")
CPUInsightIn = csv.DictReader(CPUInsightFile, delimiter=',', quotechar='"')

MemoryInsightFile = open(f"..\FinOps\{DateStamp}Memory-GCP.csv","r")
MemoryInsightIn = csv.DictReader(MemoryInsightFile, delimiter=',', quotechar='"')

SnapFile = open(f"..\Storage\{DateStamp}LastSnap-GCP.csv","r")
SnapIn = csv.DictReader(SnapFile, delimiter=',', quotechar='"')

BootDiskFile = open(f"..\Storage\{DateStamp}BootDisk-GCP.csv","r")
BootDiskIn = csv.DictReader(BootDiskFile, delimiter=',', quotechar='"')

CSVOut = open(f'{DateStamp}GCPInventory.csv', 'w', newline='')
writer = csv.DictWriter(CSVOut,fieldnames=Headers)
writer.writeheader()
    
with open(HostFile, newline='') as csvfile:
    GCPHosts = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for row in GCPHosts:
        matched = False
        matches = []
        if len(row["Hostname"]) > 0:
            Hostname = row["Hostname"]
            #SPLog.debug(f"Building line for {Hostname}")
            Line = {"Hostname": Hostname,"Source": "GCP Inventory", "Collected": DateStamp[0:8]}

            # While we're here, grab the headers from the Compute file
            #SPLog.debug(f'{Hostname}: Got Compute Headers {row}')
            for x in ComputeHeaders:
                Line[x] = row[x]
            
            # Break down the Labels and pull out the ones we want to capture
            if len(row["Labels"]) > 0:
                Labels = row["Labels"].split(' ')
                #SPLog.debug(f'{Hostname}: Got labels {Labels}') 
                
                dLabels = {}
                for Label in Labels:
                    #SPLog.debug(f'{Hostname}: processing label {Label}') 
                    if len(Label) > 0:
                        sLabel = Label.split(":")
                        dLabels[sLabel[0].lower()] = sLabel[1]
                        #SPLog.debug(f'Labels for {Hostname}: {dLabels}')
                if "application" in dLabels.keys():
                    #SPLog.debug(f'{Hostname}: Found application label {dLabels["application"]}')
                    Line["Application Label"] = dLabels["application"]
                if "environment" in dLabels.keys():
                    #SPLog.debug(f'{Hostname}: found environment label {dLabels["environment"]}')
                    Line["Environment Label"] = dLabels["environment"]
                if "tier" in dLabels.keys():
                    #SPLog.debug(f'{Hostname}: Found tier label {dLabels["tier"]}')
                    Line["Tier Label"] = dLabels["tier"]
                if "backups" in dLabels.keys():
                    #SPLog.debug(f'{Hostname}: Found backups label {dLabels["backups"]}')
                    Line["Backups Needed"] = dLabels["backups"]
                else:
                    #SPLog.debug(f'{Hostname}: no backups label - Assuming yes (required)')
                    Line["Backups Needed"] = "Yes"
            else:
                Line["Application Label"] = "None"
                Line["Environment Label"] = "None"
                Line["Tier Label"] = "None"
                Line["Backups Needed"] = "Yes"

            OSRow = False            
            for xRow in OSIn:
                SPLog.debug(f'{Hostname}: Checking {xRow["Hostname"]} = {Hostname}')
                if xRow["Hostname"] == Hostname:
                    #SPLog.debug(f'{Hostname}: Got OS Headers {xRow}')
                    OSRow = True
                    for x in OSHeaders:
                        Line[x] = xRow[x]
                    #print(row["OS Type"])
                    break
                    
            if OSRow == False:
                #SPLog.debug(f'{Hostname}: No OS Headers')
                for x in OSHeaders:
                    Line[x] = "None"
                    
            CPUInsightRow = False
            for xRow in CPUInsightIn:
                if xRow["Hostname"] == Hostname:
                    CPUInsightRow = True
                    for x in CPUInsightHeaders:
                        Line[x] = xRow[x]
                    break

            if CPUInsightRow == False:
                for x in CPUInsightHeaders:
                    Line[x] = "None"
            
            MemoryInsightRow = False
            for xRow in MemoryInsightIn:
                if xRow["Hostname"] == Hostname:
                    MemoryInsightRow = True
                    for x in MemoryInsightHeaders:
                        Line[x] = xRow[x]
                    break

            if MemoryInsightRow == False:
                for x in MemoryInsightHeaders:
                    Line[x] = "None"

            SnapRow = False    
            for xRow in SnapIn:
                if xRow["Hostname"] == Hostname:
                    SnapRow = True
                    for x in SnapHeaders:
                        Line[x] = xRow[x]
                    break

            if SnapRow == False:
                for x in SnapHeaders:
                    Line[x] = "None"
                
            BootDiskRow = False                
            for xRow in BootDiskIn:
                if xRow["Hostname"] == Hostname:
                    BootDiskRow = True
                    for x in BootDiskHeaders:
                        Line[x] = xRow[x]
                    break

            if BootDiskRow == False:
                for x in BootDiskHeaders:
                    Line[x] = "None"
                  
                    #Line["Backups Needed"] = row["Backups Needed"]
            #print(f"Line is {Line}\n")
            writer.writerow(Line)
    