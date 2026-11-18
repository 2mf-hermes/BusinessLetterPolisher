# 商業信件潤飾工具

使用自己提供的 AI API，整理商業信件的語氣、結構與用字。API Key 和使用紀錄保存在本機。

![商業信件潤飾工具介面預覽](Screenshot/Shot_tw.png)

**語言：** 繁體中文 ｜ [簡體中文](README.zh-CN.md) ｜ [English](README.en.md)

## 下載與啟動

適用於 Windows 10／11（64 位元）。

從 [Releases](https://github.com/2mf-hermes/BusinessLetterPolisher/releases) 下載 ZIP，解壓縮後執行 `商業信件潤飾工具.exe`。

有兩種版本：

- `BusinessLetterPolisher.zip`：精簡版，需要電腦已安裝 WebView2 Runtime。
- `BusinessLetterPolisher-full-<version>.zip`：完整版，內含 WebView2 Runtime，適合沒有安裝 Runtime 的電腦。

第一次啟動會顯示設定引導。也可以直接執行 `SetupWizard.exe` 安裝。

## 使用方式

1. 開啟右上角齒輪，進入設定。
2. 在 **AI 供應商** 中選擇供應商，或新增一組設定。
3. 輸入 API URL 和 API Key；按 **載入模型** 後，可從清單選擇模型，也可以手動輸入。
4. 按 **測試連線**，確認可用後儲存。
5. 在左側輸入信件，選擇信件語言、語言地區、結果語言、結果地區、潤飾風格與信件用途。
6. 按 **開始潤飾**。

### 語言欄位怎麼分工

- **信件語言**：原始信件使用的語言。
- **原始信件語言地區**：原始信件採用的地區用字、拼寫與商務習慣。
- **結果顯示語言**：潤飾結果要使用的語言。
- **結果語言地區**：潤飾結果採用的地區用字、拼寫與商務習慣。

修改建議會使用信件語言回答；程式會要求模型只回傳潤飾後的信件，並把修改建議分開顯示。

## 功能

手邊沒有草稿時，可以按「載入範例」試用。結果可與原文並排比較；工具列可切換淺色和深色。

- 儲存多組 AI 供應商，從下拉選單切換。
- 支援 OpenAI 相容、Anthropic 與 Gemini API 格式。
- 支援繁體中文、簡體中文與 English；工具列和下拉選單會一起切換語言。
- 內建潤飾風格與信件用途，也能自訂內容。
- 可選擇潤飾完整信件或只潤飾正文。
- 複製、下載結果，或以結果再次潤飾。
- 保存歷史紀錄、快速設定與個人偏好。
- 視窗會依螢幕可用空間調整大小。

## 更新

在設定裡按「檢查更新」。確認安裝後，程式會顯示下載進度，解壓縮完成後由更新程式替換檔案並重新啟動。手動更新時請保留執行檔旁的 `user_data/` 和 `runtime/`（完整版才有）。

## 資料與 API

API Key、偏好與紀錄存在 WebView2 的本機 `localStorage`，其資料目錄是 `user_data/`。點擊潤飾時，信件內容會送到你設定的 API 端點；請先確認該服務如何處理信件資料。

## 原始碼與打包

- [`App.cs`](App.cs)：WebView2 視窗和更新流程。
- [`letter-polisher.html`](letter-polisher.html)：介面和 API 呼叫。
- [`version.json`](version.json)：線上更新用的版本、下載網址和三語更新說明；不在發行 ZIP 裡。
- [`release-package.ps1`](release-package.ps1)：建立精簡版和完整版 ZIP，輸出至專案上一層的 `dist/`。

## 從原始碼編譯

需要 Windows 內建的 .NET Framework 4.x，以及 Microsoft WebView2 套件。編譯主程式：

```powershell
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:winexe /win32icon:icon.ico /out:商業信件潤飾工具.exe /reference:Microsoft.Web.WebView2.Core.dll /reference:Microsoft.Web.WebView2.WinForms.dll /reference:System.IO.Compression.dll /reference:System.IO.Compression.FileSystem.dll App.cs
```

變更 `App.cs` 後，發行前請重新編譯並掃描 EXE。只改前端或文件不必重編。

產生發行包：

```powershell
powershell -ExecutionPolicy Bypass -File release-package.ps1
```

## 使用條款

本專案供個人使用。使用任何 AI 服務前，請確認該服務的使用條款。
