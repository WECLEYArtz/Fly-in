from re import compile, Pattern
from dataclasses import dataclass


@dataclass
class Regex:
    """Define the regular expressions used to parse the input format.

    The expressions match hub data, connection data, and their associated
    metadata.

    """

    val: str = r"\S+"
    metadata: str = r"(?:\[\s*(?P<metadata>.*)?\s*\])?"
    hub_data: str = (
        rf"(?P<name>{val})\s+(?P<x>{val})\s+(?P<y>{val})\s*{metadata}\s*$"
    )

    color_meta: Pattern[str] = compile(rf"color=(?P<value>{val})")
    zone_meta: Pattern[str] = compile(rf"zone=(?P<value>{val})")
    mxd_meta: Pattern[str] = compile(rf"max_drones=(?P<value>{val})")
    mxlc_meta: Pattern[str] = compile(rf"max_link_capacity=(?P<value>{val})")

    start_hub: Pattern[str] = compile(rf"\s*start_hub:\s+{hub_data}")

    hub: Pattern[str] = compile(rf"\s*hub:\s+{hub_data}")

    end_hub: Pattern[str] = compile(rf"\s*end_hub:\s+{hub_data}")

    connection: Pattern[str] = compile(
        rf"\s*connection:\s+(?P<zone1>{val})-(?P<zone2>{val})\s*{metadata}\s*$"
    )
