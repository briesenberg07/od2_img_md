from pathlib import Path
from csv import DictReader
from subprocess import run

# FIXME -- don't think it can handle single or double quotes in csv cells
# FIXME -- not writing XMP ImageDescription to PNG files!

# REQ'D
# absolute_path/
#   files/ # assets to process
#   alt_text.csv # w headers 'file' and 'alt_text'
# some kind of check for this ^^^?

# some option to clean up backups?

str = input("enter absolute path to directory containing files/ and alt_text.csv\n>>> ")
path = Path(str)
data = Path(str, "alt_text.csv")
with open(data, "r") as csvf:
    print("Successfully opened csv")
    reader = DictReader(csvf)
    # print(f"Reader: {reader[0]}")
    for row in reader:
        if row['file'].split('.')[-1].lower() in ["jpg", "tif", "tiff", "png"]:
            print("Found file type")
            asset = Path(str, "files", row["file"])
            print(asset)
            comlist = ["exiftool",
                       f"-XMP-iptcCore:AltTextAccessibility={row['alt_text']}",
                       f"-ImageDescription={row['alt_text']}", 
                       asset]
            run(comlist, capture_output=True)
        else:
            print("No files detected in csv")

print("Finished")

# do something with captured output? log, etc.?
