# 打包發行版 / Build Distribution Package
# 執行此腳本將建立可分發的 ZIP 檔案

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$srcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$outputDir = Join-Path (Split-Path -Parent $srcDir) "dist"

# Version from date
$version = Get-Date -Format "yyyy.MM.dd"
$zipName = "BusinessLetterPolisher-v$version.zip"
$zipPath = Join-Path $outputDir $zipName
$stageDir = Join-Path $outputDir "stage_$version"

Write-Host ""
Write-Host "  打包商業信件潤飾工具 v$version" -ForegroundColor Cyan
Write-Host ""

# Clean
if (Test-Path $stageDir) { Remove-Item $stageDir -Recurse -Force }
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
New-Item -ItemType Directory -Path $stageDir -Force | Out-Null

# Files to include
$files = @(
    "商業信件潤飾工具.exe",
    "商業信件潤飾工具.exe.config",
    "letter-polisher.html",
    "icon.ico",
    "WebView2Loader.dll",
    "Microsoft.Web.WebView2.Core.dll",
    "Microsoft.Web.WebView2.WinForms.dll",
    "README.md",
    "setup.bat",
    "setup.ps1"
)

# Copy files
Write-Host "  複製檔案..." -ForegroundColor Yellow
foreach ($file in $files) {
    $src = Join-Path $srcDir $file
    if (Test-Path $src) {
        Copy-Item $src $stageDir
        Write-Host "    ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "    ✗ $file (not found)" -ForegroundColor Red
    }
}

# Copy runtime
if (Test-Path "$srcDir\runtime\*") {
    Write-Host "  複製 WebView2 Runtime..." -ForegroundColor Yellow
    Copy-Item "$srcDir\runtime" "$stageDir\runtime" -Recurse
    Write-Host "    ✓ runtime/" -ForegroundColor Green
}

# Create user_data placeholder
New-Item -ItemType Directory -Path "$stageDir\user_data" -Force | Out-Null

# Create version file
@"
app_name=商業信件潤飾工具
app_name_en=Business Letter Polisher
version=$version
release_date=$(Get-Date -Format 'yyyy-MM-dd')
min_app_version=1.0.0
"@ | Out-File -FilePath "$stageDir\version.txt" -Encoding UTF8

Write-Host ""
Write-Host "  壓縮中..." -ForegroundColor Yellow
Compress-Archive -Path "$stageDir\*" -DestinationPath $zipPath -Force

# Cleanup stage
Remove-Item $stageDir -Recurse -Force

$zipSize = [math]::Round((Get-Item $zipPath).Length / 1MB, 1)
Write-Host ""
Write-Host "  ══════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✓ 打包完成！" -ForegroundColor Green
Write-Host "  檔案: $zipPath" -ForegroundColor White
Write-Host "  大小: $zipSize MB" -ForegroundColor White
Write-Host ""
