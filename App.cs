using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Web.WebView2.WinForms;

class App : Form
{
    WebView2 wv;
    System.Windows.Forms.Timer initTimer;
    static string logPath;
    bool updating;
    bool autoFitDone;

    public App()
    {
        try
        {
            string exeDir = Path.GetDirectoryName(Application.ExecutablePath);
            logPath = Path.Combine(exeDir, "crash.log");
            Log("=== App starting ===");

            string icoPath = Path.Combine(exeDir, "icon.ico");
            if (File.Exists(icoPath))
            {
                this.Icon = new Icon(icoPath);
                Log("Icon loaded");
            }
        }
        catch (Exception ex) { Log("Icon error: " + ex.Message); }

        this.Text = "\u5546\u696d\u4fe1\u4ef6\u6f64\u98fe\u5de5\u5177";
        // Start from a preferred size, but never larger than the screen's usable area.
        Rectangle startArea = Screen.PrimaryScreen.WorkingArea;
        this.MinimumSize = new Size(Math.Min(800, startArea.Width), Math.Min(600, startArea.Height));
        this.Size = new Size(Math.Min(1200, startArea.Width), Math.Min(800, startArea.Height));
        this.StartPosition = FormStartPosition.CenterScreen;

        wv = new WebView2();
        wv.Dock = DockStyle.Fill;
        wv.Visible = false;
        this.Controls.Add(wv);
        Log("WebView2 created");

        initTimer = new System.Windows.Forms.Timer();
        initTimer.Interval = 100;
        initTimer.Tick += new EventHandler(OnInitTimer);
        initTimer.Start();
        Log("Constructor done, timer started");
    }

    void OnInitTimer(object sender, EventArgs e)
    {
        initTimer.Stop();
        initTimer.Dispose();
        Log("Timer fired, starting WebView2 init");
        StartInit();
    }

    async void StartInit()
    {
        try
        {
            string exeDir = Path.GetDirectoryName(Application.ExecutablePath);
            string runtimePath = Path.Combine(exeDir, "runtime");
            string userDataPath = Path.Combine(exeDir, "user_data");
            if (!Directory.Exists(userDataPath))
                Directory.CreateDirectory(userDataPath);

            Log("runtime=" + runtimePath + " exists=" + Directory.Exists(runtimePath));

            var env = await Microsoft.Web.WebView2.Core.CoreWebView2Environment.CreateAsync(
                browserExecutableFolder: runtimePath,
                userDataFolder: userDataPath,
                options: null);
            Log("Environment OK");

            await wv.EnsureCoreWebView2Async(env);
            Log("CoreWebView2 initialized OK");

            // Capture JS console errors
            wv.CoreWebView2.WebMessageReceived += (s, e2) =>
            {
                string payload = ReadWebMessage(e2);
                Log("JS msg: " + payload);
                try
                {
                    if (payload != null &&
                        payload.IndexOf("installUpdate", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        string url = ExtractJsonString(payload, "url");
                        Log("installUpdate requested, url=" + (url ?? "<none>"));
                        // Acknowledge immediately so the page knows the host is alive.
                        ReportUpdate("preparing", -1, "");
                        if (!string.IsNullOrWhiteSpace(url))
                            BeginInvoke(new Action(async () => await InstallUpdateAsync(url)));
                        else
                        {
                            Log("ERROR: no download url in message");
                            ReportUpdate("error", 0, "\u66f4\u65b0\u7db2\u5740\u7121\u6cd5\u89e3\u6790");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Log("WebMessage error: " + ex);
                    ReportUpdate("error", 0, ex.Message);
                }
            };

            // Expose the flag before page scripts run, so it survives reloads too.
            await wv.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync(
                "window.hostUpdateSupported=true;");

            wv.CoreWebView2.DOMContentLoaded += (s, e2) =>
            {
                Log("DOMContentLoaded OK");
                RunScript("window.hostUpdateSupported=true;window.dispatchEvent(new Event('hostready'))");
                BeginInvoke(new Action(async () => await ResizeToContentAsync()));
            };

            string htmlPath = Path.Combine(exeDir, "letter-polisher.html");
            Log("html=" + htmlPath + " exists=" + File.Exists(htmlPath));

            if (File.Exists(htmlPath))
            {
                wv.CoreWebView2.Navigate("file:///" + htmlPath.Replace("\\", "/"));
                Log("Navigate OK");
            }
            else
            {
                Log("ERROR: letter-polisher.html not found!");
                MessageBox.Show("letter-polisher.html not found in " + exeDir,
                    "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

            wv.Visible = true;
        }
        catch (Exception ex)
        {
            Log("FATAL: " + ex.ToString());
            MessageBox.Show("WebView2 \u521d\u59cb\u5316\u5931\u6557\uFF1A" + ex.Message,
                "\u932f\u8aa4", MessageBoxButtons.OK, MessageBoxIcon.Error);
            Application.Exit();
        }
    }

    // Fits the window to the page's natural content size on first load:
    // if the screen has room, show everything; otherwise cap at the usable area.
    async Task ResizeToContentAsync()
    {
        if (autoFitDone) return;
        try
        {
            // Give the page a moment to finish layout (fonts, custom dropdowns).
            await Task.Delay(150);
            if (wv == null || wv.CoreWebView2 == null) return;
            autoFitDone = true;

            double scale = 1.0;
            using (var g = CreateGraphics()) scale = g.DpiX / 96.0;
            if (scale <= 0) scale = 1.0;

            Rectangle area = Screen.FromControl(this).WorkingArea;
            int chromeW = Math.Max(0, Width - ClientSize.Width);
            int chromeH = Math.Max(0, Height - ClientSize.Height);

            // Step 1: the layout's natural width comes from the container's max-width
            // plus its horizontal padding, since body.scrollWidth only ever reports
            // the viewport width while the content still fits.
            double idealCssW = await MeasureAsync(
                "(function(){var w=document.querySelector('.wrap');" +
                "if(!w)return document.documentElement.scrollWidth;" +
                "var s=getComputedStyle(w);" +
                "var mx=parseFloat(s.maxWidth);if(!isFinite(mx))mx=w.scrollWidth;" +
                "var pad=parseFloat(s.paddingLeft)+parseFloat(s.paddingRight);" +
                "return Math.ceil(Math.max(mx+pad,document.documentElement.scrollWidth));})()");

            if (idealCssW > 0)
            {
                int wantW = (int)Math.Ceiling(idealCssW * scale) + chromeW;
                int targetW = Math.Min(area.Width, Math.Max(MinimumSize.Width, wantW));
                if (targetW != Width) Width = targetW;
            }

            // Step 2: height must be measured after the width settles, because a
            // narrower window reflows the two-column rows into one.
            await Task.Delay(120);
            double cssH = await MeasureAsync(
                "(function(){var b=document.body,e=document.documentElement;" +
                "return Math.ceil(Math.max(b.scrollHeight,e.scrollHeight,b.offsetHeight,e.offsetHeight));})()");

            if (cssH > 0)
            {
                int wantH = (int)Math.Ceiling(cssH * scale) + chromeH;
                int targetH = Math.Min(area.Height, Math.Max(MinimumSize.Height, wantH));
                if (targetH != Height) Height = targetH;

                // Content taller than the screen keeps a vertical scrollbar; widen a
                // little so it does not overlap the layout.
                if (wantH > targetH && Width < area.Width)
                    Width = Math.Min(area.Width, Width + SystemInformation.VerticalScrollBarWidth);
            }

            // Keep the window fully inside the usable area after resizing.
            int left = Math.Max(area.Left, Math.Min(area.Left + (area.Width - Width) / 2, area.Right - Width));
            int top = Math.Max(area.Top, Math.Min(area.Top + (area.Height - Height) / 2, area.Bottom - Height));
            Location = new Point(left, top);

            Log("Auto fit: window=" + Width + "x" + Height +
                " screen=" + area.Width + "x" + area.Height +
                " scale=" + scale.ToString("0.00"));
        }
        catch (Exception ex) { Log("Auto resize error: " + ex.Message); }
    }

    async Task<double> MeasureAsync(string script)
    {
        try
        {
            string raw = await wv.CoreWebView2.ExecuteScriptAsync(script);
            if (string.IsNullOrEmpty(raw)) return 0;
            double value;
            if (double.TryParse(raw.Trim('"'), System.Globalization.NumberStyles.Float,
                System.Globalization.CultureInfo.InvariantCulture, out value)) return value;
        }
        catch (Exception ex) { Log("Measure error: " + ex.Message); }
        return 0;
    }

    // The page posts a JSON *string* via chrome.webview.postMessage(JSON.stringify(...)).
    // For a string message, WebMessageAsJson returns that string JSON-encoded again --
    // quotes become \" and slashes \/ -- so matching against it fails. Prefer the raw
    // string and fall back to unescaping the JSON form.
    static string ReadWebMessage(Microsoft.Web.WebView2.Core.CoreWebView2WebMessageReceivedEventArgs e)
    {
        try
        {
            string s = e.TryGetWebMessageAsString();
            if (!string.IsNullOrEmpty(s)) return s;
        }
        catch { }
        try
        {
            string json = e.WebMessageAsJson;
            if (string.IsNullOrEmpty(json)) return null;
            if (json.Length >= 2 && json[0] == '"' && json[json.Length - 1] == '"')
                return UnescapeJsonString(json.Substring(1, json.Length - 2));
            return json;
        }
        catch { return null; }
    }

    static string UnescapeJsonString(string value)
    {
        var sb = new System.Text.StringBuilder(value.Length);
        for (int i = 0; i < value.Length; i++)
        {
            char c = value[i];
            if (c != '\\' || i + 1 >= value.Length) { sb.Append(c); continue; }
            char n = value[++i];
            switch (n)
            {
                case 'n': sb.Append('\n'); break;
                case 'r': sb.Append('\r'); break;
                case 't': sb.Append('\t'); break;
                case 'b': sb.Append('\b'); break;
                case 'f': sb.Append('\f'); break;
                case 'u':
                    if (i + 4 < value.Length)
                    {
                        int code;
                        if (int.TryParse(value.Substring(i + 1, 4), System.Globalization.NumberStyles.HexNumber,
                            System.Globalization.CultureInfo.InvariantCulture, out code))
                        {
                            sb.Append((char)code);
                            i += 4;
                            break;
                        }
                    }
                    sb.Append(n);
                    break;
                default: sb.Append(n); break;
            }
        }
        return sb.ToString();
    }

    static string ExtractJsonString(string json, string key)
    {
        string marker = "\"" + key + "\":\"";
        int start = json.IndexOf(marker, StringComparison.OrdinalIgnoreCase);
        if (start < 0) return null;
        start += marker.Length;
        int end = json.IndexOf('\"', start);
        if (end < 0) return null;
        return json.Substring(start, end - start).Replace("\\/", "/");
    }

    async Task InstallUpdateAsync(string url)
    {
        if (updating) { Log("Update already in progress; ignored"); return; }
        updating = true;
        string exeDir = Path.GetDirectoryName(Application.ExecutablePath);
        string tempRoot = Path.Combine(Path.GetTempPath(), "BusinessLetterPolisherUpdate_" + Guid.NewGuid().ToString("N"));
        string zipPath = Path.Combine(tempRoot, "update.zip");
        string extractDir = Path.Combine(tempRoot, "payload");
        string scriptPath = Path.Combine(Path.GetTempPath(), "apply-update-" + Guid.NewGuid().ToString("N") + ".cmd");
        try
        {
            Directory.CreateDirectory(tempRoot);
            Directory.CreateDirectory(extractDir);
            Log("Downloading update: " + url);
            ReportUpdate("downloading", 0, "");
            await DownloadWithProgressAsync(url, zipPath);
            Log("Download completed: " + zipPath + " bytes=" + new FileInfo(zipPath).Length);

            ReportUpdate("extracting", 100, "");
            ZipFile.ExtractToDirectory(zipPath, extractDir);
            Log("Update package extracted: " + extractDir);

            string payloadDir = ResolvePayloadRoot(extractDir);
            Log("Payload root: " + payloadDir);

            ReportUpdate("installing", 100, "");
            string exeName = Path.GetFileName(Application.ExecutablePath);
            string script = "@echo off\r\n" +
                "setlocal\r\n" +
                "set TARGET=" + Quote(exeDir) + "\r\n" +
                "set SOURCE=" + Quote(payloadDir) + "\r\n" +
                "set PID=" + Process.GetCurrentProcess().Id + "\r\n" +
                ":wait\r\n" +
                "tasklist /FI \"PID eq %PID%\" 2>NUL | find \"%PID%\" >NUL\r\n" +
                "if not errorlevel 1 (timeout /t 1 /nobreak >NUL & goto wait)\r\n" +
                "robocopy \"%SOURCE%\" \"%TARGET%\" /E /R:3 /W:1 /XD user_data runtime >NUL\r\n" +
                "start \"\" \"%TARGET%\\" + exeName + "\"\r\n" +
                "rmdir /s /q " + Quote(tempRoot) + "\r\n" +
                "del /q \"%~f0\"\r\n";
            File.WriteAllText(scriptPath, script, System.Text.Encoding.Default);
            Process.Start(new ProcessStartInfo(scriptPath) { UseShellExecute = true, WindowStyle = ProcessWindowStyle.Hidden });
            Log("Update staged; updater launched");
            ReportUpdate("restarting", 100, "");
            await Task.Delay(1200);
            Log("Exiting for replacement");
            Application.Exit();
        }
        catch (Exception ex)
        {
            updating = false;
            Log("Update failed: " + ex);
            ReportUpdate("error", 0, ex.Message);
            try { if (Directory.Exists(tempRoot)) Directory.Delete(tempRoot, true); } catch { }
            try { if (File.Exists(scriptPath)) File.Delete(scriptPath); } catch { }
        }
    }

    // Streams the package to disk while reporting progress back to the page.
    // Cache is bypassed so an updated asset is never served from a stale copy.
    async Task DownloadWithProgressAsync(string url, string destPath)
    {
        try { ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072 | (SecurityProtocolType)768; }
        catch { }
        string requestUrl = url + (url.IndexOf('?') >= 0 ? "&" : "?") + "_ts=" + DateTime.UtcNow.Ticks;
        var req = (HttpWebRequest)WebRequest.Create(requestUrl);
        req.Method = "GET";
        req.UserAgent = "BusinessLetterPolisher-Updater";
        req.AllowAutoRedirect = true;
        req.CachePolicy = new System.Net.Cache.RequestCachePolicy(System.Net.Cache.RequestCacheLevel.NoCacheNoStore);
        req.Headers["Cache-Control"] = "no-cache";
        req.Headers["Pragma"] = "no-cache";
        req.Timeout = 60000;
        req.ReadWriteTimeout = 120000;

        using (var resp = (HttpWebResponse)await req.GetResponseAsync())
        using (var input = resp.GetResponseStream())
        using (var output = new FileStream(destPath, FileMode.Create, FileAccess.Write, FileShare.None, 81920))
        {
            long total = resp.ContentLength;
            long done = 0;
            int lastPct = -1;
            var lastTick = DateTime.UtcNow;
            byte[] buffer = new byte[81920];
            int read;
            while ((read = await input.ReadAsync(buffer, 0, buffer.Length)) > 0)
            {
                await output.WriteAsync(buffer, 0, read);
                done += read;
                int pct = total > 0 ? (int)(done * 100 / total) : -1;
                if (pct != lastPct || (DateTime.UtcNow - lastTick).TotalMilliseconds > 400)
                {
                    lastPct = pct;
                    lastTick = DateTime.UtcNow;
                    ReportUpdate("downloading", pct, FormatBytes(done) + (total > 0 ? " / " + FormatBytes(total) : ""));
                }
            }
        }
    }

    // A release zip may wrap everything in a single top-level folder.
    static string ResolvePayloadRoot(string extractDir)
    {
        var files = Directory.GetFiles(extractDir);
        var dirs = Directory.GetDirectories(extractDir);
        if (files.Length == 0 && dirs.Length == 1) return ResolvePayloadRoot(dirs[0]);
        return extractDir;
    }

    static string FormatBytes(long bytes)
    {
        if (bytes >= 1048576) return (bytes / 1048576.0).ToString("0.0") + " MB";
        if (bytes >= 1024) return (bytes / 1024.0).ToString("0") + " KB";
        return bytes + " B";
    }

    void ReportUpdate(string state, int percent, string detail)
    {
        try
        {
            if (wv == null || wv.CoreWebView2 == null) return;
            string script = "window.hostUpdateProgress&&window.hostUpdateProgress(" +
                JsString(state) + "," + percent + "," + JsString(detail ?? "") + ")";
            if (InvokeRequired) BeginInvoke(new Action(() => RunScript(script)));
            else RunScript(script);
        }
        catch (Exception ex) { Log("ReportUpdate error: " + ex.Message); }
    }

    void RunScript(string script)
    {
        try { var ignored = wv.CoreWebView2.ExecuteScriptAsync(script); }
        catch (Exception ex) { Log("RunScript error: " + ex.Message); }
    }

    static string JsString(string value)
    {
        var sb = new System.Text.StringBuilder("\"");
        foreach (char c in value ?? "")
        {
            if (c == '"' || c == '\\') sb.Append('\\').Append(c);
            else if (c == '\n') sb.Append("\\n");
            else if (c == '\r') sb.Append("\\r");
            else if (c < ' ') sb.Append("\\u").Append(((int)c).ToString("x4"));
            else sb.Append(c);
        }
        return sb.Append('"').ToString();
    }

    static string Quote(string value)
    {
        return "\"" + value.Replace("\"", "\"\"") + "\"";
    }

    protected override void OnFormClosing(FormClosingEventArgs e)
    {
        Log("FormClosing");
        base.OnFormClosing(e);
        Log("Main() end");
    }

    static void Log(string msg)
    {
        try
        {
            string line = DateTime.Now.ToString("HH:mm:ss.fff") + " " + msg + "\n";
            File.AppendAllText(logPath, line, System.Text.Encoding.UTF8);
        }
        catch { }
    }

    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new App());
    }
}
