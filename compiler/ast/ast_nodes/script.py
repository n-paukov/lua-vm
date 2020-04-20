from typing import List

from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.ast_nodes.statement import StatementNode


class StatementsBlock(ASTNode):
    _printable_fields = ["_statements"]

    def __init__(self, statements: List[StatementNode]):
        super().__init__()
        self._statements = statements


class Script(ASTNode):
    _printable_fields = ["_statements_block"]

    def __init__(self, statements_block: StatementsBlock):
        super().__init__()
        self._statements_block = statements_block
