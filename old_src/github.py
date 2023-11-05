from pathlib import Path
from time import sleep
from zipfile import ZipFile
from requests import get
from tqdm import tqdm


def get_current_release(repo: str) -> str:
    """
    The get_current_version function is used to get the latest release version of a GitHub repository. The function
    uses the GitHub API to get the latest release version. If it cant connect to the API, it will raise an exception.

    Args:
        repo (str): The name of the GitHub repository. For example: mzmine/mzmine3

    Returns:
        str: The latest release version of the repository. Or None if an error occured.

    Raises:
        Exception: If the GitHub API returns an error. Or it can not connect.
    """

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = get(url)

    if response.status_code != 200:
        raise Exception(
            f"Could not get latest version of {repo}. Status code: {response.status_code}",
            response,
        )

    json = response.json()

    if "tag_name" not in json:
        raise Exception(
            f"Could not get latest version of {repo}. Response did not contain tag_name.",
            response,
        )

    return json["tag_name"]


def get_releases(
    repo: str,
) -> list[dict]:
    """
    The get_available_versions function is used to get all the available release versions of a GitHub repository. The function
    uses the GitHub API to get the available release versions. If it cant connect to the API, it will raise an exception.

    Args:
        repo (str): The name of the GitHub repository. For example: mzmine/mzmine3

    Returns:
        list[dict]: A list of available release versions of the repository with their download links. Each item in the list
        is a dictionary with the keys: version and assets. The assets key contains a list of dictionaries with the keys:
        name and browser_download_url.

    Raises:
        Exception: If the GitHub API returns an error. Or it can not connect.
    """

    url = f"https://api.github.com/repos/{repo}/releases"
    response = get(url)

    if response.status_code != 200:
        raise Exception(
            f"Could not get available versions of {repo}. Status code: {response.status_code}",
            response,
        )

    json = response.json()

    releases = []

    for release in json:
        if not {"tag_name", "assets"}.issubset(release):
            continue

        assets = [
            asset
            for asset in release["assets"]
            if {"name", "browser_download_url"}.issubset(asset)
        ]

        releases.append({"version": release["tag_name"], "assets": assets})

    return releases


def install_zip_to_path(url: str, path: Path) -> None:
    """
    The install_zip_to_path function is used to download a zip file from a url and extract it to a path.

    Args:
        url (str): The url to download the zip file from.
        path (Path): The path to extract the zip file to.
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
        raise Exception(
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
