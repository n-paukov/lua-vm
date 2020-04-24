from typing import List

from vm.exceptions.common import VirtualMachineScopeOrderError, VirtualMachineInvalidOperationError
from vm.opcodes.opcodes import OPCode
from vm.runtime.scope import Scope
from vm.runtime.value import Value, CustomFunctionValue


class CallContext:
    def __init__(self, scope: Scope, return_address: int, override_local_scope: bool = False):
        self._return_address = return_address
        self._scopes: List[Scope] = [scope] if override_local_scope else [Scope(scope)]

    @property
    def current_scope(self):
        return self._scopes[-1]

    @property
    def return_address(self):
        return self._return_address

    def create_scope(self):
        self._scopes.append(Scope(self.current_scope))

    def destroy_scope(self):
        if len(self._scopes) <= 1:
            raise VirtualMachineScopeOrderError("Failed to destroy the last scope")


class ExecutionContext:
    def __init__(self, code: List[OPCode]):
        self._global_scope = Scope(None)
        self._code: List[OPCode] = code
        self._call_stack: List[CallContext] = [CallContext(self._global_scope, -1, override_local_scope=True)]
        self._values_stack: List[Value] = []
        self._instruction_address: int = 0
        self._logical_test_result: bool = False

    @property
    def end_reached(self) -> bool:
        return self._instruction_address == len(self._code)

    @property
    def instruction_address(self) -> int:
        return self._instruction_address

    @property
    def current_call_context(self) -> CallContext:
        return self._call_stack[-1]

    @property
    def current_scope(self) -> Scope:
        return self.current_call_context.current_scope

    @property
    def global_scope(self) -> Scope:
        return self._global_scope

    @property
    def current_instruction(self) -> OPCode:
        return self._code[self._instruction_address]

    def create_scope(self):
        self.current_call_context.create_scope()

    def destroy_scope(self):
        self.current_call_context.destroy_scope()

    def move_to_next_instruction(self):
        self._instruction_address += 1

    def perform_jump(self, address: int):
        raise NotImplementedError

    def push_value(self, value: Value):
        self._values_stack.append(value)

    def peek_value(self) -> Value:
        return self._values_stack[-1]

    def pop_value(self) -> Value:
        return self._values_stack.pop()

    def skip_instruction(self):
        if self.end_reached:
            raise VirtualMachineInvalidOperationError("Impossible to skip instruction: end of program is reached")

        self._instruction_address += 1

    def enter_to_call_context(self, function: CustomFunctionValue):
        self._call_stack.append(CallContext(self.current_scope, self._instruction_address))
        self._instruction_address = function.instruction_address

    def return_from_call_context(self):
        destroyed_context = self._call_stack.pop()
        self._instruction_address = destroyed_context.return_address
