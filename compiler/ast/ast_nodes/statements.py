from typing import List, Optional

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

    def __init__(self, lvalue_tuple: ExpressionsTuple, rvalue_tuple: ExpressionsTuple, local: bool = False):
        super().__init__()
        self._lvalue_tuple = lvalue_tuple
        self._rvalue_tuple = rvalue_tuple
        self._local = local

    def generate_opcodes(self, context: OPCodesCompilationContext):
        if self._local:
            for expression in self._lvalue_tuple.expressions:
                if not isinstance(expression, ValueExpression):
                    raise OPCodesCompilationError("Left value tuple should contain only assignable value expressions")

                value_name = expression.value_name
                assert not value_name.is_class_value

                context.add_opcode(OPCode(OPCodeType.DECLARE_LOCAL, [value_name.name.value_representation]))

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

    @property
    def condition(self) -> ExpressionNode:
        return self._condition

    @property
    def then_statements(self) -> StatementsBlock:
        return self._then_statements

    def generate_opcodes(self, context: OPCodesCompilationContext):
        return NotImplementedError


class ConditionalStatement(StatementNode):
    def __init__(self, branches: List[ConditionalBranchStatement], else_statements: Optional[StatementsBlock]):
        super().__init__()
        self._branches = branches
        self._else_statements = else_statements

    def generate_opcodes(self, context: OPCodesCompilationContext):
        branches_addresses = []
        jump_next_branch_opcodes = []
        jump_complete_opcodes = []

        for branch in self._branches:
            context.add_opcode(OPCode(OPCodeType.BEGIN_SCOPE))
            branch.condition.generate_opcodes(context)

            context.add_opcode(OPCode(OPCodeType.JUMP_NEG, [-1]))
            jump_next_branch_opcodes.append(context.current_opcode)

            branches_addresses.append(context.current_address + 1)

            branch.then_statements.generate_opcodes(context)

            context.add_opcode(OPCode(OPCodeType.JUMP, [-1]))
            jump_complete_opcodes.append(context.current_opcode)

            context.add_opcode(OPCode(OPCodeType.END_SCOPE))

        if self._else_statements is not None:
            context.add_opcode(OPCode(OPCodeType.BEGIN_SCOPE))
            branches_addresses.append(context.current_address + 1)

            self._else_statements.generate_opcodes(context)

            context.add_opcode(OPCode(OPCodeType.END_SCOPE))

        # Conditional statement end address
        branches_addresses.append(context.current_address + 1)

        for jump_opcode_index in range(len(jump_next_branch_opcodes)):
            jump_next_branch_opcodes[jump_opcode_index].args[0] = branches_addresses[jump_opcode_index + 1]

        for jump_complete_opcode in jump_complete_opcodes:
            jump_complete_opcode.args[0] = branches_addresses[-1]


class ForLoopStatement(StatementNode):
    _printable_fields = ["_counter_name", "_start_expression", "_end_expression", "_step_expression",
                         "_statements_block"]

    def __init__(self, counter_name: ValueName, start_expression: ExpressionNode, end_expression: ExpressionNode,
                 step_expression: Optional[ExpressionNode], statements_block: StatementsBlock):
        super().__init__()
        self._counter_name = counter_name
        self._start_expression = start_expression
        self._end_expression = end_expression
        self._step_expression = step_expression
        self._statements_block = statements_block

    def generate_opcodes(self, context: OPCodesCompilationContext):
        context.add_opcode(OPCode(OPCodeType.BEGIN_SCOPE))

        self._start_expression.generate_opcodes(context)
        context.add_opcode(OPCode(OPCodeType.ASSIGN, [self._counter_name.full_name]))

        loop_iteration_address = context.current_address + 1

        context.add_opcode(OPCode(OPCodeType.PUSH, [self._counter_name.full_name]))
        self._end_expression.generate_opcodes(context)

        context.add_opcode(OPCode(OPCodeType.CMP_GT))
        context.add_opcode(OPCode(OPCodeType.JUMP_POS, [-1]))

        jump_to_loop_end_opcode = context.current_opcode

        self._statements_block.generate_opcodes(context)

        if self._step_expression is not None:
            self._step_expression.generate_opcodes(context)
        else:
            context.add_opcode(OPCode(OPCodeType.PUSH, ['1']))

        context.add_opcode(OPCode(OPCodeType.PUSH, [self._counter_name.full_name]))
        context.add_opcode(OPCode(OPCodeType.SUM))
        context.add_opcode(OPCode(OPCodeType.ASSIGN, [self._counter_name.full_name]))

        context.add_opcode(OPCode(OPCodeType.JUMP, [loop_iteration_address]))

        context.add_opcode(OPCode(OPCodeType.END_SCOPE))
        jump_to_loop_end_opcode.args[0] = context.current_address
