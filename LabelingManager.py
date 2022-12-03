#%%
#!/usr/bin/env python3
from collections import defaultdict
from sys import exec_prefix
import tkinter as tk
from tkinter import ttk
from tkinter import *  
from PIL import ImageTk,Image  
import matplotlib.pyplot as plt
from tkinter.messagebox import showinfo
from ttkwidgets.autocomplete import AutocompleteEntry
import os
import subprocess
import datetime
import pandas as pd
#%%
class InputWindow(object):
    def __init__(self, arg) -> None:
        self.source_folder= arg.source
        self.prefix= arg.prefix
        self.script_to_run= arg.script
        main_folders = [f for f in os.listdir(self.source_folder) if os.path.isdir(f"{self.source_folder}/{f}")]
        self.folders = {}
        for folder in main_folders:
            cases = [[f, f"{self.source_folder}/{folder}/{f}"] for f in os.listdir(f"{self.source_folder}/{folder}") if os.path.isdir(f"{self.source_folder}/{folder}/{f}")]

            self.folders[folder]=cases

    def Show(self):
        self.create_main_window()
    def Search(self, sv):
        search_key =sv.get()
        keywords_to_search = search_key.split(" ")
        if search_key=="" or len(search_key)==0:
            self.LoadContent()
            return
        self.remove_many()
        for folder in self.folders:
            x = self.Treeview.insert('', tk.END, text=folder, open=True, values=(folder))

            for case in self.folders[folder]:
                for key in keywords_to_search:
                    if key.lower() in case[0].lower():
                        self.Treeview.insert(x, tk.END, text=case[0],open=True, values=(case[1])) 
    def items_selected(self, event):
        item = self.Treeview.selection()[0]
        path = self.Treeview.item(item,"values")[0]
        pathX = f"{path}/{self.prefix}"
        subprocess.Popen(["python3", self.script_to_run, "--source", pathX])
        #os.system(f"python3 {self.script_to_run} --source {pathX}")
    def LoadContent(self):
        self.remove_many()
        for folder in self.folders:
            x = self.Treeview.insert('', tk.END, text=folder, open=False, values=(folder))
            for case in self.folders[folder]:
                self.Treeview.insert(x, tk.END, text=case[0],open=False, values=(case[1]))
    def remove_many(self):
        for item in self.Treeview.get_children():
            self.Treeview.delete(item)
    def create_list_view(self,container):
        
        #frame.columnconfigure(0, weight=1)

        # create a list box
        self.Treeview = ttk.Treeview(
            container, height=512)
        
        #self.Treeview.heading('text', text="Folders", anchor='w')
        self.LoadContent()
        # link a scrollbar to a list
        scrollbar = tk.Scrollbar(
            container,
            orient='vertical',
            command=self.Treeview.yview
        )

        self.Treeview['yscrollcommand'] = scrollbar.set

        # handle event
        self.Treeview.bind('<Double-1>', self.items_selected)     
        return self.Treeview
    
    def create_main_window(self):

        # root window
        self.root = tk.Tk()
        
        self.search_keyword = tk.StringVar()
        self.search_keyword.trace("w", lambda name, index, mode, sv=self.search_keyword: self.Search(self.search_keyword))
        self.SearchBox=tk.Entry(self.root, textvariable=self.search_keyword)#, height=2)
        self.SearchBox.pack(fill=X)
        self.root.title('Cases')
        self.root.geometry('512x512')
        list_frame = self.create_list_view(self.root)
        list_frame.pack(fill=BOTH)
        #list_frame.grid(column=0, row=0)
        self.root.mainloop()

import argparse

parser = argparse.ArgumentParser(description='User Interface for image labelling')
parser.add_argument("--source", help="provide either the folder path or a csv file with a column FullPath.")
parser.add_argument("--script", help="please provide the script you want to run the selected item.")
parser.add_argument("--prefix", help="please provide the provide prefix to add into the file path.")



args = parser.parse_args()

if __name__ == "__main__":
    win=InputWindow(args)
    win.Show()