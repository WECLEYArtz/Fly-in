from enum import Enum
from dataclasses import dataclass

#NOTE: read about __future__
#NOTE: read about "dataclass" and "slots=True" why and how they increase performance
#NOTE: read about why  "Fields without default values cannot appear after fields with default values [reportGeneralTypeIssues]"


@dataclass(slots=True)
class Drone:
    id:int
    fly_Hub:str
    fly_path:list[str]
    # fly_status:DroneStatus


class HubTypes(Enum):
    BLOCKED= float("inf")
    RESTRICTED= 2
    NORMAL= 1
    PRIORITY= 1


@dataclass
class Hub:
    name:str = "Unknown"
    cord:tuple[int,int] = (0,0)
    type:HubTypes = HubTypes.NORMAL
    color:str = 'white'
    max_drone:int = 1



@dataclass(slots=True)
class Connection:
    name:str
    max_link_capacity:int
    Hubs:set[Hub]
    travelers:list[Drone]


class Graph:
    """A gragh class to store a dictionary with the following asignments:
    - Key:      Hub name as string
    - Value:    List of every connection related to that hub

    This helps with retrieving neighbors when needed,
    Since every connection also stores the hubs pair it's linking
    """
    hubs: dict[str, Hub] = {}
    connections: list[Connection] = []
    adjacency: dict[str, list[Connection]] = {}
    start_hub:str = ""
    end_hub:str = ""
