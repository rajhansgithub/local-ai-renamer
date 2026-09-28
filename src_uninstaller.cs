using System;
using System.Windows.Forms;
using Microsoft.Win32;

namespace AutoImageRenamerUninstall {
    static class Program {
        const string MenuKeyName = "AutoImageRenamer";

        [STAThread]
        static void Main() {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            try {
                string[] keysToDelete = new string[] { "LocalAIRenamer", "AutoImageRenamer" };
                foreach (string k in keysToDelete) {
                    try {
                        Registry.CurrentUser.DeleteSubKeyTree(@"Software\Classes\Directory\shell\" + k);
                    } catch { }
                    try {
                        Registry.CurrentUser.DeleteSubKeyTree(@"Software\Classes\Directory\Background\shell\" + k);
                    } catch { }
                }

                MessageBox.Show(
                    "Local AI Renamer context menu has been completely removed from Windows Explorer.",
                    "Local AI Renamer - Uninstalled",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );
            } catch (Exception ex) {
                MessageBox.Show(
                    "Error during uninstallation:\n" + ex.Message,
                    "Uninstall Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}
