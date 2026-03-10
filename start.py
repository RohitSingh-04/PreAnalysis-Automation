from app import main
import os
from tkinter import Tk, filedialog, messagebox, Button, Label, StringVar, Toplevel, Entry, ttk, Frame, simpledialog, LabelFrame
from datetime import datetime
import traceback
import sys
import threading

def get_base_path():
    # pyinstaller
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # For PyInstaller --onefile, the "base" is a temp folder.
        # Use sys.executable to get the path where the .exe actually sits.
        return os.path.dirname(sys.executable)
    
    # Nuitka
    if "__compiled__" in globals():
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()

log_path = os.path.join(base_path, "Logs.txt")

# This finds the correct folder whether you are running .py or .exe
if getattr(sys, 'frozen', False):
    # exe
    detected_bundle_dir = os.path.dirname(sys.executable)
else:
    # .py
    detected_bundle_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(detected_bundle_dir, "favicon", "favicon_ico.ico")

class CounterpartyConfirmationBox:
    def __init__(self, parent, df_subset):
        self.popup = Toplevel(parent)
        self.popup.title("Review & Edit Counterparties")
        self.popup.geometry("700x500")
        self.popup.grab_set()
        
        # We work on a copy to avoid mutating the original df until Confirm button is clicked
        self.result_df = df_subset.copy()
        self.confirmed = False

        # treeview documents
        columns = ("Alert Information", "Counterparty", "Total Amount")
        self.tree = ttk.Treeview(self.popup, columns=columns, show='headings', selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="w")
        
        self.refresh_tree() # Fill with initial data

        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        #bottom buttons
        btn_frame = Frame(self.popup)
        btn_frame.pack(fill="x", padx=10, pady=10)

        Button(btn_frame, text="Add Row", command=self.add_row, width=12).pack(side="left", padx=5)
        Button(btn_frame, text="Remove Selected", command=self.remove_row, fg="red", width=15).pack(side="left", padx=5)
        
        Button(btn_frame, text="Confirm & Save", bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'),
                  command=self.save_and_close, width=15).pack(side="right", padx=5)

        # event for double click
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # waits for the window to close before returning to your main function
        self.popup.wait_window()

    def refresh_tree(self):
        """Clears and re-populates the tree from the internal dataframe."""

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in self.result_df.iterrows():
            # Using the DataFrame index as the iid to getting sync
            self.tree.insert("", "end", iid=index, values=(row["Alert Information"], row["Counterparty"], row["Total Amount"]))

    def on_double_click(self, event):
        """Creates an Entry widget exactly over the cell to edit it."""
        #get the x,y of the double click event
        region = self.tree.identify_region(event.x, event.y)

        #if it isn't in tree cell return
        if region != "cell": return

        #get row and column in tree
        column = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        
        # the first three colums, check the double click is inside them
        if column not in ("#1", "#2", "#3"): return

        x, y, width, height = self.tree.bbox(item_id, column)#get x y hight and width of the cell
        col_idx = int(column.replace('#', '')) - 1 #use indexing for columns
        
        #placing entry above the selected cell and add the cursor
        entry = Entry(self.tree)
        current_val = self.tree.item(item_id, 'values')[col_idx]
        entry.insert(0, current_val)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()

        def save_edit(event=None):
            new_val = entry.get()

            current_vals = list(self.tree.item(item_id, 'values'))
            current_vals[col_idx] = new_val
            self.tree.item(item_id, values=current_vals)
            
            col_name = self.tree.cget("columns")[col_idx]
            
            try:
                
                if col_name == "Total Amount":
                    new_val = float(new_val)
                
                
                self.result_df.at[int(item_id), col_name] = new_val
                
                current_vals = list(self.tree.item(item_id, 'values'))
                current_vals[col_idx] = new_val
                self.tree.item(item_id, values=current_vals)
                
                entry.destroy()

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for Total Amount.")
                entry.focus_set()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def add_row(self):
        """Asks user for a name and appends a row to the dataframe/tree."""
        new_name = simpledialog.askstring("Add Counterparty", "Enter Counterparty Name:", parent=self.popup)
        if new_name:
            # Create a new row (Index is max + 1)
            new_idx = self.result_df.index.max() + 1 if not self.result_df.empty else 0
            new_data = {"Alert Information": "Manual Entry", "Counterparty": new_name, "Total Amount": 0.0}
            
            # Update DataFrame
            self.result_df.loc[new_idx] = new_data
            # Update Treeview
            self.tree.insert("", "end", iid=new_idx, values=("Manual Entry", new_name, 0.0))

    def remove_row(self):
        """Removes selected row from both UI and DataFrame."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a row to remove.")
            return
            
        item_id = selected_item[0]
        self.result_df.drop(index=int(item_id), inplace=True)
        self.tree.delete(item_id)

    def save_and_close(self):
        self.confirmed = True
        self.popup.destroy()

class CustomerConfirmationBox:
    def __init__(self, parent, data_df):
        self.popup = Toplevel(parent)
        self.popup.title("Review Customer Details")
        self.popup.geometry("800x500")
        self.popup.grab_set()

        self.result_df = data_df.copy()
        self.confirmed = False
        self.cols = list(self.result_df.columns)

        #init tree
        self.tree = ttk.Treeview(self.popup, columns=self.cols, show='headings', selectmode="browse")
        
        for col in self.cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=350, anchor="w")
        
        self.refresh_tree()
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        #bottom buttons
        btn_frame = Frame(self.popup)
        btn_frame.pack(fill="x", padx=10, pady=10)

        Button(btn_frame, text="Add Combination", command=self.add_row, width=15).pack(side="left", padx=5)
        Button(btn_frame, text="Remove Selected", command=self.remove_row, fg="red", width=15).pack(side="left", padx=5)
        
        Button(btn_frame, text="Confirm All", bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'),
               command=self.save_and_close, width=15).pack(side="right", padx=5)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.popup.wait_window()

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, row in self.result_df.iterrows():
            self.tree.insert("", "end", iid=index, values=(row[self.cols[0]], row[self.cols[1]]))

    def on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell": return

        column_id = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        
        col_idx = int(column_id.replace('#', '')) - 1
        col_name = self.cols[col_idx]

        x, y, width, height = self.tree.bbox(item_id, column_id)
        
        entry = Entry(self.tree)
        current_val = str(self.tree.item(item_id, 'values')[col_idx])
        entry.insert(0, current_val)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()

        def commit_data(event=None):

            # Check if entry exists
            if entry.winfo_exists():
                new_val = entry.get()
                
                # update data
                self.result_df.at[int(item_id), col_name] = new_val
                
                #update ui
                current_vals = list(self.tree.item(item_id, 'values'))
                current_vals[col_idx] = new_val
                self.tree.item(item_id, values=current_vals)
                
                entry.destroy()

        # event for enter or click somewhere else
        entry.bind("<Return>", commit_data)
        entry.bind("<FocusOut>", lambda e: commit_data())

    def add_row(self):
        new_name = simpledialog.askstring("Add", "Enter Name:", parent=self.popup)
        new_addr = simpledialog.askstring("Add", "Enter Address:", parent=self.popup)
        
        if new_name and new_addr:
            new_idx = self.result_df.index.max() + 1 if not self.result_df.empty else 0
            self.result_df.loc[new_idx] = [new_name, new_addr]
            self.tree.insert("", "end", iid=new_idx, values=(new_name, new_addr))

    def remove_row(self):
        selected = self.tree.selection()
        if not selected: return
        item_id = selected[0]
        self.result_df.drop(index=int(item_id), inplace=True)
        self.tree.delete(item_id)

    def save_and_close(self):
        self.confirmed = True
        self.popup.destroy()

def ask_dir(selected_dir: StringVar):
    selected_dir.set(filedialog.askdirectory(title="select a folder"))


def perform_automation(selected_dir, root):
    folder_path = selected_dir.get()
    if folder_path:
        excel_files = [file for file in os.listdir(folder_path) if file.endswith(".xlsx")]
        if len(excel_files):
            try:
                main.start_app(excel_files, folder_path, CounterpartyConfirmationBox, CustomerConfirmationBox, root)
                messagebox.showinfo("complete", "successfully processed all files! you are good to exit")
            except ValueError:
                messagebox.showerror("invalid dataformat", "make sure you choose the correct data file")
            except Exception as e:
                with open(log_path, "a") as fh:
                    fh.write(f"----- Error: {e} Time: {datetime.now()} -----\n")
                    traceback.print_exc(file=fh)
                    fh.write(f"\n{'-'*30}\n")
                messagebox.showerror("Unknown Error", f"unwanted error occured check {log_path}")
        else:
            messagebox.showerror("No Excel Files", "This Error occcured because no excel files were identified on selected location")

    else:
        messagebox.showerror("No folder selected", "This error occured because no folder was selected")


def start_automation_thread(selected_dir, action_btn, status_var, root):
    """Kicks off the automation in a separate thread to keep UI alive."""
    
    action_btn.config(state="disabled", text="⏳ Processing...", background="gray")
    status_var.set("Automation in progress... please wait.")
    
    def worker():
        try:
            perform_automation(selected_dir, root)
        finally:
            root.after(0, lambda: action_btn.config(state="normal", text="▶️ perform actions", background="green"))
            root.after(0, lambda: status_var.set("Task complete."))
    #create a different thread to save the PDF's
    threading.Thread(target=worker, daemon=True).start()

root = Tk()
root.title("AML Pre-Analysis Automater")
root.geometry("400x180")
root.iconbitmap(icon_path)

selected_dir = StringVar(value="No Folder Selected")
status_text = StringVar(value="Ready")

Button(root, text="📂 choose folder", background="blue", foreground="white", 
       command=lambda: ask_dir(selected_dir)).pack(pady=5)

Label(root, text="Selected folder 👇").pack()
Label(root, textvariable=selected_dir, fg="blue").pack()

Label(root, text="Status:").pack(pady=(10, 0))
Label(root, textvariable=status_text, fg="darkgreen").pack()

btn_run = Button(root, text="▶️ perform actions", background="green", foreground="white")
btn_run.config(command=lambda: start_automation_thread(selected_dir, btn_run, status_text, root))
btn_run.pack(pady=10)


root.mainloop()
