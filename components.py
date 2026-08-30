from collections import defaultdict
from dataclasses import dataclass, field
from webcolors import IntegerRGB
from enum import Enum


#NOTE: read about __future__
#NOTE: read about "dataclass" and "slots=True" why and how they increase performance
#NOTE: read about why  "Fields without default values cannot appear after fields with default values [reportGeneralTypeIssues]"


@dataclass
class Drone:
    id:int
    fly_Hub:str
    fly_path:list[str]



class HubTypes(Enum):
     BLOCKED = -42
     RESTRICTED = 2
     NORMAL = 1
     PRIORITY = -1


class Hub:
    name:str = ""
    name_colored:str = ""
    cord:tuple[int,int] = (0,0)
    type:HubTypes = HubTypes.NORMAL
    color:str = ''
    max_drone:int = 1
    sim_users:int = 0

    def __str__(self) -> str:
        return self.name_colored



@dataclass
class Connection:
    xpairs:dict[Hub,Hub] = field(default_factory=dict[Hub,Hub])
    max_link_capacity:int = 1
    sim_users:int = 0


#NOTE: read about field(default_factory=list)
#NOTE: the way sim_previous_con is initialized is fucking ugly...
@dataclass
class Adjacency:
    connections:list[Connection] = field(default_factory=list[Connection])

    sim_cost_to_root:int|float = float('inf')
    sim_previous_hub:Hub = field(default_factory=Hub)
    sim_previous_con:Connection = field(default_factory=Connection)

    



#NOTE: double check if hubs is even used globally

#NOTE: connections might be potentially unused in the future
#NOTE: Read about defaultdict

class Graph:
    """A gragh class to store a dictionary with the following asignments:
    - Key:      Hub name as string
    - Value:    List of every connection related to that hub

    This helps with retrieving neighbors when needed,
    Since every connection also stores the hubs pair it's linking
    """
    hubs: dict[str, Hub] = defaultdict(Hub)
    adjacency_list: dict[Hub, Adjacency] = defaultdict(Adjacency)
    start_hub:Hub = Hub()
    end_hub:Hub = Hub()
