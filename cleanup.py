"""Remove any backup files from a specified directory"""
from pathlib import Path
import sys
from config import VALID_EXTENSIONS, BACKUP_ENDING
import shutil


def main():
    moved_count = 0

    # Get files/ path
    files_path = Path(input("Enter the path to the images folder (files/):\n>>> "))
    if not files_path.is_dir():
        print(f"Failure: {files_path} is not a directory")
        return

    # Get work directory (where backups/ folder will go)
    work_path = Path(input("Enter the path to the importer folder containing files/ and alt_text.csv, where backups should be made:\n>>> "))
    if not work_path.is_dir():
            print(f"Failure: {work_path} is not a directory")
            return

    # Create backups folder
    backups_path = work_path / "backups"
    backups_path.mkdir() # Errors if backups folder already exists -- can turn this off if desired

    # Move each file ending in .[file format]_original in the directory to a backups/ directory
    for ext in VALID_EXTENSIONS:
        for file_path in files_path.glob(f"*.{ext}{BACKUP_ENDING}"):
            shutil.move(file_path, backups_path)
            print(f"Moved {file_path}")
            moved_count += 1

    print(f"Moved {moved_count} backups to {backups_path}")

if __name__ == "__main__":
    main()