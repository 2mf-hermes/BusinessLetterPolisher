# 商业信件润饰工具

使用自己提供的 AI API，整理商务信件的语气、结构和用词。API Key 与使用记录保存在本地。

![商业信件润饰工具界面预览](Screenshot/Shot_cn.png)

**语言：** [繁體中文](README.md) ｜ 简体中文 ｜ [English](README.en.md)

## 下载与启动

适用于 Windows 10/11（64 位）。

从 [Releases](https://github.com/2mf-hermes/BusinessLetterPolisher/releases) 下载 ZIP，解压后运行 `商業信件潤飾工具.exe`。

有两个版本：

- `BusinessLetterPolisher.zip`：精简版，需要电脑已安装 WebView2 Runtime。
- `BusinessLetterPolisher-full-<version>.zip`：完整版，包含 WebView2 Runtime，适合没有安装 Runtime 的电脑。

第一次启动会显示设置引导，也可以直接运行 `SetupWizard.exe` 安装。

## 使用方法

1. 点击右上角齿轮，打开设置。
2. 在 **AI 供应商** 中选择供应商，或新增一组设置。
3. 输入 API URL 和 API Key；点击 **载入模型** 后，可从列表选择模型，也可以手动输入。
4. 点击 **测试连接**，确认可用后保存。
5. 在左侧输入信件，选择信件语言、语言地区、结果语言、结果地区、润饰风格和信件用途。
6. 点击 **开始润饰**。

### 语言字段的区别

- **信件语言**：原始信件使用的语言。
- **原始信件语言地区**：原始信件采用的地区用词、拼写和商务习惯。
- **结果显示语言**：润饰结果使用的语言。
- **结果语言地区**：润饰结果采用的地区用词、拼写和商务习惯。

修改建议会使用信件语言回答；程序会要求模型只返回润饰后的信件，并单独显示修改建议。

## 功能

手头没有草稿时，可以点击“载入范例”试用。结果可与原文并排比较；工具栏可切换浅色和深色。

- 保存多组 AI 供应商，从下拉列表切换。
- 支持 OpenAI 兼容、Anthropic 和 Gemini API 格式。
- 支持繁体中文、简体中文和 English；工具栏与下拉列表会一起切换语言。
- 提供润饰风格和信件用途，也可以自定义内容。
- 可选择润饰完整信件，或只润饰正文。
- 复制、下载结果，或使用结果再次润饰。
- 保存历史记录、快速设置和个人偏好。
- 窗口会根据屏幕可用空间调整大小。

## 更新

在设置里点击“检查更新”。确认安装后，程序会显示下载进度，解压完成后由更新程序替换文件并重启。手动更新时请保留可执行文件旁的 `user_data/` 和 `runtime/`（仅完整版包含后者）。

## 数据与 API

API Key、偏好和历史记录保存在 WebView2 的本地 `localStorage` 中，数据目录为 `user_data/`。点击润饰时，信件内容会发送至你配置的 API 端点；请先确认该服务如何处理信件数据。

## 源码与打包

- [`App.cs`](App.cs)：WebView2 窗口和更新流程。
- [`letter-polisher.html`](letter-polisher.html)：界面和 API 调用。
- [`version.json`](version.json)：在线更新用的版本、下载地址和三语更新说明；不在发行 ZIP 中。
- [`release-package.ps1`](release-package.ps1)：生成精简版和完整版 ZIP，输出至项目上一级的 `dist/`。

## 从源码编译

需要 Windows 内置的 .NET Framework 4.x，以及 Microsoft WebView2 包。编译主程序：

```powershell
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:winexe /win32icon:icon.ico /out:商業信件潤飾工具.exe /reference:Microsoft.Web.WebView2.Core.dll /reference:Microsoft.Web.WebView2.WinForms.dll /reference:System.IO.Compression.dll /reference:System.IO.Compression.FileSystem.dll App.cs
```

修改 `App.cs` 后，请在发布前重新编译并扫描 EXE。只改前端或文档不必重新编译。

生成发行包：

```powershell
powershell -ExecutionPolicy Bypass -File release-package.ps1
```

## 使用条款

本项目供个人使用。使用任何 AI 服务前，请确认该服务的使用条款。
