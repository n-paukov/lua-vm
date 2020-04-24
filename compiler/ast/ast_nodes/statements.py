from typing import List

from compiler.ast.ast_nodes.common import ValueName, FunctionParameter, LiteralType
from compiler.ast.ast_nodes.expression import ExpressionNode
from compiler.ast.ast_nodes.expressions import ExpressionsTuple, ValueExpression
from compiler.ast.ast_nodes.script import StatementsBlock
from compiler.ast.ast_nodes.statement import StatementNode
from compiler.exceptions.common import OPCodesCompilationError
from compiler.opcodes.context import OPCodesCompilationContext
from vm.opcodes.opcodes import OPCode, OPCodeType


class AssignmentStatement(StatementNode):
    _printable_fields = ["_lvalue_tuple", "_rvalue_tuple"]

    def __init__(self, lvalue_tuple: ExpressionsTuple, rvalue_tuple: ExpressionsTuple):
        super().__init__()
        self._lvalue_tuple = lvalue_tuple
        self._rvalue_tuple = rvalue_tuple

    def generate_opcodes(self, context: OPCodesCompilationContext):
        for expression in self._rvalue_tuple.expressions:
            expression.generate_opcodes(context)

        for expression in reversed(self._lvalue_tuple.expressions):
            if not isinstance(expression, ValueExpression):
                raise OPCodesCompilationError("Left value tuple should contain only assignable value expressions")

            value_name = expression.value_name
            assert not value_name.is_class_value

            if value_name.name.type != LiteralType.IDENTIFIER:
                raise OPCodesCompilationError("Left value tuple subexpressions should be identifiers")

            context.add_opcode(OPCode(OPCodeType.ASSIGN, [value_name.name.value_representation]))


class FunctionDeclarationStatement(StatementNode):
    _printable_fields = ["_name", "_parameters", "_statements_block"]

    def __init__(self, name: ValueName, parameters: List[ValueName], statements: StatementsBlock):
        super().__init__()
        self._name = name
        self._parameters = parameters
        self._statements_block = statements

    def generate_opcodes(self, context: OPCodesCompilationContext):
        context.add_opcode(OPCode(OPCodeType.FUNCTION, [self._name.full_name]))
        context.add_opcode(OPCode(OPCodeType.BEGIN_SCOPE))

        for parameter_name in reversed(self._parameters):
            context.add_opcode(OPCode(OPCodeType.ASSIGN, [parameter_name.full_name]))

        self._statements_block.generate_opcodes(context)

        return_statement_found = False

        for statement in self._statements_block.statements:
            if isinstance(statement, ReturnStatement):
                return_statement_found = True
                break

        if not return_statement_found:
            context.add_opcode(OPCode(OPCodeType.PUSH, ["nil"]))
            context.add_opcode(OPCode(OPCodeType.RETURN, [1]))

        context.add_opcode(OPCode(OPCodeType.END_SCOPE))


class ReturnStatement(StatementNode):
    _printable_fields = ["_rvalue_tuple"]

    def __init__(self, rvalue_tuple: ExpressionsTuple):
        super().__init__()
        self._rvalue_tuple = rvalue_tuple

    def generate_opcodes(self, context: OPCodesCompilationContext):
        for expression in self._rvalue_tuple.expressions:
            expression.generate_opcodes(context)

        context.add_opcode(OPCode(OPCodeType.RETURN, [len(self._rvalue_tuple.expressions)]))


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
