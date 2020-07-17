from typing import Dict


def locals_to_params(args: Dict) -> Dict:
    copy = dict()
    for key in args:
        if key == "self":
            continue
        if args[key] is not None:
            copy[key] = args[key]
    return copy
