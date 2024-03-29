###############################################################################
# Powershell script: PyunixInit.ps1
# Author: Warren Dempsey
#
# Usage: SP_Auth.ps1 <AuthType>
#
# Description:
# Run this script to 
# Generate Auth tokens
###############################################################################

###############################################################################
# Check for Command Line Arguments - This section goes first.

param(
    [Parameter()]
    [String]$AuthType
)


###############################################################################
# Bail if we get any errors
$ErrorActionPreference = "Stop"

###############################################################################
# Who are we?
$ScriptName = $MyInvocation.InvocationName

#--------------------------------------------------------------------------------------------------------------------------------
# Look here for the main script folder.
$ScriptPath = $MyInvocation.MyCommand.Path

function Exit_Script {
	Param (
        [Int]$Countdown,
        [Int]$ExitCode
    )
	
	
	while ($Countdown -gt 0) {
		write-host -foregroundcolor "Green" "$Scriptname : Info: Script will exit in $Countdown seconds`r" -nonewline
		start-sleep 1
		$Countdown--
	}
	write-host -foregroundcolor "Green" "`n$Scriptname : Info: Have a nice day!`n"
	
	exit $ExitCode
}

if (($CustomerDir.length -gt 0) -and  ($ActiveCustomer.length -gt 0)) {
	$AuthFileDir = "$CustomerDir\$ActiveCustomer\Gather\AuthFiles"
} else {
	write-host -foregroundcolor "Red" "Error: Usage: $Scriptname <AuthType>"
	Exit_Script 0 2
}

if (-Not (Test-Path -PathType Container $AuthFileDir)){
write-host -foregroundcolor "Red" "Error: ${Scriptname}: AuthFileDir ($AuthFileDir) does not exist"
	Exit_Script 0 3
}

switch ($AuthType) {
	"gcp" {
        # For gcloud CLI, use
        # gcloud auth login	
        gcloud auth application-default login
        gcloud auth application-default print-access-token | set-content -Path "$AuthFileDir\GCPAuth.txt"
    }
	"gcloud" {
		gcloud auth login
	}
	Default {
		write-host -foregroundcolor "Red" "Error: Usage: $Scriptname <AuthType>"
		Exit_Script 0 1
	}
}
