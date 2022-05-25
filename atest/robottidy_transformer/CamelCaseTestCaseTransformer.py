from robot.api.parsing import ModelTransformer, Token


class CamelCaseTestCaseTransformer(ModelTransformer):
    def visit_TestCaseName(self, node):  # noqa
        token = node.get_token(Token.TESTCASE_NAME)
        if token.value:
            token_value = ""
            for word in token.value.split(" "):
                token_value = f"{token_value} {word[0].upper()}{word[1:]}"
            token.value = token_value.strip()
        return node
