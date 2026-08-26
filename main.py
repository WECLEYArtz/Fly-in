import sys
from components import Graph
from parser import Parser
from argvalidator import ArgValidator


def  main():
    file_path:str = ArgValidator.validate(sys.argv)
    nb_drones, graph = Parser().file_to_gragh(file_path) 
    print("Got data:\n", nb_drones, graph)



    # algo to bring back path
    # simulation to take that path later

    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[{e.__class__.__name__}]:", e)
