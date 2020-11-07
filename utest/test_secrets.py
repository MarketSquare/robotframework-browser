import Browser.keywords.interaction as interaction


def test_fill_or_type_secret_in_plain_text_logs_warning():
    def whole_lib():
        pass
    whole_lib.current_arguments = False

    class MyLogger:
        def __init__(self):
            self.message = None

        def warn(self, message):
            self.message = message

    interaction.logger = MyLogger()
    interaction.get_variable_value = lambda *args: 'value'

    browser = interaction.Interaction(whole_lib)
    browser._fill_text = lambda selector, secret, log_response=False: 0
    browser._type_text = lambda selector, secret, delay, clear, log_response=False: 0

    browser.fill_secret("selector", "my secret in plain text")
    assert interaction.logger.message == "Direct assignment of values as 'secret' is deprecated.Use variables or " \
                                         "environment variables instead."
    interaction.logger = MyLogger()
    browser.fill_secret("selector", "$variable")
    assert interaction.logger.message is None

    interaction.logger = MyLogger()
    browser.type_secret("selector", "$variable")
    assert interaction.logger.message is None

    interaction.logger = MyLogger()
    browser.type_secret("selector", "my secret in plain text")
    assert interaction.logger.message == "Direct assignment of values as 'secret' is deprecated.Use variables or " \
                                         "environment variables instead."
