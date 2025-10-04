# coding: utf-8
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import DataGovBase


class RawDatasets(DataGovBase):
    __tablename__ = "raw_datasets"

    id: Mapped[str] = mapped_column(primary_key=True)
    # content: Mapped[str] = mapped_column(JSONB, nullable=False)
    name: Mapped[str]
    notes: Mapped[str]
    metadata_created: Mapped[datetime]
    metadata_modified: Mapped[datetime]
    organization: Mapped[str] = mapped_column(JSONB, nullable=False)
    resources: Mapped[str] = mapped_column(JSONB, nullable=False)
    title: Mapped[str]
