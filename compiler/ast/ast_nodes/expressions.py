from enum import Enum
from typing import List

from compiler.ast.ast_nodes.common import LiteralNode, ValueName
from compiler.ast.ast_nodes.expression import ExpressionNode
from compiler.opcodes.context import OPCodesCompilationContext
from vm.opcodes.opcodes import OPCode, OPCodeType


class ExpressionsTuple(ExpressionNode):
    _printable_fields = ["_expressions"]

    def __init__(self, expressions: List[ExpressionNode]):
        super().__init__()
        self._expressions = expressions

    @property
    def expressions(self):
        return self._expressions

    def generate_opcodes(self, context: OPCodesCompilationContext):
        raise NotImplementedError


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

    def generate_opcodes(self, context: OPCodesCompilationContext):
        self._left.generate_opcodes(context)
        self._right.generate_opcodes(context)

        if self._expression_type == BinaryExpressionType.ADD:
            context.add_opcode(OPCode(OPCodeType.SUM))
        elif self._expression_type == BinaryExpressionType.SUBTRACT:
            context.add_opcode(OPCode(OPCodeType.SUBTRACT))
        elif self._expression_type == BinaryExpressionType.MULTIPLY:
            context.add_opcode(OPCode(OPCodeType.MULTIPLY))
        elif self._expression_type == BinaryExpressionType.DIVIDE:
            context.add_opcode(OPCode(OPCodeType.DIVIDE))
        else:
            raise NotImplementedError


class FunctionCallExpression(ExpressionNode):
    _printable_fields = ["_callable", "_args"]

    def __init__(self, callable_expression: ExpressionNode, args: ExpressionsTuple):
        super().__init__()
        self._callable = callable_expression
        self._args = args

    def generate_opcodes(self, context: OPCodesCompilationContext):
        for expression in self._args.expressions:
            expression.generate_opcodes(context)

        if isinstance(self._callable, ValueExpression):
            self._callable.generate_opcodes(context)
        elif isinstance(self._callable, ValueName):
            self._callable.generate_opcodes(context)
        else:
            raise NotImplementedError

        context.add_opcode(OPCode(OPCodeType.CALL, [len(self._args.expressions)]))


class ValueExpression(ExpressionNode):
    _printable_fields = ["_value_name"]

    def __init__(self, value_name: ValueName):
        super().__init__()
        self._value_name = value_name

    @property
    def value_name(self):
        return self._value_name

    def generate_opcodes(self, context: OPCodesCompilationContext):
        self._value_name.generate_opcodes(context)
