# ============================================================
#  產出 GitHub Release 所需的兩個發行包
#  精簡版: BusinessLetterPolisher.zip (不含 runtime，供 latest/download/)
#  完整版: BusinessLetterPolisher-full-<version>.zip (含 runtime)
# ============================================================
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'

$srcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$versionFile = Join-Path $srcDir "version.json"
if (-not (Test-Path $versionFile)) { throw "version.json not found: $versionFile" }
$versionInfo = Get-Content -Raw -Encoding UTF8 $versionFile | ConvertFrom-Json
$version = [string]$versionInfo.version
if (-not $version -or $version.Trim().Length -eq 0) { throw "version.json does not contain a valid version" }
$distDir = Join-Path (Split-Path -Parent $srcDir) "dist"
New-Item -ItemType Directory -Path $distDir -Force | Out-Null

# 精簡版要包含的檔案（不含 runtime）
$liteFiles = @(
    "商業信件潤飾工具.exe",
    "商業信件潤飾工具.exe.config",
    "letter-polisher.html",
    "icon.ico",
    "WebView2Loader.dll",
    "Microsoft.Web.WebView2.Core.dll",
    "Microsoft.Web.WebView2.WinForms.dll",
    "README.md",
    "setup.bat",
    "setup.ps1",
    "SetupWizard.exe"
)

function New-Stage {
    param($name)
    $s = Join-Path $distDir $name
    if (Test-Path $s) { Remove-Item $s -Recurse -Force }
    New-Item -ItemType Directory -Path $s -Force | Out-Null
    return $s
}

function Copy-LiteFiles {
    param($stage)
    $ok = 0; $miss = 0
    foreach ($f in $liteFiles) {
        $src = Join-Path $srcDir $f
        if (Test-Path $src) {
            Copy-Item $src $stage
            $ok++
        } else {
            Write-Host ("    [x] missing: " + $f) -ForegroundColor Yellow
            $miss++
        }
    }
    Write-Host ("    copied $ok files ($miss missing)") -ForegroundColor Gray
}

Write-Host "`n=== 1/2 產出精簡版 (BusinessLetterPolisher.zip) ===" -ForegroundColor Cyan
$liteStage = New-Stage "stage_lite"
Copy-LiteFiles $liteStage
$liteZip = Join-Path $distDir "BusinessLetterPolisher.zip"
if (Test-Path $liteZip) { Remove-Item $liteZip -Force }
Compress-Archive -Path (Join-Path $liteStage "*") -DestinationPath $liteZip -Force
Remove-Item $liteStage -Recurse -Force
$liteMB = [math]::Round((Get-Item $liteZip).Length/1MB, 2)
Write-Host ("  完成: $liteZip  ($liteMB MB)") -ForegroundColor Green

Write-Host "`n=== 2/2 產出完整版 (BusinessLetterPolisher-full-$version.zip) ===" -ForegroundColor Cyan
$fullStage = New-Stage "stage_full"
Copy-LiteFiles $fullStage
# 複製 runtime（WebView2 執行環境）
if (Test-Path (Join-Path $srcDir "runtime")) {
    Write-Host "    複製 runtime/ ..." -ForegroundColor Yellow
    Copy-Item (Join-Path $srcDir "runtime") (Join-Path $fullStage "runtime") -Recurse
}
$fullZip = Join-Path $distDir "BusinessLetterPolisher-full-$version.zip"
if (Test-Path $fullZip) { Remove-Item $fullZip -Force }
Compress-Archive -Path (Join-Path $fullStage "*") -DestinationPath $fullZip -Force
Remove-Item $fullStage -Recurse -Force
$fullMB = [math]::Round((Get-Item $fullZip).Length/1MB, 2)
Write-Host ("  完成: $fullZip  ($fullMB MB)") -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  精簡版: $liteMB MB" -ForegroundColor White
Write-Host "  完整版: $fullMB MB" -ForegroundColor White
Write-Host "  輸出目錄: $distDir" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
