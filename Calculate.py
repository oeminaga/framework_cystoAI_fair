#%%
 #!/usr/bin/env python3
from enum import unique
from itertools import count
import os
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import pandas as pd
#Cysview_BLC_Registry_2016_2018 or CystoNetDatabase_2019_Current
#%% MODIFY HERE the folder to search
#############
# ONLY CHANGE HERE
############
folder_to_search = "../Data"
#############
# DO NOT TOUCH AFTER THIS
#############
import datetime
print("DATE", datetime.datetime.now())
def CountTheFilesAndCalculateTheirSize(folder_to_search):
    print(f"Get information about all files in the folder {folder_to_search}")

    files_sorted = defaultdict(list)
    for root, folders, files in os.walk(folder_to_search):
        for fl in files:
            files_sorted[os.path.basename(fl).split(".")[1].lower()].append(f"{root}/{fl}")
    #Get unique file extension
    print("Found the following unique file extensions:")
    print(list(files_sorted.keys()))
    #Calculate the size of files meeting one of these file extension
    print("The total number and size of files meeting one of these file extension")
    img_format=['mp4', 'png', 'jpg', 'mov', 'bmp','mpg','cMDX']
    valc = defaultdict(list)
    summary = {"Format": [], "Size (GB)": [ ], "Total files": []}
    total_values = []
    
    for k in img_format:
        sum_data=0
        files = files_sorted[k]
        #files.set_description_str(k)
        for fl in files:
            valc[k].append(os.path.getsize(fl))
            sum_data = np.sum(valc[k])/1e9
            total_values.append(os.path.getsize(fl))
            #files.set_description_str(f"{k} - total size (GB): {sum_data:0.2f}")
        summary["Format"].append(k)
        summary["Total files"].append(len(files))
        summary["Size (GB)"].append(sum_data)
        
    total_size =sum(total_values)/1e9
    total_file_list =sum(summary["Total files"])
    print(f"Total size of all files {total_file_list} (GB): " + "{:0.2f}".format(total_size))
    return pd.DataFrame(summary)
print(CountTheFilesAndCalculateTheirSize(folder_to_search))

#Check the files in each folder
print("Check the files in each folder")
folders_to_search = [f"{folder_to_search}/{f}" for f in os.listdir(folder_to_search) if os.path.isdir(f"{folder_to_search}/{f}")]
print(folders_to_search)

for folder in folders_to_search:
    print("*"*100)
    print(CountTheFilesAndCalculateTheirSize(folder))
print("")
print("*"*100)
print("Check cases")
print("*"*100)
folders_to_search = [f for f in os.listdir(folder_to_search) if os.path.isdir(f"{folder_to_search}/{f}")]
for exclude_folder in ["InformedConsents"]:
    folders_to_search.remove(exclude_folder)
#1. Get the unique patient id
collection_data = []
data_present = defaultdict(dict)
for folder_ in folders_to_search:
    
    folder = f"{folder_to_search}/{folder_}"
    folders_to_search_case = [f"{folder}/{f}" for f in os.listdir(folder) if os.path.isdir(f"{folder}/{f}")]
    print(folder," | cases no.:",len(folders_to_search_case))
    try:
        cases=[(f.split("/")[-1].split("_")[0]) for f in folders_to_search_case]
        complete_foldername=[f.split("/")[-1].split("_") for f in folders_to_search_case]
        patients = set(cases)
        
        for pt in patients:
            data_present[pt][folder_]=f"{cases.count(pt)}|"+" ".join([f[2] for f in complete_foldername if pt == f[0]])
        print("No. unique patients",len(patients))
    except:
        print("Can not determine any unique cases ")
    print("*"*100)

pat_id = list(data_present.keys())
columnes = []
for key in data_present:
    for v in data_present[key]:
        columnes.append(v)
columnes=set(columnes)

data_table = defaultdict(list)
for pat in pat_id:
    data_table["PID"].append(pat)
    case_counter=0
    for col in columnes:
        if col in data_present[pat]:
            case_counter+= int(data_present[pat][col].split("|")[0])
            data_table[col].append(data_present[pat][col])
        else:
            data_table[col].append(0)
    data_table["NoOfCases"].append(case_counter)
print("")
print("*"*10)
print("Total no. cases",sum(data_table["NoOfCases"]))
print("Total no. pat.",len(data_table["NoOfCases"]))
print("*"*10)
data_table_B=pd.DataFrame(data_table)
data_table_B.to_csv(f"{folder_to_search}/{folder_to_search}_PatientSummary.csv", index=False)
data_table_B
# %%
