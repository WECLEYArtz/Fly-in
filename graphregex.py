from re import compile, Pattern
from dataclasses import dataclass

@dataclass
class Regex:
    val:str=r"\S+"

    metadata:str=rf"(?:\[\s*(?P<metadata>.*)?\s*\])?"

    hub_data:str=\
    rf"(?P<name>{val})\s+(?P<x>{val})\s+(?P<y>{val})\s*{metadata}\s*$"

    start_hub:Pattern[str]=compile(rf"start_hub:\s+{hub_data}")
    hub:Pattern[str]=compile(rf"hub:\s+{hub_data}")
    end_hub:Pattern[str]=compile(rf"end_hub:\s+{hub_data}")
    connnection:Pattern[str]=\
    compile(rf"connection:\s+(?P<zone1>{val})-(?P<zone2>{val})\s*{metadata}\s*$")
