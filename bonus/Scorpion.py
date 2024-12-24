import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return {"Error": "No EXIF data found in this image."}
        
        exif_info = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_info[tag_name] = value

        return exif_info
    except Exception as e:
        return {"Error": f"Error reading EXIF data: {e}"}

def get_file_metadata(file_path):
    try:
        file_stats = os.stat(file_path)
        creation_date = os.path.getctime(file_path)
        metadata = {
            "File Name": os.path.basename(file_path),
            "File Size (bytes)": file_stats.st_size,
            "Creation Date": creation_date
        }
        return metadata
    except Exception as e:
        return {"Error": f"Error retrieving file metadata: {e}"}

def display_metadata(file_path):
    if not os.path.isfile(file_path):
        return [f"Error: {file_path} is not a valid file."]

    allowed_extensions = {".jpg", ".jpeg", ".png", ".tiff"}
    if not any(file_path.lower().endswith(ext) for ext in allowed_extensions):
        return [f"Invalid file format: {file_path}"]

    result = []
    result.append(f"\n--- Metadata for {file_path} ---")
    result.append("-" * 50)

    file_metadata = get_file_metadata(file_path)
    result.append("File Information:")
    for key, value in file_metadata.items():
        result.append(f"{key: <20}: {value}")
    result.append("-" * 50)

    exif_data = get_exif_data(file_path)
    if isinstance(exif_data, dict):
        result.append("-" * 50)
        result.append("EXIF Information:")
        for key, value in exif_data.items():
            result.append(f"{key: <20}: {value}")
    else:
        result.append(f"\nEXIF Information: {exif_data}")
    result.append("-" * 50)

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py FILE1 [FILE2 ...]")
        return

    files = sys.argv[1:]
    for file_path in files:
        display_metadata(file_path)

if __name__ == "__main__":
    main()
