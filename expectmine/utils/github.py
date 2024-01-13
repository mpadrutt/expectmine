from pathlib import Path
from zipfile import ZipFile

import requests
from requests import get
from requests.exceptions import RequestException
from tqdm import tqdm

from src.logger.base_logger import BaseLogger


def current_release_number(owner: str, name: str, logger: BaseLogger) -> str | None:
    """
    Fetches the current release number. There will be no error thrown if the
    method fails but rather the error is logged to the logger and None is returned.

    :param owner: Owner of the repo (e.g. ziglang)
    :type owner: str
    :param name: Name of the repo (e.g. zig)
    :type name: str
    :param logger: Logger to log errors.
    :type name: BaseLogger

    :return: An unformatted string of the current version or None if an error happened.
    :rtype: str | None
    """
    query_url = f"https://api.github.com/repos/{owner}/{name}/releases/latest"

    try:
        response = requests.get(query_url)

        if response.status_code != 200:
            raise RequestException(f"Status code is {response.status_code}")

        json = response.json()

        if "tag_name" not in json:
            raise RequestException(f"No tag_name in {owner}/{name}")

        return json["tag_name"]

    except Exception as e:
        logger.error(
            f"An error while fetching the current release number of {query_url}: {repr(e)}"
        )
        return None


def all_release_numbers(owner: str, name: str, logger: BaseLogger) -> list[str] | None:
    """
    Fetches all release_numbers. There will be no error thrown if the
    method fails but rather the error is logged to the logger and None is returned.

    :param owner: Owner of the repo (e.g. ziglang)
    :type owner: str
    :param name: Name of the repo (e.g. zig)
    :type name: str
    :param logger: Logger to log errors.
    :type name: BaseLogger

    :return: A list of release numbers or None if the method fails.
    :rtype: list[str] | None
    """
    query_url = f"https://api.github.com/repos/{owner}/{name}/releases/latest"

    try:
        response = requests.get(query_url)

        if response.status_code != 200:
            raise RequestException(f"Status code is {response.status_code}")

        json = response.json()

        releases: list[str] = []

        for release in json:
            if "tag_name" in release:
                release.append(json["tag_name"])

        return releases

    except Exception as e:
        logger.error(
            f"An error while fetching all release numbers of {query_url}: {repr(e)}"
        )
        return None


def unstable_install_zip_to_path(url: str, path: Path) -> None:
    """
    The install_zip_to_path function is used to download a zip file from
    an url and extract it to a path.

    :param url: The url to download the zip file from.
    :type url: str
    :param path: The path to extract the zip file to.
    :type path: Path
    """
    if url.split(".")[-1] != "zip":
        raise Exception(
            f"Could not download zip file from {url}. URL does not end with .zip",
        )

    if not path.exists():
        path.mkdir(parents=True)

    response = get(url, stream=True)
    total = int(response.headers.get("content-length", 0))

    if response.status_code != 200:
        raise RuntimeError(
            f"Could not download zip file from {url}. Status code: {response.status_code}",
            response,
        )

    download_path = path / "temp.zip"

    with open(download_path, "wb") as file, tqdm(
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

    with ZipFile(download_path, "r") as zip_file:
        zip_file.extractall(path)

    download_path.unlink()
