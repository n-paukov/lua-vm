from antlr_ast.ast import (
    parse as parse_ast,
)

from compiler.parser.luaParser import luaParser
from compiler.parser.luaLexer import luaLexer


class Grammar:
    @staticmethod
    def Lexer(arg):
        return luaLexer(arg)

    @staticmethod
    def Parser(arg):
        return luaParser(arg)


def parse_script(text, start="root"):
    return parse_ast(Grammar, text, start)
