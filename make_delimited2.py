from pathlib import Path
from os import listdir
import pandas as pd

# absolute_path/
#   files/ # assets to process

str = input("enter absolute path to top-level importer folder\n>>>")
files = Path(str, "files")
fileseries = [file for file in listdir(files)]
blankseries = [None for file in listdir(files)]

# make alt text spreadsheet
alt_text_data = {"file": fileseries, "alt_text": blankseries}
dfat = pd.DataFrame(data=alt_text_data)
# FIXME -- eliminate need to have two separate to_csv
dfat.to_csv(f"{str}/alt_text.csv", index=False) # Windows
# dfat.to_csv(f"{str}/alt_text.csv", index=False) # Linux
