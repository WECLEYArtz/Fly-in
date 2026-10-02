import sys

from algo import Algo
from errors import ParseError, ArgError, AlgoError
from parser import Parser
from argvalidator import ArgValidator
from simulation import Simulation

if __name__ == "__main__":
    try:
        file_path: str = ArgValidator.validate(sys.argv)

        nb_drones, graph = Parser().file_to_graph(file_path)
        sim = Simulation(nb_drones, graph)
        sim.path_tiers = Algo.get_paths(graph, 2)
        sim.init_drone_paths()
        sim.run_simulation()
    except (ArgError, ParseError, AlgoError) as e:
        sys.exit(f"\033[31m[{e.__class__.__name__}]: \033[33m {e} \033[0m ")
    except UnicodeDecodeError:
        sys.exit("None UTF-8 file was given\n")
    except KeyboardInterrupt:
        sys.exit("Program Terminated!\n")
    # except Exception as e:
    #     sys.exit("Unexpected error: " + str(e))
