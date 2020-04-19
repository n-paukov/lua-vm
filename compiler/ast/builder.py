from antlr_ast.ast import (
    process_tree,
    BaseNodeTransformer,
)

from compiler.ast.parse import parse_script
from compiler.ast.transformer_context import NodesTransformerContext


class Transformer(BaseNodeTransformer):
    pass


class ASTBuilder:
    def __init__(self, text: str):
        self.__text = text
        self.__parse_tree = parse_script(text)
        self.__ast = self.__create_ast_tree()

    def get_tree(self):
        return self.__ast

    def __create_ast_tree(self):
        Transformer.bind_alias_nodes(NodesTransformerContext.get_available_nodes())

        return process_tree(self.__parse_tree, transformer_cls=Transformer)
