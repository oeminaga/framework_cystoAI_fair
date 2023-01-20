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


# %%
def GetPandasDataFrameRemovedPHI(filename : str):
    """
    Mandatory column names in the csv file are:
    DATE %m%d%Y
    ID
    CASE_ID
    Filename
    FullPath
    """
    data=pd.read_csv(filename)
    data["DATE_TIME"]=pd.to_datetime(data["DATE"], format="%m%d%Y")
    data_=data.sort_values(by=["ID", "DATE"])
    to_process=data.drop_duplicates(["CASE_ID"])
    ID_VA=to_process.ID.unique().tolist()
    dict_key = {}
    seq_key = {}
    for key in ID_VA:
        itms=to_process[to_process.ID==key]
        for i,(_, itm) in enumerate(itms.iterrows()):
            case_id=itm["CASE_ID"]
            typ_=case_id.split("_")[1]
            dict_key[case_id]=f"{key}_{typ_}_{i+1}"
            seq_key[case_id]=f"{i+1}"
    data_["CASE_ID_ANYON"] = data_.CASE_ID
    data_.CASE_ID_ANYON.replace(dict_key, inplace=True)
    data_["Filename_ANYON"] = data_.Filename
    data_.Filename_ANYON.replace(dict_key, regex=True,inplace=True)
    data_["SEQ_ID_ANYON"] = data_.CASE_ID
    data_.SEQ_ID_ANYON.replace(seq_key, inplace=True)
    data_complete_ready_for_copy_process=data_#.sort_values(by=["CASE_ID"])
    del data_["FullPath"]
    del data_["Filename"]
    del data_["CASE_ID"]
    del data_["DATE_TIME"]
    del data_["DATE"]
    data_=data_.rename(columns={"CASE_ID_ANYON":"CASE_ID",
                        "Filename_ANYON":"Filename",
                        "SEQ_ID_ANYON":"SEQ_ID"
                        })
    data_["FullPath"]=data_["CASE_ID"]+"/"+data_["Filename"]
    data_complete_and_ready_to_share=data_#.sort_values(by=["CASE_ID"])
    return data_complete_ready_for_copy_process,data_complete_and_ready_to_share