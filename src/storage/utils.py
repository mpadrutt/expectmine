import os
import pickle
import sys
from pathlib import Path


def validate_adapter_init(persistent_path: Path, working_directory: Path):
    """
    Validates that the init arguments are of valid format. Throws an error
    if not.

    :param persistent_path: The path which the storage can use to persist
        data.
    :type persistent_path: Path
    :param working_directory: The path which the storage can use to create
        temporary files in for the user or pipeline to access.
    :type working_directory: Path

    :Example:

    >>> validate_adapter_init(Path("path1"), Path("path2"))


    >>> validate_adapter_init(Path("path2"))
    ValueError("Storage paths can not be empty.")


    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If either step name or any of the
        paths are empty.
    """
    if not persistent_path or not working_directory:
        raise ValueError("Storage paths can not be empty.")

    if not isinstance(persistent_path, Path) or not isinstance(working_directory, Path):
        raise TypeError(
            "persistent_path and working_directory need to be of type Path."
        )


def validate_storage_init(
    step_name: str, persistent_path: Path, working_directory: Path
):
    """
    Validates that the init arguments are of valid format. Throws an error
    if not.

    :param step_name: Step name to which the storage should be scoped
    :type step_name: str
    :param persistent_path: The path which the storage can use to persist
        data.
    :type persistent_path: Path
    :param working_directory: The path which the storage can use to create
        temporary files in for the user or pipeline to access.
    :type working_directory: Path

    :Example:

    >>> validate_storage_init("hello", Path("path1"), Path("path2"))


    >>> validate_storage_init("", Path("path1"), Path("path2"))
    ValueError("Step name can not be empty.")


    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If either step name or any of the
        paths are empty.
    """
    if not step_name:
        raise ValueError("Step name can not be empty.")

    if not persistent_path or not working_directory:
        raise ValueError("Storage paths can not be empty.")

    if not isinstance(persistent_path, Path) or not isinstance(working_directory, Path):
        raise TypeError(
            "persistent_path and working_directory need to be of type Path."
        )


def validate_key(key: str):
    """
    Validates that the given key is of valid format. Throws an error
    if not.

    :param key: The key to associate with the value. A key cannot be
        empty. Keys have a maximum length of 255 characters.
    :type key: str

    :Example:

    >>> validate_key("hello")


    >>> validate_key("")
    ValueError("Key can not be empty")

    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If the key is empty or too long.
    """
    if not isinstance(key, str):
        raise TypeError("Key should be of type string.")

    if len(key) < 1:
        raise ValueError("Key needs to be at least one character long.")

    if len(key) > 255:
        raise ValueError("Key needs to be shorter than 255 characters.")


def validate_value(value: object):
    """
    Validates that the given object is of valid format. Throws an error
    if not.

    :param value: The value to store. The maximum size of a value is
        25 MiB. The object needs to be Pickled.
    :type value: object

    :Example:

    >>> validate_value("hello")


    >>> validate_value("")
    ValueError("Key can not be empty")

    :raises TypeError: If the arguments have the wrong type.
    :raises ValueError: If the object or file is too big, the wrong
        size or can't be pickled.
    """

    if isinstance(value, Path):
        if os.path.getsize(value) / (1024 * 1024) > 100:
            raise ValueError("File should be smaller than 100MiB.")
        return

    if isinstance(value, object):
        if (sys.getsizeof(value) / (1024 * 1024)) > 25:
            raise ValueError("Size of object should be smaller than 25mb.")

        try:
            pickle.dumps(value)
        except Exception:
            raise ValueError("Object can not be pickled.")

        return

    raise TypeError("Value should be of type object or Path.")


def validate_step_name(step_name: str):
    if not isinstance(step_name, str):
        raise TypeError("Step_name should be of type string.")

    if len(step_name) > 255:
        raise ValueError("Step name is too long.")

    if len(step_name) < 1:
        raise ValueError("Step name can not be empty.")
