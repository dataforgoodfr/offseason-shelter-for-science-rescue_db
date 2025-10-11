from datetime import datetime
import json
import os
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from data_pipelines.dp_lib.utils import DATA_DIR
from rescue_api.models import RawDatasets


def load_raw_datasets(db_session: Session, data_folder_names: List[str], mode: str = "upsert") -> None:
    for data_folder_name in data_folder_names:
        data_folder_path = os.path.join(f"{DATA_DIR}/data_gov", data_folder_name)
        _load_data_from_folder(db_session=db_session, data_folder_path=data_folder_path, mode=mode)

def _load_data_from_folder(db_session: Session, data_folder_path: str, mode: str = "upsert") -> None:
    latest_created_subfolder_name = _identify_latest_created_subfolder(data_folder_path)
    subfolder_path = os.path.join(data_folder_path, latest_created_subfolder_name)
    filenames = [element.name for element in os.scandir(subfolder_path) if element.is_file()]
    for filename in filenames:
        full_filepath = os.path.join(subfolder_path, filename)
        _load_data_from_json_file(db_session=db_session, filepath=full_filepath, mode=mode)

def _identify_latest_created_subfolder(parent_folder_path: str) -> str:
    timestamps = [
        datetime.strptime(subfolder_name, "%Y-%m-%dT%H-%M-%S")
        for subfolder_name in os.listdir(parent_folder_path)
    ]
    latest_timestamp = max(timestamps)
    return latest_timestamp.strftime("%Y-%m-%dT%H-%M-%S")

def _load_data_from_json_file(db_session: Session, filepath: str, mode: str = "upsert") -> None:
    with open(filepath, "r") as fhandle:
        data = json.load(fhandle)

    if type(data) is not list:
        raise TypeError(f"The data written at {filepath} is not a list.")

    data = [
        {
            key: value
            for key, value in element.items()
            if key in RawDatasets.column_names()
        }
        for element in data
    ]
    if mode == "upsert":
        _upsert_table(db_session, data)
    else:
        raise ValueError(f"The writing mode '{mode}' is incorrect. Please provide 'upsert'.")

def _upsert_table(db_session: Session, data: List[Dict[str, Any]]) -> None:
    print("Upserting RawDatasets table: starting...")
    insert_statement = insert(RawDatasets).values(data)
    update_statement = insert_statement.on_conflict_do_update(
        index_elements=[RawDatasets.id],
        set_={col.name: col for col in insert_statement.excluded if col.name not in ('id', 'sfs_created_at')}
    )
    _ = db_session.execute(update_statement)
    db_session.commit()
    print("> Upserting RawDatasets table: done!")
