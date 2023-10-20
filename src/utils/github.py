import requests
from requests.exceptions import RequestException

from ..logger import BaseLogger


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

        releases = []

        for release in json:
            if "tag_name" in release:
                release.append(json["tag_name"])

        return releases

    except Exception as e:
        logger.error(
            f"An error while fetching all release numbers of {query_url}: {repr(e)}"
        )
        return None
