from typing import List, Callable

from vm.exceptions.common import VirtualMachineInvalidInstructionError
from vm.opcodes.opcodes import OPCode, OPCodeType
from vm.runtime.context import ExecutionContext
from vm.runtime.utils import is_float_literal
from vm.runtime.value import NumberValue, StringValue, IdentifierValue


class VirtualMachine:
    def __init__(self, opcodes: List[OPCode]):
        self._context = ExecutionContext(opcodes)
        self._instructions_handlers = {
            OPCodeType.PUSH: self._handle_push,
            OPCodeType.MULTIPLY: self._handle_multiply,
            OPCodeType.SUM: self._handle_sum,
            OPCodeType.ASSIGN: self._handle_assign
        }

    def run(self):
        while not self._context.end_reached:
            instruction = self._context.get_current_instruction()
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
            self._context.push_value(StringValue(str(value)))
        elif is_float_literal(value):
            self._context.push_value(NumberValue(float(value)))
        elif value == "nil":
            raise NotImplementedError
        elif value == "true" or value == "false":
            raise NotImplementedError
        else:
            self._context.push_value(IdentifierValue(str(value)))

    def _handle_multiply(self, instruction: OPCode):
        right = self._context.pop_value()
        left = self._context.pop_value()

        self._context.push_value(left * right)

    def _handle_sum(self, instruction: OPCode):
        right = self._context.pop_value()
        left = self._context.pop_value()

        self._context.push_value(left + right)

    def _handle_assign(self, instruction: OPCode):
        value = self._context.pop_value()
        value_identifier = instruction.first_arg

        self._context.current_scope.set_value(value_identifier, value)
