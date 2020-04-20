from enum import Enum
from typing import List

from compiler.ast.ast_nodes.common import LiteralNode, ValueName
from compiler.ast.ast_nodes.expression import ExpressionNode


class ExpressionsTuple(ExpressionNode):
    _printable_fields = ["_expressions"]

    def __init__(self, expressions: List[ExpressionNode]):
        super().__init__()
        self._expressions = expressions


class LocalAssignmentExpression(ExpressionNode):
    _printable_fields = ["_lvalue_tuple", "_rvalue_tuple"]

    def __init__(self, lvalue_tuple: ExpressionsTuple, rvalue_tuple: ExpressionsTuple):
        super().__init__()
        self._lvalue_tuple = lvalue_tuple
        self._rvalue_tuple = rvalue_tuple


class BinaryExpressionType(Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3


class BinaryOperationExpression(ExpressionNode):
    _printable_fields = ["_left", "_expression_type", "_right"]

    def __init__(self, left: ExpressionNode, right: ExpressionNode, expression_type: BinaryExpressionType):
        super().__init__()
        self._left = left
        self._right = right
        self._expression_type = expression_type


class FunctionCallExpression(ExpressionNode):
    _printable_fields = ["_callable", "_args"]

    def __init__(self, callable_expression: ExpressionNode, args: ExpressionsTuple):
        super().__init__()
        self._callable = callable_expression
        self._args = args


class ValueExpression(ExpressionNode):
    _printable_fields = ["_value_name"]

    def __init__(self, value_name: ValueName):
        super().__init__()
        self._value_name = value_name

