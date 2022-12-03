#%%
from collections import defaultdict
from numpy import isin
import pandas as pd
import os
import json
import datetime
import shutil
from tqdm import tqdm
#%%
class Validation():
    def __init__(self, source="",policy_name="CystoscopyImages",folder_to_consider= ["InComplete_IncompleteLabels", "InComplete_NoScreenShots", "InComplete_NotLabelled"]) -> None:
        #Load validation policy
        self.folder_to_consider=folder_to_consider
        self.source =source
        self.policy_name=policy_name
        with open("validation.json", "r") as f:
            self.policy=json.loads(f.read())
    def Check(self, policy_name, itm, value):
        if isinstance( self.policy[policy_name][itm], list):
            if value in self.policy[policy_name][itm]:
                return True, []
            else:
                values_ =value.split(self.policy[policy_name]["ContainerSplitter"])
                correct_b = 0
                if len(values_)>1:
                    for vl in values_:
                        if vl in self.policy[policy_name][itm]:
                            correct_b+=1
                if correct_b == len(values_):
                    return True, []
                return False, f"Err: {value} not found or incorrect provided"
        if isinstance(self.policy[policy_name][itm],dict):
            status = False
            for key in self.policy[policy_name][itm]:
                if self.policy[policy_name][itm][key][0]=="STOP":
                    if key.lower() == value[:len(key)].lower():
                        status=True
                if self.policy[policy_name][itm][key][0]=="nummeric":
                    if key.lower() == value[:len(key)].lower():
                        if isinstance(int(value[len(key):].split("-")[0]), int):
                            status=True
                if self.policy[policy_name][itm][key][0]=="string":
                    if key.lower() == value[:len(key)].lower():
                        status = True
                
                if status:
                    return status, self.policy[policy_name][itm][key][1]
            return status, f"Err: {value} not identified"

        if self.policy[policy_name][itm] == "string":
            return isinstance(value, str), []
        if "%" in self.policy[policy_name][itm]:
            try:
                datetime.datetime.strptime(value, self.policy[policy_name][itm])
                return True, []
            except:
                return False, "Date format is not correct"

    def CheckCase(self, folder, policy_name="CystoscopyImages"):
        NoIssue = False
        reports = {"FOLDER": [], "Filename": [], "INFO": []}
        if self.policy[policy_name]["CheckFolder"]:
            #1. Check the case folder format
            subfolders = [f for f in os.listdir(folder) if os.path.isdir(f"{folder}/{f}")]
            if len(subfolders)==0:
                reports["FOLDER"].append(folder)
                reports["Filename"].append("")
                reports["INFO"].append("No folder")
                return "No folder" ,reports
            subfolder_counter =0 
            itm_folders = self.policy[policy_name]["FolderArchitecture"]
            target_no_folders = len(itm_folders)
            for subfolder in subfolders:
                if subfolder.lower() in itm_folders:
                    subfolder_counter+=1
            if subfolder_counter!=target_no_folders:
                reports["FOLDER"].append(folder)
                reports["Filename"].append("")
                reports["INFO"].append("the case folder does not meet folder architecture")
                return "the case folder does not meet folder architecture",reports
            
            
            itms = folder.split("/")[-1].split(self.policy[policy_name]["FolderNameSplitter"])
            if len(itms) != len(self.policy[policy_name]["FolderNameFormat"]):
                reports["FOLDER"].append(folder)
                reports["Filename"].append("")
                reports["INFO"].append("the case folder does not meet the standard format for the case folder")
                return "the case folder does not meet the standard format for the case folder",reports
            
            for i, itm in enumerate(self.policy[policy_name]["FolderNameFormat"]):
                status, msg =self.Check(policy_name, itm, itms[i])
                if status==False:
                    reports["FOLDER"].append(folder)
                    reports["Filename"].append("")
                    reports["INFO"].append(msg)
                    return msg, reports

        #2. Check the video filename format
        if self.policy[policy_name]["CheckVideoFileNameormat"]: 
            vid_folders = self.policy[policy_name]["VideoFolder"]
            SupportedVideoFormat= self.policy[policy_name]["SupportedVideoFormat"]

            for vid_fold in vid_folders:
                video_folder = f"{folder}/{vid_fold}"
                video_files = [f for f in os.listdir(video_folder) if os.path.isfile(f"{video_folder}/{f}") and f.split(".")[1] in SupportedVideoFormat and f.lower() != ".ds_store"]
                for fl in video_files:
                    itms = os.path.basename(fl).split(".")[0].split(self.policy[policy_name]["VideoNameSplitter"])
                    if len(itms) < len(self.policy[policy_name]["VideoNameFormat"]):
                        reports["FOLDER"].append(folder)
                        reports["Filename"].append(fl)
                        reports["INFO"].append("not meeting the standard format for video")
                        print(f"ERR {folder}: {fl} is not meeting the standard format for video")
                        NoIssue=False
                        continue
                    
                    for i, key in enumerate(self.policy[policy_name]["VideoNameFormat"]):
                        #print(itms)
                        #print(self.policy[policy_name]["VideoNameFormat"])
                        status, msg = self.Check(policy_name, key, itms[i])
                        if status==False:
                            NoIssue=False
                            print(f"ERR {folder}: ",msg)
                            reports["FOLDER"].append(folder)
                            reports["Filename"].append(fl)
                            reports["INFO"].append(f"{key}_{msg}")
                        else:
                            NoIssue=True
                            reports["FOLDER"].append(folder)
                            reports["Filename"].append(fl)
                            reports["INFO"].append(f"{key}_OK")

            
        #3. Check the image filename format
        if self.policy[policy_name]["CheckImageFileNameFormat"]:
            img_folders = self.policy[policy_name]["ImageFolder"]
            SupportedImageFormat= self.policy[policy_name]["SupportedImageFormat"]
            for img_fold in img_folders:
                img_folder = f"{folder}/{img_fold}"
                img_files = [f for f in os.listdir(img_folder) if os.path.isfile(f"{img_folder}/{f}") and f.split(".")[1] in SupportedImageFormat and f.lower() != ".ds_store"]
                for fl in img_files:
                    itms = os.path.basename(fl).split(".")[0].split(self.policy[policy_name]["Splitter"])
                    if len(itms) < len(self.policy[policy_name]["MinImageFileNameFormat"]):
                        reports["FOLDER"].append(folder)
                        reports["Filename"].append(fl)
                        reports["INFO"].append("not meeting the standard format for images")
                        NoIssue=False
                        print(f"ERR {folder}: {fl} is not meeting the standard format for images")
                        continue
                    for i, key in enumerate(self.policy[policy_name]["MinImageFileNameFormat"]):
                        status, msg = self.Check(policy_name, key, itms[i])
                        if status==False:
                            reports["FOLDER"].append(folder)
                            reports["Filename"].append(fl)
                            reports["INFO"].append(msg)
                            NoIssue=False
                            print(f"ERR {folder}: ",msg)
                        
                        if not isinstance(msg, list):
                            if status:
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append("OK")
                            continue
                        if len(msg)==0:
                            if status:
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append("OK")
                            else:
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append("Something happend..")

                        for mg in msg:
                            ind_f=self.policy[policy_name]["MaxImageFileNameFormat"].index(mg)
                            if len(itms)<=ind_f:
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append("has lesser information than expected...")
                                NoIssue=False
                                print(f"ERR {folder}: {fl} has lesser information than expected...")
                                break
                            status, msg = self.Check(policy_name, mg, itms[ind_f])
                            if status==False:
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append(msg)
                                NoIssue=False
                                print(f"ERR {folder}: ",msg)
                            else:
                                NoIssue=True
                                reports["FOLDER"].append(folder)
                                reports["Filename"].append(fl)
                                reports["INFO"].append("OK")
        return NoIssue, reports

    def RunValidation(self,executeMovingCaseFoldersWhenComplete=False):

        self.folders_to_consider =[f"{self.source}/{f}" for f in os.listdir(self.source) if os.path.isdir(f"{self.source}/{f}") and f in self.folder_to_consider]
        report_collector = defaultdict(list)
        folder_to_copy = self.policy[self.policy_name]["MoveWheMeetThePolicyTo"][0]
        for folder in self.folders_to_consider:
            cases =[[f, f"{folder}/{f}"] for f in os.listdir(folder) if os.path.isdir(f"{folder}/{f}")]
            prog = tqdm(cases)
            prog.set_description(folder)
            for case in prog:
                status, msg =self.CheckCase(case[1],self.policy_name)
                if isinstance(msg, dict):
                    for key in msg:
                        report_collector[key].extend(msg[key])
                if isinstance(status, bool):
                    if status and executeMovingCaseFoldersWhenComplete:
                        shutil.copytree(case, f"{self.source}/{folder_to_copy}/{case[0]}")

        pd.DataFrame(report_collector).to_csv("ValidationReport_Files.csv")

# %%
test_unit=True
if test_unit:
    val=Validation("../Data")
    val.RunValidation()
