# Keylogger 

**Keylogger Pro** is a Python-based keylogging tool with both a modern GUI (Tkinter/ttkbootstrap) and a CLI mode.
It is intended *only* for authorized security assessments where you have explicit written permission.

> ⚠️ **Legal Notice**  
> Unauthorized use of keyloggers may be illegal in your jurisdiction.  
> Use this tool only on systems you own or are explicitly authorized to test.

## Features

- Cross-platform keylogging using `pynput`
- GUI mode with live keystroke view and session statistics
- CLI/headless mode with optional timeout and quiet output
- Per-session log files with timestamps and duration
- Safe local logging only (no network exfiltration)

## Installation

```bash
git clone https://github.com/<your-username>/keylogger-pro.git
cd keylogger-pro
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### GUI mode

```bash
python keylogger_pro.py
```

### CLI mode

```bash
python keylogger_pro.py -h        # Show help
python keylogger_pro.py -o logs.txt
python keylogger_pro.py -t 300    # Stop after 300 seconds
python keylogger_pro.py -q        # Quiet mode (no live output)
```

Logs are stored by default in the `keylogs/` directory next to the script.

## Ethical & Legal Use

This project is for **educational and authorized penetration testing** only.
The author accepts no liability for misuse or damage.

## Roadmap / Ideas

- Hotkey support (e.g., Ctrl+Alt+K) for toggling capture
- Optional encryption of log files
- Export sessions in JSON/CSV format

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.
