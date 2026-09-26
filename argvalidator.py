import os

from errors import ArgError


class ArgValidator:
    """Contain the argument validation method."""

    @staticmethod
    def validate(argv: list[str]) -> str:
        """Retrieve and validate the file path from the program arguments.

        Args:
            argv: All program arguments.

        Returns:
            The validated file path.
        """
        file = argv[1].strip()
        if len(argv) < 2:
            raise ArgError("No arguments given")
        if len(argv) > 2:
            raise ArgError("More than one argument recieved")
        if not len(file):
            raise ArgError("File path can't be a whole of nothing")
        if not os.path.isfile(argv[1]):
            raise ArgError(f"File '{argv[1]}' doesn't exist")
        if not os.access(file, os.R_OK):
            raise ArgError(f"Lacking read permission for file '{argv[1]}'")
        return argv[1]
