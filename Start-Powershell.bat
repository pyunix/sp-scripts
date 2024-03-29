@echo off
:: ###############################################################################
:: # Powershell script: Start-powershell.bat
:: # Author: Warren Dempsey
:: # Company: OSS Group NZ
:: #
:: # Modification History:
:: # 20220717WD - Create first version
:: #
:: # Usage: Start-Powershell.bat
:: #
:: # Description:
:: # Run this script to 
:: # Set and execution policy that lets us run powershell scripts off a file share (A.K.A P:\  )
:: ###############################################################################

:: #----------------------------------------------------------------------------------------------------------------------------------
powershell.exe -executionpolicy ByPass

