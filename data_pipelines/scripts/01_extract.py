from concurrent.futures import ThreadPoolExecutor
from data_pipelines.dp_lib.data_gov import OrganizationalDatasetEndpoints


organisational_dataset_endpoints = OrganizationalDatasetEndpoints()
with ThreadPoolExecutor() as executor:
    executor.map(
        lambda endpoint: endpoint.save_data(),
        organisational_dataset_endpoints.endpoints,
    )
