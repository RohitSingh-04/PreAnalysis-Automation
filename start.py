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
            main.start_app(excel_files, folder_path)
            messagebox.showinfo("complete", "successfully processed all files! you are good to exit")
        except ValueError:
            messagebox.showerror("invalid dataformat", "make sure you choose the correct data file")
        except Exception as e:
            print(e)
            messagebox.showerror("Unknown Error", "unwanted error occured")
    else:
        messagebox.showerror("No Excel Files", "This Error occcured because no excel files were identified on selected location")

else:
    messagebox.showerror("No folder selected", "This error occured because no folder was selected")

root.mainloop()
