from errors import ArgError
import os


# NOTE: read about os, os.path, os.R_OK
class ArgValidator:
    @staticmethod
    def validate(argv: list[str]) -> str:
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
