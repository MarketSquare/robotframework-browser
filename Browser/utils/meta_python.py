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
from typing import Any, TypeVar


def locals_to_params(args: dict) -> dict:
    copy: dict[str, Any] = {}
    for key, value in args.items():
        if key == "self":
            continue
        if value is not None:
            if isinstance(value, Enum):
                copy[key] = value.name
            elif isinstance(value, list):
                copy[key] = [
                    item.name if isinstance(item, Enum) else item for item in value
                ]
            else:
                copy[key] = value
    return copy


""" Finds first dict in list of dicts containing field id with value equal to id"""
T = TypeVar("T")


def find_by_id(_id: str, item_list: list[dict[str, T]], log_error=True) -> dict[str, T]:
    from ..utils import logger  # noqa: PLC0415

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
