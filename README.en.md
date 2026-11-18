# Business Letter Polisher

A small desktop tool for polishing business letters with an AI API that you provide. API keys and history stay on the local machine.

![Business Letter Polisher interface preview](Screenshot/Shot_en.png)

**Language:** [繁體中文](README.md) ｜ [简体中文](README.zh-CN.md) ｜ English

## Download and start

Runs on 64-bit Windows 10 or 11.

Download a ZIP from [Releases](https://github.com/2mf-hermes/BusinessLetterPolisher/releases), extract it, and run `商業信件潤飾工具.exe`.

There are two packages:

- `BusinessLetterPolisher.zip`: lite package; WebView2 Runtime must already be installed.
- `BusinessLetterPolisher-full-<version>.zip`: full package with WebView2 Runtime included.

The first launch opens the setup guide. You can also run `SetupWizard.exe` directly.

## How to use

1. Click the gear icon in the top-right toolbar to open Settings.
2. Select a provider under **AI Provider**, or add one.
3. Enter the API URL and API key. Click **Load Models** to fetch a list, or enter a model name manually.
4. Click **Test Connection**, then save the provider.
5. Enter the letter on the left and choose its language, source region, result language, result region, tone and purpose.
6. Click **Polish**.

### What the language fields mean

- **Letter language**: the language of the source letter.
- **Source Language Region**: the spelling, wording and business conventions used by the source letter.
- **Output Language**: the language of the polished result.
- **Output Language Region**: the spelling, wording and business conventions to use in the result.

Revision notes use the letter language. The app asks the model to return the letter without a preamble and shows revision notes separately.

## Features

Click **Sample** if you don’t have a draft at hand. You can compare the result with the original and switch between light and dark themes from the toolbar.

- Save multiple AI providers and switch between them from a dropdown.
- OpenAI-compatible, Anthropic and Gemini API formats.
- Traditional Chinese, Simplified Chinese and English UI, including the toolbar and dropdowns.
- Built-in tones and letter purposes, plus custom text.
- Polish a complete letter or only its body.
- Copy or download the result, then polish it again if needed.
- History, quick setup and persistent preferences.
- Window size adapts to the available screen area.

## Updates

Open Settings and select **Check for Updates**. Once you confirm, the app shows download progress. After extraction, the updater replaces the files and restarts the app. If you update manually, leave `user_data/` and `runtime/` (full package only) next to the executable.

## Data and API requests

WebView2 stores API keys, preferences, and history in `localStorage`, under `user_data/`. When you polish a letter, the app sends its text to the API endpoint you configured. Check how that service handles your data before sending sensitive correspondence.

## Source and packaging

- [`App.cs`](App.cs): WebView2 window and updater.
- [`letter-polisher.html`](letter-polisher.html): interface and API calls.
- [`version.json`](version.json): version, download URL, and localized release notes for the updater. The release ZIPs do not include this file.
- [`release-package.ps1`](release-package.ps1): builds both ZIPs in `dist/`, one level above the project folder.

## Build from source

You need .NET Framework 4.x on Windows and the Microsoft WebView2 assemblies. Build the main application with:

```powershell
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:winexe /win32icon:icon.ico /out:商業信件潤飾工具.exe /reference:Microsoft.Web.WebView2.Core.dll /reference:Microsoft.Web.WebView2.WinForms.dll /reference:System.IO.Compression.dll /reference:System.IO.Compression.FileSystem.dll App.cs
```

After editing `App.cs`, rebuild and scan the EXE before publishing. Changes to the frontend or docs alone don’t need a rebuild.

Create the release packages with:

```powershell
powershell -ExecutionPolicy Bypass -File release-package.ps1
```

## Terms of use

This project is for personal use. Check the terms of service of the AI provider you use.
