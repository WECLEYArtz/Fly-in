from components import Graph, Hub, HubTypes, Adjacency, Path, DEBUG_PATH
from errors import AlgoError
from heapq  import heappush, heappop


class Algo:
    @staticmethod
    def dijktra(graph: Graph) -> None:
        pq:list[tuple[int, Hub]] = [(0, graph.start_hub)]
        visited:list[Hub] = []

    
        while pq:
            turns, current = heappop(pq)

            if current.type == HubTypes.BLOCKED:
                continue

            if current == graph.end_hub:
                break;


            for connection in graph.adjacency_list[current.name].connections:

                neighbor:Hub = connection.xpairs[current.name]
                adjacency:Adjacency = graph.adjacency_list[neighbor.name]

                if neighbor in visited:
                    continue

                cost = turns + abs(neighbor.type.value) \
                            + neighbor.algo_penalty \
                            + connection.algo_penalty


                if (cost < adjacency.algo_cost_to_root):
                    adjacency.algo_cost_to_root = cost
                    adjacency.algo_prev_hub = current
                    adjacency.algo_prev_con = connection

                heappush(pq, (cost, neighbor))
                visited.append(current)


    #NOTE: The way this is structured should probably be optimised,
    #       do i need the structure connected this way?

    @staticmethod
    def get_paths(graph: Graph, requested_paths:int) -> list[Path]:
        paths : list[Path] = []

        if not graph.mutli_routes_possible:
            requested_paths = 1

        while len(paths) < requested_paths:
            for adj in graph.adjacency_list.values():
                adj.algo_cost_to_root = float('inf')

            Algo.dijktra(graph)

            crrnt_hub = graph.end_hub
            path: Path = [graph.end_hub]
            crrnt_adj:Adjacency = graph.adjacency_list[graph.end_hub.name]

            if crrnt_adj.algo_prev_hub == None:
                raise AlgoError("END_UNRCHED")

            # Extract result path from adjacency_list
            while (crrnt_hub != graph.start_hub):
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
                # DEBUG_PATH(path)
        return paths
