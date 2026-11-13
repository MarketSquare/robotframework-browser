from pathlib import Path
from unittest.mock import MagicMock

import pytest

from Browser.keywords.evaluation import Evaluation


def make_evaluation() -> tuple[Evaluation, MagicMock]:
    library = MagicMock()
    library.strict_mode = True
    stub = MagicMock()
    library.playwright.grpc_channel.return_value.__enter__.return_value = stub
    evaluation = Evaluation.__new__(Evaluation)
    evaluation.library = library
    return evaluation, stub


TAG_KEYWORDS = [
    pytest.param("add_style_tag", "AddStyleTag", id="style"),
    pytest.param("add_script_tag", "AddScriptTag", id="script"),
]


@pytest.mark.parametrize(("keyword", "rpc"), TAG_KEYWORDS)
@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({}, id="none"),
        pytest.param({"content": "a", "url": "http://x/a"}, id="content-url"),
        pytest.param({"content": "a", "path": "a"}, id="content-path"),
        pytest.param({"url": "http://x/a", "path": "a"}, id="url-path"),
        pytest.param({"content": ""}, id="empty-content"),
        pytest.param({"url": ""}, id="empty-url"),
        pytest.param({"path": ""}, id="empty-path"),
        pytest.param({"path": Path(".")}, id="dot-path"),
    ],
)
def test_exactly_one_tag_source_is_required(keyword, rpc, kwargs):
    evaluation, stub = make_evaluation()
    with pytest.raises(ValueError, match="Give exactly one of content, url and path."):
        getattr(evaluation, keyword)(**kwargs)
    getattr(stub, rpc).assert_not_called()


@pytest.mark.parametrize(("keyword", "rpc"), TAG_KEYWORDS)
def test_empty_content_with_url_sends_the_url(keyword, rpc):
    evaluation, stub = make_evaluation()
    getattr(evaluation, keyword)(content="", url="http://x/a")
    request = getattr(stub, rpc).call_args.args[0]
    assert request.url == "http://x/a"
    assert not request.HasField("content")


@pytest.mark.parametrize(("keyword", "rpc"), TAG_KEYWORDS)
def test_whitespace_content_is_sent_as_it_is(keyword, rpc):
    evaluation, stub = make_evaluation()
    getattr(evaluation, keyword)(content="  ")
    assert getattr(stub, rpc).call_args.args[0].content == "  "


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({}, id="none"),
        pytest.param({"script": "a", "path": "a"}, id="script-path"),
        pytest.param({"script": ""}, id="empty-script"),
        pytest.param({"path": ""}, id="empty-path"),
        pytest.param({"path": Path(".")}, id="dot-path"),
    ],
)
def test_exactly_one_init_script_source_is_required(kwargs):
    evaluation, stub = make_evaluation()
    with pytest.raises(ValueError, match="Give exactly one of script and path."):
        evaluation.add_init_script(**kwargs)
    stub.AddContextInitScript.assert_not_called()


@pytest.mark.parametrize(
    ("keyword", "rpc"),
    [
        pytest.param("add_script_tag", "AddScriptTag", id="script-tag"),
        pytest.param("add_init_script", "AddContextInitScript", id="init-script"),
    ],
)
def test_javascript_path_is_named_in_page_errors(keyword, rpc, tmp_path):
    script = tmp_path / "helpers.js"
    script.write_text("window.a = 1;", encoding="utf-8")
    evaluation, stub = make_evaluation()
    getattr(evaluation, keyword)(path=script)
    request = getattr(stub, rpc).call_args.args[0]
    assert request.content == f"window.a = 1;\n//# sourceURL={script.as_posix()}"


def test_path_is_read_and_sent_as_content(tmp_path):
    css = tmp_path / "no-animations.css"
    css.write_text("* { animation: none !important; } /* ä */", encoding="utf-8")
    evaluation, stub = make_evaluation()
    evaluation.add_style_tag(path=css)
    request = stub.AddStyleTag.call_args.args[0]
    assert request.content == "* { animation: none !important; } /* ä */"
    assert not request.HasField("url")
