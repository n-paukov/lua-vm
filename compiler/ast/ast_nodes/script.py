from typing import List

from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.ast_nodes.statement import StatementNode
from compiler.opcodes.context import OPCodesCompilationContext


class StatementsBlock(ASTNode):
    _printable_fields = ["_statements"]

    def __init__(self, statements: List[StatementNode]):
        super().__init__()
        self._statements = statements

    @property
    def statements(self) -> List[StatementNode]:
        return self._statements

    def generate_opcodes(self, context: OPCodesCompilationContext):
        for statement in self._statements:
            statement.generate_opcodes(context)


class Script(ASTNode):
    _printable_fields = ["_statements_block"]

    def __init__(self, statements_block: StatementsBlock):
        super().__init__()
        self._statements_block = statements_block

    def generate_opcodes(self, context: OPCodesCompilationContext):
        self._statements_block.generate_opcodes(context)
