from typing import List, Callable

from vm.exceptions.common import VirtualMachineInvalidInstructionError, VirtualMachineRuntimeError, \
    VirtualMachineScopeOrderError
from vm.opcodes.opcodes import OPCode, OPCodeType
from vm.runtime.context import ExecutionContext
from vm.runtime.standard_library import GeneralFunctions
from vm.runtime.utils import is_float_literal
from vm.runtime.value import NumberValue, StringValue, IdentifierValue, Value, BuiltinFunctionValue, NilValue, \
    CustomFunctionValue, BooleanValue


def binary_operation_handler(func):
    def wrap_db_exceptions_internal(self, instruction: OPCode):
        right = self._pop_operand_value()
        left = self._pop_operand_value()

        value = func(self, left, right)

        self._context.push_value(value)

    return wrap_db_exceptions_internal


class VirtualMachine:
    def __init__(self, opcodes: List[OPCode]):
        self._context = ExecutionContext(opcodes)
        self._instructions_handlers = {
            OPCodeType.PUSH: self._handle_push,
            OPCodeType.MULTIPLY: self._handle_multiply,
            OPCodeType.SUM: self._handle_sum,
            OPCodeType.SUBTRACT: self._handle_subtract,
            OPCodeType.DIVIDE: self._handle_divide,
            OPCodeType.ASSIGN: self._handle_assign,
            OPCodeType.FUNCTION: self._handle_function,
            OPCodeType.CALL: self._handle_call,
            OPCodeType.RETURN: self._handle_return,
            OPCodeType.BEGIN_SCOPE: self._handle_begin_scope,
            OPCodeType.END_SCOPE: self._handle_end_scope,
            OPCodeType.BOOLEAN_AND: self._handle_boolean_and,
            OPCodeType.BOOLEAN_OR: self._handle_boolean_or,
            OPCodeType.BOOLEAN_NOT: self._handle_boolean_not,
            OPCodeType.MINUS: self._handle_minus,
            OPCodeType.CMP_GT: self._handle_cmp_gt,
            OPCodeType.CMP_EQ: self._handle_cmp_eq,
            OPCodeType.CMP_GE: self._handle_cmp_ge,
            OPCodeType.CMP_LE: self._handle_cmp_le,
            OPCodeType.CMP_LT: self._handle_cmp_lt,
            OPCodeType.CMP_NE: self._handle_cmp_ne,
        }

    def register_builtin_function(self, name: str, function: Callable):
        if self._context.global_scope.has_value(name):
            raise VirtualMachineRuntimeError("Failed to register builtin function {}: it already exists".format(name))

        self._context.global_scope.set_value(name, BuiltinFunctionValue(name, function))

    def load_standard_library(self):
        self.register_builtin_function("print", GeneralFunctions.print)

    def run(self):
        while not self._context.end_reached:
            instruction = self._context.current_instruction
            self._handle_instruction(instruction)

    def _handle_instruction(self, instruction: OPCode):
        handler: Callable = self._instructions_handlers.get(instruction.type)

        if handler is None:
            raise VirtualMachineInvalidInstructionError(
                "Invalid instruction: {} at address {}".format(instruction, self._context.instruction_address))

        self._context.move_to_next_instruction()
        handler(instruction)

    def _handle_push(self, instruction: OPCode):
        value: str = instruction.first_arg

        if value.startswith('"'):
            self._context.push_value(StringValue(str(value[1:-1])))
        elif is_float_literal(value):
            self._context.push_value(NumberValue(float(value)))
        elif value == "nil":
            self._context.push_value(NilValue())
        elif value == "true" or value == "false":
            self._context.push_value(BooleanValue(value == "true"))
        else:
            pushed_value = self._context.current_scope.get_value(value)

            if pushed_value is None:
                pushed_value = NilValue()

            self._context.push_value(pushed_value)

    @binary_operation_handler
    def _handle_multiply(self, left: Value, right: Value):
        return left * right

    @binary_operation_handler
    def _handle_sum(self, left: Value, right: Value):
        return left + right

    @binary_operation_handler
    def _handle_subtract(self, left: Value, right: Value):
        return left - right

    @binary_operation_handler
    def _handle_divide(self, left: Value, right: Value):
        return left / right

    @binary_operation_handler
    def _handle_boolean_and(self, left: Value, right: Value):
        return left.boolean_and(right)

    @binary_operation_handler
    def _handle_boolean_or(self, left: Value, right: Value):
        return left.boolean_or(right)

    @binary_operation_handler
    def _handle_cmp_gt(self, left: Value, right: Value):
        return left.__gt__(right)

    @binary_operation_handler
    def _handle_cmp_eq(self, left: Value, right: Value):
        return left.__eq__(right)

    @binary_operation_handler
    def _handle_cmp_ge(self, left: Value, right: Value):
        return left.__ge__(right)

    @binary_operation_handler
    def _handle_cmp_le(self, left: Value, right: Value):
        return left.__le__(right)

    @binary_operation_handler
    def _handle_cmp_lt(self, left: Value, right: Value):
        return left.__lt__(right)

    @binary_operation_handler
    def _handle_cmp_ne(self, left: Value, right: Value):
        return left.__ne__(right)

    def _handle_boolean_not(self, instruction: OPCode):
        right = self._pop_operand_value()

        self._context.push_value(right.boolean_not())

    def _handle_minus(self, instruction: OPCode):
        right = self._pop_operand_value()

        self._context.push_value(-right)

    def _handle_assign(self, instruction: OPCode):
        value = self._pop_operand_value()
        value_identifier = instruction.first_arg

        self._context.current_scope.set_value(value_identifier, value)

    def _handle_call(self, instruction: OPCode):
        callable_value = self._context.pop_value()

        if isinstance(callable_value, BuiltinFunctionValue):
            args_count = instruction.first_arg
            args = []

            for i in range(args_count):
                arg = self._pop_operand_value()
                args.append(arg)

            args = reversed(args)

            call_result = callable_value.call(*args)
            assert isinstance(call_result, Value)

            self._context.push_value(call_result)
        elif isinstance(callable_value, CustomFunctionValue):
            self._context.enter_to_call_context(callable_value)
        else:
            raise VirtualMachineInvalidInstructionError(
                "Impossible to call value '{}': it is not callable".format(callable_value))

    def _handle_return(self, instruction: OPCode):
        self._context.return_from_call_context()

    def _handle_function(self, instruction: OPCode):
        self._context.create_scope()

        function_name = instruction.first_arg
        function_value = CustomFunctionValue(function_name, self._context.instruction_address,
                                             self._context.current_scope)

        self._context.current_scope.set_value(function_name, function_value)
        # skip instructions until function end

        if self._context.current_instruction.type != OPCodeType.BEGIN_SCOPE:
            raise VirtualMachineInvalidInstructionError("'begin_scope' opcode must follow after function definition")

        scopes_stack = [self._context.current_instruction.type]

        while len(scopes_stack) > 0:
            self._context.skip_instruction()

            current_instruction = self._context.current_instruction

            if current_instruction.type == OPCodeType.BEGIN_SCOPE:
                scopes_stack.append(current_instruction.type)
            elif current_instruction.type == OPCodeType.END_SCOPE:
                ended_scope = scopes_stack.pop()

                if ended_scope != OPCodeType.BEGIN_SCOPE:
                    raise VirtualMachineScopeOrderError(
                        "Corresponding 'begin_scope' opcode is expected for `end_scope` "
                        "but other 'end_scope' is reached")
            else:
                pass

        # skip function 'end_scope' opcode
        if not self._context.end_reached:
            self._context.skip_instruction()

    def _handle_begin_scope(self, instruction: OPCode):
        self._context.create_scope()

    def _handle_end_scope(self, instruction: OPCode):
        self._context.destroy_scope()

    def _pop_operand_value(self) -> Value:
        value = self._context.pop_value()

        if isinstance(value, IdentifierValue):
            value = self._context.current_scope.get_value(value.value)

            if value is None:
                value = NilValue()

        return value
