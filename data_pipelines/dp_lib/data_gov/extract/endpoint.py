from typing import Any, Dict, List, Union
from urllib.parse import urljoin

from datetime import datetime
import os
import json

import pandas as pd
import requests

from data_pipelines.dp_lib.utils import DATA_DIR


class DataGovEndpoint:
    """
    This class aims to be the parent of all data.gov endpoints.
    Adapt it when necessary so it covers all their specificities.
    """
    base_url = "https://catalog.data.gov/api/3/action/"

    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    @property
    def full_url(self) -> str:
        return urljoin(base=self.base_url, url=self.url)


class DataGovPackageSearchEndpoint(DataGovEndpoint):

    def __init__(
            self,
            name: str,
            url: str,
            organization_code: str,
            batch_size: int = 30000,
            max_elements_by_call: int = 1000,
            offset: int = 0,
    ) -> None:
        super().__init__(name=name, url=url)
        self.max_elements_by_call = max_elements_by_call
        self.total_elements = None
        self.batch_size = batch_size
        self.offset = offset
        self.organization_code = organization_code

    # TODO: retry sending a request when the error comes from the server (50X errors), use tenacity?
    def _get_response(self) -> Any:
        response = requests.get(
            url=self.full_url,
            params={
                "rows": str(self.max_elements_by_call),
                "start": str(self.offset),
                "fq": f"organization:{self.organization_code}"
            }
        )
        print(f"Called {response.url}")
        response.raise_for_status()

        json_response = response.json()
        result = json_response["result"]

        # The count value changes at each call, not sure yet if we should update it at each call
        if not self.total_elements:
            self.total_elements = result["count"]

        if self._has_next_page():
            self.offset += self.max_elements_by_call

        return result["results"]

    def _has_next_page(self) -> bool:
        return (self.offset + 1) < self.total_elements

    @property
    def _destination_folder_path(self) -> str:
        now = datetime.now()
        # TODO: fix the timestamp so we have for example 2025-10-04T16-00-34 instead of 2025-10-4T16-0-34
        return os.path.join(DATA_DIR, f"data_gov/{self.name}", now.strftime("%Y-%m-%dT%H-%M-%S"))

    @staticmethod
    def _write_data_to_json(data: Union[List, Dict], dst_folder_path: str, file_number: int) -> None:
        dst_file_path = os.path.join(dst_folder_path, f"data_{file_number}.json")
        with open(dst_file_path, "w") as fhandle:
            # TODO; subset the data with only what we need to limit the size of the files
            json.dump(data, fhandle, indent=4)

        print(f"Data written at {dst_file_path}")

    def save_data(self) -> None:
        dst_folder_path = self._destination_folder_path
        os.makedirs(dst_folder_path)

        # We need to do an initial response to set self.total_elements first
        rows = self._get_response()

        file_number = 1
        while self._has_next_page():
            response = self._get_response()
            rows.extend(response)
            if len(rows) >= self.batch_size or not self._has_next_page():
                self._write_data_to_json(
                    data=rows,
                    dst_folder_path=dst_folder_path,
                    file_number=file_number,
                )
                rows = []
                file_number += 1
