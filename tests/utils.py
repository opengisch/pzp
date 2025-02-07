import shutil
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir
from typing import Optional


def get_data_path(file_name: Optional[str] = "", process_type: Optional[str] = "") -> Path:
    """
    Returns the path of the "data" dir for tests, or, if file_name is
    given, returns the file_name appended to the data dir for tests.

    In case that process_type is given, the file_name will be returned
    as belonging to the process_type folder. A path to the process_type
    folder may also be returned if process_type is the only parameter
    given.
    """
    file_path = file_name if file_name else ""
    if process_type:
        file_path = Path(process_type) / file_name

    return Path.cwd() / "tests" / "data" / file_path


def get_copy_path(file_path: Path) -> Path:
    """
    Returns a path to a copied version of the file. The file should exist.
    """
    dst_path = get_tmp_path(file_path.name)
    shutil.copyfile(str(file_path), str(dst_path))
    return dst_path


def get_tmp_path(file_name: str) -> Path:
    # Get a unique non-existent path (up to milliseconds)
    return Path(gettempdir()) / (
        datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y%m%d_%H%M%S%f") + "_" + file_name
    )
