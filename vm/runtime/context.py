from typing import List

from vm.opcodes.opcodes import OPCode
from vm.runtime.scope import Scope
from vm.runtime.value import Value


class CallContext:
    def __init__(self, scope: Scope, return_address: int):
        self._scope = scope
        self._return_address = return_address

    @property
    def scope(self):
        return self._scope

    @property
    def return_address(self):
        return self._return_address


class ExecutionContext:
    def __init__(self, code: List[OPCode]):
        self._code: List[OPCode] = code
        self._call_stack: List[CallContext] = []
        self._values_stack: List[Value] = []
        self._instruction_address: int = 0
        self._logical_test_result: bool = False

    @property
    def end_reached(self) -> bool:
        return self._instruction_address == len(self._code)

    @property
    def instruction_address(self) -> int:
        return self._instruction_address

    def get_current_instruction(self) -> OPCode:
        return self._code[self._instruction_address]

    def move_to_next_instruction(self):
        self._instruction_address += 1

    def perform_jump(self, address: int):
        self._instruction_address += 1

    def push_value(self, value: Value):
        self._values_stack.append(value)

    def peek_value(self) -> Value:
        return self._values_stack[-1]

    def pop_value(self) -> Value:
        return self._values_stack.pop()
