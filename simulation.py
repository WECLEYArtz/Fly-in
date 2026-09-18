from components import Graph, Drone, Path, HubTypes, Hub, Connection
from heapq import heappop, heappush


class Simulation:
    def __init__(self, nb_drones: int, graph: Graph):
        self.nb_drones: int = nb_drones
        self.graph: Graph = graph
        self.path_tiers: list[Path] = []

    def init_drone_paths(self):
        bottlenecks: list[int | float] = [
                min([e.max_capacity for e in self.path_tiers[0]]),
                min([e.max_capacity for e in self.path_tiers[1]])]

        path_turns: list[int] = [
                sum([abs(e.type.value) for e in self.path_tiers[0]
                     if isinstance(e, Hub)]),
                sum([abs(e.type.value) for e in self.path_tiers[1]
                     if isinstance(e, Hub)])]

        paths_hq: list[tuple[int, int, Path]] = [
                (path_turns[0], 0, self.path_tiers[0]),
                (path_turns[1], 1, self.path_tiers[1])]

        start_hub_users = self.graph.start_hub.users
        nb_drones = self.nb_drones
        drone_id = 0
        while (nb_drones):
            turns, path_index, path = heappop(paths_hq)

            for _ in range(int(bottlenecks[path_index])):
                start_hub_users.append(Drone(drone_id, path_index, 0))
                drone_id += 1
                nb_drones -= 1
            heappush(paths_hq, (turns + 1, path_index, path))

    def run_simulation(self):
        logs: list[str] = []
        paths_len: list[int] = [len(self.path_tiers[0]),
                                len(self.path_tiers[1])]
        next_con: Connection = Connection()  # hacky way to fix typing
        next_hub: Hub = Hub()                # hacky way to fix typing

        drones = self.graph.start_hub.users.copy()
        connections_to_clean: list[Connection] = [
                e for path in self.path_tiers
                for e in path if isinstance(e, Connection)]
        while (len(self.graph.end_hub.users) < self.nb_drones):
            # print()
            for _drone in drones:
                # print("[Debug]: >>> testing drone", _drone.id)
                _path = self.path_tiers[_drone.path_id]
                # DEBUG_PATH(_path)
                if (_drone.hub_id == paths_len[_drone.path_id]-1):
                    continue
                if (_drone.hub_id % 2):
                    _drone.hub_id += 1
                    logs.append(f'D{_drone.id}-'
                                + f'{_path[_drone.hub_id].name_clr}')
                    continue

                if (isinstance(e := _path[_drone.hub_id + 1], Connection)):
                    next_con = e
                if (isinstance(e := _path[_drone.hub_id + 2], Hub)):
                    next_hub = e

                if (len(next_con.users) < next_con.max_capacity) and\
                   (len(next_hub.users) < next_hub.max_capacity):
                    next_con.users.append(_drone)
                    next_hub.users.append(_drone)
                    _path[_drone.hub_id].users.remove(_drone)

                    if (next_hub.type == HubTypes.RESTRICTED):
                        _drone.hub_id += 1
                        logs.append(f'D{_drone.id}-'
                                    + f'{_path[_drone.hub_id-1].name_clr}-'
                                    + f'{_path[_drone.hub_id+1].name_clr}')
                    else:
                        _drone.hub_id += 2
                        logs.append(f'D{_drone.id}-'
                                    + f'{_path[_drone.hub_id].name_clr}')
            if logs:
                print(' '.join(logs))
                logs = []

            for con in connections_to_clean:
                con.users = []
