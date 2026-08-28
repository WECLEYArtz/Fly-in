import sys
from errors import ParseError, ArgError
from components import Graph
from parser import Parser
from argvalidator import ArgValidator


def  main() -> None:
    file_path:str = ArgValidator.validate(sys.argv)
    nb_drones, graph = Parser().file_to_gragh(file_path) 

    # algo to bring back path
    # simulation to take that path later

    

if __name__ == "__main__":
    try:
        main()
    except (ArgError, ParseError) as e:
        print(f"[{e.__class__.__name__}]:", e)
