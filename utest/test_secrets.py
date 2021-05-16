from unittest.mock import MagicMock

import Browser.keywords.interaction as interaction

WARN_MESSAGE = (
    "WARNING  RobotFramework:logger.py:95 Direct assignment of values as 'secret' is "
    "deprecated. Use variables or environment variables instead.\n"
)


def test_fill_secret_in_plain_text(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts.fill_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_in_plain_text(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts.type_secret("selector", "password")
    assert caplog.text == WARN_MESSAGE


def test_type_secret_with_prefix(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts._replace_placeholder_variables = MagicMock(return_value="123")
    secrerts.type_secret("selector", "$password")
    assert caplog.text == ""
    secrerts.type_secret("selector", "%password")
    assert caplog.text == ""


def test_fill_secret_with_prefix(caplog):
    secrerts = interaction.Interaction(MagicMock())
    secrerts._replace_placeholder_variables = MagicMock(return_value="123")
    secrerts.fill_secret("selector", "$password")
    assert caplog.text == ""
    secrerts.fill_secret("selector", "%password")
    assert caplog.text == ""
