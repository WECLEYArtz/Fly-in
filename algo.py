from heapq import heappop, heappush

from components import Adjacency, Graph, Hub, HubTypes, Path
from errors import AlgoError


class Algo:
    """Base class for finding and generating paths.

    This class provides methods for finding paths through the graph.
    """

    @staticmethod
    def dijktra(graph: Graph) -> None:
        """Produce the best path in a graph.

        Args:
            graph: A graph containing all map data.
        """
        pq: list[tuple[int, int, str]] = [(0, 1, graph.start_hub.name)]
        visited: list[Hub] = []

        while pq:
            turns, _, current_name = heappop(pq)
            current = Graph.hubs[current_name]

            if current.type == HubTypes.BLOCKED:
                continue

            if current == graph.end_hub:
                break

            for connection in graph.adjacency_list[current.name].connections:

                neighbor: Hub = connection.xpairs[current.name]
                adjacency: Adjacency = graph.adjacency_list[neighbor.name]

                if neighbor in visited:
                    continue

                cost = (
                    turns
                    + abs(neighbor.type.value)
                    + neighbor.algo_penalty
                    + connection.algo_penalty
                )

                if cost < adjacency.algo_cost_to_root:
                    adjacency.algo_cost_to_root = cost
                    adjacency.algo_prev_hub = current
                    adjacency.algo_prev_con = connection

                heappush(pq, (cost, neighbor.type.value, neighbor.name))
                visited.append(current)

    @staticmethod
    def get_paths(graph: Graph, requested_paths: int) -> list[Path]:
        """Generate paths by collecting the results of ``dijktra``.

        Args:
            graph: A graph containing all map data.
            requested_paths: The number of paths to try to find. This is
                currently set to 2.

        Returns:
            A list of paths.
        """
        paths: list[Path] = []

        if not graph.mutli_routes_possible:
            requested_paths = 1

        while len(paths) < requested_paths:
            for adj in graph.adjacency_list.values():
                adj.algo_cost_to_root = float("inf")

            Algo.dijktra(graph)

            crrnt_hub = graph.end_hub
            path: Path = [graph.end_hub]
            crrnt_adj: Adjacency = graph.adjacency_list[graph.end_hub.name]

            if not crrnt_adj.algo_prev_hub:
                raise AlgoError("END_UNRCHED")

            while crrnt_hub != graph.start_hub:

                if not (crrnt_adj.algo_prev_con and crrnt_adj.algo_prev_hub):
                    raise AlgoError("ADJ_EMPT")
                crrnt_con = crrnt_adj.algo_prev_con
                crrnt_hub = crrnt_adj.algo_prev_hub
                crrnt_con.algo_penalty += 1
                crrnt_hub.algo_penalty += 1
                path.extend([crrnt_con, crrnt_hub])
                crrnt_adj = graph.adjacency_list[crrnt_hub.name]
            path.reverse()

            if path not in paths:
                paths.append(path)

        if not graph.mutli_routes_possible:
            paths.append(paths[0])
        elif isinstance(h := paths[0][2], Hub) and h.type == HubTypes.PRIORITY:
            paths = [paths[0], paths[0]]
        elif isinstance(h := paths[1][2], Hub) and h.type == HubTypes.PRIORITY:
            paths = [paths[1], paths[1]]
        return paths
