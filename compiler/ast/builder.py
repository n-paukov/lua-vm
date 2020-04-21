from antlr_ast.ast import (
    process_tree,
    BaseNodeTransformer,
)

from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse import parse_script
from compiler.ast.transformer_context import NodesTransformerContext


class Transformer(BaseNodeTransformer):
    pass


class ASTBuilder:
    def __init__(self, text: str):
        self._text = text
        self._parse_tree = parse_script(text)
        self._ast = self._create_ast_tree()

    def get_tree(self) -> ASTNode:
        return self._ast

    def _create_ast_tree(self):
        Transformer.bind_alias_nodes(NodesTransformerContext.get_available_nodes())
        return process_tree(self._parse_tree, transformer_cls=Transformer).get_ast_node()
