from app import main
import os
from tkinter import Tk, filedialog, messagebox

root = Tk()

root.title("AML Pre-Analysis Automater")

folder_path = filedialog.askdirectory(title="select a folder")

if folder_path:
    excel_files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]
    if len(excel_files):
        try:
            main.start_app(excel_files)
        except ValueError:
            messagebox.showerror("invalid dataformat", "make sure you choose the correct data file")
        except:
            messagebox.showerror("Unknown Error", "unwanted error occured")
    else:
        messagebox.showerror("No Excel Files", "This Error occcured because no excel files were identified on selected location")

else:
    messagebox.showerror("No folder selected", "This error occured because no folder was selected")

root.mainloop()
