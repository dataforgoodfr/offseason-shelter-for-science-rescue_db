from sqlalchemy.orm import Session

from rescue_api import database
from data_pipelines.dp_lib.data_gov.load import load_raw_datasets


def load_data(db_session: Session) -> None:
    load_raw_datasets(
        db_session=db_session,
        data_folder_names=[
          "package_search_ca_gov",
          "package_search_doe_gov",
          "package_search_edac_unm_edu",
          "package_search_epa_gov",
          "package_search_hhs_gov",
          "package_search_nasa_gov",
          "package_search_noaa_gov",
          "package_search_usaid_gov",
          "package_search_usda_gov",
        ],
    )

db_session = next(database.get_db())
load_data(db_session)
