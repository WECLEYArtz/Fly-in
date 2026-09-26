from components import Graph, Drone, Path, HubTypes, Hub, Connection
from collections import defaultdict
from heapq import heappop, heappush


class Simulation:
    """Run the drone simulation.

    Attributes:
        users: The users of each hub or connection during the simulation.
    """

    users: dict[Hub | Connection, list[Drone]] = defaultdict(list[Drone])

    def __init__(self, nb_drones: int, graph: Graph):
        """Initialize the simulation.

        Args:
            nb_drones: The number of drones.
            graph: The graph containing the map data.

        Attributes:
            path_tiers: Paths ordered by length.
        """
        self.nb_drones: int = nb_drones
        self.graph: Graph = graph
        self.path_tiers: list[Path] = []

    def init_drone_paths(self) -> None:
        """Assign each drone a path for the simulation.

        Calculate the bottleneck and number of turns for each path. The
        algorithm assigns drones to the first path until it reaches its turn
        count, then distributes the remaining drones across both paths.

        A heap queue automatically switches between paths.
        """
        bottlenecks: list[int | float] = [
            min([e.max_capacity for e in self.path_tiers[0]]),
            min([e.max_capacity for e in self.path_tiers[1]]),
        ]

        path_turns: list[int] = [
            sum(
                [
                    abs(e.type.value)
                    for e in self.path_tiers[0]
                    if isinstance(e, Hub)
                ]
            ),
            sum(
                [
                    abs(e.type.value)
                    for e in self.path_tiers[1]
                    if isinstance(e, Hub)
                ]
            ),
        ]

        paths_hq: list[tuple[int, int, Path]] = [
            (path_turns[0], 0, self.path_tiers[0]),
            (path_turns[1], 1, self.path_tiers[1]),
        ]

        start_hub_users = self.users[self.graph.start_hub]
        nb_drones = self.nb_drones
        drone_id = 0
        while nb_drones:
            turns, path_index, path = heappop(paths_hq)
            for _ in range(int(bottlenecks[path_index])):
                start_hub_users.append(Drone(drone_id, path_index, 0))
                drone_id += 1
                nb_drones -= 1
            heappush(paths_hq, (turns + 1, path_index, path))

    def run_simulation(self) -> None:
        """Run the simulation using the prepared paths.

        Iterate over each drone and process its next move while recording its
        action and position for the other drones.

        Each iteration cleans the connections for the next run.
        """
        logs: list[str] = []
        paths_len: list[int] = [
            len(self.path_tiers[0]),
            len(self.path_tiers[1]),
        ]
        next_con: Connection = Connection({})  # hacky way to fix typing
        next_hub: Hub = Hub()  # hacky way to fix typing

        drones = self.users[self.graph.start_hub].copy()
        connections_to_clean: list[Connection] = [
            e
            for path in self.path_tiers
            for e in path
            if isinstance(e, Connection)
        ]
        while len(self.users[self.graph.end_hub]) < self.nb_drones:
            for _drone in drones:
                _path = self.path_tiers[_drone.path_id]
                if _drone.hub_id == paths_len[_drone.path_id] - 1:
                    continue
                if _drone.hub_id % 2:
                    _drone.hub_id += 1
                    logs.append(
                        f"D{_drone.id}-" + f"{_path[_drone.hub_id].name_clr}"
                    )
                    continue

                if isinstance(e := _path[_drone.hub_id + 1], Connection):
                    next_con = e
                if isinstance(e := _path[_drone.hub_id + 2], Hub):
                    next_hub = e

                if (len(self.users[next_con]) < next_con.max_capacity) and (
                    len(self.users[next_hub]) < next_hub.max_capacity
                ):
                    self.users[next_con].append(_drone)
                    self.users[next_hub].append(_drone)
                    self.users[_path[_drone.hub_id]].remove(_drone)

                    if next_hub.type == HubTypes.RESTRICTED:
                        _drone.hub_id += 1
                        logs.append(
                            f"D{_drone.id}-"
                            + f"{_path[_drone.hub_id-1].name_clr}-"
                            + f"{_path[_drone.hub_id+1].name_clr}"
                        )
                    else:
                        _drone.hub_id += 2
                        logs.append(
                            f"D{_drone.id}-"
                            + f"{_path[_drone.hub_id].name_clr}"
                        )
            if logs:
                print(" ".join(logs))
                logs = []

            for con in connections_to_clean:
                self.users[con] = []
