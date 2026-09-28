import os
import sys
import winreg

MENU_KEY_NAME = "LocalAIRenamer"
OLD_MENU_KEY_NAME = "AutoImageRenamer"
MENU_LABEL = "Rename with Local AI"

def get_target_executable_or_command() -> str:
    """
    Determines the command string to run when user clicks the context menu.
    If LocalAIRenamer.exe or AutoImageRenamer.exe exists in the application directory, uses that.
    Otherwise falls back to invoking Python with main.py.
    """
    app_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
        return f'"{exe_path}" "%1"', f'"{exe_path}" "%V"'
    
    for candidate_name in ["LocalAIRenamer.exe", "AutoImageRenamer.exe"]:
        candidate_path = os.path.join(app_dir, candidate_name)
        if os.path.exists(candidate_path):
            return f'"{candidate_path}" "%1"', f'"{candidate_path}" "%V"'
    
    # Python script invocation
    python_exe = sys.executable
    main_py = os.path.join(app_dir, "main.py")
    
    # Prefer pythonw.exe to avoid flashing console if desired, or python.exe
    pythonw_candidate = os.path.join(os.path.dirname(python_exe), "pythonw.exe")
    runner = pythonw_candidate if os.path.exists(pythonw_candidate) else python_exe

    cmd_folder = f'"{runner}" "{main_py}" "%1"'
    cmd_bg = f'"{runner}" "{main_py}" "%V"'
    return cmd_folder, cmd_bg

def install_context_menu(icon_path: str = "") -> bool:
    """
    Registers the context menu in HKEY_CURRENT_USER.
    Does NOT require administrator elevation.
    """
    cmd_folder, cmd_bg = get_target_executable_or_command()
    app_dir = os.path.dirname(os.path.abspath(__file__))
    default_icon = icon_path or os.path.join(app_dir, "assets", "app_icon.ico")
    
    try:
        # 1. Directory right click (clicking ON a folder)
        dir_key_path = rf"Software\Classes\Directory\shell\{MENU_KEY_NAME}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, dir_key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, MENU_LABEL)
            if os.path.exists(default_icon):
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, default_icon)
        
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"{dir_key_path}\command") as cmd_key:
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd_folder)

        # 2. Directory Background right click (clicking on EMPTY SPACE inside a folder)
        bg_key_path = rf"Software\Classes\Directory\Background\shell\{MENU_KEY_NAME}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, bg_key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, MENU_LABEL)
            if os.path.exists(default_icon):
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, default_icon)

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"{bg_key_path}\command") as cmd_key:
            winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, cmd_bg)

        print("[Success] Windows Context Menu installed successfully!")
        print(f"  Command (Folder): {cmd_folder}")
        print(f"  Command (Background): {cmd_bg}")
        return True

    except Exception as e:
        print(f"[Error] Failed to install context menu: {e}")
        return False

def uninstall_context_menu() -> bool:
    """
    Removes the context menu entries from HKEY_CURRENT_USER.
    """
    def _delete_key_tree(root, subkey):
        try:
            with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                while True:
                    try:
                        child = winreg.EnumKey(key, 0)
                        _delete_key_tree(root, f"{subkey}\\{child}")
                    except OSError:
                        break
            winreg.DeleteKey(root, subkey)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"[Warning] Error deleting key {subkey}: {e}")

    try:
        for key_name in [MENU_KEY_NAME, OLD_MENU_KEY_NAME]:
            _delete_key_tree(winreg.HKEY_CURRENT_USER, rf"Software\Classes\Directory\shell\{key_name}")
            _delete_key_tree(winreg.HKEY_CURRENT_USER, rf"Software\Classes\Directory\Background\shell\{key_name}")
        print("[Success] Windows Context Menu uninstalled cleanly.")
        return True
    except Exception as e:
        print(f"[Error] Failed to uninstall context menu: {e}")
        return False

def is_context_menu_installed() -> bool:
    """Checks if the context menu entry exists in the registry."""
    try:
        winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            rf"Software\Classes\Directory\shell\{MENU_KEY_NAME}"
        )
        return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action in ("--install", "-i", "install"):
            install_context_menu()
        elif action in ("--uninstall", "-u", "uninstall"):
            uninstall_context_menu()
        elif action in ("--status", "-s"):
            print("Installed" if is_context_menu_installed() else "Not Installed")
        else:
            print("Usage: python context_menu_manager.py [--install | --uninstall | --status]")
    else:
        # Default interactive behavior
        if is_context_menu_installed():
            print("Context Menu is currently INSTALLED.")
            choice = input("Do you want to (U)ninstall or (R)einstall? [u/r]: ").strip().lower()
            if choice == "u":
                uninstall_context_menu()
            else:
                install_context_menu()
        else:
            print("Context menu is NOT installed.")
            choice = input("Do you want to install it now? [y/n]: ").strip().lower()
            if choice == "y":
                install_context_menu()
