# coding: utf-8
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import DataGovBase


class RawDatasets(DataGovBase):
    __tablename__ = "raw_datasets"

    id: Mapped[str] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(JSONB, nullable=False)
