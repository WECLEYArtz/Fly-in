from typing import TypeAlias
from components import Graph, Hub, Connection, HubTypes, Adjacency
from errors import AlgoError
from heapq  import heappush, heappop

Path : TypeAlias = list[Connection|Hub]

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


            for connection in graph.adjacency_list[current].connections:

                neighbor:Hub = connection.xpairs[current]
                adjacency:Adjacency = graph.adjacency_list[neighbor]

                if neighbor in visited:
                    continue

                cost = turns + abs(neighbor.type.value);

                if (cost < adjacency.sim_cost_to_root):
                    adjacency.sim_cost_to_root = cost
                    adjacency.sim_previous_hub = current
                    adjacency.sim_previous_con = connection

                heappush(pq, (cost, neighbor))
                visited.append(current)


    #NOTE: The way this is structured should probably be optimised,
    #       do i need the structure connected this way?
    @staticmethod
    def get_paths(graph: Graph) -> Path:
        Algo.dijktra(graph)

        current_hub = graph.end_hub
        path: Path = [current_hub]
        current_adj:Adjacency = graph.adjacency_list[current_hub]

        if current_adj.sim_previous_hub == None:
            raise AlgoError("Couldn't reach end_hub,"+
                            " is it connected to start_hub?")
        while(current_hub != graph.start_hub):
            if (not current_adj.sim_previous_con) or (not current_adj.sim_previous_hub):
                raise AlgoError("Empty adjacency during path creation")
            path.append(current_adj.sim_previous_con)
            path.append(current_adj.sim_previous_hub)
            current_hub = current_adj.sim_previous_hub
            current_adj = graph.adjacency_list[current_adj.sim_previous_hub]
        path.reverse()


        for e in path:
            if isinstance(e, Hub): print(e, end=' ')
        return path
