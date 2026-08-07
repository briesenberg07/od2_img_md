"""Embed alt text and image description tags into tifs in a given folder"""
from pathlib import Path
from csv import DictReader
from subprocess import run
from config import VALID_EXTENSIONS

def main():
    # Get directory path
    input_string = input("enter absolute path to directory containing files/ and alt_text.csv\n>>> ")
    path = Path(input_string)
    data = Path(input_string, "alt_text.csv")

    # Add corresponding alt text to each file
    with open(data, "r") as csvf:
        reader = DictReader(csvf)
        for row in reader:

            # Add alt text and image description to each file (take from csv)
            if row['file'].split('.')[-1].lower() in VALID_EXTENSIONS:
                asset = Path(input_string, "files", row["file"])

                # Build exiftool command
                comlist = ["exiftool",
                        f"-XMP-iptcCore:AltTextAccessibility={row['alt_text']}",
                        f"-ImageDescription={row['alt_text']}", 
                        asset]
                # Run exiftool command
                result = run(comlist, capture_output=True, text=True)

                # Show results
                if result.stdout:
                    print(f"STDOUT for {asset}:")
                    print(result.stdout.strip())

                if result.stderr:
                    print(f"STDERR for {asset}:")
                    print(result.stderr.strip())

                if result.returncode != 0:
                    print(f"ExifTool failed for {asset} with code {result.returncode}")
if __name__ == "__main__":
    main()