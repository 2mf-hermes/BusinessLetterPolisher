using System;
using System.Drawing;
using System.IO;
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
            };

            wv.CoreWebView2.DOMContentLoaded += (s, e2) =>
            {
                Log("DOMContentLoaded OK");
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
