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
import pandas as pd
import os
#%%
#Get
#1. Check if SummaryReportImagesWithTextForPathOP exits to use otherwise conisder SummaryReportImages
data  = None
filename="../Data/SummaryReportImagesWithTextForPathOP.csv"
if not os.path.exists(filename):
    filename="../Data/SummaryReportImages.csv"
data=pd.read_csv(filename)
data=data.drop(["Unnamed: 0"], axis=1)
#%%
cMDX_Report = pd.read_csv("ReportCasesWithcMDXFils.csv")
#ID	IND	DATE	IDENTIFICATION	LOCATION	ImageModality	PATHOLOGY	STAGE	Filename	FullPath	CASE_ID	TEXT
#,CML,DATE,CaseID,cMDX_Filename,cMDX_FilePath
for i, itm in cMDX_Report.iterrows():
    row ={"ID":[str(itm.CML)], 
    "IND": ["O"], 
    "DATE": [str(itm.DATE)],
    "IDENTIFICATION": ["cMDX_MAP"], 
    "LOCATION": [""], 
    "ImageModality":[""],
    "PATHOLOGY":[""],
    "STAGE": [""], 
    "Filename": [itm.cMDX_Filename], 
    "FullPath": [itm.cMDX_FilePath],
    "CASE_ID" : [itm.CaseID],
    "TEXT":[""]}
    data=data.append(pd.DataFrame(row))
data.to_csv("../Data/SummaryReportImagesWithTextForPathOPAndcMDX.csv", index=False)
