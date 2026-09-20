from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

# NOTE: read about __future__
# NOTE: read about "dataclass"
#   and "slots=True" why and how they increase performance

# NOTE: read about why:
#   "Fields without default values cannot appear after fields
#   with default values [reportGeneralTypeIssues]"


class HubTypes(Enum):
    BLOCKED = -42
    RESTRICTED = 2
    NORMAL = 1
    PRIORITY = -1


@dataclass
class Drone:
    id: int
    path_id: int
    hub_id: int


@dataclass
class Hub:
    name: str = ""
    name_clr: str = ""
    cord: tuple[int, int] = (0, 0)
    type: HubTypes = HubTypes.NORMAL
    max_capacity: int | float = 1
    algo_penalty: int = 0
    users: list[Drone] = field(default_factory=list[Drone])

    def __str__(self) -> str:
        return self.name_clr


@dataclass
class Connection:
    xpairs: dict[str, Hub] = field(default_factory=dict[str, Hub])
    name: str = ""
    name_clr: str = ""
    max_capacity: int | float = 1
    algo_penalty: int = 0
    users: list[Drone] = field(default_factory=list[Drone])


Path: TypeAlias = list[Hub | Connection]


# NOTE: read about field(default_factory=list)
# NOTE: the way sim_previous_con is initialized is fucking ugly...
@dataclass
class Adjacency:
    connections: list[Connection] = field(default_factory=list[Connection])

    algo_cost_to_root: int | float = float("inf")
    algo_prev_hub: Hub | None = None
    algo_prev_con: Connection | None = None


# NOTE: double check if hubs is even used globally

# NOTE: connections might be potentially unused in the future
# NOTE: Read about defaultdict


class Graph:
    """A gragh class to store a dictionary with the following asignments:
    - Key:      Hub name as string
    - Value:    List of every connection related to that hub

    This helps with retrieving neighbors when needed,
    Since every connection also stores the hubs pair it's linking
    """

    hubs: dict[str, Hub] = defaultdict(Hub)
    adjacency_list: dict[str, Adjacency] = defaultdict(Adjacency)
    start_hub: Hub = Hub()
    end_hub: Hub = Hub()
    mutli_routes_possible: bool = False
    cons_count: int = 0


def DEBUG_PATH(path: Path) -> None:
    print("[Debug]: Path: ")
    for hub in path:
        if not isinstance(hub, Hub):
            continue
        print(f"    {hub.name, hub.max_capacity, hub.users}")
