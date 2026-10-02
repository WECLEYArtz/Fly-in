class ArgError(Exception):
    """Represent an error in the program arguments."""

    def __init__(self, message: str) -> None:
        """Initialize the exception with an error message."""
        super().__init__(message)


class AlgoError(Exception):
    """Represent an error raised by the pathfinding algorithm."""


class EndHubUnreachableError(AlgoError):
    """Represent an unreachable end hub."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__(
            "Couldn't reach end_hub, is it connected to start_hub?"
        )


class EmptyAdjacencyError(AlgoError):
    """Represent missing adjacency data during path creation."""

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__("Empty adjacency during path creation")


class ParseError(Exception):
    """Base class for errors raised while parsing input."""

    message: str = ""

    def __init__(self, line: int, detail: str = "") -> None:
        """Initialize a colorized parsing error message."""
        message: str = self.message.format(detail)
        super().__init__(f"(line {line}) | {message}")


class InvalidMaxLinkCapacityError(ParseError):
    """Represent an invalid max_link_capacity value."""

    message: str = "Invalid max_link_capacity value {}"

    def __init__(self, line: int, value: str) -> None:
        """Initialize the exception with the invalid value."""
        super().__init__(line, value)


class BlockedMaxLinkCapacityError(ParseError):
    """Represent an unsupported blocked connection capacity."""

    message: str = (
        "max_link_capacity {} is unsupported, "
        "please clear map from blocked connections"
    )

    def __init__(self, line: int, value: int) -> None:
        """Initialize the exception with the unsupported capacity."""
        super().__init__(line, str(value))


class InvalidHubTypeError(ParseError):
    """Represent an invalid hub type."""

    message: str = (
        "Invalid type - got: '{}'\n"
        "Available types: ( blocked | restricted | normal | priority )"
    )

    def __init__(self, line: int, hub_type: str) -> None:
        """Initialize the exception with the invalid hub type."""
        super().__init__(line, hub_type)


class InvalidColorSingleWord(ParseError):
    """Represent an invalid color single word."""

    message: str = "Invalid single word color - got: '{}'"

    def __init__(self, line: int, color: str) -> None:
        """Initialize the exception with the invalid color."""
        super().__init__(line, color)


class InvalidMaxDronesError(ParseError):
    """Represent an invalid max_drones value."""

    message: str = "Invalid max drone - '{}'"

    def __init__(self, line: int, value: str) -> None:
        """Initialize the exception with the invalid value."""
        super().__init__(line, value)


class BlockedHubMaxDronesError(ParseError):
    """Represent a non-positive max_drones value on a hub."""

    message: str = (
        "Unsupported value of {} for max_drones\n"
        "If attempting to block a zone, "
        "Please consider using zone=blocked instead"
    )

    def __init__(self, line: int, value: int | float) -> None:
        """Initialize the exception with the unsupported value."""
        super().__init__(line, str(value))


class BlockedEndHubError(ParseError):
    """Represent a blocked end hub."""

    message: str = "Cannot reach a blocked type end_hub"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class DuplicateCoordinatesError(ParseError):
    """Represent duplicated hub coordinates."""

    message: str = "Cordination duplicated '{}'"

    def __init__(self, line: int, coordinates: tuple[int, int]) -> None:
        """Initialize the exception with the duplicated coordinates."""
        super().__init__(line, str(coordinates))


class IncompleteConnectionMetadataError(ParseError):
    """Represent malformed connection metadata."""

    message: str = (
        "Incomplete meta data: '{}'\n" "Expected max_link_capacity=<value>"
    )

    def __init__(self, line: int, metadata: str) -> None:
        """Initialize the exception with the malformed metadata."""
        super().__init__(line, metadata)


class OverridingMetadataError(ParseError):
    """Represent overriding in metadata."""

    message: str = "Overriding meta data: '{}'\n"

    def __init__(self, line: int, metadata: str) -> None:
        """Initialize the exception with the malformed metadata."""
        super().__init__(line, metadata)


class IncompleteHubMetadataError(ParseError):
    """Represent malformed hub metadata."""

    message: str = (
        "Incomplete meta data: '{}'\n"
        "Expected <key>=<value> pair, Available pair:\n"
        "- zone=(normal|blocked|restricted|priority)\n"
        "- color=(existing css color)\n"
        "- max_drones=(positive integer)"
    )

    def __init__(self, line: int, metadata: str) -> None:
        """Initialize the exception with the malformed metadata."""
        super().__init__(line, metadata)


class InvalidNbDronesPrefixError(ParseError):
    """Represent a missing nb_drones prefix."""

    message: str = "File must start with literal 'nb_drones:' got '{}'"

    def __init__(self, line: int, token: str) -> None:
        """Initialize the exception with the first token."""
        super().__init__(line, token)


class ExtraNbDronesValuesError(ParseError):
    """Represent extra values on the nb_drones line."""

    message: str = "Got extra values for nb_drones"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class MissingNbDronesValueError(ParseError):
    """Represent a missing nb_drones value."""

    message: str = "Got no value for nb_drones"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class NonPositiveNbDronesError(ParseError):
    """Represent a non-positive number of drones."""

    message: str = "Can't do much with {} drones"

    def __init__(self, line: int, drones: int) -> None:
        """Initialize the exception with the invalid count."""
        super().__init__(line, str(drones))


class InvalidNbDronesError(ParseError):
    """Represent a non-numeric number of drones."""

    message: str = "[nb_drones] - Invalid number: {}"

    def __init__(self, line: int, value: str) -> None:
        """Initialize the exception with the invalid value."""
        super().__init__(line, value)


class HubNameContainsDashError(ParseError):
    """Represent a hub name containing a dash."""

    message: str = (
        "'{}' contains a dash character '-'"
        ", this may conflict with connection initialising"
    )

    def __init__(self, line: int, name: str) -> None:
        """Initialize the exception with the invalid name."""
        super().__init__(line, name)


class InvalidHubCoordinatesError(ParseError):
    """Represent invalid hub coordinates."""

    message: str = "Error while parsing zone cordination - {}"

    def __init__(self, line: int, error: str) -> None:
        """Initialize the exception with the parsing error."""
        super().__init__(line, error)


class SelfConnectionError(ParseError):
    """Represent a connection from a hub to itself."""

    message: str = (
        "Connection ends must be different, got: '{}' self connection"
    )

    def __init__(self, line: int, hub_name: str) -> None:
        """Initialize the exception with the hub name."""
        super().__init__(line, hub_name)


class UndefinedHubError(ParseError):
    """Represent a connection to an undefined hub."""

    message: str = "Attempting to connect undefined zone '{}'"

    def __init__(self, line: int, hub_name: str) -> None:
        """Initialize the exception with the hub name."""
        super().__init__(line, hub_name)


class DuplicateStartHubError(ParseError):
    """Represent a duplicate start hub."""

    message: str = "start_hub duplication"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class DuplicateHubError(ParseError):
    """Represent a duplicate hub."""

    message: str = "Duplicated hub '{}'"

    def __init__(self, line: int, hub_name: str) -> None:
        """Initialize the exception with the hub name."""
        super().__init__(line, hub_name)


class DuplicateEndHubError(ParseError):
    """Represent a duplicate end hub."""

    message: str = "end_hub duplication"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class DuplicateConnectionError(ParseError):
    """Represent a duplicate connection."""

    message: str = "Duplicated connection '{}'"

    def __init__(self, line: int, connection: set[str]) -> None:
        """Initialize the exception with the duplicate connection."""
        super().__init__(line, f"({connection})")


class InvalidMapFormatError(ParseError):
    """Represent an incorrectly formatted map line."""

    message: str = (
        "Incorrect scheema, Available formats:\n"
        "- start_hub: <name> <x> <y> [metadata]\n"
        "- end_hub: <name> <x> <y> [metadata]\n"
        "- hub: <name> <x> <y> [metadata]\n"
        "- connection: <name1>-<name2> [metadata]\n"
    )

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class MissingStartHubError(ParseError):
    """Represent a map without a start hub."""

    message: str = "Missing 'start_hub:'"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)


class MissingEndHubError(ParseError):
    """Represent a map without an end hub."""

    message: str = "Missing 'end_hub:'"

    def __init__(self, line: int) -> None:
        """Initialize the exception."""
        super().__init__(line)
