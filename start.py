from app import main
import os
from tkinter import Tk, filedialog, messagebox, Button, Label, StringVar
from datetime import datetime
import traceback
import sys
import threading

base_path = os.path.dirname(sys.executable)
log_path = os.path.join(base_path, "Logs.txt")

def ask_dir(selected_dir: StringVar):
    selected_dir.set(filedialog.askdirectory(title="select a folder"))


def perform_automation(selected_dir):
    folder_path = selected_dir.get()
    if folder_path:
        excel_files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]
        if len(excel_files):
            try:
                main.start_app(excel_files, folder_path)
                messagebox.showinfo("complete", "successfully processed all files! you are good to exit")
            except ValueError:
                messagebox.showerror("invalid dataformat", "make sure you choose the correct data file")
            except Exception as e:
                with open(log_path, "a") as fh:
                    fh.write(f"----- Error: {e} Time: {datetime.now()} -----\n")
                    traceback.print_exc(file=fh)
                    fh.write(f"\n{'-'*30}\n")
                messagebox.showerror("Unknown Error", "unwanted error occured")
        else:
            messagebox.showerror("No Excel Files", "This Error occcured because no excel files were identified on selected location")

    else:
        messagebox.showerror("No folder selected", "This error occured because no folder was selected")


def start_automation_thread(selected_dir, action_btn, status_var):
    """Kicks off the automation in a separate thread to keep UI alive."""
    
    action_btn.config(state="disabled", text="⏳ Processing...", background="gray")
    status_var.set("Automation in progress... please wait.")
    
    def worker():
        try:
            perform_automation(selected_dir)
        finally:
            root.after(0, lambda: action_btn.config(state="normal", text="▶️ perform actions", background="green"))
            root.after(0, lambda: status_var.set("Task complete."))
    #create a different thread to save the PDF's
    threading.Thread(target=worker, daemon=True).start()

root = Tk()
root.title("AML Pre-Analysis Automater")
root.geometry("400x180")
root.iconbitmap('favicon/favicon_ico.ico')

selected_dir = StringVar(value="No Folder Selected")
status_text = StringVar(value="Ready")

Button(root, text="📂 choose folder", background="blue", foreground="white", 
       command=lambda: ask_dir(selected_dir)).pack(pady=5)

Label(root, text="Selected folder 👇").pack()
Label(root, textvariable=selected_dir, fg="blue").pack()

Label(root, text="Status:").pack(pady=(10, 0))
Label(root, textvariable=status_text, fg="darkgreen").pack()

btn_run = Button(root, text="▶️ perform actions", background="green", foreground="white")
btn_run.config(command=lambda: start_automation_thread(selected_dir, btn_run, status_text))
btn_run.pack(pady=10)

root.mainloop()
