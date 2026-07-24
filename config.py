# The extensions that exiftool can generate metadata for and that are valid to upload to OD
VALID_EXTENSIONS = {"png", "jpg", "jpeg", "tif", "tiff"}
# The string exiftool adds to original versions of file names after the file was edited. Used to find backups to delete
BACKUP_ENDING = "_original"