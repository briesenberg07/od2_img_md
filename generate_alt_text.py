import subprocess
from pathlib import Path
import ollama
from ollama import Client
from config import VALID_EXTENSIONS, MODEL, PROMPT, CLOUD_MODEL
import os
from io import BytesIO
from PIL import Image
from csv import DictReader, DictWriter
from dotenv import load_dotenv

load_dotenv()

# Set up Ollama API if using cloud model
if CLOUD_MODEL:
    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
    )

def main():
    # Get images path
    path_input = input("Enter the path to the files folder containing images\n>>> ")
    alt_text_input = input("Enter the path to the alt text file to edit\n>>> ")
    path = Path(path_input)

    alt_text_path = Path(alt_text_input)
    if not alt_text_path.is_file():
        print(f"Alt text CSV not found at {alt_text_path}")
        return
    with alt_text_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = DictReader(csv_file)
        fieldnames = reader.fieldnames
        rows = list(reader)
    if not fieldnames or "file" not in fieldnames or "alt_text" not in fieldnames:
        print("CSV must contain 'file' and 'alt_text' columns")
        return

    # Build valid files list from given folder
    files = [
    Path(entry.path)
    for entry in os.scandir(path)
    if entry.is_file()
    and Path(entry.name).suffix.lower().lstrip(".") in VALID_EXTENSIONS
    ]

    for img_path in files:
        # Resize and convert image to JPEG (vision-readable format)
        with Image.open(img_path) as image:
            print(f"Processing {img_path.name}...")
            image = image.convert("RGB")
            image.thumbnail((1024, 1024))
            image_buffer = BytesIO()
            image.save(image_buffer, format="JPEG", quality=85)

        # Generate alt text for image
        # Use client.chat for cloud models
        if CLOUD_MODEL:
            response = client.chat(            
                model=MODEL,
                options={"num_ctx": 4096},
                messages=[{
                    "role": "user",
                    "content": PROMPT,
                    "images": [image_buffer.getvalue()],
                }],
            )
        # Use ollama.chat for local running
        else:
            response = ollama.chat(
                model=MODEL,
                options={"num_ctx": 4096},
                messages=[{
                    "role": "user",
                    "content": PROMPT,
                    "images": [image_buffer.getvalue()],
                }],
                )

        #FIXME: check that alt text file exists at start, then edit fields here 
        # as you go rather than printing
        alt_text = response["message"]["content"].strip()

        # Uncomment for testing
        # print(f"{img_path.name}: {alt_text}")
        
        # Write alt text to csv
        row = next((row for row in rows if row["file"] == img_path.name),None,)

        if row is None:
            print(f"No CSV row found for {img_path.name}")
            continue

        row["alt_text"] = alt_text

        with alt_text_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Updated {img_path.name}: {alt_text}")
        

if __name__ == "__main__":
    main()