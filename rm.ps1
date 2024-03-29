#--------------------------------------------------------------------------------------------------------------------------------
# Powershell script: touch.ps1
# Author: Warren Dempsey
# Company OSS Group NZ
#
# Modification History:
# 20230626 WD - Initial version
#
# Usage: Emulate the functionality of Unix touch (SO we can use it in Makefiles)

param(
	[Parameter(Position=1, ValueFromRemainingArguments)]
	[string[]]$Remaining
)
	
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

foreach ($File in $Remaining) {
	if (test-path $File) {
		#write-host "$file file exists, updating lastwritetime"
		remove-Item $File
	}
}


