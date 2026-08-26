from dataclasses import dataclass
from errors import ParseError
from components import Graph
from graphregex import Regex



# NOTE:  read about "Pattern[str]" anotation

@dataclass
class Parser:
    def __init__(self):
        self.nb_drone:int = -1
        self.graph:Graph = Graph()
        self.disposed_keys: list[str]  = []
        self.line_num:int = 1


    @staticmethod
    def expurgate_line(line:str) -> str:
        """One liner method to expurgate a line from comment
            return: a clean line from comments"""

        return (line.split('#',1)[0].rstrip())



    def extract_nb_drones(self, line:str) -> None:

        tokkens = line.split(' ')
        print(f"tokken: '{tokkens[0]}'")
        if tokkens[0] != "nb_drones:":
            raise ParseError(self.line_num,
                             "File must start with nb_drone, "+
                             f"got `{tokkens[0]}`")
        if len(tokkens) < 2:
            raise ParseError(self.line_num,
                             "[nb_drones] - Got no value")
        if len(tokkens) > 2:
            raise ParseError(self.line_num,
                             "[nb_drones] - Got extra values")
        try:
            if (val := int(tokkens[1])) == 0:
                raise ParseError(self.line_num,
                                 f"[nb_drones] - Can't do much with 0 drones")
        except TypeError:
            raise ParseError(self.line_num,
                    f"[nb_drones] - Expected number, got: {tokkens[1]}")
        else:
            self.disposed_keys.append('nb_drone:')
            self.nb_drone = val



    def extract_hub(self, line:str) -> None:



        


        

    def file_to_gragh(self, file_path:str) -> tuple[int, Graph]:
        """return: tuple containing number of drone and gragh"""

        with open(file_path, 'r') as f:
            # Loop to extract 'nb_drone:'
            for self.line_num, line in enumerate(f, self.line_num):
                if len(line := self.expurgate_line(line)) == 0:
                    continue
                self.extract_nb_drones(line)
                break;


            # Loop to extract 'Hubs:'
            for self.line_num, line in enumerate(f, self.line_num):
                if len(line := self.expurgate_line(line)) == 0:
                    continue
                if (Parser.extract_hub(self, line) == None):
                    break


            if not 'end_hub:' in self.disposed_keys:
                raise ParseError(
                        self.line_num, "Hubs section missing `start_hub:`")
            if not 'start_hub:' in self.disposed_keys:
                raise ParseError(
                        self.line_num, "Hubs section missing `end_hub:`")

            #Loop to extract 'Connections:'
            for self.line_num, line in enumerate(f, self.line_num):
                if len(line := self.expurgate_line(line)) == 0:
                    continue



                # more to parse later
        return (self.nb_drone, self.graph)
