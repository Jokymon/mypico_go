Get-ChildItem .\mybot -Filter *.py |
ForEach-Object {
    mpremote.exe cp $_.FullName :
}