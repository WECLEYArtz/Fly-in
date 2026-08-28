from collections import defaultdict
from dataclasses import dataclass

#NOTE: read about __future__
#NOTE: read about "dataclass" and "slots=True" why and how they increase performance
#NOTE: read about why  "Fields without default values cannot appear after fields with default values [reportGeneralTypeIssues]"


@dataclass
class Drone:
    id:int
    fly_Hub:str
    fly_path:list[str]


class HubTypes:
    Data:dict[str,int]=\
    { 
     'blocked': -1,
     'restricted': 2,
     'normal': 1,
     'priority': 1
     }


class Hub:
    name:str = "unknown"
    cord:tuple[int,int] = (0,0)
    type:str = 'normal'
    color:str | None = None
    max_drone:int = 1



@dataclass
class Connection:
    max_link_capacity:int
    Hubs:set[Hub]
    travelers_count:int = 0


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
    adjacency: dict[str, list[Connection]] = defaultdict(list)
    start_hub:str = ""
    end_hub:str = ""
