# ============================================================
#  商業信件潤飾工具 - 首次執行環境設定 (WebView2 Runtime)
#  Business Letter Polisher - WebView2 Runtime setup
# ============================================================
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host "   商業信件潤飾工具 - 環境設定" -ForegroundColor Cyan
Write-Host "   Business Letter Polisher - Setup" -ForegroundColor Cyan
Write-Host "  ============================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$clsid = '{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}'

# 檢查 WebView2 Runtime 是否已安裝
function Test-WebView2Installed {
    $paths = @(
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\$clsid",
        "HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\$clsid"
    )
    foreach ($p in $paths) {
        if (Test-Path $p) { return $true }
    }
    return $false
}

if (Test-WebView2Installed) {
    Write-Host "  [OK] WebView2 Runtime 已安裝，可直接啟動主程式。" -ForegroundColor Green
} else {
    Write-Host "  [提示] 未偵測到 WebView2 Runtime，開始安裝..." -ForegroundColor Yellow

    $wizard = Join-Path $scriptDir "SetupWizard.exe"
    if (Test-Path $wizard) {
        Write-Host "  執行內建安裝精靈..." -ForegroundColor Yellow
        $p = Start-Process -FilePath $wizard -Wait -PassThru
    } else {
        Write-Host "  改以下載官方線上安裝程式..." -ForegroundColor Yellow
        $bootstrapper = Join-Path $scriptDir "MicrosoftEdgeWebView2Setup.exe"

        if (-not (Test-Path $bootstrapper)) {
            Write-Host "  下載 WebView2 Evergreen Bootstrapper..." -ForegroundColor Yellow
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri 'https://go.microsoft.com/fwlink/p/?LinkId=2124703' -OutFile $bootstrapper
        }

        if (Test-Path $bootstrapper) {
            Write-Host "  執行安裝程式..." -ForegroundColor Yellow
            $p = Start-Process -FilePath $bootstrapper -Wait -PassThru
        } else {
            Write-Host "  [錯誤] 無法取得 WebView2 安裝程式。" -ForegroundColor Red
            Write-Host "  請手動至 https://developer.microsoft.com/microsoft-edge/webview2/ 下載安裝。" -ForegroundColor Red
            Read-Host "  按 Enter 結束"
            exit 1
        }
    }
}

Write-Host ""
Write-Host "  [完成] 環境就緒，正在啟動 商業信件潤飾工具..." -ForegroundColor Green
Write-Host ""

# 啟動主程式
$exe = Join-Path $scriptDir "商業信件潤飾工具.exe"
if (Test-Path $exe) {
    Start-Process -FilePath $exe
} else {
    Write-Host "  [錯誤] 找不到主程式 $exe" -ForegroundColor Red
    exit 1
}