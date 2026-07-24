from pathlib import Path
from subprocess import run
import os
import json
from config import VALID_EXTENSIONS

def main():
    # Get path from user
    path_input = input("Enter the path to the files folder containing images: ")
    path = Path(path_input)

    # Build files list from files/ folder
    files = [
        entry.path
        for entry in os.scandir(path)
        if entry.is_file() and Path(entry.name).suffix.lower().lstrip(".") in VALID_EXTENSIONS
    ]
    if not files:
        print("No files found")
        return

    # Check each file for alt text
    for file_path in files:
        result = run(
            [
                "exiftool",
                "-j",
                "-EXIF:ImageDescription",
                "-XMP:AltTextAccessibility", # -XMP-iptcCore:AltTextAccessibility seems to work just as well
                file_path,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        # Print results
        data = json.loads(result.stdout)[0]
        print("File:", data.get("SourceFile"))
        print("ImageDescription:", data.get("ImageDescription", "MISSING"))
        print("AltTextAccessibility:", data.get("AltTextAccessibility", "MISSING"))

if __name__ == "__main__":
    main()