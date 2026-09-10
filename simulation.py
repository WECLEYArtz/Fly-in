from components import Graph, Drone
from algo import Path


class Simulation:
    drones: list[Drone] = []
    path_tier1: Path = []
    path_tier2: Path = []

    @staticmethod
    def id_gen(nb_drones:int ):
        for i in range(nb_drones):
            yield i

    @staticmethod
    def init_drone_paths(nb_drones:int):
        bottleneck_1 = min([e.max_capacity for e in Simulation.path_tier1])
        bottleneck_2 = min([e.max_capacity for e in Simulation.path_tier2])
        path_turns_2 = len(Simulation.path_tier2) -1
        turns = 0
        bottlenecks = [bottleneck_2, bottleneck_1]
        paths_list = [Simulation.path_tier2, Simulation.path_tier1]
        drone_id = Simulation.id_gen(nb_drones)

        while (nb_drones):
            if turns == 0:
                turns = path_turns_2 -1
                bottlenecks.reverse()
                paths_list.reverse()

            for _ in range(bottlenecks[0]): #[ init every drone for the current turn]
                Simulation.drones.append(Drone(next(drone_id), paths_list[0]))
                nb_drones -= 1
                if not turns:
                    break
            turns -= 1

    @staticmethod
    def run_simulation(graph: Graph, ):
        pass

