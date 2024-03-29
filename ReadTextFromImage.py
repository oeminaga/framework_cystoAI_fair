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
import pytesseract
from PIL import Image
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
#%%
data=pd.read_csv("../Data/SummaryReportImages.csv")
#%%
Texts = []
for i, row in tqdm(data.iterrows()):
    if row.IDENTIFICATION.lower() in ["path", "op", "path2","path1", "op1", "op2", "op3"]:
        img=cv2.imread(row.FullPath)
        img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'--oem 3 --psm 6'
        text_b=pytesseract.image_to_string(img, config=custom_config)
        Texts.append(text_b)
    else:
        Texts.append("")
#%%
data["TEXT"]=Texts
data.to_csv("../Data/SummaryReportImagesWithTextForPathOP.csv", index=False)
# %%
