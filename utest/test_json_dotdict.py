import copy
import json

from robot.libraries.Collections import Collections
from robot.utils import DotDict

from Browser.utils import JsonDotDict


def test_json_dumps_writes_bytes_as_base64():
    data = JsonDotDict(raw=b"\x89PNG", name="logo")
    assert json.loads(json.dumps(data)) == {"raw": "iVBORw==", "name": "logo"}


def test_json_dumps_with_indent_writes_bytes_as_base64():
    data = JsonDotDict(raw=b"ab")
    assert json.loads(json.dumps(data, indent=4)) == {"raw": "YWI="}


def test_nested_json_dotdict_is_serialized_too():
    data = JsonDotDict(request=JsonDotDict(postDataBuffer=b"ab"))
    assert json.loads(json.dumps(data)) == {"request": {"postDataBuffer": "YWI="}}


def test_key_and_attribute_access_return_real_bytes():
    data = JsonDotDict(raw=b"\x89")
    assert data["raw"] == b"\x89"
    assert data.raw == b"\x89"


def test_copies_keep_real_bytes():
    data = JsonDotDict(raw=b"\x89")
    assert copy.copy(data)["raw"] == b"\x89"
    assert copy.deepcopy(data)["raw"] == b"\x89"
    assert Collections().copy_dictionary(data)["raw"] == b"\x89"
    assert type(copy.copy(data)) is JsonDotDict


def test_converting_to_dotdict_writes_bytes_as_base64():
    assert DotDict(JsonDotDict(raw=b"ab"))["raw"] == "YWI="
