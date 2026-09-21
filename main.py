import sys

from algo import Algo
from errors import ParseError, ArgError, AlgoError
from parser import Parser
from argvalidator import ArgValidator
from simulation import Simulation


# NOTE: delete when pushing

# def debug_visualise_paths(sim: Simulation) -> None:
#
#     paths: list[Path] = [sim.path_tiers[0], sim.path_tiers[1]]
#     for path in paths:
#         for e in path:
#             print(e, end=" ")
#         print("\n")


if __name__ == "__main__":
    try:
        file_path: str = ArgValidator.validate(sys.argv)

        nb_drones, graph = Parser().file_to_graph(file_path)
        sim = Simulation(nb_drones, graph)
        sim.path_tiers = Algo.get_paths(graph, 2)
        if len(sim.path_tiers) < 2:
            sim.path_tiers.append(sim.path_tiers[0])
        sim.init_drone_paths()
        sim.run_simulation()

    except (ArgError, ParseError, AlgoError) as e:
        print(f"[{e.__class__.__name__}]", e)
    except KeyboardInterrupt:
        print("Program Terminated!\n")
