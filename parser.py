from dataclasses import dataclass
from errors import (
    BlockedEndHubError,
    BlockedHubMaxDronesError,
    BlockedMaxLinkCapacityError,
    DuplicateConnectionError,
    DuplicateCoordinatesError,
    DuplicateEndHubError,
    DuplicateHubError,
    DuplicateStartHubError,
    ExtraNbDronesValuesError,
    HubNameContainsDashError,
    IncompleteConnectionMetadataError,
    IncompleteHubMetadataError,
    InvalidColorSingleWord,
    InvalidHubCoordinatesError,
    InvalidHubTypeError,
    InvalidMapFormatError,
    InvalidMaxDronesError,
    InvalidMaxLinkCapacityError,
    InvalidNbDronesError,
    InvalidNbDronesPrefixError,
    MissingEndHubError,
    MissingNbDronesValueError,
    MissingStartHubError,
    NonPositiveNbDronesError,
    SelfConnectionError,
    UndefinedHubError,
)
from components import Graph, Hub, HubTypes, Connection
from graphregex import Regex
from re import Match
from webcolors import name_to_rgb, IntegerRGB, names as webnames


@dataclass
class Parser:
    """Parse input data and construct a graph."""

    def __init__(self) -> None:
        """Initialize the parser state.

        The parser state includes the parsed graph, connection data, blocked
        hubs and connections, zone types, and rainbow colors.
        """
        self.nb_drone: int
        self.graph: Graph = Graph()
        self.line_i: int = 1
        self.cordinations: list[tuple[int, int]] = []
        self.types: dict[str, HubTypes] = {
            "blocked": HubTypes.BLOCKED,
            "restricted": HubTypes.RESTRICTED,
            "normal": HubTypes.NORMAL,
            "priority": HubTypes.PRIORITY,
        }
        self.rainbow: list[IntegerRGB] = [
            name_to_rgb("red"),
            name_to_rgb("orange"),
            name_to_rgb("yellow"),
            name_to_rgb("green"),
            name_to_rgb("blue"),
            name_to_rgb("indigo"),
            name_to_rgb("violet"),
        ]

    def name_colorizer(self, name: str, color: str) -> str:
        """Colorize a name with the specified color.

        For the rainbow option, each character receives a different ANSI
        color code.

        Args:
            name: The name to colorize.
            color: The color to apply.

        Returns:
            The colorized name.
        """
        if color == "rainbow":
            gay_form: list[str] = []
            for i in range(len(name)):
                r, g, b = self.rainbow[i % len(self.rainbow)]
                gay_form.append(f"\x1b[38;2;{r};{g};{b}m{name[i]}")
            gay_form.append("\x1b[0m")
            return "".join(gay_form)
        else:
            r, g, b = name_to_rgb(color)
            return f"\x1b[38;2;{r};{g};{b}m{name}\x1b[0m"

    @staticmethod
    def expurgate_line(line: str) -> str:
        """Remove comments and trailing whitespace from a line.

        Args:
            line: The line to clean.

        Returns:
            The line without comments or trailing whitespace.
        """
        return line.split("#", 1)[0].rstrip()

    def metadata_connection(self, metadata_list: list[str]) -> int:
        """Parse connection metadata and return its capacity.

        Args:
            metadata_list: The connection metadata to parse.

        Returns:
            The parsed maximum link capacity.
        """
        value: int = 0
        for meta in metadata_list:
            if not (match := Regex.mxlc_meta.match(meta)):
                raise IncompleteConnectionMetadataError(self.line_i, meta)

            value_str = match.group("value")
            if not value_str.isdigit() or (value := int(value_str)) < 0:
                raise InvalidMaxLinkCapacityError(self.line_i, value_str)
            if value == 0:
                raise BlockedMaxLinkCapacityError(self.line_i, value)

        return value

    def metadata_hub(self, metadatas: list[str]) -> tuple[HubTypes, int, str]:
        """Parse hub metadata.

        Args:
            metadatas: The hub metadata to parse.

        Returns:
            A tuple containing the hub type, maximum capacity, and color.
        """
        zone_type: HubTypes = HubTypes.NORMAL
        color: str = "white"
        max_drone: int = 1

        for meta in metadatas:
            if m := Regex.zone_meta.match(meta):
                if (
                    not (ztype := m.group("value").lower())
                    in self.types.keys()
                ):
                    raise InvalidHubTypeError(self.line_i, m.group("value"))
                zone_type = self.types[ztype]

            elif m := Regex.color_meta.match(meta):
                color = m.group("value")
                if not color.isalpha():
                    raise InvalidColorSingleWord(self.line_i, color)
                if not (color in webnames() or color == "rainbow"):
                    color = "white"

            elif m := Regex.mxd_meta.match(meta):
                max_drone_str = m.group("value")
                if (
                    not max_drone_str.isdigit()
                    or (max_drone := int(max_drone_str)) < 0
                ):
                    raise InvalidMaxDronesError(self.line_i, max_drone_str)
            else:
                raise IncompleteHubMetadataError(self.line_i, meta)

        return (zone_type, max_drone, color)

    def extract_nb_drones(self, line: str) -> None:
        """Extract the number of drones from a line.

        Args:
            line: The line currently being parsed.
        """
        tokkens = line.split()
        if tokkens[0] != "nb_drones:":
            raise InvalidNbDronesPrefixError(self.line_i, tokkens[0])
        if len(tokkens) < 2:
            raise MissingNbDronesValueError(self.line_i)
        if len(tokkens) > 2:
            raise ExtraNbDronesValuesError(self.line_i)
        try:
            if (val := int(tokkens[1])) <= 0:
                raise NonPositiveNbDronesError(self.line_i, val)
        except ValueError:
            raise InvalidNbDronesError(self.line_i, tokkens[1])
        self.nb_drone = val

    def extract_hub(self, match: Match[str]) -> Hub:
        """Extract hub data from a matched line.

        Args:
            match: The matched regular expression.

        Returns:
            The extracted hub.
        """
        hub = Hub()
        hub.name_clr = hub.name = match.group("name")
        if "-" in hub.name:
            raise HubNameContainsDashError(self.line_i, hub.name)
        try:
            hub.cord = (int(match.group("x")), int(match.group("y")))
            if (hub.cord) in self.cordinations:
                raise DuplicateCoordinatesError(self.line_i, hub.cord)
            self.cordinations.append(hub.cord)
        except ValueError as e:
            raise InvalidHubCoordinatesError(self.line_i, str(e))

        if match.group("metadata"):
            meta_list = match.group("metadata").split()
            hub.type, hub.max_capacity, color = self.metadata_hub(meta_list)
            if hub.type == HubTypes.BLOCKED:
                self.graph.block_hubs.add(hub)

            hub.name_clr = self.name_colorizer(hub.name, color)

        if self.graph.hubs.get(hub.name):
            raise DuplicateHubError(self.line_i, hub.name)
        self.graph.hubs[hub.name] = hub
        return hub

    def extract_connection(self, match: Match[str]) -> None:
        """Extract connection data from a matched line.

        Args:
            match: The matched regular expression.
        """
        zone1 = match.group("zone1")
        zone2: str = match.group("zone2")
        if zone1 == zone2:
            raise SelfConnectionError(self.line_i, zone1)
        if zone1 not in self.graph.hubs.keys():
            raise UndefinedHubError(self.line_i, zone1)
        if zone2 not in self.graph.hubs.keys():
            raise UndefinedHubError(self.line_i, zone2)

        zonepair: tuple[str, str] = (zone1, zone2)
        if zonepair in self.graph.connections:
            raise DuplicateConnectionError(self.line_i, zonepair)

        hub1 = self.graph.hubs[zone1]
        hub2 = self.graph.hubs[zone2]

        connection = Connection({hub1.name: hub2, hub2.name: hub1})
        if hub1.type == HubTypes.BLOCKED or hub2.type == HubTypes.BLOCKED:
            self.graph.block_connections.add(connection)

        if match.group("metadata"):
            meta_list: list[str] = match.group("metadata").split()
            connection.max_capacity = self.metadata_connection(meta_list)

        self.graph.adjacency_list[hub1.name].connections.append(connection)
        self.graph.adjacency_list[hub2.name].connections.append(connection)

        self.graph.connections.add(zonepair)

    def file_to_graph(self, file_path: str) -> tuple[int, Graph]:
        """Parse a file and construct its graph.

        Args:
            file_path: The path to the input file.

        Returns:
            A tuple containing the number of drones and the graph.
        """
        with open(file_path, "r") as f:
            for self.line_i, line in enumerate(f, self.line_i):
                if len(line := self.expurgate_line(line)) == 0:
                    continue

                # [[    NB_DRONES   ]]
                self.extract_nb_drones(line)
                break

            self.line_i = self.line_i + 1
            for self.line_i, line in enumerate(f, self.line_i):
                if len(line := self.expurgate_line(line)) == 0:
                    continue

                # [[    START_HUB   ]]
                if match := Regex.start_hub.match(line):
                    if self.graph.start_hub.name:
                        raise DuplicateStartHubError(self.line_i)
                    self.graph.start_hub = Parser.extract_hub(self, match)
                    self.graph.start_hub.max_capacity = float("inf")

                # [[    END_HUB     ]]
                elif match := Regex.end_hub.match(line):
                    if self.graph.end_hub.name:
                        raise DuplicateEndHubError(self.line_i)
                    self.graph.end_hub = Parser.extract_hub(self, match)
                    if self.graph.end_hub.type == HubTypes.BLOCKED:
                        raise BlockedEndHubError(self.line_i)
                    self.graph.end_hub.max_capacity = float("inf")

                # [[        HUB     ]]
                elif match := Regex.hub.match(line):
                    hub = Parser.extract_hub(self, match)
                    if hub.max_capacity == 0:
                        raise BlockedHubMaxDronesError(
                            self.line_i, hub.max_capacity
                        )

                # [[    CONNECTION  ]]
                elif match := Regex.connection.match(line):
                    Parser.extract_connection(self, match)
                else:
                    raise InvalidMapFormatError(self.line_i)

            if not self.graph.start_hub.name:
                raise MissingStartHubError(self.line_i)
            if not self.graph.end_hub.name:
                raise MissingEndHubError(self.line_i)

            ok_hubs_count = len(self.graph.hubs) - len(self.graph.block_hubs)
            ok_cons_count = len(self.graph.connections) - len(
                self.graph.block_connections
            )

            if ok_cons_count >= ok_hubs_count:
                self.graph.mutli_routes_possible = True

        return (self.nb_drone, self.graph)
