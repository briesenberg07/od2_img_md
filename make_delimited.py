"""Create an alt_text.csv document with a row for every tif file in the files/ folder"""
from pathlib import Path
from os import listdir
import pandas as pd


def main():
    # absolute_path/
    #   files/ # assets to process

    input_str = input("Enter absolute path to top-level importer folder\n>>> ")
    files = Path(input_str, "files")
    fileseries = [file for file in listdir(files)]
    blankseries = [None for file in listdir(files)]

    # make alt text spreadsheet
    alt_text_data = {"file": fileseries, "alt_text": blankseries}
    dfat = pd.DataFrame(data=alt_text_data)
    dfat.to_csv(f"{input_str}/alt_text.csv", index=False)
    print(f"Finished creating csv at {input_str}/alt_text.csv")

if __name__ == "__main__":
    main()