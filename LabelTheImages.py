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
import tkinter as tk
from tkinter import ttk
from tkinter import *  
from PIL import ImageTk,Image  
import matplotlib.pyplot as plt
from tkinter.messagebox import showinfo
from ttkwidgets.autocomplete import AutocompleteEntry
import os
import datetime
import pandas as pd
from tkinter import filedialog
os.chdir(os.path.dirname(__file__))
class InputWindow(object):
    def FindInfo(self,var, index, mode):
        keylesion = self.lesion_id.get()
        if keylesion=="":
            return
        keylesions = keylesion.split("-")
        if len(keylesions)>1:
            keylesion=keylesions[0]
        check_it =[self.selected_Location,
                    self.selected_PATHOLOGY, self.selected_Stage]
        GetData = False
        for itm in check_it:
            if itm.get().lower()=="":
                GetData=True
        if GetData==False:
            return
        for file in self.files:
            filename = os.path.basename(file)
            items = filename.split(".")[0].split("_")
            to_fill=[self.cml_text, self.selected_IND,
                    self.dateValue, self.lesion_id, 
                    self.selected_Location, self.selected_ImageModality,
                    self.selected_PATHOLOGY, self.selected_Stage]

            if len(items)<4:
                return
            key_name =items[3] 
            if "-" in key_name:
                key_name = key_name.split("-")[0]
            if key_name.lower()==keylesion.lower():
                for i in range(len(items)):
                    if i >3 and i!=5:
                        to_fill[i].set(items[i])
                return

    def __init__(self, folder_path) -> None:
        self.folder_path= folder_path
        self.selected_index = -1
        self.selected_filename = ""
        if folder_path[-3:]=="csv":
            data=pd.read_csv(folder_path)
            self.files=data["FullPath"].to_list()
        else:
            self.files = [f"{folder_path}/{f}" for f in os.listdir(folder_path) if os.path.isfile(f"{folder_path}/{f}") and f.lower() != ".ds_store"]
        
    def CheckDate(self,var, index, mode):
        try:
            value = self.dateValue.get()
            format = "%m%d%Y"
            if value != "" and len(value)>=8:
                datetime.datetime.strptime(value, format)
        except:
            showinfo("Error", "Date format is wrong! Please correct it and ensure the date format matchs to MMDDYYYY")
            self.dateValue.set("")
    def CheckIND(self,var, index, mode):
        value = self.selected_IND.get()
        if value not in ["","O","C"]:
            showinfo("Error", "Please select one of the codes [O ,C]")
            self.selected_IND.set("")

    def RESETDATA(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices)==0:
            return

        self.selected_index = selected_indices[0]
        selected_langs = [self.listbox.get(i) for i in selected_indices]
        if len(selected_langs)==0:
            return
        selected_langs = selected_langs[0]
        self.selected_filename = selected_langs
        filename = os.path.basename(selected_langs)
        items = filename.split(".")[0].split("_")
        to_fill=[self.cml_text, self.selected_IND,
         self.dateValue, self.lesion_id, 
         self.selected_Location, self.selected_ImageModality,
         self.selected_PATHOLOGY, self.selected_Stage]
        
        if len(items)>1:
            Escape = False
            for i, itm in enumerate(items):
                if items[i].lower() == "ch2" or items[1] not in ["O","C"]:
                    Escape=True
                if Escape:
                    items = ["SpaceHolder"]
                    break
        if len(items)==1:
            if "images" in selected_langs.lower():
                f=selected_langs.split("/")[-3]
                items = f.split("_")
                Escape = False
                for i in range(len(to_fill)):
                    if i < len(items):
                        if items[i].lower() == "ch2" or items[1] not in ["O","C"]:
                            Escape=True
                            break;
                        
                        to_fill[i].set(items[i])
                    else:
                        to_fill[i].set("")
                if Escape:
                    for i in range(len(to_fill)):
                        to_fill[i].set("")


            else:
                f=selected_langs.split("/")[-2]
                items = f.split("_")
                if len(items)==3:
                    for i in range(len(to_fill)):
                        if i < len(items):
                            to_fill[i].set(items[i])
                        else:
                            to_fill[i].set("")
                else:
                    print('Failed to find CML')
        else:
            for i, itm in enumerate(items):
                to_fill[i].set(itm)
            if len(items)<len(to_fill):
                index_to_start = len(to_fill)-len(items)
                for i in range(index_to_start, len(to_fill)):
                    to_fill[i].set("")
        image=Image.open(selected_langs)
        h,w=image.size
        image=image.resize((h//4,w//4))
        img2 = ImageTk.PhotoImage(image)
        self.panel.configure(image=img2)
        self.panel.image = img2

    def items_selected(self, event):
        """ handle item selected event
        """
        self.RESETDATA()
    def Show(self):
        self.create_main_window()

    def create_input_frame(self, container):
        frame = ttk.Frame(container)
        # grid layout for the input frame
        frame.columnconfigure(4, weight=3)

        # CML
        ttk.Label(frame, text='CML:').grid(column=1, row=0, sticky=tk.W)
        keyword = ttk.Entry(frame, width=20,textvariable=self.cml_text)
        keyword.focus()
        keyword.grid(column=2, row=0, sticky=tk.W)

        #IND
        IND_values = ['O','C']
        ttk.Label(frame, text='IND:').grid(column=3, row=0, sticky=tk.W)
        IND = AutocompleteEntry(frame, width=5,textvariable=self.selected_IND,completevalues=IND_values)
        IND.grid(column=4, row=0, sticky=tk.W)

        #date
        ttk.Label(frame, text='DATE:').grid(column=5, row=0, sticky=tk.W)
        self.date_entry = ttk.Entry(frame, width=8, textvariable=self.dateValue)
        self.date_entry.grid(column=6, row=0, sticky=tk.W)
        #ID,IND,DATE,LESION_ID,LOCATION,ImageModality,PATHOLOGY,STAGE,Filename,FullPath,CASE_ID
        
        #LESION ID
        ttk.Label(frame, text='Identification:').grid(column=7, row=0, sticky=tk.W)
        LESIONID = ttk.Entry(frame, width=8, textvariable=self.lesion_id)
        LESIONID.grid(column=8, row=0, sticky=tk.W)

        #LOCATION
        Location_values = ['L', 'R', 'Ant', 'L Ant', 'R Ant','Dome', 'L Dome', 'R Dome','Lat', 'L Lat', 'R Lat','Pos', 'L Pos', 'R Pos' ,'Trig', 'L Trig','R Trig','UO', 'L UO', 'R UO', 'Prostate', 'L Prostate','R Prostate', 'U', 'Ureter', 'L Ureter', 'R Ureter', 'BN']
        ttk.Label(frame, text='Location:').grid(column=9, row=0, sticky=tk.W)
        Location = AutocompleteEntry(frame, width=5,textvariable=self.selected_Location,completevalues=Location_values)
        Location.grid(column=10, row=0, sticky=tk.W)
        
        #ImageModality
        ImageModality_values = ['WLC', '-WLC', '+WLC','BLC','+BLC','-BLC' ,'CLE', 'NBI', 'H', 'H100', 'H100PAX8', 'H200', 'H200CK20', 'H200p53', 'H40','H400', 'H40PAX8', 'H40p63', 'CT', 'MRT']
        ttk.Label(frame, text='Image modality:').grid(column=11, row=0, sticky=tk.W)
        ImageModality = AutocompleteEntry(frame, width=4,textvariable=self.selected_ImageModality,completevalues=ImageModality_values)
        ImageModality.grid(column=12, row=0, sticky=tk.W)

        #PATHOLOGY
        PATHOLOGY_values = ['B', 'LG', 'HG', 'AtypicalProliferation', 'CystitisCystica','CystitisCystica CystitisGlandularis','FPBLC','Fibrosis' ,'FollicularCystitis', 'PUNLMP','UPUMP','LG focal HG', 'GranulationTissue', 'Inflammation', 'reactiveChanges', 'Inflammation reactiveChanges', 'InflammationNOS', 'IntestinalMetaplasia', 'IntestinalMetaplasia CystitisCystica CystitisGlandularis', 'Malakoplakia','Melanosis', 'MildInflammation', 'NephrogenicAdenoma','NoBiopsy', 'NA', 'PolypoidCystitis', 'Papilloma', 'PostResection', 'ProcedureSiteChanges', 'SquamousMetaplasia', 'reactiveChanges']
        
        ttk.Label(frame, text='Pathology:').grid(column=1, row=1, sticky=tk.W)
        PATHOLOGY = AutocompleteEntry(frame, width=20,textvariable=self.selected_PATHOLOGY,completevalues=PATHOLOGY_values)
        PATHOLOGY.grid(column=2, row=1, sticky=tk.W)

        #Stage
        Stage_values = ['NA','T0', 'Ta','TIS','T1', 'T2']
        ttk.Label(frame, text='Stage:').grid(column=3, row=1, sticky=tk.W)
        Stage = AutocompleteEntry(frame, width=5,textvariable=self.selected_Stage,completevalues=Stage_values)
        Stage.grid(column=4, row=1, sticky=tk.W)

        '''
        # Match Case checkbox
        match_case = tk.StringVar()
        match_case_check = ttk.Checkbutton(
            frame,
            text='Match case',
            variable=match_case,
            command=lambda: print(match_case.get()))
        match_case_check.grid(column=0, row=2, sticky=tk.W)

        # Wrap Around checkbox
        wrap_around = tk.StringVar()
        wrap_around_check = ttk.Checkbutton(
            frame,
            variable=wrap_around,
            text='Wrap around',
            command=lambda: print(wrap_around.get()))
        wrap_around_check.grid(column=0, row=3, sticky=tk.W)
        '''
        for widget in frame.winfo_children():
            widget.grid(padx=0, pady=5)

        return frame

    def Reset(self):
        self.RESETDATA()
    def OpenFolder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path= folder_selected
        self.files = [f"{folder_selected}/{f}" for f in os.listdir(folder_selected) if os.path.isfile(f"{folder_selected}/{f}") and f.lower() != ".ds_store"]
        self.langs_var = tk.StringVar(value=self.files)
        self.selected_filename=""
        self.listbox["listvariable"]=self.langs_var
        self.listbox.select_set(self.selected_index)
    def Save(self):
        #ID,IND,DATE,LESION_ID,LOCATION,ImageModality,PATHOLOGY,STAGE,Filename,FullPath,CASE_ID
        to_fill=[self.cml_text.get(), self.selected_IND.get(),
         self.dateValue.get(), self.lesion_id.get(), 
         self.selected_Location.get(), self.selected_ImageModality.get(),
         self.selected_PATHOLOGY.get(), self.selected_Stage.get()]
        
        filename ="_".join(to_fill)
        selected_langs=self.selected_filename
        path_of_file = os.path.split(selected_langs)[0]
        extension = os.path.splitext(os.path.basename(selected_langs))[1]
        new_filename=f"{path_of_file}/{filename}{extension}"
        if os.path.exists(new_filename):
            showinfo("File is the similar label information exist.\nPlease check the correctness and avoid duplication!")
            return
        os.rename(selected_langs, new_filename)

        if self.folder_path[-3:]=="csv":
            data=pd.read_csv(self.folder_path)
            data["FullPath"].iloc[self.selected_index]=new_filename
            data.to_csv( self.folder_path, index=False)
            self.files=data["FullPath"].to_list()
        else:
            self.files = [f"{self.folder_path}/{f}" for f in os.listdir(self.folder_path) if os.path.isfile(f"{self.folder_path}/{f}") and f.lower() != ".ds_store"]
        self.langs_var = tk.StringVar(value=self.files)
        self.selected_filename=new_filename
        self.listbox["listvariable"]=self.langs_var
        self.listbox.select_set(self.selected_index)
        
    def create_button_frame(self, container):
        frame = ttk.Frame(container)

        frame.columnconfigure(4, weight=1)

        ttk.Button(frame, text='Reset',command=self.Reset).grid(column=1, row=0)
        ttk.Button(frame, text='Save',command=self.Save).grid(column=2, row=0)

        ttk.Button(frame, text='Open',command=self.OpenFolder).grid(column=3, row=0)
        
        for widget in frame.winfo_children():
            widget.grid(padx=0, pady=3)

        return frame

    def create_list_view(self,container):
        frame = ttk.Frame(container)

        #frame.columnconfigure(0, weight=1)

        # create a list box
        self.listbox = tk.Listbox(
            frame,
            listvariable=self.langs_var,
            selectmode=tk.SINGLE
            )
        self.listbox.config(width=0, height=6)
        self.listbox.grid(
            column=0,
            row=0
        )

        # link a scrollbar to a list
        scrollbar = tk.Scrollbar(
            frame,
            orient='vertical',
            command=self.listbox.yview
        )

        self.listbox['yscrollcommand'] = scrollbar.set

        scrollbar.grid(
            column=1,
            row=0,
            sticky='nse')

        # handle event
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)
        for widget in frame.winfo_children():
            widget.grid(padx=0, pady=5)
        return frame
    def ViewImage(self, event):
        selected_indices = self.listbox.curselection()
        if len(selected_indices)==0:
            return
        selected_langs = [self.listbox.get(i) for i in selected_indices]
        img=Image.open(selected_langs[0])
        #img=ImageTk.getimage(self.panel.image)
        plt.imshow(img)
        plt.show()
    def create_main_window(self):

        # root window
        self.root = tk.Tk()
        self.cml_text = tk.StringVar()
        self.lesion_id = tk.StringVar()
        self.lesion_id.trace_add("write", self.FindInfo)
        self.selected_IND = tk.StringVar()
        self.selected_IND.trace_add("write", self.CheckIND)
        self.dateValue = tk.StringVar()
        self.dateValue.trace_add("write", self.CheckDate)
        self.selected_Location = tk.StringVar()
        self.selected_ImageModality = tk.StringVar()
        self.selected_PATHOLOGY= tk.StringVar()
        self.selected_Stage= tk.StringVar()
        self.langs_var = tk.StringVar(value=self.files)
        self.root.title('Image labelling')
        self.root.geometry('1024x786')
        #root.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        self.root.columnconfigure(0, weight=4)
        # layout on the root window\
        '''
        image = Image.open("")
        h,w=image.size
        image=image.resize((h//4,w//4))
        img = ImageTk.PhotoImage(image)
        '''
        self.panel = tk.Label(self.root)#, image = img)
        self.panel.pack(side = "top", fill = "both", expand = "no")
        self.panel.bind('<Double-1>', self.ViewImage)
        self.panel.grid(column=0, row=1)
        list_frame = self.create_list_view(self.root)
        list_frame.grid(column=0, row=0)
        input_frame = self.create_input_frame(self.root)
        input_frame.grid(column=0, row=2)
        button_frame = self.create_button_frame(self.root)
        button_frame.grid(column=0, row=3)
        self.root.mainloop()

import argparse

parser = argparse.ArgumentParser(description='User Interface for image labelling')
parser.add_argument("--source", help="provide either the folder path or a csv file with a column FullPath.")

args = parser.parse_args()
args.source
if __name__ == "__main__":
    win=InputWindow(args.source)
    win.Show()