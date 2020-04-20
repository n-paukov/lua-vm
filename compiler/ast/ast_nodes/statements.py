from typing import List

from compiler.ast.ast_nodes.common import ValueName, FunctionParameter
from compiler.ast.ast_nodes.expression import ExpressionNode
from compiler.ast.ast_nodes.expressions import ExpressionsTuple
from compiler.ast.ast_nodes.script import StatementsBlock
from compiler.ast.ast_nodes.statement import StatementNode


class AssignmentStatement(StatementNode):
    _printable_fields = ["_lvalue_tuple", "_rvalue_tuple"]

    def __init__(self, lvalue_tuple: ExpressionsTuple, rvalue_tuple: ExpressionsTuple):
        super().__init__()
        self._lvalue_tuple = lvalue_tuple
        self._rvalue_tuple = rvalue_tuple


class FunctionDeclarationStatement(StatementNode):
    def __init__(self, name: ValueName, parameters: List[FunctionParameter], statements: StatementsBlock):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._statements = statements


class ReturnStatement(StatementNode):
    def __init__(self, rvalue_tuple: ExpressionsTuple):
        super().__init__()
        self._rvalue_tuple = rvalue_tuple


class BreakStatement(StatementNode):
    def __init__(self):
        super().__init__()


class ConditionalBranchStatement(StatementNode):
    def __init__(self, condition: ExpressionNode, then_statements: StatementsBlock):
        super().__init__()
        self._condition = condition
        self._then_statements = then_statements


class ConditionalStatement(StatementNode):
    def __init__(self, branches: List[ConditionalBranchStatement], else_statements: StatementsBlock):
        super().__init__()
        self._branches = branches
        self._else_statements = else_statements
