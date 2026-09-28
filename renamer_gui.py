import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

from config import load_config, save_config
from renamer_core import run_rename_process

class RenamerApp:
    def __init__(self, root: tk.Tk, target_folder: str = ""):
        self.root = root
        self.target_folder = target_folder or ""
        self.config = load_config()

        self.root.title("Local AI Renamer")
        self.root.geometry("740x580")
        self.root.minsize(640, 480)
        self.root.configure(bg="#181825")

        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # Styling
        self.setup_styles()

        # Cancellation flag
        self.cancel_requested = False
        self.is_running = False

        # Build UI layout
        self.build_ui()

        # Keep reference to thumbnail image to prevent garbage collection
        self.current_photo_image = None

        # Start automatically if target_folder was provided
        if self.target_folder and os.path.exists(self.target_folder):
            self.root.after(300, self.start_renaming)

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Configure dark colors
        bg_dark = "#181825"
        card_bg = "#1e1e2e"
        accent_blue = "#89b4fa"
        text_light = "#cdd6f4"
        text_sub = "#a6adc8"

        style.configure("TFrame", background=bg_dark)
        style.configure("Card.TFrame", background=card_bg, relief="flat")
        
        style.configure(
            "TLabel", 
            background=bg_dark, 
            foreground=text_light, 
            font=("Segoe UI", 10)
        )
        style.configure(
            "Header.TLabel", 
            background=bg_dark, 
            foreground=accent_blue, 
            font=("Segoe UI", 14, "bold")
        )
        style.configure(
            "Subheader.TLabel", 
            background=bg_dark, 
            foreground=text_sub, 
            font=("Segoe UI", 9)
        )
        style.configure(
            "Card.TLabel", 
            background=card_bg, 
            foreground=text_light, 
            font=("Segoe UI", 9)
        )
        style.configure(
            "CardBold.TLabel", 
            background=card_bg, 
            foreground=accent_blue, 
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor="#313244",
            background="#a6e3a1",
            darkcolor="#a6e3a1",
            lightcolor="#a6e3a1",
            bordercolor="#1e1e2e",
            thickness=14
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            background="#89b4fa",
            foreground="#11111b",
            borderwidth=0,
            focusthickness=0,
            padding=6
        )
        style.map("Action.TButton",
            background=[("active", "#b4befe"), ("disabled", "#45475a")],
            foreground=[("disabled", "#6c7086")]
        )

        style.configure(
            "Cancel.TButton",
            font=("Segoe UI", 10),
            background="#f38ba8",
            foreground="#11111b",
            borderwidth=0,
            focusthickness=0,
            padding=6
        )
        style.map("Cancel.TButton",
            background=[("active", "#eba0ac"), ("disabled", "#45475a")],
            foreground=[("disabled", "#6c7086")]
        )

    def build_ui(self):
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        title_lbl = ttk.Label(header_frame, text="⚡ Local AI Renamer", style="Header.TLabel")
        title_lbl.pack(anchor="w")

        subtitle_text = "Context-aware AI image renaming • On-demand VRAM loading"
        sub_lbl = ttk.Label(header_frame, text=subtitle_text, style="Subheader.TLabel")
        sub_lbl.pack(anchor="w")

        # Folder Selection / Display Bar
        folder_frame = ttk.Frame(self.root)
        folder_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(folder_frame, text="Target Folder:", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        
        self.folder_var = tk.StringVar(value=self.target_folder or "No folder selected. Browse or right-click a folder.")
        folder_entry = tk.Entry(
            folder_frame, 
            textvariable=self.folder_var, 
            bg="#313244", 
            fg="#cdd6f4", 
            insertbackground="#cdd6f4", 
            relief="flat", 
            font=("Segoe UI", 9)
        )
        folder_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=4)

        browse_btn = tk.Button(
            folder_frame, 
            text="Browse...", 
            command=self.browse_folder, 
            bg="#45475a", 
            fg="#cdd6f4", 
            activebackground="#585b70", 
            activeforeground="#cdd6f4", 
            relief="flat", 
            font=("Segoe UI", 9)
        )
        browse_btn.pack(side="left", padx=(0, 5))

        settings_btn = tk.Button(
            folder_frame, 
            text="⚙ Settings", 
            command=self.open_settings_dialog, 
            bg="#45475a", 
            fg="#cdd6f4", 
            activebackground="#585b70", 
            activeforeground="#cdd6f4", 
            relief="flat", 
            font=("Segoe UI", 9)
        )
        settings_btn.pack(side="left")

        # Live Card Area (Progress + Thumbnail Preview)
        card = ttk.Frame(self.root, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=10, ipady=8)

        # Status text & counter
        status_bar_frame = ttk.Frame(card, style="Card.TFrame")
        status_bar_frame.pack(fill="x", padx=15, pady=(5, 5))

        self.status_var = tk.StringVar(value="Ready. Waiting to start...")
        self.status_lbl = ttk.Label(status_bar_frame, textvariable=self.status_var, style="CardBold.TLabel")
        self.status_lbl.pack(side="left")

        self.counter_var = tk.StringVar(value="")
        self.counter_lbl = ttk.Label(status_bar_frame, textvariable=self.counter_var, style="Card.TLabel")
        self.counter_lbl.pack(side="right")

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            card, 
            variable=self.progress_var, 
            maximum=100, 
            style="Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", padx=15, pady=5)

        # Preview Container (Thumbnail + Filename details)
        preview_container = ttk.Frame(card, style="Card.TFrame")
        preview_container.pack(fill="x", padx=15, pady=(5, 5))

        # Thumbnail canvas / label
        self.thumb_lbl = tk.Label(
            preview_container, 
            bg="#313244", 
            width=15, 
            height=6, 
            text="[No Image]", 
            fg="#6c7086"
        )
        self.thumb_lbl.pack(side="left", padx=(0, 15))

        # File names info
        file_info_frame = ttk.Frame(preview_container, style="Card.TFrame")
        file_info_frame.pack(side="left", fill="both", expand=True)

        self.orig_file_var = tk.StringVar(value="Original: —")
        self.new_file_var = tk.StringVar(value="New Name: —")

        ttk.Label(file_info_frame, textvariable=self.orig_file_var, style="Card.TLabel").pack(anchor="w", pady=2)
        ttk.Label(
            file_info_frame, 
            textvariable=self.new_file_var, 
            style="Card.TLabel", 
            foreground="#a6e3a1", 
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=2)

        # Activity Log Area
        log_label = ttk.Label(self.root, text="Activity Log:", font=("Segoe UI", 9, "bold"))
        log_label.pack(anchor="w", padx=20, pady=(5, 2))

        log_container = ttk.Frame(self.root)
        log_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.log_text = tk.Text(
            log_container, 
            bg="#11111b", 
            fg="#cdd6f4", 
            insertbackground="#cdd6f4", 
            relief="flat", 
            font=("Consolas", 9), 
            wrap="none"
        )
        log_scroll_y = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        log_scroll_x = ttk.Scrollbar(log_container, orient="horizontal", command=self.log_text.xview)
        self.log_text.configure(xscrollcommand=log_scroll_x.set, yscrollcommand=log_scroll_y.set)

        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll_y.grid(row=0, column=1, sticky="ns")
        log_scroll_x.grid(row=1, column=0, sticky="ew")

        log_container.grid_rowconfigure(0, weight=1)
        log_container.grid_columnconfigure(0, weight=1)

        # Log color tags
        self.log_text.tag_config("SUCCESS", foreground="#a6e3a1")
        self.log_text.tag_config("INFO", foreground="#89b4fa")
        self.log_text.tag_config("WARNING", foreground="#f9e2af")
        self.log_text.tag_config("ERROR", foreground="#f38ba8")
        self.log_text.tag_config("STATUS", foreground="#cba6f7")
        self.log_text.tag_config("DEBUG", foreground="#6c7086")

        # Bottom Action Bar
        action_bar = ttk.Frame(self.root)
        action_bar.pack(fill="x", padx=20, pady=(5, 15))

        self.start_btn = ttk.Button(action_bar, text="▶ Start Renaming", style="Action.TButton", command=self.start_renaming)
        self.start_btn.pack(side="left", padx=(0, 10))

        self.cancel_btn = ttk.Button(action_bar, text="⏹ Cancel", style="Cancel.TButton", command=self.request_cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=(0, 10))

        self.open_folder_btn = tk.Button(
            action_bar, 
            text="📁 Open Folder", 
            command=self.open_target_folder, 
            bg="#45475a", 
            fg="#cdd6f4", 
            activebackground="#585b70", 
            activeforeground="#cdd6f4", 
            relief="flat", 
            font=("Segoe UI", 9)
        )
        self.open_folder_btn.pack(side="left")

        self.close_btn = tk.Button(
            action_bar, 
            text="Close", 
            command=self.root.destroy, 
            bg="#313244", 
            fg="#cdd6f4", 
            activebackground="#45475a", 
            activeforeground="#cdd6f4", 
            relief="flat", 
            font=("Segoe UI", 9)
        )
        self.close_btn.pack(side="right")

    def browse_folder(self):
        selected = filedialog.askdirectory(title="Select Folder Containing Images")
        if selected:
            self.target_folder = selected
            self.folder_var.set(selected)

    def open_target_folder(self):
        folder = self.folder_var.get()
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showinfo("Folder Not Found", "The specified folder does not exist.")

    def log_message(self, message: str, level: str = "INFO"):
        def _append():
            self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n", level)
            self.log_text.see(tk.END)
        self.root.after(0, _append)

    def update_status(self, msg: str):
        self.root.after(0, lambda: self.status_var.set(msg))

    def update_progress(self, current: int, total: int, filename: str):
        def _prog():
            percent = (current / total) * 100 if total > 0 else 0
            self.progress_var.set(percent)
            self.counter_var.set(f"{current} / {total} ({int(percent)}%)")
            self.orig_file_var.set(f"Original: {filename}")
        self.root.after(0, _prog)

    def update_image_processed(self, orig_name: str, new_name: str, full_path: str, thumbnail: Image.Image):
        def _update():
            self.new_file_var.set(f"New Name: {new_name}")
            if thumbnail:
                try:
                    photo = ImageTk.PhotoImage(thumbnail)
                    self.thumb_lbl.configure(image=photo, text="", width=120, height=120)
                    self.current_photo_image = photo
                except Exception:
                    pass
        self.root.after(0, _update)

    def request_cancel(self):
        if self.is_running:
            self.cancel_requested = True
            self.update_status("Cancelling... please wait for current image to finish.")
            self.cancel_btn.configure(state="disabled")

    def start_renaming(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.exists(folder):
            messagebox.showwarning("Invalid Folder", "Please select a valid folder first.")
            return

        if self.is_running:
            return

        self.is_running = True
        self.cancel_requested = False
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_var.set(0)
        self.counter_var.set("")
        self.log_text.delete("1.0", tk.END)

        thread = threading.Thread(target=self._worker_thread, args=(folder,), daemon=True)
        thread.start()

    def _worker_thread(self, folder: str):
        start_time = time.time()
        try:
            stats = run_rename_process(
                folder_path=folder,
                config=self.config,
                on_status=self.update_status,
                on_progress=self.update_progress,
                on_image_processed=self.update_image_processed,
                on_log=self.log_message,
                is_cancelled=lambda: self.cancel_requested
            )
            elapsed = time.time() - start_time
            summary_msg = (
                f"Finished in {elapsed:.1f}s. "
                f"Renamed: {stats['renamed']} | Skipped: {stats['skipped']} | Errors: {stats['errors']}. "
                f"AI model VRAM released."
            )
            self.log_message(summary_msg, "SUCCESS")
            self.update_status("Completed! AI Model freed from memory.")

            if self.config.get("auto_close_on_complete", False):
                delay = int(self.config.get("auto_close_delay_seconds", 3))
                self.log_message(f"Window will close automatically in {delay} seconds...", "INFO")
                self.root.after(delay * 1000, self.root.destroy)

        except Exception as e:
            self.log_message(f"Fatal error: {str(e)}", "ERROR")
            self.update_status(f"Error occurred: {str(e)}")
        finally:
            self.root.after(0, self._on_finish)

    def _on_finish(self):
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

    def open_settings_dialog(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("450x380")
        win.configure(bg="#1e1e2e")
        win.transient(self.root)
        win.grab_set()

        pad = {"padx": 15, "pady": 8}

        ttk.Label(win, text="⚙ Local AI Renamer Settings", font=("Segoe UI", 12, "bold"), background="#1e1e2e", foreground="#89b4fa").pack(anchor="w", padx=15, pady=(15, 10))

        # Max Words
        f1 = tk.Frame(win, bg="#1e1e2e")
        f1.pack(fill="x", **pad)
        tk.Label(f1, text="Word Count (1 to 5):", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9)).pack(side="left")
        max_words_var = tk.IntVar(value=self.config.get("max_words", 5))
        spin = tk.Spinbox(f1, from_=1, to=10, textvariable=max_words_var, width=5, bg="#313244", fg="#cdd6f4")
        spin.pack(side="right")

        # Word Separator
        f2 = tk.Frame(win, bg="#1e1e2e")
        f2.pack(fill="x", **pad)
        tk.Label(f2, text="Word Separator:", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9)).pack(side="left")
        sep_var = tk.StringVar(value=self.config.get("word_separator", "_"))
        sep_combo = ttk.Combobox(f2, textvariable=sep_var, values=["_", "-", " "], width=6)
        sep_combo.pack(side="right")

        # Engine Selection
        f3 = tk.Frame(win, bg="#1e1e2e")
        f3.pack(fill="x", **pad)
        tk.Label(f3, text="Vision AI Engine:", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9)).pack(side="left")
        engine_var = tk.StringVar(value=self.config.get("engine", "local_florence2"))
        engine_combo = ttk.Combobox(f3, textvariable=engine_var, values=["local_florence2", "api_gemini"], width=16)
        engine_combo.pack(side="right")

        # Gemini API Key (if using api_gemini)
        f4 = tk.Frame(win, bg="#1e1e2e")
        f4.pack(fill="x", **pad)
        tk.Label(f4, text="Gemini API Key (Optional):", bg="#1e1e2e", fg="#cdd6f4", font=("Segoe UI", 9)).pack(side="left")
        api_key_var = tk.StringVar(value=self.config.get("gemini_api_key", ""))
        api_entry = tk.Entry(f4, textvariable=api_key_var, show="*", width=20, bg="#313244", fg="#cdd6f4")
        api_entry.pack(side="right")

        # Recursive Checkbox
        f5 = tk.Frame(win, bg="#1e1e2e")
        f5.pack(fill="x", **pad)
        recursive_var = tk.BooleanVar(value=self.config.get("recursive", True))
        rec_chk = tk.Checkbutton(
            f5, 
            text="Recursively rename in subfolders", 
            variable=recursive_var, 
            bg="#1e1e2e", 
            fg="#cdd6f4", 
            selectcolor="#313244", 
            activebackground="#1e1e2e", 
            activeforeground="#cdd6f4"
        )
        rec_chk.pack(anchor="w")

        # Auto Close Checkbox
        f6 = tk.Frame(win, bg="#1e1e2e")
        f6.pack(fill="x", **pad)
        autoclose_var = tk.BooleanVar(value=self.config.get("auto_close_on_complete", False))
        auto_chk = tk.Checkbutton(
            f6, 
            text="Auto-close window when done", 
            variable=autoclose_var, 
            bg="#1e1e2e", 
            fg="#cdd6f4", 
            selectcolor="#313244", 
            activebackground="#1e1e2e", 
            activeforeground="#cdd6f4"
        )
        auto_chk.pack(anchor="w")

        def save_and_close():
            self.config["max_words"] = max_words_var.get()
            self.config["word_separator"] = sep_var.get()
            self.config["engine"] = engine_var.get()
            self.config["gemini_api_key"] = api_key_var.get()
            self.config["recursive"] = recursive_var.get()
            self.config["auto_close_on_complete"] = autoclose_var.get()
            save_config(self.config)
            win.destroy()

        save_btn = tk.Button(win, text="Save Settings", command=save_and_close, bg="#89b4fa", fg="#11111b", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=5)
        save_btn.pack(pady=15)

def run_gui(folder_path: str = ""):
    root = tk.Tk()
    app = RenamerApp(root, target_folder=folder_path)
    root.mainloop()

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else ""
    run_gui(folder)
