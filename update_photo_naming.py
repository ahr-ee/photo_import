from pathlib import Path
from common import rename_and_transfer_photos

def validate_input_directory(input_directory: str):
    in_dir = Path(input_directory)
    if in_dir.is_dir():
        return in_dir
    raise RuntimeError('Invalid Input Directory')

def fromat_single_dir(start_path: Path):
    path_list = [start_path] # HACK!
    return path_list

def import_photos(args):
    indir: Path = validate_input_directory(args.indir)
    path_list = fromat_single_dir(indir)
    rename_and_transfer_photos(path_list, Path(args.dir), args.body, args.lens)
        
def do_update(args):
    import_photos(args)
