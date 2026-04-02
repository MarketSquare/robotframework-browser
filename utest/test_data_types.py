from typing import TypedDict, Union

import pytest

from Browser.utils.data_types import convert_typed_dict
from Browser.utils.types import Secret


class _RequiredPayload(TypedDict):
    name: str


class Payload(_RequiredPayload, total=False):
    count: int


class Credential(TypedDict):
    username: str | Secret
    password: str | Secret


class CredentialIntTuple(TypedDict):
    username: int | float
    password: int | float


class CredentialOptional(Credential, total=False):
    domain: str | Secret


class TypedDict1(TypedDict):
    name: str
    value: int


class TypedDict2(TypedDict):
    name: str
    data: TypedDict1


class TypedDict3(TypedDict):
    name: str
    data: TypedDict1 | None


def test_convert_typed_dict_converts_required_and_optional_keys_case_insensitively():
    annotations = {"payload": Payload}
    params = {"payload": {"NAME": "robot", "CoUnT": "3"}}

    converted = convert_typed_dict(annotations, params)

    assert converted["payload"] == {"name": "robot", "count": 3}


def test_convert_typed_dict_converts_union_typed_dict_argument():
    annotations = {"payload": Union[Payload, None]}
    params = {"payload": {"NAME": "robot"}}

    converted = convert_typed_dict(annotations, params)

    assert converted["payload"] == {"name": "robot"}


def test_convert_typed_dict_raises_when_required_key_is_missing():
    annotations = {"payload": Payload}
    params = {"payload": {"count": 2}}

    with pytest.raises(RuntimeError, match="required key 'name'"):
        convert_typed_dict(annotations, params)


def test_convert_typed_dict_raises_for_non_dict_value():
    annotations = {"payload": Payload}
    params = {"payload": "not-a-dict"}

    with pytest.raises(TypeError, match="expects a dictionary like object"):
        convert_typed_dict(annotations, params)


def test_convert_typed_dict_with_secret():
    annotations = {"credential": Credential}
    params = {"credential": {"username": "user", "password": "pass"}}
    converted = convert_typed_dict(annotations, params)
    assert converted["credential"]["username"] == "user"
    assert converted["credential"]["password"] == "pass"

    params = {"credential": {"username": 1, "password": 2}}
    converted = convert_typed_dict(annotations, params)
    assert converted["credential"]["username"] == "1"
    assert converted["credential"]["password"] == "2"

    annotations = {"credential": CredentialIntTuple}
    params = {"credential": {"username": "joulu", "password": "pukki"}}
    with pytest.raises(TypeError):
        convert_typed_dict(annotations, params)


@pytest.mark.skipif(
    hasattr(Secret, "robot_framework_browser_secret"),
    reason="This test is only relevant for Robot Framework older than 7.4.0.",
)
def test_convert_typed_dict_with_secret_legacy_secret_object():
    annotations = {"credential": Credential}
    secret = Secret("Joulupukki")
    params = {"credential": {"username": secret, "password": secret}}
    converted = convert_typed_dict(annotations, params)
    assert converted["credential"]["username"] == secret
    assert converted["credential"]["password"] == secret


def test_convert_typed_dict_with_secret_and_optional_key():
    annotations = {"credential": CredentialOptional}
    params = {
        "credential": {"username": "user", "password": "pass", "domain": "example.com"}
    }
    converted = convert_typed_dict(annotations, params)
    assert converted["credential"]["username"] == "user"
    assert converted["credential"]["password"] == "pass"
    assert converted["credential"]["domain"] == "example.com"


@pytest.mark.skipif(
    hasattr(Secret, "robot_framework_browser_secret"),
    reason="This test is only relevant for Robot Framework older than 7.4.0.",
)
def test_convert_typed_dict_with_secret_and_optional_key_legacy_secret_object():
    annotations = {"credential": CredentialOptional}
    secret = Secret("Joulupukki")
    params = {
        "credential": {"username": secret, "password": secret, "domain": "example.com"}
    }
    converted = convert_typed_dict(annotations, params)
    assert converted["credential"]["username"] == secret
    assert converted["credential"]["password"] == secret
    assert converted["credential"]["domain"] == "example.com"


def test_typed_dict():
    annotations = {"data": TypedDict2}
    params = {"data": {"name": "test", "data": {"name": "test", "value": "42"}}}
    converted = convert_typed_dict(annotations, params)
    assert converted["data"] == {"name": "test", "data": {"name": "test", "value": 42}}


def test_typed_dict_raises_for_non_dict_nested_value():
    annotations = {"data": TypedDict2}
    params = {"data": {"name": "test", "data": "not-a-dict"}}
    with pytest.raises(TypeError, match="Expected dictionary like object"):
        convert_typed_dict(annotations, params)


def test_typed_dict_union_nested_dict_value_is_converted():
    annotations = {"data": TypedDict3}
    params = {"data": {"name": "test", "data": {"name": "inner", "value": "42"}}}
    converted = convert_typed_dict(annotations, params)
    assert converted["data"] == {"name": "test", "data": {"name": "inner", "value": 42}}
