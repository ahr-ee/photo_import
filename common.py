import os
import re
import uuid
import shutil
from datetime import datetime
from pathlib import Path


IMG_EXT = {".jpg", ".jpeg", ".cr2", ".nef", ".arw", ".dng", ".rw2", ".orf", ".raf"}

def sanitize_filename(name, replacement="_"):
    invalid_chars = r'[<>:"/\\|?* ]'
    return re.sub(invalid_chars, replacement, name)

def get_file_creation(path): # WINDOWS ONLY
    timestamp = os.path.getctime(path)
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%B%Y").lower() 

def rename_and_transfer_photos(dcim_dirs: list[Path], output_dir: Path, camera_body: str, lens: str=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    camera_body_clean = sanitize_filename(camera_body)

    for dcim_dir in dcim_dirs:
        print(f"Transferring from {dcim_dir}")
        count = 0
        for file in Path(dcim_dir).rglob("*"):
            if file.is_file() and file.suffix.lower() in IMG_EXT:
                file_uuid = str(uuid.uuid4())
                ext = file.suffix.lower()
                if not lens:
                    new_filename = f"{file_uuid}_{camera_body_clean}{ext}"
                else:
                    lens_clean = sanitize_filename(lens)
                    new_filename = f"{file_uuid}_{camera_body_clean}_{lens_clean}{ext}"

                dir_month = get_file_creation(file)
                destination = output_dir / dir_month / new_filename
                destination_dir = output_dir / dir_month
                os.makedirs(destination_dir, exist_ok=True)
                shutil.copy2(file, destination)
                count+=1
        print(f"Transferred {count} files to {output_dir}")