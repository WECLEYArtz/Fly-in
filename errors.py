class ArgError(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)


class ParseError(Exception):
    def __init__(self, line:int, message:str) -> None:
        super().__init__(f"(line {line}) - " + message)
