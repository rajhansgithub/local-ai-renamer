using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace AutoImageRenamerLauncher {
    static class Program {
        [STAThread]
        static void Main(string[] args) {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            try {
                string appDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
                string venvPythonW = Path.Combine(appDir, @".venv\Scripts\pythonw.exe");
                string venvPython = Path.Combine(appDir, @".venv\Scripts\python.exe");
                string mainPy = Path.Combine(appDir, "main.py");

                string pythonExe = File.Exists(venvPythonW) ? venvPythonW : (File.Exists(venvPython) ? venvPython : "python.exe");

                if (!File.Exists(mainPy)) {
                    MessageBox.Show("Could not find main.py at:\n" + mainPy, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                string arguments = "\"" + mainPy + "\"";
                if (args.Length > 0) {
                    arguments += " \"" + string.Join(" ", args).Trim('"') + "\"";
                }

                ProcessStartInfo psi = new ProcessStartInfo {
                    FileName = pythonExe,
                    Arguments = arguments,
                    WorkingDirectory = appDir,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                Process.Start(psi);
            } catch (Exception ex) {
                MessageBox.Show("Failed to launch AutoImageRenamer:\n" + ex.Message, "Launch Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
