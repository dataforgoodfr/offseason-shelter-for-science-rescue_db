'''
Data loader scripts to update db with useful data to prepare rescue
'''

import requests
import logging
from sqlalchemy.orm import load_only
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor, as_completed

from rescue_api.models.mvp_downloader_library import MvpDownloaderLibrary
from rescue_api.models.rescues import Rescue
from rescue_api.database import get_db

MAX_WORKERS = 12

def request_http_size(url):
    import requests

    headers = {'User-Agent': 'Mozilla/5.0',
               "Upgrade-Insecure-Requests": "1",
               "DNT": "1"}
    try:
        response = requests.head(url, timeout=3, headers=headers)
        headers = response.headers
        if 'Content-Length' in headers:
            file_size = int(headers['Content-Length'])
            #print(f"File size: {file_size} bytes")
            #print(file_size)
            return file_size
        else:
            # Try a GET request with stream=True to get content-length
            response = requests.get(url, stream=True, timeout=3, headers=headers)
            headers = response.headers
            if 'Content-Length' in headers:
                file_size = int(headers['Content-Length'])
                print(file_size)
                return file_size
            else:
                return None
    except Exception as e:
        return -1
    finally:
        if 'response' in locals() and hasattr(response, 'close'):
            response.close()

def request_ftp_size(url):
    from ftplib import FTP

    ftp_info = url.replace('ftp://', '').split('/')
    host = ftp_info[0]
    path = '/' + '/'.join(ftp_info[1:])

    ftp = FTP(host, timeout=3)
    try:
        ftp.login()
        file_size = ftp.size(path)
        ftp.quit()
        return file_size
    except Exception as e:
        return None

def request_link_size(dataset, reload: bool) -> float:
    url = dataset.deeplink
    file_size = dataset.deeplink_file_size
    if not reload and file_size is not None:
        return file_size
    try:
        if url.startswith('http'):
            return request_http_size(url)
        elif url.startswith('ftp'):
            return request_ftp_size(url)
        else:
            print(f">> Unsupported type {url}")
            return None
    except Exception as e:
        return None

def update_dataset_size(dataset: MvpDownloaderLibrary) -> MvpDownloaderLibrary:
    """
    Update a single dataset
    Args:
        dataset: object, MvpDownloaderLibrary database
    Returns: MvpDownloaderLibrary with download file size
    """
    dataset.deeplink_file_size = request_link_size(dataset, False)
    return dataset

def get_deeplink_size(max_workers: int = 12) -> None:
    """
    Update size of deeplink
    """
    session = next(get_db())
    deeplink_table = (session.query(MvpDownloaderLibrary)
                      .options(load_only(MvpDownloaderLibrary.id,
                                         MvpDownloaderLibrary.deeplink_file_size,
                                         MvpDownloaderLibrary.deeplink))
                      .all()
                      )

    # Use ThreadPoolExecutor to parallelize the requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks to the executor
        futures = [executor.submit(update_dataset_size, dataset) for dataset in deeplink_table]

        # Wait for all tasks to complete
        for future in tqdm(as_completed(futures), total=len(futures), desc="Updating deeplink sizes"):
            # Handle any exceptions if needed
            try:
                future.result()
            except Exception as e:
                print(f"Error updating dataset: {e}")

    session.commit()
    session.close()

if __name__ == "__main__":
    get_deeplink_size(MAX_WORKERS)
    print("DONE")