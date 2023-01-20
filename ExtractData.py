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
import pandas as pd
import os
import shutil
from tqdm import tqdm

#%%
import argparse
class ExtractData():
    def __init__(self, csv_filename, source, destination) -> None:
        self.csv_filename = csv_filename
        self.source = source
        self.destination = destination
    def Run(self):
        filenames = []
        data=pd.read_csv(self.csv_filename)
        if os.path.exists(self.source):
            os.mkdir(os.path.join(self.source, "images"))
        for filename in tqdm(data["FullPath"]):
            src=filename
            fl_=os.path.basename(filename)
            dst=os.path.join(self.destination, "images", fl_)
            shutil.copyfile(src, dst)
            filenames.append(fl_)
        data["OriginFullPath"]=data["FullPath"]
        data["FullPath"]=filenames
        print("PROC: SAVING...")
        data.to_csv(os.path(self.destination, "master_data.csv"))
        print("INFO: DONE")

parser = argparse.ArgumentParser(description='Data Extraction script')
parser.add_argument("--csv", help="provide the csv file with a column FullPath.")
parser.add_argument("--src", help="provide the folder from which the images.")
parser.add_argument("--dst", help="provide the folder to which the extracted images are stored.")

args = parser.parse_args()

if __name__ == "__main__":
    print(args)
    cmd=ExtractData(args.csv,args.src,args.dst)
    cmd.Run()