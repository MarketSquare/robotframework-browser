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


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param({}, id="none"),
        pytest.param({"content": "a{}", "url": "http://x/a.css"}, id="content-url"),
        pytest.param({"content": "a{}", "path": "a.css"}, id="content-path"),
        pytest.param({"url": "http://x/a.css", "path": "a.css"}, id="url-path"),
    ],
)
def test_exactly_one_style_source_is_required(kwargs):
    evaluation, stub = make_evaluation()
    with pytest.raises(ValueError, match="Give exactly one of content, url and path."):
        evaluation.add_style_tag(**kwargs)
    stub.AddStyleTag.assert_not_called()


def test_path_is_read_and_sent_as_content(tmp_path):
    css = tmp_path / "no-animations.css"
    css.write_text("* { animation: none !important; } /* ä */", encoding="utf-8")
    evaluation, stub = make_evaluation()
    evaluation.add_style_tag(path=css)
    request = stub.AddStyleTag.call_args.args[0]
    assert request.content == "* { animation: none !important; } /* ä */"
    assert not request.HasField("url")
