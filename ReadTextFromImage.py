#%%
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
# %%
Texts
#%%
data["TEXT"]=Texts
data.to_csv("../Data/SummaryReportImagesWithTextForPathOP.csv")
# %%
