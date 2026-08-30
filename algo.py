from typing import TypeAlias
from components import Graph, Hub, Connection, HubTypes, Adjacency
import heapq 

Path : TypeAlias = list[Connection|Hub]

class Algo:
    @staticmethod
    def dijktra(graph: Graph) -> None:
        pq:list[tuple[int, int, Hub]] = [(0, 1, graph.start_hub)]
        visited:list[Hub] = []


    
        while pq:
            turns, _, current = pq.pop()

            if current.type == HubTypes.BLOCKED:
                continue

            if current == graph.end_hub:
                break;

            for connection in graph.adjacency_list[current].connections:

                neighbor:Hub = connection.xpairs[current]
                adjacency:Adjacency = graph.adjacency_list[neighbor]

                if neighbor in visited:
                    continue


                cost = turns + abs(neighbor.type.value);
                node_weight = int(current.type != HubTypes.PRIORITY)
                if (cost < adjacency.sim_cost_to_root):
                    adjacency.sim_cost_to_root = cost
                    adjacency.sim_previous_hub = current
                    adjacency.sim_previous_con = connection

                pq.append((cost, node_weight, neighbor))

                visited.append(current)


    #NOTE: The way this is structured should probably be optimised,
    #       do i need the structure connected this way?
    @staticmethod
    def get_paths(graph: Graph) -> Path:
        Algo.dijktra(graph)

        current_hub = graph.end_hub
        path: Path = [current_hub]
        current_adj:Adjacency = graph.adjacency_list[current_hub]

        while(current_hub != graph.start_hub):
            path.append(current_adj.sim_previous_con)
            path.append(current_adj.sim_previous_hub)
            current_hub = current_adj.sim_previous_hub
            current_adj = graph.adjacency_list[current_adj.sim_previous_hub]

        path.reverse()


        # print(' > '.join(e if isinstance(e, Hub) else '' for e in path))
        for e in path:
            if isinstance(e, Hub): print(e, end=' ')
        return path

