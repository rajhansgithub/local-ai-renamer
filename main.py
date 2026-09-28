import os
import sys
import argparse

from context_menu_manager import install_context_menu, uninstall_context_menu, is_context_menu_installed
from renamer_gui import run_gui
from renamer_core import run_rename_process
from config import load_config

def main():
    parser = argparse.ArgumentParser(
        description="Local Auto Image Renamer: Context-aware AI image renaming for Windows Explorer."
    )
    parser.add_argument(
        "folder", 
        nargs="?", 
        default="", 
        help="Target folder to process (passed automatically via context menu or manual path)."
    )
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Run in headless CLI mode instead of GUI."
    )
    parser.add_argument(
        "--install", 
        action="store_true", 
        help="Register the Windows Explorer right-click context menu."
    )
    parser.add_argument(
        "--uninstall", 
        action="store_true", 
        help="Remove the Windows Explorer right-click context menu."
    )

    args = parser.parse_args()

    if args.install:
        install_context_menu()
        return

    if args.uninstall:
        uninstall_context_menu()
        return

    target_folder = args.folder.strip('"').strip("'")

    if args.cli:
        if not target_folder or not os.path.exists(target_folder):
            print(f"[Error] Target folder does not exist: {target_folder}")
            sys.exit(1)
        print(f"Starting Local Auto Image Renamer in CLI mode for: {target_folder}")
        config = load_config()
        run_rename_process(target_folder, config=config)
    else:
        # Launch GUI
        run_gui(target_folder)

if __name__ == "__main__":
    main()
