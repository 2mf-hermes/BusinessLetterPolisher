# 驗證精簡包內容：解壓後確認主程式 HTML 是本次版本，且新功能符號齊全。
$ErrorActionPreference = 'Stop'
$srcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $srcDir
$zip = Join-Path $root 'dist\BusinessLetterPolisher.zip'
$ver = (Get-Content -Raw -Encoding UTF8 (Join-Path $srcDir 'version.json') | ConvertFrom-Json).version
$tmp = Join-Path $env:TEMP ('zipcheck_' + [guid]::NewGuid().ToString('N'))
Expand-Archive -Path $zip -DestinationPath $tmp -Force

Write-Host "--- zip contents ---"
Get-ChildItem -Path $tmp -Recurse -File | ForEach-Object {
  Write-Host ("  {0}  ({1} bytes)" -f $_.FullName.Substring($tmp.Length + 1), $_.Length)
}

$htmlIn = Join-Path $tmp 'letter-polisher.html'
$htmlSrc = Join-Path $srcDir 'letter-polisher.html'
Write-Host ''
Write-Host ("expected version : {0}" -f $ver)
Write-Host ("html hash match  : {0}" -f ((Get-FileHash $htmlIn).Hash -eq (Get-FileHash $htmlSrc).Hash))

$h = Get-Content -Raw -Encoding UTF8 $htmlIn
$checks = @{
  'APP_VERSION is this release' = $h.Contains("var APP_VERSION='$ver';")
  'provider picker present'     = $h.Contains('id="provCS"')
  'provider dropdown list'      = $h.Contains('id="provDD"')
  'provider name field'         = $h.Contains('id="provName"')
  'add/delete provider actions' = ($h.Contains('function newProvider()') -and $h.Contains('function deleteProvider()'))
  'model loader button'         = $h.Contains('id="loadModelsBtn"')
  'model dropdown list'         = $h.Contains('id="modelDD"')
  'model list fetch'            = $h.Contains('function fetchModelList()')
  'models endpoint per format'  = $h.Contains('function modelsUrlFor(')
  'legacy settings migration'   = $h.Contains('function loadProviders()')
  'i18n aiProvider x3'          = (([regex]::Matches($h, 'aiProvider:')).Count -eq 3)
  'i18n loadModels x3'          = (([regex]::Matches($h, 'loadModels:')).Count -eq 3)
  'old single-endpoint gone'    = (-not $h.Contains('data-i="apiEndpoint"'))
  'update fix still present'    = $h.Contains('function armUpdWatchdog(')
}
$bad = 0
foreach ($k in $checks.Keys) {
  $ok = $checks[$k]
  if (-not $ok) { $bad++ }
  Write-Host ("  {0} {1}" -f $(if ($ok) { 'OK  ' } else { 'MISS' }), $k)
}

# The updater lives in the exe, so check the packaged exe itself: it must be the
# freshly built one, and its UTF-16 string heap must carry the fixed template.
$exeName = '商業信件潤飾工具.exe'
$exeIn = Join-Path $tmp $exeName
$exeSrc = Join-Path $srcDir $exeName
Write-Host ''
Write-Host ("exe hash match   : {0}" -f ((Get-FileHash $exeIn).Hash -eq (Get-FileHash $exeSrc).Hash))
$bytes = [IO.File]::ReadAllBytes($exeIn)
function Test-Utf16String {
  param([byte[]]$data, [string]$needle)
  foreach ($off in 0, 1) {
    $len = $data.Length - $off
    if ($len -le 0) { continue }
    $s = [Text.Encoding]::Unicode.GetString($data, $off, $len - ($len % 2))
    if ($s.Contains($needle)) { return $true }
  }
  return $false
}
$exeChecks = [ordered]@{
  'updater quoted-set TARGET'  = (Test-Utf16String $bytes 'set "TARGET=')
  'updater quoted-set SOURCE'  = (Test-Utf16String $bytes 'set "SOURCE=')
  'updater start is quoted'    = (Test-Utf16String $bytes 'start "" "%TARGET%\')
  'updater robocopy /IS'       = (Test-Utf16String $bytes '/E /IS /R:5 /W:1 /XD user_data runtime')
  'updater wait is bounded'    = (Test-Utf16String $bytes 'if %TRIES% GEQ 90 goto copy')
  'updater writes a log'       = (Test-Utf16String $bytes 'blp-update-log.txt')
  'old broken template gone'   = (-not (Test-Utf16String $bytes 'set TARGET="'))
}
foreach ($k in $exeChecks.Keys) {
  $ok = $exeChecks[$k]
  if (-not $ok) { $bad++ }
  Write-Host ("  {0} {1}" -f $(if ($ok) { 'OK  ' } else { 'MISS' }), $k)
}

Remove-Item $tmp -Recurse -Force
if ($bad -gt 0) { throw "$bad check(s) failed" }
Write-Host ''
Write-Host 'zip verification passed' -ForegroundColor Green
