# **DO NOT** edit these variables unless you know what you're doing.

# The extensions that exiftool can generate metadata for and that are valid to upload to OD.
VALID_EXTENSIONS = {"png", "jpg", "jpeg", "tif", "tiff"}
# This is the string exiftool adds to original versions of file names after the file was 
# edited (i.e. after alt text was added). Used to find backups to delete in cleanup.py.
BACKUP_ENDING = "_original"

# -------------------------------------------------------------------------------------------------------------------

# **DO** edit these variables as you see fit.

# Uncomment the model you want to use. Use gemma4:31b for the Ollama Cloud API, and any other model to run locally
# Or add your own model by just following the same formatting, with MODEL = "your model"

# MODEL = "qwen2.5vl:7b" # Better, slower model
# MODEL = "qwen2.5vl:3b" # Decent performance, medium speed
# MODEL = "moondream" # Worse, faster model
MODEL = "gemma4:31b" # Only vision model for free Ollama Cloud API

# Set this to True if you're using a cloud model. Set it to False if you're locally running one.
CLOUD_MODEL = True

# This is the prompt sent to the model to generate your alt text. Edit as you need for different subjects.
# Recommend keeping "write one concise alt-text sentence" and "Do not guess sex" if relevant, 
# but feel free to  experiment.
PROMPT = (
    "Write one concise alt-text sentence for this sports photo. "
    "Present tense, active voice. No 'image of' or 'picture of.' "
    "Describe the specific action or moment shown (e.g. mid-jump, "
    "completing a formation, starting a race) rather than a generic pose. "
    "Do not guess the sex of athletes."
)