import uuid
import psutil
import shutil
import argparse
from pathlib import Path
import re
from dataclasses import dataclass
from collections import defaultdict

@dataclass(frozen=True)
class MountpointInfo:
    device: str
    mountpoint: Path
    fstype: str

def parse_args():
    parser = argparse.ArgumentParser(
        description="Import tool for extracting photos from DCIM folders on USB devices."
    )

    parser.add_argument(
        "-d", "--drive",
        required=True,
        help="Drive (mountpoint) to search for DCIM folders. (e.g. 'F' or 'G')"
             "If not provided, all USB devices will be scanned."
    )

    parser.add_argument(
        "-b", "--body",
        required=True,
        help="Camera body (e.g., 'Canon R6', 'Nikon D850'). Required."
    )

    parser.add_argument(
        "-l", "--lens",
        default=None,
        help="Lens used (e.g., '24-70mm f/2.8'). If not specified, assumes point-and-shoot or cellphone."
    )

    parser.add_argument(
        "-o", "--dir",
        required=True,
        help="Output directory. Required."
    )

    return parser.parse_args()

def validate_and_get_selected_mountpoint(mountpoints: list[MountpointInfo], selected_drive:str):
    for mp in mountpoints:
        if selected_drive in mp.device:
            return mp
    raise RuntimeError('Invalid Selected Mountpoint')

def sanitize_filename(name, replacement="_"):
    invalid_chars = r'[<>:"/\\|?* ]'
    return re.sub(invalid_chars, replacement, name)

def find_dcim_dirs(start_path: Path):
    dcim_paths = []

    for path in start_path.rglob("*"):
        if path.is_dir() and path.name.lower() == "dcim":
            dcim_paths.append(path)

    return dcim_paths

def get_mountpoints()-> list[MountpointInfo]:
    mountpoint_info_list = []
    partitions = psutil.disk_partitions()

    for p in partitions:
        if 'removable' in p.opts.lower() or '/media' in p.mountpoint or '/Volumes' in p.mountpoint:
            mountpoint_info_list.append(MountpointInfo(device=p.device.split(':', 1)[0].lower(), mountpoint=Path(p.mountpoint), fstype=p.fstype))

    return mountpoint_info_list

def rename_and_transfer_photos(dcim_dirs: list[Path], output_dir: Path, camera_body: str, lens: str=None):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    camera_body_clean = sanitize_filename(camera_body)

    image_extensions = {".jpg", ".jpeg", ".cr2", ".nef", ".arw", ".dng", ".rw2", ".orf", ".raf"}
    grouped_files = defaultdict(list)


    # SOOOOOO SLOW BAD BAD BAD BAD BAD
    for dcim_dir in dcim_dirs:
        for file in Path(dcim_dir).rglob("*"):
            if file.is_file() and file.suffix.lower() in image_extensions:
                grouped_files[file.stem].append(file)

    for files in grouped_files.values():
        file_uuid = str(uuid.uuid4())
        ext = file.suffix.lower()
        for file in files:
            if not lens:
                new_filename = f"{file_uuid}_{camera_body_clean}{ext}"
            else:
                lens_clean = sanitize_filename(lens)
                new_filename = f"{file_uuid}_{camera_body_clean}_{lens_clean}{ext}"
            destination = output_dir / new_filename
            shutil.copy2(file, destination)

    print(f"Transferred {sum(len(files) for files in grouped_files.values())} files to {output_dir}")

def import_photos():
    args = parse_args()
    mountpoints: MountpointInfo = get_mountpoints()
    mp: Path = validate_and_get_selected_mountpoint(mountpoints, args.drive.lower())
    dcim_dirs = find_dcim_dirs(mp.mountpoint)
    rename_and_transfer_photos(dcim_dirs, Path(args.dir), args.body, args.lens)
        
if __name__ == '__main__':
    import_photos()
