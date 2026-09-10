import sys

from components import Hub
from algo import Algo, Path
from errors import ParseError, ArgError, AlgoError
from parser import Parser
from argvalidator import ArgValidator
from simulation import Simulation 

# NOTE: delete when pushing
def debug_visualise_paths():
    paths: list[Path] = [Simulation.path_tier1, Simulation.path_tier2]
    for path in paths:
        for e in path:
            print(e, end=' ')
        print("\n")


if __name__ == "__main__":
    try:
        file_path:str = ArgValidator.validate(sys.argv)

        nb_drones, graph = Parser().file_to_graph(file_path) 
        Simulation.path_tier1, Simulation.path_tier2 = Algo.get_paths(graph, 2)
        Simulation.init_drone_paths(nb_drones)

        debug_visualise_paths()


        # simulation to take that path later
    except (ArgError, ParseError, AlgoError) as e:
        print(f"[{e.__class__.__name__}]", e)
    except KeyboardInterrupt:
        print("Program Terminated!\n"+
              "enough with the childish takesies backsies.")
