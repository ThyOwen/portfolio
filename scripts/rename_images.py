# %%
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--path", help = "path to images to be renamed", required=True)

args = parser.parse_args()

path = args.path

for file in os.listdir(path):
    if file[0] == "_":
        rename = file[1:-4] + "_" + file[-4:]
        os.rename(path + file, path + rename)
