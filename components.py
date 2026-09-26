from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

class HubTypes(Enum):
    """Define the available hub, or zone, types."""

    BLOCKED = -42
    RESTRICTED = 2
    NORMAL = 1
    PRIORITY = -1


class Drone:
    """Represent a drone and its current path and hub."""

    def __init__(self, id: int, path_id: int, hub_id: int):
        """Initialize a drone.

        Args:
            id: The drone ID, starting at 1.
            path_id: The assigned path ID.
            hub_id: The current hub, connection ID, or position.
        """
        self.id: int = id
        self.path_id: int = path_id
        self.hub_id: int = hub_id


class Hub:
    """Represent a hub and its metadata.

    Attributes:
        name: The hub name.
        name_clr: The ANSI-colored hub name.
        cord: The hub coordinates as an ``(x, y)`` tuple.
        type: The hub's zone type.
        max_capacity: The hub's maximum capacity.
        algo_penalty: A per-hub penalty used by the pathfinding algorithm.
    """

    name: str = ""
    name_clr: str = ""
    cord: tuple[int, int] = (0, 0)
    type: HubTypes = HubTypes.NORMAL
    max_capacity: int | float = 1
    algo_penalty: int = 0

    def __str__(self) -> str:
        """Return the colored hub name."""
        return self.name_clr


class Connection:
    """Represent a connection between two hubs."""

    def __init__(self, xpairs: dict[str, Hub]):
        """Initialize a connection.

        Args:
            xpairs: A dictionary mapping each hub name to the hub at the
                opposite end of the connection.
        """
        self.xpairs: dict[str, Hub] = xpairs
        self.name: str = ""
        self.name_clr: str = ""
        self.max_capacity: int | float = 1
        self.algo_penalty: int = 0


Path: TypeAlias = list[Hub | Connection]


@dataclass
class Adjacency:
    """Store the data needed to find paths from a hub.

    Instances are stored as values in the graph's adjacency list.

    Attributes:
        connections: The hub's connections.
        algo_cost_to_root: The cost from the start to the current hub.
        algo_prev_hub: The previous hub.
        algo_prev_con: The previous connection.
    """

    connections: list[Connection] = field(default_factory=list[Connection])

    algo_cost_to_root: int | float = float("inf")
    algo_prev_hub: Hub | None = None
    algo_prev_con: Connection | None = None


class Graph:
    """Store the graph and its pathfinding data.

    Attributes:
        hubs: A mapping of hub names to hub objects.
        adjacency_list: A mapping of hub names to adjacency data.
        start_hub: The start hub.
        end_hub: The end hub.
        mutli_routes_possible: Whether multiple paths can be found.

    The adjacency list helps retrieve neighbors when needed. Each connection
    also stores the pair of hubs that it links.
    """

    hubs: dict[str, Hub] = defaultdict(Hub)
    adjacency_list: dict[str, Adjacency] = defaultdict(Adjacency)
    start_hub: Hub = Hub()
    end_hub: Hub = Hub()
    mutli_routes_possible: bool = False
