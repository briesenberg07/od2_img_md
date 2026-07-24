"""Remove any backup files from a specified directory"""
from pathlib import Path
import sys
from config import VALID_EXTENSIONS, BACKUP_ENDING


def main():
    deleted_count = 0

    # Get files/ path
    target_dir = Path(input("Enter the files/ directory path:\n>>> "))

    # Delete each file ending in .[file format]_original in the directory
    for ext in VALID_EXTENSIONS:
        for file_path in target_dir.glob(f"*.{ext}{BACKUP_ENDING}"): # FIXME: Have to change this each time because no tuple allowed here
            file_path.unlink()
            print(f"Deleted {file_path}")
            deleted_count += 1
    
    print(f"Deleted {deleted_count} backups")

if __name__ == "__main__":
    main()