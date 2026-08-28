from dataclasses import dataclass
from errors import ParseError
from components import Graph, Hub, HubTypes, Connection
from graphregex import Regex
from re import Match
import webcolors


# NOTE:  read about "Pattern[str]" anotation

@dataclass
class Parser:
    def __init__(self) -> None:
        self.nb_drone:int
        self.graph:Graph = Graph()
        self.line_i:int = 1
        self.connections:list[set[str]] = []



    @staticmethod
    def expurgate_line(line:str) -> str:
        """One liner method to expurgate a line from comment
            return: a clean line from comments"""

        return (line.split('#',1)[0].rstrip())



    def metadata_connection(self, metadata_list: list[str]) -> int:
        value:int = 0;
        for meta in metadata_list:
            if not (match := Regex.mxlc_meta.match(meta)):
                raise ParseError(self.line_i, "INC_META_C", meta)
            try:
                value = int(match.group('value'))   
            except ValueError as e:
                raise ParseError(self.line_i, "MXLC_INV", e.__str__())
        return value



    def metadata_hub(self, metadata_list: list[str]) -> tuple[str, str, int]:
        zone_type: str = 'normal'
        color: str = ''
        max_drone: int = 1

        for meta in metadata_list:
            if  (m := Regex.zone_meta.match(meta)):
                if not m.group('value') in HubTypes.Data.keys():
                    raise ParseError(self.line_i, "TYP_INV", m.group('value'))
                zone_type = m.group('value')

            elif (m := Regex.color_meta.match(meta)):
                try:
                    color = webcolors.name_to_hex(m.group('value'))
                except:
                    raise ParseError(self.line_i,"CLR_INV",
                                     m.group('value'))
                    
            elif (m := Regex.mxd_meta.match(meta)):
                try:
                    max_drone = int(m.group('value'))
                except TypeError as e:
                    raise ParseError(self.line_i, "MXD_INV", e.__str__())
            else:
                raise ParseError(self.line_i, "INC_META_H", meta)
        return (zone_type, color, max_drone)



    #PERF: will this be better off with a regex?
    def extract_nb_drones(self, line:str) -> None:

        tokkens = line.split()
        if tokkens[0] != "nb_drones:":
            raise ParseError(self.line_i, "NBD_FIRST", tokkens[0])
        if len(tokkens) < 2:
            raise ParseError(self.line_i, "NBD_EMPTY")
        if len(tokkens) > 2:
            raise ParseError(self.line_i, "NBD_EXTRA")
        try:
            if (val := int(tokkens[1])) <= 0:
                raise ParseError(self.line_i, "NBD_USELESS", val)
        except ValueError:
            raise ParseError(self.line_i, "NBD_INV_NUM", tokkens[1])
        self.nb_drone = val

    

    def extract_hub(self, match: Match[str]) -> None:
        hub = Hub()
        hub.name = match.group('name')
        if '-' in hub.name:
            raise ParseError(self.line_i, "DSH_NAME", hub.name)
        try:
            hub.cord = (int(match.group("x")), int(match.group("y")))
        except ValueError as e:
            raise ParseError(self.line_i, "CORD_ERR", e.__str__())

        if match.group('metadata'):
            meta_list = match.group('metadata').split()
            hub.type, hub.color, hub.max_drone = self.metadata_hub(meta_list)

        print("[Debug Hub]:",hub.name, hub.cord, hub. color, hub.max_drone, hub.type)

        if self.graph.hubs.get(hub.name):
            raise ParseError(self.line_i, "H_DUP", hub.name)
        self.graph.hubs[hub.name] = hub
        


    def extract_connection(self, match: Match[str]) -> None:
        zone1=match.group('zone1')
        zone2:str=match.group('zone2')
        zonepair:set[str]={zone1,zone2}

        if (zone1 == zone2):
            raise ParseError(self.line_i, "END_DUP", zone1)
        if not zone1 in self.graph.hubs.keys():
            raise ParseError(self.line_i, "CN_UNDF", zone2)
        if not zone2 in self.graph.hubs.keys():
            raise ParseError(self.line_i, "CN_UNDF", zone2)
        if zonepair in self.connections:
            raise ParseError(self.line_i, "CN_DUP", zonepair)


        max_link_capacity:int = 1;
        if match.group('metadata'):
            meta_list:list[str] = match.group('metadata').split()
            max_link_capacity = self.metadata_connection(meta_list)
        new_connection=Connection(max_link_capacity,{
            self.graph.hubs[zone1],
            self.graph.hubs[zone2]
            })
        self.graph.adjacency[zone1].append(new_connection)
        self.graph.adjacency[zone2].append(new_connection)
        self.connections.append(zonepair)



    def file_to_gragh(self, file_path:str) -> tuple[int, Graph]:
        """return: tuple containing number of drone and gragh"""

        with open(file_path, 'r') as f:
            for self.line_i, line in enumerate(f, self.line_i):
                if len(line := self.expurgate_line(line)) == 0:
                    continue

                # [[    NB_DRONES   ]]
                self.extract_nb_drones(line)
                break;

            self.line_i = self.line_i +1
            for self.line_i, line in enumerate(f, self.line_i):
                if len(line := self.expurgate_line(line)) == 0:
                    continue


                # [[    START_HUB   ]]
                if (match:= Regex.start_hub.match(line)):
                    if self.graph.start_hub:
                        raise ParseError(self.line_i, "SH_DUP")
                    Parser.extract_hub(self, match)
                    self.graph.start_hub = match.group('name')
                    

                # [[    END_HUB     ]]
                elif (match:= Regex.end_hub.match(line)):
                    if self.graph.end_hub:
                        raise ParseError(self.line_i, "EH_DUP")
                    Parser.extract_hub(self, match)
                    self.graph.end_hub = match.group('name')


                # [[        HUB     ]]
                elif (match:= Regex.hub.match(line)):
                    Parser.extract_hub(self, match)


                # [[    CONNECTION  ]]
                elif (match:= Regex.connection.match(line)):
                    Parser.extract_connection(self, match)
                else:
                    raise ParseError(self.line_i, "INC_FRM")

            if not self.graph.start_hub:
                raise ParseError(self.line_i, "SH_NON")
            if not self.graph.end_hub:
                raise ParseError(self.line_i, "EH_NON")

        return (self.nb_drone, self.graph)
