import sys

from algo import Algo, Path
from errors import ParseError, ArgError
from parser import Parser
from argvalidator import ArgValidator




def main() -> None:
    file_path:str = ArgValidator.validate(sys.argv)
    nb_drones, graph = Parser().file_to_gragh(file_path) 
    print('getting path:')
    path1 = Algo.get_paths(graph)


    # simulation to take that path later

    

if __name__ == "__main__":
    try:
        main()
    except (ArgError, ParseError) as e:
        print(f"[{e.__class__.__name__}]", e)
