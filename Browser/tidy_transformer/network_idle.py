from robot.api.parsing import Token
from robot.parsing.model.statements import KeywordCall
from robotidy.transformers import Transformer


OLD_KW_NAME = "wait until network is idle"


class NetworkIdle(Transformer):
    def visit_KeywordCall(self, node: KeywordCall):
        keyword_token = node.get_token(Token.KEYWORD)
        if keyword_token.value.lower() == OLD_KW_NAME:
            return self._keyword_formatter(node)
        return node
    
    def _keyword_formatter(self, node: KeywordCall):
        raw_args = node.get_token(Token.ARGUMENT)
        tokens = []
        found = False
        separator = Token(node.tokens[2].type, node.tokens[2].value)
        for token in node.tokens:
            if token.value.lower() != OLD_KW_NAME and not found:
                tokens.append(Token(token.type, token.value))
                continue
            if token.value.lower() == OLD_KW_NAME:
                found = True
                tokens.append(Token(token.type, "Wait For Load State"))
                tokens.append(separator)
                continue
            if found and not raw_args:
                found = False
            elif found and raw_args and token.type == Token.ARGUMENT:
                found = False
                tokens.extend(self._argument_formatter(token, raw_args, separator))
        return KeywordCall.from_tokens(tokens)

    def _argument_formatter(self, token: KeywordCall, raw_args: Token, separator: Token):
        tokens = [(Token(token.type, "state=networkidle"))]
        if raw_args:
            tokens.append(separator)
        if raw_args and raw_args.value.startswith("timeout"):
            tokens.append(Token(token.type, token.value))
            tokens.append(separator)
        elif raw_args:
            tokens.append(Token(token.type, f"timeout={token.value}"))
            tokens.append(separator)
        return tokens
