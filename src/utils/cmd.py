import subprocess
from typing import Optional


def validate_cmd(cmd: str, options: Optional[list[tuple[str, str] | str]] = None):
    """
    Validates the cmd parameters.


    :param cmd: The base command to run.
    :type cmd: str
    :param options: List of options added to the command. Options can be either arguments
        or tuples of option followed by the argument.
    :type options: Optional[list[tuple[str, str] | str]]

    :Example:

    >>> validate_cmd("ls", ["-lh", "*"])

    >>> validate_cmd(None , ["-lh", "*"])
    TypeError("Cmd needs to be of type str.")


    :raises TypeError: If the arguments have the wrong type.
    """
    if not isinstance(cmd, str):
        raise TypeError("Cmd needs to be of type str.")
    if not isinstance(options, list | None):
        raise TypeError("Options are not a list or None.")

    if not options:
        return

    if not all(
        isinstance(o, str)
        or (isinstance(o, tuple) and isinstance(o[0], str) and isinstance(o[1], str))
        for o in options
    ):
        raise TypeError("Option of options list is not of type tuple[str, str] or str")


def run_cmd(
    cmd: str, options: list[tuple[str, str] | str] | None = None
) -> tuple[int, str, str]:
    """
    Runs a command and options in the command line. Returns three values,
    the result status code, a string of the cmd output and a string containing
    the error message if any is produced during execution.


    :param cmd: The base command to run.
    :type cmd: str
    :param options: List of options added to the command. Options can be either arguments
        or tuples of option followed by the argument.
    :type options: Optional[list[tuple[str, str] | str]]

    :Example:

    >>> run_cmd("ls", ["-lh", "foo.bar"])
    0, "...", ""

    >>> run_cmd(None , ["-lh", "*"])
    TypeError("Cmd needs to be of type str.")


    :raises TypeError: If the arguments have the wrong type.
    """
    validate_cmd(cmd, options)

    if not options:
        full_cmd = cmd
    else:
        options_string = ""

        for option in options:
            if isinstance(option, str):
                options_string += f" {option}"
            else:
                options_string += f" {option[0]} {option[1]}"

        full_cmd = f"{cmd} {options_string}"

    result = subprocess.run(
        full_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )

    stdout = result.stdout
    stderr = result.stderr

    return result.returncode, stdout, stderr
