import psutil
from pathlib import Path
from dataclasses import dataclass
from common import rename_and_transfer_photos

@dataclass(frozen=True)
class MountpointInfo:
    device: str
    mountpoint: Path
    fstype: str

def validate_and_get_selected_mountpoint(mountpoints: list[MountpointInfo], selected_drive:str):
    for mp in mountpoints:
        if selected_drive in mp.device:
            return mp
    raise RuntimeError('Invalid Selected Mountpoint')

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

def import_photos(args):
    mountpoints: MountpointInfo = get_mountpoints()
    mp: Path = validate_and_get_selected_mountpoint(mountpoints, args.drive.lower())
    dcim_dirs = find_dcim_dirs(mp.mountpoint)
    rename_and_transfer_photos(dcim_dirs, Path(args.dir), args.body, args.lens)
        
def do_import(args):
    import_photos(args)
