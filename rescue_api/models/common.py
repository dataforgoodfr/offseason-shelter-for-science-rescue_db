# coding: utf-8

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

CREATED_AT_COLUMN = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
UPDATED_AT_COLUMN = mapped_column(server_default=text("CURRENT_TIMESTAMP"), onupdate=text("NOW()"))
