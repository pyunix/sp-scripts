#--------------------------------------------------------------------------------------------------------------------------------
# Powershell script: .Profile.ps1
# Author: Warren Dempsey
# Company OSS Group NZ
#
# Modification History:
# 20230626 WD - Initial version
#
# Usage: Run this script to set the environment for a customer

#--------------------------------------------------------------------------------------------------------------------------------
# Bail if we get any errors
$ErrorActionPreference = "Stop"

# Who are we?
$ScriptName = $MyInvocation.InvocationName


# Look here for the base script path in case we need this later (For example to find a "tmp" directory at the same folder level)
$ScriptPath = $MyInvocation.MyCommand.Path

# For testing we may want to have multiple BIN directories. Look at where the script was called from for the "right" helper scripts.
$Global:BinDir = "$Home\Scripts"

$ExitCode = 9

#--------------------------------------------------------------------------------------------------------------------------------
# Exit the script in a controlled way
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


if ((sp-admin) -eq $False) {
	write-host -foregroundcolor "Red" "`n${Scriptname}: Error: You must have Administrator rights to run this script`n"
	Exit_Script 5 1
} else {
	if ($Global:CustomerRoutes.count -eq 0) {
		write-host -foregroundcolor "Green" "`n$Scriptname : No routes to add from Global:CustomerRoutes`n"
	} else {
		foreach ($Route in $Global:CustomerRoutes) {
			write-host -foregroundcolor "Green" "$Scriptname : Running:" route $Route.split(' ')
			route $Route.split(' ')
			$ExitStatus = $LASTEXITCODE
		}
	}
}

Exit_Script 0 0