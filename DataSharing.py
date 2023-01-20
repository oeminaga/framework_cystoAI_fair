#%%
#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2023 Okyaz Eminaga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from cmd import Cmd
from email import message
from tkinter import messagebox
from matplotlib.pyplot import title
import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import shutil
from tqdm import tqdm
import RemovePHI
#%%
import argparse
os.chdir(os.path.dirname(__file__))

class DataSharing():
    def __init__(self, csv_filename : str, destination : str) -> None:
        self.csv_filename = csv_filename
        self.data_complete_ready_for_copy_process,self.data_complete_and_ready_to_share = RemovePHI.GetPandasDataFrameRemovedPHI(self.csv_filename)
        self.destination = destination
    def Run(self):
        
        if os.path.exists(self.destination):
            v=tk.messagebox.askyesno(title="The destination folder exists. Do you want to continue?")
            if v == "no":
                return
        else:
            os.mkdir(os.path.join(self.destination))
        rows=[]
        for i,(_,row) in tqdm(enumerate(self.data_complete_ready_for_copy_process.iterrows())):
            src=row["FullPath"]
            dest_folder = self.destination + "/" + row["CASE_ID_ANYON"]
            if not os.path.exists(dest_folder):
                os.mkdir(dest_folder)
            des=dest_folder+"/"+row["Filename_ANYON"]
            shutil.copyfile(src, des)
            rows.append(self.data_complete_and_ready_to_share.iloc[i])
        data_final=pd.concat(rows)
        data_final.to_csv(f"{self.destination}/metadata.csv", index=False)
        print("PROC: SAVING...")
        print("INFO: DONE")

class InputWindow(object):
    def __init__(self) -> None:
        pass
    def Show(self):
        self.create_main_window()
    def ValidateFolder(self, folder_):
        SuppressWarn = False
        if not isinstance(folder_, str):
            folder=folder_.get()
            SuppressWarn=True
        else:
            folder=folder_
        if folder=="":
            return folder
    def SelectADirectory(self):
        r=filedialog.askdirectory(initialdir=self.casefolder_vle.get())
        if (r!=""):
            if self.ValidateFolder(r)=="":
                pass
            else:
                self.casefolder_vle.set(r)
    def SelectAFile(self):
        r=filedialog.askopenfile(mode="r",  filetypes =[('csv', '*.csv')])
        if not r:
            return None
        self.file_vle.set(r.name)
        
    def RunProcess(self):
        dest_folder = self.casefolder_vle.get()
        csv_file = self.file_vle.get()
        self.root.config(cursor="wait")
        self.root.update()
        Cmd=DataSharing(csv_file, dest_folder)
        Cmd.Run()
        self.root.config(cursor="")
        messagebox.showinfo("The export process is complete","Data export is successfully executed.")
        self.root.update()
        
    def create_main_window(self):
        self.root = tk.Tk()
        self.casefolder_vle = tk.StringVar()
        self.casefolder_vle.trace("w", lambda name, index, mode, sv=self.casefolder_vle: self.ValidateFolder(self.casefolder_vle))
        
        self.file_vle = tk.StringVar()
        
        '''
        self.USR_LABEL = tk.Label(self.root, text="Provide the user id to share")
        self.USR_LABEL.pack(fill=tk.X)

        self.user_id = tk.StringVar()
        self.user_id.trace_add("write", self.user_id)
        self.user_id_entry = ttk.Entry(self.root, width=20,textvariable=self.user_id)
        self.user_id_entry.pack(fill=tk.X)
        '''
        self.LabelSelect_CSV_TO = tk.Label(self.root, text="Please select the csv file that includes the information about the file list to export")
        self.LabelSelect_CSV_TO.pack(fill=tk.X)

        self.SelectFile = tk.Button(self.root, text="Select a csv file", command=self.SelectAFile, textvariable=self.file_vle)
        self.SelectFile.pack(fill=tk.X)

        self.LabelSelect_FOLDER_TO = tk.Label(self.root, text="Where do you want to store?")
        self.LabelSelect_FOLDER_TO.pack(fill=tk.X)
        self.SelectDirectory = tk.Button(self.root, text="Select a directory to export the images", command=self.SelectADirectory, textvariable=self.casefolder_vle)
        self.SelectDirectory.pack(fill=tk.X)
        self.CMD_EXECUTION = tk.Button(self.root, text="EXPORT", command=self.RunProcess)
        self.CMD_EXECUTION.pack(fill=tk.X)
        self.root.title('Export for data sharing')
        self.root.geometry('512x140')
        self.root.mainloop()
        
if __name__ == "__main__":
    win=InputWindow()
    win.Show()
'''  
parser = argparse.ArgumentParser(description='Data Extraction script')
parser.add_argument("--csv", help="provide the csv file with a column FullPath.")
parser.add_argument("--dst", help="provide the folder to which the extracted images are stored.")

args = parser.parse_args()

if __name__ == "__main__":
    print(args)
    cmd=DataSharing(args.csv,args.dst)
    cmd.Run()
'''