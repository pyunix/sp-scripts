# Find Domainname
$junk, $Domain = (systeminfo |select-string "^domain:") -replace "\s+"," " -split' '

# List Domain Controllers for Domain
nltest /dclist:$Domain

# List Domain Trusts
nltest /domain_trusts

# Loop through each domain found on a server and list Domain Controllers
$Lines = (nltest /domain_trusts | select-string ': ') -replace "\s+"," "
foreach ($Line in $Lines) {
    $Domain = $Line -replace "\s+"," " -split' '
    nltest "/dclist:$($Domain[3])"
}