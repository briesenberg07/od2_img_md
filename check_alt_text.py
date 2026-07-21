from pathlib import Path
from subprocess import run
import exiftool
import os

def main():
    # Get path from user for files/ folder
    path_input = input("Enter the path to the files folder containing images: ")
    path = Path(path_input)

    # Make files list
    files = [entry.path for entry in os.scandir(path) if entry.is_file() and entry.name.lower().endswith((".tif", ".tiff"))]
    if not files:
        print("No files found")
        return

    # Read file(s) metadata
    with exiftool.ExifToolHelper() as et:
        metadata = et.get_tags(files, tags=["XMP-iptcCore:AltTextAccessibility", "ImageDescription"]) # Note: no leading - in tags here, unlike command line
        # Print alt text field value for each image
        for d in metadata:
            print("File: ", d.get("SourceFile"))
            print("Alt Text: ", d.get("XMP-iptcCore:AltTextAccessibility", "MISSING"))
            print("Image Description: ", d.get("ImageDescription", "MISSING"))
        #FIXME: save missing ones to summarize at bottom

if __name__ == "__main__":
    main()