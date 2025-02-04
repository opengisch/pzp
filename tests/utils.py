import shutil
from datetime import datetime
from pathlib import Path
from tempfile import gettempdir


def get_copy_path(file_name: str) -> Path:
    data_dir = Path.cwd() / "tests" / "data"
    src_path = data_dir / file_name

    dst_path = get_tmp_path(file_name)
    shutil.copyfile(str(src_path), str(dst_path))
    return dst_path


def get_tmp_path(file_name: str) -> Path:
    # Get a unique non-existent path (up to milliseconds)
    return Path(gettempdir()) / (
        datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f").strftime("%Y%m%d_%H%M%S%f") + "_" + file_name
    )
