import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from docx import Document
import os
import sys

def paste_text():
    print("Paste triggered")  # For debugging only
    text_input.event_generate("<<Paste>>")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def parse_entries(text):
    lines = [line.strip() for line in text.strip().splitlines()]
    entries = []
    i = 0
    while i < len(lines):
        if lines[i].isdigit():
            try:
                source = lines[i + 1]
                context = lines[i + 2]
                translation = lines[i + 3]
                entries.append((source, translation, context))
                i += 4
                while i < len(lines) and not lines[i].isdigit():
                    i += 1
            except IndexError:
                break
        else:
            i += 1
    return entries


def custom_messagebox(title, message, type="info"):
    dialog = tk.Toplevel(window)
    dialog.title(title)
    dialog.transient(window)
    dialog.grab_set()
    dialog.resizable(False, False)

    window.update_idletasks()
    w, h = 360, 140
    x = window.winfo_rootx() + (window.winfo_width() - w) // 2
    y = window.winfo_rooty() + (window.winfo_height() - h) // 2
    dialog.geometry(f"{w}x{h}+{x}+{y}")


    icon_map = {
        "info": ("\u2139\ufe0f", "#0078d7"),
        "error": ("\u274c", "#e81123"),
        "warning": ("\u26a0", "#ffb900")
    }
    symbol, color = icon_map.get(type, ("\u2139\ufe0f", "#0078d7"))

    frame = tk.Frame(dialog, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text=symbol, font=("Segoe UI Emoji", 24), fg=color, bg="white").grid(row=0, column=0, padx=(20, 10), pady=20, sticky="n")
    tk.Label(frame, text=message, wraplength=250, justify="left", font=("Tahoma", 10), bg="white").grid(row=0, column=1, padx=(0, 20), pady=20, sticky="w")

    button_frame = tk.Frame(dialog, bg="#f0f0f0")
    button_frame.pack(fill="x", side="bottom")

    tk.Button(button_frame, text="OK", width=10, command=dialog.destroy, bg="#5158ff", fg="white").pack(pady=10, side="right", padx=(0, 10))

    dialog.wait_window()


def save_outputs():
    raw_text = text_input.get("1.0", tk.END)
    entries = parse_entries(raw_text)

    if not entries:
        custom_messagebox("Error", "No valid entries found in the text.", type="error")
        return

    save_dir = filedialog.askdirectory(title="Select folder to save output files")
    if not save_dir:
        return

    files_saved = []

    if var_tab.get():
        tab_file = os.path.join(save_dir, "output_tab_delimited.txt")
        with open(tab_file, "w", encoding="utf-8") as f:
            f.write("Source\tTranslation\tContext\n")
            for src, trans, ctx in entries:
                f.write(f"{src}\t{trans}\t{ctx}\n")
        files_saved.append(tab_file)

    if var_docx.get():
        doc = Document()
        for _, trans, _ in entries:
            doc.add_paragraph(trans)
        docx_file = os.path.join(save_dir, "translations.docx")
        doc.save(docx_file)
        files_saved.append(docx_file)

    if files_saved:
        custom_messagebox("Success", f"Files saved:\n" + "\n".join(files_saved), type="info")
    else:
        custom_messagebox("No Files Selected", "No output file types were selected.", type="warning")


def copy_translations():
    raw_text = text_input.get("1.0", tk.END)
    entries = parse_entries(raw_text)
    if not entries:
        custom_messagebox("Error", "No valid translations found to copy.", type="error")
        return
    translations = "\n".join(trans for _, trans, _ in entries)
    window.clipboard_clear()
    window.clipboard_append(translations)
    window.update()
    custom_messagebox("Copied", "All translations copied to clipboard!", type="info")


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0",
                         relief='solid', borderwidth=1, font=("Tahoma", 9))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


# GUI Setup
window = tk.Tk()
window.title("Moon Prism Power, Paste and Go!")
window.geometry("700x670")
window.resizable(False, False)
window.iconbitmap(default=resource_path("icon.ico"))

help_label = tk.Label(window, text="(?)", fg="#5158ff", cursor="question_arrow", font=("Tahoma", 9))
help_label.pack(anchor="ne", padx=12, pady=(0, 0))

ToolTip(help_label,
    "Paste the text copied from Translation Task Manager (TTM).\n"
    "Each entry must follow this format:\n"
    "  {Segment No.}\n  {Source}\n  {Context}\n  {Translation}")

label_input = tk.Label(window, text="Paste your input text below:", font=("Tahoma", 10))
label_input.pack(pady=(8, 0))

text_input = scrolledtext.ScrolledText(window, width=90, height=28, wrap=tk.WORD, font=("Tahoma", 10))
text_input.pack(padx=12, pady=(4, 4))

copy_frame = tk.Frame(window)
copy_frame.pack(fill=tk.X, padx=25, pady=(0, 10))

def on_enter(e):
    copy_link.config(fg="#d260ff", cursor="hand2", font=("Tahoma", 9, "underline"))

def on_leave(e):
    copy_link.config(fg="#d260ff", cursor="arrow", font=("Tahoma", 9))

copy_link = tk.Label(copy_frame, text="\U0001f5d0 Copy translations to clipboard", fg="#d260ff", font=("Tahoma", 9), cursor="hand2")
copy_link.pack(side=tk.RIGHT)
copy_link.bind("<Button-1>", lambda e: copy_translations())
copy_link.bind("<Enter>", on_enter)
copy_link.bind("<Leave>", on_leave)

options_frame = tk.Frame(window)
options_frame.pack(pady=10)

var_tab = tk.BooleanVar(value=True)
var_docx = tk.BooleanVar()

chk_tab = tk.Checkbutton(options_frame, text="Generate Tab-Delimited .txt", variable=var_tab)
chk_docx = tk.Checkbutton(options_frame, text="Generate .docx", variable=var_docx)

chk_tab.pack(side=tk.LEFT, padx=20)
chk_docx.pack(side=tk.LEFT, padx=20)

save_btn = tk.Button(window, text="Save Outputs", command=save_outputs, bg="#5158ff", fg="white", height=2, width=20)
save_btn.pack(pady=10)
save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#d260ff", cursor="hand2"))
save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#5158ff", cursor="arrow"))
save_btn.bind("<Button-1>", lambda e: save_btn.config(bg="#d260ff"))
save_btn.bind("<ButtonRelease-1>", lambda e: save_btn.config(bg="#5158ff"))

window.mainloop()
