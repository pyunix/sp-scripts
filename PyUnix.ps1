###############################################################################
# Powershell script: PyunixInit.ps1
# Author: Warren Dempsey
#
# Usage: PyUnixInit.ps1 -VDrive [DriveLetter] -VENV [VENV Folder]
#
# Description:
# Run this script to 
# Start a Python instance from a VENV
###############################################################################

###############################################################################
# Check for Command Line Arguments - This section goes first.

param(
    [Parameter()]
    [String]$VDrive,
    [String]$VENV,
    [String]$PVersion
)

# Was: param($ConfigFile = "$PSScriptRoot/config.ini")
$ExitStatus = 0

###############################################################################
# Bail if we get any errors
$ErrorActionPreference = "Stop"

###############################################################################
# Who are we?
$ScriptName = $MyInvocation.InvocationName

#--------------------------------------------------------------------------------------------------------------------------------
# Look here for the main script folder.
$ScriptPath = $MyInvocation.MyCommand.Path

#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: PSScriptRoot is: $PSScriptRoot"
#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: VDrive is: $VDrive"
#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: VENV is: $VENV"
#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: Python Version is: $PVersion"

#$VDrive
#exit 0

if ($VDrive.length -gt 0) {
	$Map_Drive = $VDrive
} elseif ($PYUnixDrive.length -gt 0) {
	$Map_Drive = $PYUnixDrive
} else {
	$Map_Drive = "V:"
}


if ($PVersion.length -eq 0) {
	$PythonVersion = "Python311"
} else {
	$PythonVersion = $PVersion
}

$PythonPath = "C:\Users\wdempsey\AppData\Local\Programs\Python\Python311\"

if ($VENV.length -gt 0) {
	#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: VENV.length -gt 0"
	$Map_VENV = $VENV
} elseif ($PYUnixVENV.length -gt 0) {
	#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: VENV.length -gt 0"
	$Map_VENV = $PYUnixVENV
} else {
	$Map_VENV = $PythonVersion
}

write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: Map_VENV = $Map_VENV PythonVersion = $PythonVersion, Map_Drive = $Map_Drive"
#exit 0 

if (Test-Path -path $Map_VENV) {
	write-host -foregroundcolor "Green" "Info: ${Scriptname}: Python VENV $Map_VENV already exists"
} else {
	write-host -foregroundcolor "Green" "Info: ${Scriptname}: Creating a new VENV: $Map_VENV"
	try {
		(& "$($PythonPath)python" -m venv $Map_VENV --copies)
		if ($LastExitCode -eq 0) {
			write-host -foregroundcolor "Green" "Info: ${Scriptname}: New VENV created OK"
		} else {
			write-host -foregroundcolor "Red" "ERROR: ${Scriptname}: New VENV creation failed"
			exit 1
		}
	}
	catch {
		write-host -foregroundcolor "Red" "ERROR: ${Scriptname}: New VENV creation failed"
		exit 1
	}
}

#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: Map_Drive is: $Map_Drive"
#write-host -foregroundcolor "Blue" "Debug: ${Scriptname}: Map_VENV is: $Map_VENV"

if (Test-Path -path $Map_Drive) {
	write-host -foregroundcolor "Green" "Info: ${Scriptname}: Drive $Map_Drive already exists"
} else {
	subst $Map_Drive $Map_VENV
}


& ($Map_Drive + "\scripts\activate.ps1")

#write-host -foregroundcolor "Green" "Info: ${Scriptname}: Starting Python-enabled Powershell"
#set-location $Map_Drive
#start-process powershell

write-host -foregroundcolor "Green" "Info: ${Scriptname}: Finished. VENV mounted at $Map_Drive. Run: $Map_Drive\Scripts\Activate.ps1"
#sleep 10



