#%%
 #!/usr/bin/env python3
import pandas as pd
import numpy as np
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

parser = argparse.ArgumentParser(description='User Interface for image labelling')
parser.add_argument("--csv", help="provide the csv file with a column FullPath.")
parser.add_argument("--src", help="provide the folder from which the images.")
parser.add_argument("--dst", help="provide the folder to which the extracted images are stored.")

args = parser.parse_args()

if __name__ == "__main__":
    print(args)
    cmd=ExtractData(args.csv,args.src,args.dst)
    cmd.Run()