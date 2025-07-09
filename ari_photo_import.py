import argparse
from import_from_camera import do_import
from update_photo_naming import do_update

def parser_factory():

    parser = argparse.ArgumentParser(
        description="Transfer photos from one dir to another, updating the photo names in the process."
    )

    parser.add_argument(
        "action",
        choices=["update", "import"],
        help="Action to perform: 'update' (from old dir into new dir) or 'import' (from camera device)."
    )

    parser.add_argument(
        "-d", "--drive",
        help="Drive (mountpoint) to search for DCIM folders. (e.g. 'f' or 'g'). (Required if import)."
    )

    parser.add_argument(
        "-i", "--indir",
        help="Directory containing photos whose names are to be updated. (Required if update)."
    )

    parser.add_argument(
        "-b", "--body",
        required=True,
        help="Camera body (e.g., 'xt4', 'nikon1v1', 'iphone16e). Required Always."
    )

    parser.add_argument(
        "-l", "--lens",
        default=None,
        help="Lens used (24-70mmf4-8). If not specified, assumes point-and-shoot or cellphone."
    )

    parser.add_argument(
        "-o", "--dir",
        required=True,
        help="Output directory. Required Always."
    )

    return parser

if __name__ == '__main__':
    parser = parser_factory()
    args = parser.parse_args()
    if args.action == 'import':
        if not args.drive:
            parser.error("--drive is required when action is 'import'")
        do_import(args)
    if args.action == 'update':
        if not args.indir:
            parser.error("--indir is required when action is 'update'")
        do_update(args)

