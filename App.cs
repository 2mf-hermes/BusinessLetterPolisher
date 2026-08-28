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
        this.Size = new Size(1200, 800);
        this.StartPosition = FormStartPosition.CenterScreen;
        this.MinimumSize = new Size(800, 600);

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
                Log("JS msg: " + e2.WebMessageAsJson);
                try
                {
                    string json = e2.WebMessageAsJson;
                    if (json.IndexOf("\"installUpdate\"", StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        string url = ExtractJsonString(json, "url");
                        if (!string.IsNullOrWhiteSpace(url))
                            BeginInvoke(new Action(async () => await InstallUpdateAsync(url)));
                    }
                }
                catch (Exception ex) { Log("WebMessage error: " + ex); }
            };

            wv.CoreWebView2.DOMContentLoaded += (s, e2) =>
            {
                Log("DOMContentLoaded OK");
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

    async Task ResizeToContentAsync()
    {
        try
        {
            string raw = await wv.CoreWebView2.ExecuteScriptAsync("Math.max(document.body.scrollHeight,document.documentElement.scrollHeight).toString()");
            int contentHeight;
            if (!int.TryParse(raw.Trim('"'), out contentHeight)) return;
            Rectangle area = Screen.FromControl(this).WorkingArea;
            int chrome = Math.Max(0, Height - ClientSize.Height);
            int target = Math.Min(area.Height, Math.Max(MinimumSize.Height, contentHeight + chrome));
            if (Height < target) Height = target;
        }
        catch (Exception ex) { Log("Auto resize error: " + ex.Message); }
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
        string exeDir = Path.GetDirectoryName(Application.ExecutablePath);
        string tempRoot = Path.Combine(Path.GetTempPath(), "BusinessLetterPolisherUpdate_" + Guid.NewGuid().ToString("N"));
        string zipPath = Path.Combine(tempRoot, "update.zip");
        string extractDir = Path.Combine(tempRoot, "payload");
        string scriptPath = Path.Combine(tempRoot, "apply-update.cmd");
        try
        {
            Directory.CreateDirectory(tempRoot);
            Directory.CreateDirectory(extractDir);
            Log("Downloading update: " + url);
            using (var wc = new WebClient())
                await wc.DownloadFileTaskAsync(new Uri(url), zipPath);
            ZipFile.ExtractToDirectory(zipPath, extractDir);

            string exeName = Path.GetFileName(Application.ExecutablePath);
            string script = "@echo off\r\n" +
                "setlocal\r\n" +
                "set TARGET=" + Quote(exeDir) + "\r\n" +
                "set SOURCE=" + Quote(extractDir) + "\r\n" +
                "set PID=" + Process.GetCurrentProcess().Id + "\r\n" +
                ":wait\r\n" +
                "tasklist /FI \"PID eq %PID%\" 2>NUL | find \"%PID%\" >NUL\r\n" +
                "if not errorlevel 1 (timeout /t 1 /nobreak >NUL & goto wait)\r\n" +
                "robocopy \"%SOURCE%\" \"%TARGET%\" /E /R:3 /W:1 >NUL\r\n" +
                "start \"\" \"%TARGET%\\" + exeName + "\"\r\n" +
                "rmdir /s /q " + Quote(tempRoot) + "\r\n";
            File.WriteAllText(scriptPath, script, System.Text.Encoding.Default);
            Process.Start(new ProcessStartInfo(scriptPath) { UseShellExecute = true, WindowStyle = ProcessWindowStyle.Hidden });
            Log("Update staged; exiting for replacement");
            Application.Exit();
        }
        catch (Exception ex)
        {
            Log("Update failed: " + ex);
            MessageBox.Show("更新失敗：" + ex.Message, "錯誤", MessageBoxButtons.OK, MessageBoxIcon.Error);
            try { if (Directory.Exists(tempRoot)) Directory.Delete(tempRoot, true); } catch { }
        }
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
