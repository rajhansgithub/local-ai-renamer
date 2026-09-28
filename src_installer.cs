using System;
using System.IO;
using System.Windows.Forms;
using Microsoft.Win32;

namespace AutoImageRenamerSetup {
    static class Program {
        const string MenuKeyName = "LocalAIRenamer";
        const string MenuLabel = "Rename with Local AI";

        [STAThread]
        static void Main() {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            try {
                string currentDir = AppDomain.CurrentDomain.BaseDirectory.TrimEnd('\\');
                string targetExe = Path.Combine(currentDir, "LocalAIRenamer.exe");
                if (!File.Exists(targetExe)) {
                    targetExe = Path.Combine(currentDir, "AutoImageRenamer.exe");
                }
                string iconPath = Path.Combine(currentDir, "assets", "app_icon.ico");

                if (!File.Exists(targetExe)) {
                    // Fallback to python runner if exe not present yet
                    string mainPy = Path.Combine(currentDir, "main.py");
                    targetExe = "python.exe \"" + mainPy + "\"";
                } else {
                    targetExe = "\"" + targetExe + "\"";
                }

                string cmdFolder = targetExe + " \"%1\"";
                string cmdBg = targetExe + " \"%V\"";

                // 1. Directory context menu (clicking on a folder)
                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Software\Classes\Directory\shell\" + MenuKeyName)) {
                    key.SetValue("", MenuLabel);
                    if (File.Exists(iconPath)) {
                        key.SetValue("Icon", iconPath);
                    }
                    using (RegistryKey cmdKey = key.CreateSubKey("command")) {
                        cmdKey.SetValue("", cmdFolder);
                    }
                }

                // 2. Directory Background context menu (clicking inside a folder)
                using (RegistryKey key = Registry.CurrentUser.CreateSubKey(@"Software\Classes\Directory\Background\shell\" + MenuKeyName)) {
                    key.SetValue("", MenuLabel);
                    if (File.Exists(iconPath)) {
                        key.SetValue("Icon", iconPath);
                    }
                    using (RegistryKey cmdKey = key.CreateSubKey("command")) {
                        cmdKey.SetValue("", cmdBg);
                    }
                }

                MessageBox.Show(
                    "Local AI Renamer has been successfully installed!\n\n" +
                    "You can now right-click on any folder in Windows Explorer and choose:\n" +
                    "'Rename with Local AI'\n\n" +
                    "To remove it anytime, simply double-click Uninstall.exe.",
                    "Local AI Renamer - Installation Complete",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );
            } catch (Exception ex) {
                MessageBox.Show(
                    "Failed to register context menu:\n" + ex.Message,
                    "Installation Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}
