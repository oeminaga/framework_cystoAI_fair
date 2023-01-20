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
import os
import cv2
import matplotlib
#%%
source="../BladderMap"
files = [f for f in os.listdir(source)]
data = {"CML":[], "DATE":[], "CaseID":[], "cMDX_Filename": [], "cMDX_FilePath":[]}

for fl in files:
    row=fl.split(".")[0].split("-")
    data["CML"].append(row[0])
    data["DATE"].append("".join(row[-3:]))
    data["CaseID"].append(f"{row[0]}_O_"+"".join(row[-3:]))
    data["cMDX_Filename"].append(fl)
    data["cMDX_FilePath"].append(f"{source}/{fl}")
# %%
import pandas as pd
pd.DataFrame(data).to_csv("ReportCasesWithcMDXFils.csv", index= False)
# %%
