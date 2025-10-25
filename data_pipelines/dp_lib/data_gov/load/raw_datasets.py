from datetime import datetime
import json
import os
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import text

from data_pipelines.dp_lib.utils import DATA_DIR
from rescue_api.models import RawDatasets


def load_raw_datasets(db_session: Session, data_folder_names: List[str], mode: str = "overwrite") -> None:
    # TODO: manage other writing modes
    if mode != "overwrite":
        raise ValueError(
            f"The writing mode '{mode}' is incorrect, we only manage the 'overwrite' mode. Please provide 'overwrite'."
        )

    if mode == "overwrite":
        query = text("TRUNCATE TABLE data_gov.raw_datasets;")
        db_session.execute(query)
        db_session.commit()
        print("Table 'data_gov.raw_datasets' truncated.")

    for data_folder_name in data_folder_names:
        data_folder_path = os.path.join(f"{DATA_DIR}/data_gov", data_folder_name)
        _load_data_from_folder(db_session=db_session, data_folder_path=data_folder_path, mode=mode)
        organization_code = data_folder_name.replace("package_search_", "")
        print(f"Organization {organization_code}: data loaded into raw_datasets.")

def _load_data_from_folder(db_session: Session, data_folder_path: str, mode: str = "upsert") -> None:
    latest_created_subfolder_name = _identify_latest_created_subfolder(data_folder_path)
    subfolder_path = os.path.join(data_folder_path, latest_created_subfolder_name)
    filenames = [element.name for element in os.scandir(subfolder_path) if element.is_file()]
    for filename in filenames:
        full_filepath = os.path.join(subfolder_path, filename)
        print(f"Loading data from {full_filepath} started.")
        _load_data_from_json_file(db_session=db_session, filepath=full_filepath, mode=mode)

def _identify_latest_created_subfolder(parent_folder_path: str) -> str:
    timestamps = [
        datetime.strptime(subfolder_name, "%Y-%m-%dT%H-%M-%S")
        for subfolder_name in os.listdir(parent_folder_path)
    ]
    latest_timestamp = max(timestamps)
    return latest_timestamp.strftime("%Y-%m-%dT%H-%M-%S")

def _load_data_from_json_file(
        db_session: Session,
        filepath: str,
        mode: str = "upsert",
        batch_size: int = 500
) -> None:
    with open(filepath, "r") as fhandle:
        data = json.load(fhandle)

    if type(data) is not list:
        raise TypeError(f"The data written at {filepath} is not a list.")

    # TODO: move this logic of subsetting data to the extraction step to limit the size of the read files
    data = [
        {
            key: value
            for key, value in element.items()
            if key in RawDatasets.column_names()
        }
        for element in data
    ]
    print("Data subset selected.")
    if mode == "overwrite":
        for start in range(0, len(data), batch_size):
            end = start + batch_size
            data_batch = data[start:end]
            _insert_table(db_session=db_session, data=data_batch)
            print(f"Batch {start}-{end} is inserted.")
    else:
        raise ValueError(f"The writing mode '{mode}' is incorrect. Please provide 'overwrite'.")


def _insert_table(db_session: Session, data: List[Dict[str, Any]]) -> None:
    raw_datasets = [RawDatasets(**row) for row in data]
    db_session.add_all(raw_datasets)
    db_session.commit()


def _upsert_table(db_session: Session, data: List[Dict[str, Any]]) -> None:
    insert_statement = insert(RawDatasets).values(data)
    update_statement = insert_statement.on_conflict_do_update(
        index_elements=[RawDatasets.id],
        set_={col.name: col for col in insert_statement.excluded if col.name not in ('id', 'sfs_created_at')}
    )
    _ = db_session.execute(update_statement)
    db_session.commit()
