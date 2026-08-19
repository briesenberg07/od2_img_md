import subprocess
from pathlib import Path
import ollama
from config import VALID_EXTENSIONS
import os
from io import BytesIO
from PIL import Image

#FIXME: This is specifically for uo athletics, not OD broadly. Find general guidelines and update.
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
    path = Path(path_input)

    files = [
    Path(entry.path)
    for entry in os.scandir(path)
    if entry.is_file()
    and Path(entry.name).suffix.lower().lstrip(".") in VALID_EXTENSIONS
]

    # Build files list from files/ folder
    for img_path in files:
        with Image.open(img_path) as image:
            print(f"Processing {img_path.name}...")
            image = image.convert("RGB")
            image.thumbnail((1024, 1024))
            image_buffer = BytesIO()
            image.save(image_buffer, format="JPEG", quality=85)

        response = ollama.chat(
            model="qwen2.5vl:7b", # Better, slower model
            # model="qwen2.5vl:3b", # Decent performance, medium speed
            # model="moondream", # Worse, faster model
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
        print(f"{img_path.name}: {alt_text}")

if __name__ == "__main__":
    main()