import argparse
import os
import shutil
import zipfile
from pathlib import Path


def archive_db_data():
    archive_path = Path.cwd() / "data" / "db_data.zip"
    if os.path.exists(archive_path):
        os.remove(archive_path)

    shutil.make_archive(base_name="db_data",
                        format='zip',
                        root_dir=Path.cwd() / "data",
                        base_dir="db_data")

    shutil.move(Path.cwd() / "db_data.zip", Path.cwd() / "data")


def archive_unpack():
    with zipfile.ZipFile(Path.cwd() / "data" / "db_data.zip", 'r') as zip_file:
        zip_file.extractall(Path.cwd() / "data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", action="store_true", help="Make archive db_data")
    parser.add_argument("-u", action="store_true", help="Unpack archive db_data")

    args = parser.parse_args()
    if args.m:
        archive_db_data()
    if args.u:
        archive_unpack()