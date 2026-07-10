import tkinter as tk
import os
import boto3
import webbrowser

from tkinter import filedialog, messagebox


#--------------------------
# File Functions
#--------------------------

#github function

def open_github():

    webbrowser.open(
        "https://github.com/Dhruvkunn"
    )

#linkedin function

def open_linkedin():

    webbrowser.open(
        "https://www.linkedin.com/in/dhruv-sharma-319370413/"
    )

#upload file function

def upload_file():

    bucket = bucket_entry.get().strip()
    file_path = selected_file_entry.get().strip()

    if bucket == "":
        messagebox.showerror(
            "Error",
            "Please enter a bucket name."
        )
        return

    if file_path == "":
        messagebox.showerror(
            "Error",
            "Please select a file."
        )
        return

    key = os.path.basename(file_path)

    s3 = boto3.client("s3")

    try:
        s3.upload_file(
            file_path,
            bucket,
            key
        )

        messagebox.showinfo(
            "Success",
            "File uploaded successfully!"
        )

        status_label.config(
            text=f"Status : Uploaded {key} ☁️"
        )

        refresh_files()

    except Exception as e:
        messagebox.showerror(
            "Upload Failed",
            str(e)
        )

        status_label.config(
            text="Status : Upload Failed ❌"
        )

#refresh files function

def refresh_files():

    files_list.delete(0, tk.END)

    bucket = bucket_entry.get().strip()

    if bucket == "":
        messagebox.showerror(
            "Error",
            "Please enter bucket name."
        )
        return

    s3 = boto3.client("s3")

    try:

        response = s3.list_objects_v2(
            Bucket=bucket
        )

        if "Contents" in response:

            for obj in response["Contents"]:
                files_list.insert(
                    tk.END,
                    obj["Key"]
                )

        status_label.config(
            text="🟢 Connected to AWS"
        )

    except Exception as e:

        messagebox.showerror(
            "Refresh Failed",
            str(e)
        )

        status_label.config(
            text="🔴 AWS Connection Failed"
        )

#download file function
    
def download_file():

    selected = files_list.curselection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a file."
        )
        return

    key = files_list.get(selected[0])

    bucket = bucket_entry.get().strip()

    save_path = filedialog.asksaveasfilename(
        initialfile=key
    )

    if not save_path:
        return

    s3 = boto3.client("s3")

    try:

        s3.download_file(
            bucket,
            key,
            save_path
        )

        messagebox.showinfo(
            "Success",
            "File downloaded successfully!"
        )

        status_label.config(
            text=f"Status : Downloaded {key} 📥"
        )

    except Exception as e:

        messagebox.showerror(
            "Download Failed",
            str(e)
        )

        status_label.config(
            text="Status : Download Failed ❌"
        )

#delete file function

def delete_file():

    selected = files_list.curselection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a file."
        )
        return

    key = files_list.get(selected[0])

    answer = messagebox.askyesno(
        "Delete File",
        f"Are you sure you want to delete\n\n{key} ?"
    )

    if not answer:
        return

    bucket = bucket_entry.get().strip()

    s3 = boto3.client("s3")

    try:

        s3.delete_object(
            Bucket=bucket,
            Key=key
        )

        messagebox.showinfo(
            "Success",
            f"{key} deleted successfully!"
        )

        status_label.config(
            text=f"Status : Deleted {key} 🗑️"
        )

        refresh_files()

    except Exception as e:

        messagebox.showerror(
            "Delete Failed",
            str(e)
        )

        status_label.config(
            text="Status : Delete Failed ❌"
        )

root = tk.Tk()
root.title(" AWS S3 File Manager")
root.geometry("700x900")
root.resizable(False, False)
root.configure(bg="#161616")

# --------------------------
# Menu Bar
# --------------------------

def about():
    messagebox.showinfo(
        "About",
        "AWS S3 File Manager\n\n"
        "Version : 1.0\n\n"
        "Developed by Dhruv Sharma\n\n"
        "Built with:\n"
        "• Python\n"
        "• Tkinter\n"
        "• AWS S3\n"
        "• boto3"
    )

menu_bar = tk.Menu(root)

# File Menu

file_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

file_menu.add_command(
    label="Refresh",
    command=refresh_files
)

file_menu.add_separator()

file_menu.add_command(
    label="Exit",
    command=root.destroy
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)

# Help Menu
help_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

help_menu.add_command(
    label="About",
    command=about
)

help_menu.add_separator()

help_menu.add_command(
    label="GitHub",
    command=open_github
)

help_menu.add_command(
    label="LinkedIn",
    command=open_linkedin
)

menu_bar.add_cascade(
    label="Help",
    menu=help_menu
)

root.config(menu=menu_bar)

#browse file function

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_file_entry.delete(0, tk.END)
        selected_file_entry.insert(0, file_path)
        status_label.config(
    text="Status : Ready to Upload ☁️"
)
        
#--------------------------
#scrollbar
#--------------------------

scrollbar = tk.Scrollbar(
    root,
    orient="vertical"
)

scrollbar.grid(
    row=7,
    column=4,
    sticky="ns",
    pady=(20, 5)
)

for i in range(4):
    root.columnconfigure(i, weight=1)

#--------------------------
# Title label
#--------------------------

title = tk.Label(
    root,
    text=" AWS S3 File Manager",
    font=("Segoe UI",20,"bold"),
    bg="#161616",
    fg="#0A58CA"
)    
title.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=20,
    padx=25,
)
bucket_label = tk.Label(
    root,
    text="Bucket Name",
    font=("Segoe UI",12),
    bg="#161616",
    fg="#FFFFFF"
)
bucket_label.grid(
    row=1,
    column=0,
    columnspan=4,
    padx=20,
    pady=10,
    sticky="w"
)
selected_file_label = tk.Label(
    root,
    text="Selected File ",
    font=("Segoe UI",12),
    bg="#161616",
    fg="#FFFFFF"
)
selected_file_label.grid(
    row=3,
    column=0,
    columnspan=4,
    padx=20,
    pady=10,
    sticky="w"
)

#---------------------------------------
# Label
#---------------------------------------

files_label = tk.Label(
    root,
    text="Files in Bucket",
    font=("Segoe UI",12),
    bg="#161616",
    fg="#FFFFFF"
)
files_label.grid(
    row=6,
    column=0,
    columnspan=4,
    padx=20,
    pady=(10, 5),
    sticky="w"  
)

#---------------------------------------
# Listbox
#---------------------------------------

files_list = tk.Listbox(
    root,
    font=("Segoe UI",12),
    bg="#2B2B2B",
    fg="#FFFFFF",
    selectbackground="#0A58CA",
    selectforeground="#FFFFFF",
    activestyle="none",
    width=60,
    height=15,
    relief="flat",
    yscrollcommand=scrollbar.set
)
files_list.grid(
    row=7,
    column=0,
    columnspan=4,
    padx=20,
    pady=(20, 5),
    sticky="we"
)

files_list.config(
    yscrollcommand=scrollbar.set
)

scrollbar.config(
    command=files_list.yview
)

#-------------------------
#status label
#-------------------------

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Segoe UI",12),
    bg="#161616",
    fg="#FFFFFF"
)

status_label.grid(
    row=8,
    column=0,
    columnspan=4,
    padx=20,
    pady=(10, 20),
    sticky="w"
)

#--------------------------
# Bucket name entry
#--------------------------

bucket_entry = tk.Entry(
    root,
    font=("Segoe UI",12),
    width=45,
    bg="#2B2B2B",
    fg="#FFFFFF"
)
bucket_entry.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=10,
    padx=20,
    sticky="we"
)
selected_file_entry = tk.Entry(
    root,   
    font=("Segoe UI",12),
    width=45,
    bg="#2B2B2B",
    fg="#FFFFFF"
)
selected_file_entry.grid(
    row=4,
    column=0,
    columnspan=3,
    pady=20,
    padx=20,

    sticky="we"
)

#--------------------------
# Frame
#--------------------------

button_frame = tk.Frame(
    root,
    bg="#161616"
)

button_frame.grid(
    row=5,
    column=0,
    columnspan=4,
    pady=20,
    padx=20,   
)
#--------------------------
# Buttons
#--------------------------

browse_btn = tk.Button(
    root,
    text="Browse",
    font=("Segoe UI",12),
    bg="#0A58CA",
    fg="#FFFFFF",
    width=19,
    height=1,
    command=browse_file
)
browse_btn.grid(
    row=4,
    column=3,
    pady=10,
    padx=20,
)

upload_btn = tk.Button(
    button_frame,
    text="Upload",
    font=("Segoe UI",12),
    bg="#0A58CA",
    fg="#FFFFFF",
    width=12,
    height=1,
    command=upload_file,
)
upload_btn.grid(
    row=0,
    column=0,
    pady=10,
    padx=28,  
)  

download_btn = tk.Button(
    button_frame,
    text="Download",
    font=("Segoe UI",12),
    bg="#198754",
    fg="#FFFFFF",
    width=12,
    height=1,
    command=download_file
)
download_btn.grid(
    row=0,
    column=1,
    pady=10,
    padx=20,  
)

delete_btn = tk.Button(
   button_frame,
    text="Delete",
    font=("Segoe UI",12),
    bg="#DC3545",
    fg="#FFFFFF",
    width=12,
    height=1,
    command=delete_file
)
delete_btn.grid(
    row=0,
    column=2,
    pady=10,
    padx=20,  
)

Refresh_btn = tk.Button(
    button_frame,
    text="Refresh",
    font=("Segoe UI",12),
    bg="#6C757D",
    fg="#FFFFFF",
    width=12,
    height=1,
    command=refresh_files
)
Refresh_btn.grid(
    row=0,
    column=3,
    pady=10,
    padx=20,  
)

root.mainloop()