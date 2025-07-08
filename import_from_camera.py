import os

# AI slop to get me started

def find_dcim_dirs(start_path):
    """
    Recursively search for all directories named 'DCIM' starting from 'start_path'.
    
    Args:
        start_path (str): The root directory to begin searching from.
    
    Returns:
        List[str]: A list of full paths to any 'DCIM' directories found.
    """
    dcim_paths = []

    for root, dirs, files in os.walk(start_path):
        for dir_name in dirs:
            if dir_name.lower() == 'dcim':
                dcim_paths.append(os.path.join(root, dir_name))
    
    return dcim_paths

def list_usb_drives():
    usb_drives = []
    partitions = psutil.disk_partitions()

    for p in partitions:
        # On Windows, removable drives often have 'removable' in the opts
        # On Linux/macOS, you might filter by mount point like /media or /Volumes
        if 'removable' in p.opts.lower() or '/media' in p.mountpoint or '/Volumes' in p.mountpoint:
            usb_drives.append({
                'device': p.device,
                'mountpoint': p.mountpoint,
                'fstype': p.fstype
            })

    return usb_drives

# Example usage
for drive in list_usb_drives():
    print(f"Device: {drive['device']} mounted at {drive['mountpoint']}")