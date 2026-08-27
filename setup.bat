@echo off
REM ============================================================
REM  商業信件潤飾工具 - 首次執行環境設定 (WebView2 Runtime)
REM  Business Letter Polisher - WebView2 Runtime setup
REM ============================================================
setlocal

echo.
echo  ============================================
echo   商業信件潤飾工具 - 環境設定
echo   Business Letter Polisher - Setup
echo  ============================================
echo.

REM 檢查是否已安裝 WebView2 Runtime
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" >nul 2>&1
if %errorlevel%==0 (
    echo  [OK] WebView2 Runtime 已安裝。可直接啟動主程式。
    echo.
    goto :run
)

reg query "HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" >nul 2>&1
if %errorlevel%==0 (
    echo  [OK] WebView2 Runtime 已安裝。可直接啟動主程式。
    echo.
    goto :run
)

echo  [提示] 未偵測到 WebView2 Runtime。
echo  正在嘗試以本套件內含的安裝程式進行安裝...
echo.

if exist "%~dp0SetupWizard.exe" (
    echo  啟動 WebView2 安裝精靈...
    start /wait "" "%~dp0SetupWizard.exe"
    goto :run
)

echo  未找到內建安裝精靈。改以官方線上安裝程式下載...
echo.
set "BOOTSTRAP=%~dp0MicrosoftEdgeWebView2Setup.exe"
if not exist "%BOOTSTRAP%" (
    echo  下載 WebView2 Evergreen Bootstrapper...
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://go.microsoft.com/fwlink/p/?LinkId=2124703' -OutFile '%BOOTSTRAP%'"
)
if exist "%BOOTSTRAP%" (
    echo  執行安裝程式...
    start /wait "" "%BOOTSTRAP%"
) else (
    echo  [錯誤] 無法取得 WebView2 安裝程式。
    echo  請手動至 https://developer.microsoft.com/microsoft-edge/webview2/ 下載安裝。
    pause
    exit /b 1
)

:run
echo.
echo  [完成] 環境就緒，正在啟動 商業信件潤飾工具...
echo.
start "" "%~dp0商業信件潤飾工具.exe"
endlocal
exit /b 0