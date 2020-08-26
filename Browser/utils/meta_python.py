from typing import Dict, List, TypeVar


def locals_to_params(args: Dict) -> Dict:
    copy = dict()
    for key in args:
        if key == "self":
            continue
        if args[key] is not None:
            copy[key] = args[key]
    return copy


""" Finds first dict in list of dicts containing field id with value equal to id"""
T = TypeVar("T")


def find_by_id(id: str, item_list: List[Dict[str, T]]) -> Dict[str, T]:
    from ..utils import logger

    def filter_fn(item):
        logger.error(item)
        return item["id"] == id

    return next(filter(filter_fn, item_list))
