class ArgError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AlgoError(Exception):
    error_msg: dict[str, str] = {
        "END_UNRCHED": "Couldn't reach end_hub, is it connected to start_hub?",
        "ADJ_EMPT": "Empty adjacency during path creation",
    }

    def __init__(self, code: str) -> None:
        super().__init__(AlgoError.error_msg[code])


class ParseError(Exception):
    error_msg: dict[str, str] = {
        "MXLC_BLK": "max_link_capacity 0 is unsupported"
        + "please clear map from blocked connections",
        "MXLC_INV": "Invalid max_link_capacity value {}",
        "TYP_INV": "Invalid type - got: '{}'\n"
        + "Available types: "
        + "( blocked | restricted | normal | priority )",
        "CLR_INV": "Invalid css color - got: '{}'",
        "MXD_INV": "Invalid max drone - '{}'",
        "MXD_BLK": "Unsupported value of {} for max_drones\n"
        + "If attempting to block a zone,"
        + "Please consider using zone=blocked instead",
        "EH_BLK": "Cannot reach a blocked type end_hub",
        "CORD_DUP": "Cordination duplicated '{}'",
        "INC_META_C": "Incomplete meta data: '{}'\n"
        + "Expected max_link_capacity=<value>",
        "INC_META_H": "Incomplete meta data: '{}'\n"
        + "Expected <key>=<value> pair, Available pair:\n"
        + "- zone=(normal|blocked|restricted|priority)\n"
        + "- color=(existing css color)\n"
        + "- max_drones=(positive integer)",
        "NBD_FIRST": "File must start with literal 'nb_drones:'" + " got '{}'",
        "NBD_EXTRA": "Got extra values for nb_drones",
        "NBD_EMPTY": "Got no value for nb_drones",
        "NBD_USELESS": "Can't do much with {} drones",
        "NBD_INV_NUM": "[nb_drones] - Invalid number: {}",
        "DASH_NAME": "'{}' contains a dash character '-'"
        + ", this may conflict with connection initialising",
        "CORD_ERR": "Error while parsing zone cordination - {}",
        "SLF_LOOP": "Connection ends must be different "
        + ", got: '{}' self connection",
        "CN_UNDF": "Attempting to connect undefined zone '{}'",
        "SH_DUP": "start_hub duplication",
        "H_DUP": "Duplicated hub '{}'",
        "EH_DUP": "end_hub duplication",
        "CN_DUP": "Duplicated connection '{}'",
        "INC_FRM": "Incorrect scheema, Available formats:\n"
        + "- start_hub: <name> <x> <y> [metadata]\n"
        + "- end_hub: <name> <x> <y> [metadata]\n"
        + "- hub: <name> <x> <y> [metadata]\n"
        + "- connection: <name1>-<name2> [metadata]\n",
        "SH_NON": "Missing 'start_hub:'",
        "EH_NON": "Missing 'end_hub:'",
    }

    def __init__(
        self,
        line: int,
        code: str,
        val: str | int | set[str] | tuple[int, int] | None = None,
    ) -> None:
        super().__init__(
            f"[{code}] (line {line}):" + self.error_msg[code].format(val)
        )
