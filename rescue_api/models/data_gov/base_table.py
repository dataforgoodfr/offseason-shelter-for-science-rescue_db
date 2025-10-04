from typing import List
from datetime import datetime
import inspect

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped

from rescue_api.models.common import CREATED_AT_COLUMN, UPDATED_AT_COLUMN


class DataGovBase(DeclarativeBase):
    metadata = MetaData(schema="data_gov")

    sfs_created_at: Mapped[datetime] = CREATED_AT_COLUMN
    sfs_updated_at: Mapped[datetime] = UPDATED_AT_COLUMN

    @classmethod
    def column_names(cls) -> List[str]:
        excluded_attributes = [
            "metadata",
            "registry",
        ]
        return [
            name
            for name, value in inspect.getmembers(cls)
            if not callable(value) and not name.startswith('_') and name not in excluded_attributes
        ]
