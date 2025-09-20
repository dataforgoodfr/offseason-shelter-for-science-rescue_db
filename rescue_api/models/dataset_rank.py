# coding: utf-8

from datetime import datetime

from rescue_api.database import Base
from sqlalchemy import ForeignKey, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DatasetRank(Base):
    __tablename__ = "dataset_ranks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    ranking_id: Mapped[int] = mapped_column(ForeignKey("dataset_rankings.id"))
    rank: Mapped[int]
    event_count: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=text("NOW()")
    )

    # Unicity constraint on dataset_id and ranking_id
    __table_args__ = (
        UniqueConstraint(
            "dataset_id", "ranking_id", name="dataset_ranks_dataset_id_ranking_id_key"
        ),
    )

    # Relationships
    ranking = relationship("DatasetRanking", back_populates="ranks")
