import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Known suspicious keywords
suspicious_keywords = [
    "eval(",
    "exec(",
    "base64",
    "subprocess",
    "os.system",
    "socket"
]

# Simple known bad hashes (example only)
known_bad_hashes = [
    "44d88612fea8a8f36de82e1278abb02f",  # example MD5
]

# Get file hash (MD5)
def get_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return hashlib.md5(data).hexdigest()
    except:
        return None

# Scan single file
def scan_file(file_path):
    result = []

    # 1. hash check
    file_hash = get_md5(file_path)
    if file_hash in known_bad_hashes:
        result.append("❌ Known malicious hash detected")

    # 2. keyword scan
    try:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read().lower()
            for kw in suspicious_keywords:
                if kw in content:
                    result.append(f"⚠️ Suspicious keyword: {kw}")
    except:
        pass

    return result

# Scan folder
def scan_folder(folder_path, output_box):
    output_box.delete(1.0, tk.END)

    infected_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            findings = scan_file(path)

            if findings:
                infected_count += 1
                output_box.insert(tk.END, f"\n🚨 {path}\n")
                for f in findings:
                    output_box.insert(tk.END, f"   -> {f}\n")

    if infected_count == 0:
        output_box.insert(tk.END, "\n✅ No threats found!")

# Select folder
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        scan_folder(folder, text_box)

# GUI setup
app = tk.Tk()
app.title("Simple Virus Scanner (Educational)")
app.geometry("700x500")

btn = tk.Button(app, text="Select Folder & Scan", command=select_folder)
btn.pack(pady=10)

text_box = scrolledtext.ScrolledText(app, width=80, height=25)
text_box.pack(pady=10)

app.mainloop()