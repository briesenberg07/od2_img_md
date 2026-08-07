# od_img_md
Script to embed metadata in image files for ingest in Oregon Digital

## How to Use

1. Run make_delimited
```zsh
python make_delimited.py
```
Enter the path to the top-level importer folder (the one that contains files/ and your metadata csv) when prompted.

2. Write alt text for each file as desired in the 'alt_text' column and save
3. Run embed_tags2.py
```zsh
python embed_tags2.py
```

Enter the path to the top-level importer folder, just like before, when prompted. You should see each file printed in the terminal as it's processed.

4. Run check_alt_text.py to ensure it added it correctly
```zsh
python check_alt_text.py
```
Enter the path to the files/ folder, *not* the top-level importer folder. You should see the alt text and image description for each image in the terminal, or "MISSING" if there is none.

5. Run cleanup.py to move all backups to the backups/ folder
```zsh
python cleanup.py
```
Enter the path to the files/ folder with images (with backups inside to move), and then enter the path to the folder you'd like to create the backups/ folder in. 

NOTE: if you already have a backups folder this will cause an error, to avoid accidentally moving multiple backups to the same place.




