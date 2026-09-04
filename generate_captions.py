import subprocess
from pathlib import Path
# import ollama
from ollama import Client
from config import VALID_EXTENSIONS
import os
from io import BytesIO
from PIL import Image
from csv import DictReader, DictWriter
from dotenv import load_dotenv

# MODEL = "qwen2.5vl:7b" # Better, slower model
# MODEL = "qwen2.5vl:3b" # Decent performance, medium speed
# MODEL = "moondream" # Worse, faster model
MODEL = "gemma4:31b" # Only vision model for free Ollama Cloud API

#NOTE: For now, if you want to switch between Ollama Cloud API and local hosting you have to edit not only the model
# but also the 'response = [client / ollama].chat' section. Can be fixed later with a local/client bool and if statement

load_dotenv()

# Set up Ollama API
client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

#FIXME: This is specifically for uo athletics, not OD broadly. Find general guidelines and update. Something like
# "Write one concise alt-text sentence for this image. Present tense, active voice. No 'image of' or 'picture of.'
# Describe the specific action, moment, scene, or item shown rather than a generic statement. 
# Do not guess the sex of people in the image."
PROMPT = (
    "Write one concise alt-text sentence for this sports photo. "
    "Present tense, active voice. No 'image of' or 'picture of.' "
    "Describe the specific action or moment shown (e.g. mid-jump, "
    "completing a formation, starting a race) rather than a generic pose. "
    "Do not guess the sex of athletes."
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

        # For Ollama Cloud API:
        response = client.chat(
        # For local usage:
        # response = ollama.chat(

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