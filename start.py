from app import main
import os
from tkinter import Tk, filedialog, messagebox, Button, Label, StringVar
from datetime import datetime
import traceback
import sys

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



root = Tk()

root.title("AML Pre-Analysis Automater")
root.geometry("400x100")
root.iconbitmap('favicon/favicon_ico.ico')
selected_dir = StringVar()
selected_dir.set("No Folder Selected")
Button(root, text="📂 choose folder", background="blue", foreground="white", command=lambda : [ask_dir(selected_dir)]).pack()
Label(root, text=f"selected folder 👇").pack()
Label(root, textvariable=selected_dir).pack()
Button(root, text="▶️ perform actions", background="green", foreground="white", command=lambda : [perform_automation(selected_dir)]).pack()

root.mainloop()
