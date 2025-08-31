# coding: utf-8

from datetime import datetime

from rescue_api.database import Base
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column


class MvpDownloaderLibrary(Base):
    __tablename__ = "mvp_downloader_library"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id"))
    dataset_rank: Mapped[int]
    deeplink: Mapped[str]
    deeplink_file_size: Mapped[float]
    magnet_link: Mapped[int]
    defective_link_flag: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), onupdate=text("NOW()")
    )
