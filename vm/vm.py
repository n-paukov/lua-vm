from typing import List

from vm.exceptions.common import VirtualMachineInvalidInstructionError
from vm.opcodes.opcodes import OPCode, OPCodeType
from vm.runtime.context import ExecutionContext


class VirtualMachine:
    def __init__(self, opcodes: List[OPCode]):
        self._context = ExecutionContext(opcodes)
        self._instructions_handlers = {
            OPCodeType.PUSH: self._handle_push
        }

    def run(self):
        while not self._context.end_reached:
            instruction = self._context.get_current_instruction()
            self._handle_instruction(instruction)

    def _handle_instruction(self, instruction: OPCode):
        handler = self._instructions_handlers.get(instruction.type)

        if handler is None:
            raise VirtualMachineInvalidInstructionError("Invalid instruction: {} at address {}".format(instruction,
                                                                                                       self._context.instruction_address))

        self._context.move_to_next_instruction()
        handler()

    def _handle_push(self, instruction: OPCode):
        pass