from dataclasses import dataclass
from errors import ParseError
from components import Graph, Hub, HubTypes, Connection
from graphregex import Regex
from re import Match
from webcolors import name_to_rgb, IntegerRGB, names as webnames


# NOTE:  read about "Pattern[str]" anotation


@dataclass
class Parser:
    def __init__(self) -> None:
        self.nb_drone:int
        self.graph:Graph = Graph()
        self.line_i:int = 1
        self.connections:list[set[str]] = []
        self.types : dict[str,HubTypes] = { 
         'blocked': HubTypes.BLOCKED,
         'restricted': HubTypes.RESTRICTED,
         'normal': HubTypes.NORMAL,
         'priority':  HubTypes.PRIORITY
                                           }
        self.rainbow:list[IntegerRGB] = [
            name_to_rgb("red"),
            name_to_rgb("orange"),
            name_to_rgb("yellow"),
            name_to_rgb("green"),
            name_to_rgb("blue"),
            name_to_rgb("indigo"),
            name_to_rgb("violet")
            ]



    
    def name_colorizer(self, name: str, color:str) -> str:
        if color == 'rainbow':
            gay_form:list[str]=[];
            for i in range(len(name)):
                r, g, b = self.rainbow[i % len(self.rainbow)]
                gay_form.append(f"\x1b[38;2;{r};{g};{b}m{name[i]}\x1b[0m")
            return ''.join(gay_form)
        else:
            r, g, b = name_to_rgb(color)
            return f"\x1b[38;2;{r};{g};{b}m{name}\x1b[0m"


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



    def metadata_hub(self, metadata_list: list[str]) -> tuple[HubTypes, str, int]:
        zone_type: HubTypes = HubTypes.NORMAL
        color: str = '';
        max_drone: int = 1

        for meta in metadata_list:
            if  (m := Regex.zone_meta.match(meta)):
                if not (zone_type_str:= m.group('value')) in self.types.keys():
                    raise ParseError(self.line_i, "TYP_INV", m.group('value'))
                zone_type = self.types[zone_type_str]

            elif (m := Regex.color_meta.match(meta)):

                color = m.group('value')
                if (not color in webnames()) and (color != 'rainbow'):
                    raise ParseError(self.line_i,"CLR_INV", color)
                    
            elif (m := Regex.mxd_meta.match(meta)):
                try:
                    max_drone = int(m.group('value'))
                except TypeError as e:
                    raise ParseError(self.line_i, "MXD_INV", e.__str__())
                if max_drone <= 0:
                    raise ParseError(self.line_i, "MXD_BLK", max_drone)
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

    

    def extract_hub(self, match: Match[str]) -> Hub:
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
            hub.name_colored = self.name_colorizer(hub.name, hub.color)

        # print("[Debug Hub]:",hub.name, hub.cord, hub. color, hub.max_drone, hub.type)

        if self.graph.hubs.get(hub.name):
            raise ParseError(self.line_i, "H_DUP", hub.name)
        self.graph.hubs[hub.name] = hub
        return hub
        


    def extract_connection(self, match: Match[str]) -> None:
        zone1=match.group('zone1')
        zone2:str=match.group('zone2')
        zonepair:set[str]={zone1,zone2}

        if (zone1 == zone2):
            raise ParseError(self.line_i, "SLF_LOOP", zone1)
        if not zone1 in self.graph.hubs.keys():
            raise ParseError(self.line_i, "CN_UNDF", zone1)
        if not zone2 in self.graph.hubs.keys():
            raise ParseError(self.line_i, "CN_UNDF", zone2)
        if zonepair in self.connections:
            raise ParseError(self.line_i, "CN_DUP", zonepair)

        
        hub1=self.graph.hubs[zone1]
        hub2=self.graph.hubs[zone2]

        connection=Connection({hub1:hub2,
                               hub2:hub1})

        if match.group('metadata'):
            meta_list:list[str] = match.group('metadata').split()
            connection.max_link_capacity = self.metadata_connection(meta_list)


        self.graph.adjacency_list[hub1].connections.append(connection)
        self.graph.adjacency_list[hub2].connections.append(connection)

        self.connections.append(zonepair) #Only parsing life-time



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
                    if self.graph.start_hub.name:
                        raise ParseError(self.line_i, "SH_DUP")
                    self.graph.start_hub = Parser.extract_hub(self, match)


                    # [[    END_HUB     ]]
                elif (match:= Regex.end_hub.match(line)):
                    if self.graph.end_hub.name:
                        raise ParseError(self.line_i, "EH_DUP")
                    self.graph.end_hub =  Parser.extract_hub(self, match)


                    # [[        HUB     ]]
                elif (match:= Regex.hub.match(line)):
                    _ = Parser.extract_hub(self, match)


                    # [[    CONNECTION  ]]
                elif (match:= Regex.connection.match(line)):
                    Parser.extract_connection(self, match)
                else:
                    raise ParseError(self.line_i, "INC_FRM")

            if not self.graph.start_hub.name:
                raise ParseError(self.line_i, "SH_NON")
            if not self.graph.end_hub.name:
                raise ParseError(self.line_i, "EH_NON")

        return (self.nb_drone, self.graph)
