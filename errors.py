from components import  HubTypes
class ArgError(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)


class ParseError(Exception):
    error_msg:dict[str,str]=\
            {
                    "MXLC_INV":"Invalid max_link_capacity value {}",

                    "TYP_INV": "Invalid type - got: '{}'\n"+
                        "Available types: "+
                        "( blocked | restricted | normal | priority )",

                    "CLR_INV": "Invalid css color - got: '{}'",

                    "MXD_INV": "Invalid max drone - '{}'",

                    "INC_META_C": "Incomplete meta data: '{}'\n"+
                        "Expected max_link_capacity=<value>",

                    "INC_META_H": "Incomplete meta data: '{}'\n"+
                        "Expected <key>=<value> pair, Available pair:\n"+
                        "- zone=(normal|blocked|restricted|priority)\n"+
                        "- color=(existing css color)\n"+
                        "- max_drones=(positive integer)",

                    "NBD_FIRST": "File must start with literal 'nb_drone:'"+
                        "- got '{}'",

                    "NBD_EXTRA":    "Got extra values for nb_drones",

                    "NBD_EMPTY":    "Got no value for nb_drones",

                    "NBD_USELESS":  "Can't do much with {} drones",

                    "NBD_INV_NUM":  "[nb_drones] - Invalid number: {}",

                    "DSH_NAME": "'{}' contains '-'",

                    "CORD_ERR": "Error while parsing zone cordination - {}",

                    "SLF_LOOP":  "Connection ends must be different "+
                        ", got: '{}' self connection",

                    "CN_UNDF": "Attempting to connect undefined zone '{}'",

                    "SH_DUP":   "start_hub duplication",

                    "H_DUP":    "Duplicated hub '{}'",

                    "EH_DUP":   "end_hub duplication",

                    "CN_DUP":   "Duplicated connection '{}'",

                    "INC_FRM":  "Incorrect scheema, Available formats:\n"+
                        "- start_hub: <name> <x> <y> [metadata]\n"+
                        "- end_hub: <name> <x> <y> [metadata]\n"+
                        "- hub: <name> <x> <y> [metadata]\n"+
                        "- connection: <name1>-<name2> [metadata]\n",

                    "SH_NON":   "Missing 'start_hub:'",

                    "EH_NON":   "Missing 'end_hub:'",

                    }

    def __init__(self, line:int, code:str,
                 val:str|int|set[str]|None = None) -> None:
        super().__init__(f"[{code}] (line {line}): " +
                         self.error_msg[code].format(val))

