from pathlib import Path, PosixPath
import os
import shutil
import pandas as pd
import json
import uuid
from typing import Any, List, Dict

FILE_STORAGE = os.path.expanduser('~/.pingpi')


def get_storage_folder() -> Path:
    """Get the path to the file storage folder"""
    return Path(FILE_STORAGE)


def setup_storage() -> None:
    """Setup the storage folder by making the directory"""
    storage_folder = get_storage_folder()
    storage_folder.mkdir(exist_ok=True)


def save_data(df: pd.DataFrame) -> str:
    """Save dataframe to a json file"""
    storage_folder = get_storage_folder()
    data_dict = df.to_json(orient="records")
    file_id = str(uuid.uuid4())
    json_file = storage_folder / file_id
    json_file.write_text(data_dict)
    return file_id


def read_data_file(file_id: str) -> List[Dict[str, Any]]:
    """Read the data file from stored uploaded file"""
    storage_folder = get_storage_folder()
    json_file = storage_folder / file_id
    if not json_file.exists():
        return None
    return json.loads(json_file.read_bytes())


def clean_storage() -> None:
    """Delete the whole file storage folder"""
    shutil.rmtree(FILE_STORAGE)
