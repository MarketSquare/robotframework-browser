# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from enum import Enum
from typing import Dict, List, TypeVar


def locals_to_params(args: Dict) -> Dict:
    copy = dict()
    for key in args:
        if key == "self":
            continue
        if args[key] is not None:
            value = args[key]
            if isinstance(value, Enum):
                copy[key] = value.name
            else:
                copy[key] = value
    return copy


""" Finds first dict in list of dicts containing field id with value equal to id"""
T = TypeVar("T")


def find_by_id(_id: str, item_list: List[Dict[str, T]], log_error=True) -> Dict[str, T]:
    from ..utils import logger

    def filter_fn(item):
        return item["id"] == _id

    try:
        filtered = filter(filter_fn, item_list)
        return next(filtered)
    except StopIteration:
        if log_error:
            logger.error(
                f"No item with correct id {_id}. Existing ids: {[item['id'] for item in item_list]}"
            )
        raise
