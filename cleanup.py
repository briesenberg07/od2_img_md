"""Remove any backup files from a specified directory"""
from pathlib import Path
import sys


def main():
    deleted_count = 0

    # Get files/ path
    target_dir = Path(input("Enter the files/ directory path:\n>>> "))

    # Delete each file ending in .tif_original in the directory
    for file_path in target_dir.glob("*.tif_original"):
        file_path.unlink()
        print(f"Deleted {file_path}")
        deleted_count += 1
    
    print(f"Deleted {deleted_count} backups")

if __name__ == "__main__":
    main()