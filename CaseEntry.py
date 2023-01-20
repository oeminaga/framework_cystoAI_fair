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
from collections import defaultdict
from sys import exec_prefix
import Validation
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo,askyesno
import shutil
import numpy as np
from tkinter import ttk

from tkcalendar import Calendar, DateEntry
from PIL import ImageTk,Image  
import matplotlib.pyplot as plt
import os
import subprocess
from datetime import datetime
import pandas as pd

#%%
os.chdir(os.path.dirname(__file__))
class InputWindow(object):
    def __init__(self) -> None:
        pass
    def Show(self):
        self.create_main_window()

    def SelectADirectory(self):
        r=filedialog.askdirectory(initialdir=self.casefolder_vle.get())
        if (r!=""):
            if self.ValidateFolder(r)=="":
                pass
            else:
                self.casefolder_vle.set(r)
    def RunProcess(self):
        
        pid=self.patient_id.get()
        date = self.date.get()
        self.ValidateDate(self.date)
        
        if len(self.MoveToFolder.curselection())==0:
            showinfo("ERROR", "Please select one of the status (e.g. Complete, InComplete...)")
            return;
        dest = self.MoveToFolder.get(self.MoveToFolder.curselection()[0])
        source = self.casefolder_vle.get()
        for vle in [pid, date, dest, source]:
            if vle=="" or vle=="PatientID":
                showinfo("ERROR","Please complete the fields before continuing!")
                return
        ans=askyesno("WARNING","Please ensure that all files are provided for the case."+
                 "\nYou can also add additional files later by directly accessing to the corresponding case folder in the 'Data' folder.\n"+
                 "Do you want to continue?")
        if not ans:
            return
        date= self.date.get().replace("/", "")

        type_of_procedure = "O"    
        if "officecystoscopy" in dest.lower():
            type_of_procedure="C"
        case_id = f"{pid}_{type_of_procedure}_{date}"
        val_process=Validation.ValidationEntryData(case_id, source, dest)
        check_list=val_process.Check()

        if check_list["DestinationStatus"]==1:
            showinfo("ERROR","This case already exists in Data folder.So, you cannot add. \n"+
            "\n You need to manually change the case in the data folder. Please seek approval from your supervisor when needed")
            return
        Error= ""
        for key in check_list:
            if (key!="other" and key!="DestinationStatus" ):
                if check_list[key]==0:
                    Error=Error+f"no {key} found. "
        if Error!="":
            Error = Error + "\n Do you want to continue despite having this warning?"
            if not askyesno("WARNING",Error):
                return
        username = os.getlogin()
        log = []
        log.append(f"USERNAME: {username}\n")
        log.append(f"DATE TIME: {datetime.now()}\n")
        log.append(f"WARNS: {Error}\n")
        log.append(f"ADDED: {case_id}\n")        
        log.append(f"VALID STATUS:\n")
        for key in check_list:
            log.append(f"{key} : {check_list[key]}\n")
        val_process.PrepareTheCaseToCopy()
        
        dest_folder = f"../Data/{dest}/{case_id}"
        if os.path.exists(dest_folder):
            showinfo("This case already exists in Data folder.So, you cannot add. \n"+
            "\n You need to manually change the case in the data folder. Please seek approval from your supervisor when needed")
            return;
        else:
            log.append("FOLDER:\n")
            os.mkdir(dest_folder)
            log.append(f"{dest_folder}\n")
            for subfolder in ["Images", "Videos", "Other"]:
                os.mkdir(f"{dest_folder}/{subfolder}")
                log.append(f"{dest_folder}/{subfolder}\n")
        log.append(f"FILES:\n")
        for fl in val_process.file_list:
            source = fl[0]
            dest = fl[1]
            shutil.copyfile(source,dest)
            log.append(f"Source: {source}\n")
            log.append(f"Destination:{dest}\n")
        log.append("*"*10+"\n")
        log.append("Image Quality Check:")
        for x in val_process.ImageQualityScores:
            log.append(f"{x[0]} {x[1]}\n")
        log.append("DONE: EXIST")
        with open(f"{dest_folder}/info.log", "w") as f:
            f.writelines(log)
        self.Reset(Silent=True)
    def ValidatePID(self, value):
        return value
        
    def ValidateDate(self, date_vl):
        data =datetime.strptime(date_vl.get(), '%m/%d/%Y')
        present = datetime.now()
        if data.date() > present.date():
            showinfo("ERROR", "Please check that the date is correct!")
        return date_vl
    def ValidateFolder(self, folder_):
        SuppressWarn = False
        if not isinstance(folder_, str):
            folder=folder_.get()
            SuppressWarn=True
        else:
            folder=folder_
        if folder=="":
            return folder
        cv=Validation.ValidationEntryData("", folder, "")
        result=cv.Check()
        Error= ""
        for key in result:
            if (key!="other" and key!="DestinationStatus"):
                if result[key]==0:
                    Error=Error+f"no {key} found. "
        if Error!="" and SuppressWarn==False:
            Error = Error + "\n Do you want to select this folder?"
            if askyesno("WARNING",Error):
                pass
            else:
                folder =""
        return folder
    def Reset(self, Silent=False):
        if Silent==False:
            res=askyesno(title="Confirmation",message="Do you want to reset or add a new case?")
        else:
            res=True
        if res:
            self.casefolder_vle.set("")
            self.patient_id.set("PatientID")
            self.date.set(datetime.today().strftime("%m/%d/%Y"))
            self.SelectDirectory.selection_clear()
            self.PatientID.focus()
            self.PatientID.select_range(0, tk.END)
    def create_main_window(self):
        # root window
        self.root =tk.Tk()
        style = ttk.Style(self.root)
        

        style.theme_use('clam')

        self.patient_id = tk.StringVar()
        self.patient_id.trace("w", lambda name, index, mode, sv=self.patient_id: self.ValidatePID(self.patient_id))
        self.date = tk.StringVar(value=datetime.today().strftime("%m/%d/%Y"))
        self.date.trace("w", lambda name, index, mode, sv=self.date: self.ValidateDate(self.date))
        self.casefolder_vle = tk.StringVar()
        self.casefolder_vle.trace("w", lambda name, index, mode, sv=self.casefolder_vle: self.ValidateFolder(self.casefolder_vle))
        
        self.PatientID=tk.Entry(self.root, textvariable=self.patient_id)#, height=2)
        self.PatientID.pack(fill=tk.X)
        
        self.PatientID.insert(0, "PatientID")
        
        self.PatientID.focus()
        self.PatientID.select_range(0, tk.END)
        self.DateInfo=tk.Entry(self.root, textvariable=self.date)#, height=2)
        self.DateInfo.pack(fill=tk.X)
        self.cal = Calendar(self.root,
                                locale='en_US',
                                selectmode="day",
                                year=datetime.now().year,
                                month=datetime.now().month, 
                                day=datetime.now().day,
                                date_pattern="mm/dd/yyyy",
                                background='darkblue',
                                foreground='white', textvariable=self.date)
        self.cal.pack(padx=10, pady=10)
        self.CaseFolder=tk.Label(self.root, textvariable=self.casefolder_vle)#, height=2)
        self.CaseFolder.pack(fill=tk.X)
        self.SelectDirectory = tk.Button(self.root, text="Select a case directory", command=self.SelectADirectory)
        self.SelectDirectory.pack(fill=tk.X)
        
        self.MoveToFolder = tk.Listbox(self.root)
        self.MoveToFolder.insert(0, "Complete")
        self.MoveToFolder.insert(1, "Complete_NoPathology")
        self.MoveToFolder.insert(2, "InComplete_IncompleteLabels")
        self.MoveToFolder.insert(3, "InComplete_NoScreenShots")
        self.MoveToFolder.insert(4, "InComplete_NotLabelled")
        self.MoveToFolder.insert(5, "OfficeCystoscopy")
        self.MoveToFolder.insert(6, "RequireApproval")
        self.MoveToFolder.insert(7, "UnderReview")
        self.MoveToFolder.pack(fill=tk.X)
        
        self.CMD_EXECUTION = tk.Button(self.root, text="Add the new case into 'Data' folder", command=self.RunProcess)
        self.CMD_EXECUTION.pack(fill=tk.X)
        self.CMD_NEWCASE = tk.Button(self.root, text="Add new case or Reset", command=self.Reset)
        self.CMD_NEWCASE.pack(fill=tk.X)
        self.root.title('Add new case')
        self.root.geometry('512x512')
        self.root.mainloop()

if __name__ == "__main__":
    win=InputWindow()
    win.Show()