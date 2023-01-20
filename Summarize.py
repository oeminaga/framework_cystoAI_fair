#%%
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
import os

folder_to_search = "../Data"
folders_to_consider= []
with open(f"{folder_to_search}/GetSummaryFromTheseFolders.cfg") as f:
    folders_to_consider=f.readlines()
folder_to_consider=folders_to_consider[0]

folder_to_consider=f"{folder_to_search}/{folder_to_consider}"
folders_exists=[[f,f"{folder_to_consider}/{f}"] for f in os.listdir(folder_to_consider) if os.path.isdir(f"{folder_to_consider}/{f}")]
collect_keywords = []
files = defaultdict(list)
for folder_ in folders_exists:
    folder=folder_[1]
    subfolders = [[f, f"{folder}/{f}"] for f in os.listdir(folder)]
    found = []
    
    for subfolder in subfolders:
        if "videos" == subfolder[0].lower():
            found.append(subfolder[0])
        if "images" == subfolder[0].lower():
            found.append(subfolder[0])
    
    if len(found)<2:
        print("Found only", found)
        continue

    #index files
    for subcontent in found:
        files[subcontent.lower()].extend([[f, f"{folder}/{subcontent}/{f}"] for f in os.listdir(f"{folder}/{subcontent}") if os.path.isfile(f"{folder}/{subcontent}/{f}")])

    for x in files["images"]:
        collect_keywords.extend(x[0].split(".")[0].split("_"))

#%%
import numpy as np
import pandas as pd
pd.DataFrame({"Keywords": np.unique(collect_keywords)}).to_csv(f"./{folder_to_search}/keywords.csv", index=False)

#%%
data = defaultdict(list)
columns = ["ID", "IND", "DATE", "IDENTIFICATION", "LOCATION", "ImageModality","PATHOLOGY", "STAGE", "Filename", "FullPath", "CASE_ID"]
ErrorInLabels = {"ID": [], "Filename": [], "FullPath":[] }
print(len(files["images"]))
for fl in files["images"]:
    items = fl[0].split(".")[0].split("_")
    if len(items)==8:
        for i,k in enumerate(columns[:-3]):
            if k=="IDENTIFICATION":
                data[k].append(items[i].split("-")[0][1:])
            else:
                data[k].append(items[i])
        data["Filename"].append(fl[0])
        data["FullPath"].append(fl[1])
        data["CASE_ID"].append("_".join(items[:3]))
    elif len(items)==4:
        for i,k in enumerate(columns[:4]):
            data[k].append(items[i])
        for k in columns[4:-3]:
            data[k].append("")
        data["Filename"].append(fl[0])
        data["FullPath"].append(fl[1])
        data["CASE_ID"].append("_".join(items[:3]))

    else:
        ErrorInLabels["ID"].append(fl[0].split(".")[0])
        ErrorInLabels["Filename"].append(fl[0])
        ErrorInLabels["FullPath"].append(fl[1])
        
data_=pd.DataFrame(data)
data_.to_csv(f"{folder_to_search}/SummaryReportImages.csv", index=False)
pd.DataFrame(ErrorInLabels).to_csv(f"{folder_to_search}/ErrorReportImages.csv", index=False)
# %%
