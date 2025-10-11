from typing import List
from .endpoint import DataGovPackageSearchEndpoint


class OrganizationalDatasetEndpoints:
    def __init__(self) -> None:
        self.ca_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_ca_gov",
            url="package_search",
            organization_code="ca-gov",
        )
        self.doe_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_doe_gov",
            url="package_search",
            organization_code="doe-gov",
        )
        self.edac_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_edac_unm_edu",
            url="package_search",
            organization_code="edac-unm-edu",
        )
        self.epa_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_epa_gov",
            url="package_search",
            organization_code="epa-gov",
        )
        self.hhs_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_hhs_gov",
            url="package_search",
            organization_code="hhs-gov",
        )
        self.nasa_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_nasa_gov",
            url="package_search",
            organization_code="nasa-gov",
        )
        self.noaa_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_noaa_gov",
            url="package_search",
            organization_code="noaa-gov",
        )
        self.usaid_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_usaid_gov",
            url="package_search",
            organization_code="usaid-gov",
        )
        self.usda_dataset_endpoint = DataGovPackageSearchEndpoint(
            name="package_search_usda_gov",
            url="package_search",
            organization_code="usda-gov",
        )

    @property
    def endpoints(self) -> List[DataGovPackageSearchEndpoint]:
        return [
            self.ca_dataset_endpoint,
            self.doe_dataset_endpoint,
            self.edac_dataset_endpoint,
            self.epa_dataset_endpoint,
            self.hhs_dataset_endpoint,
            self.nasa_dataset_endpoint,
            self.noaa_dataset_endpoint,
            self.usaid_dataset_endpoint,
            self.usda_dataset_endpoint,
        ]
