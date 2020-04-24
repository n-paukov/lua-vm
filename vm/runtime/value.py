from typing import Callable

from vm.exceptions.common import VirtualMachineRuntimeError, VirtualMachineInvalidOperationError


class Value:
    def __init__(self):
        pass

    def __mul__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '*' operation: {} and {}".format(self, other))

    def __add__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '+' operation: {} and {}".format(self, other))

    def __sub__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '+' operation: {} and {}".format(self, other))

    def __truediv__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '/' operation: {} and {}".format(self, other))

    def call(self, *args):
        raise VirtualMachineInvalidOperationError("Impossible to call value: {}".format(self))

    def concat(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '..' operation: {} and {}".format(self, other))


class StringValue(Value):
    def __init__(self, value: str):
        super().__init__()

        self.value = value

    def __str__(self):
        return "StringValue(\"{}\")".format(self.value)


class NilValue(Value):
    def __init__(self, ):
        super().__init__()

    def __str__(self):
        return "NilValue()"


class NumberValue(Value):
    def __init__(self, value: float):
        super().__init__()

        self.value = value

    def __add__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value + other.value)
        else:
            raise VirtualMachineRuntimeError("Invalid operands for '+' operation: {} and {}".format(self, other))

    def __mul__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value * other.value)
        else:
            raise VirtualMachineRuntimeError("Invalid operands for '*' operation: {} and {}".format(self, other))

    def __sub__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value - other.value)
        else:
            raise VirtualMachineRuntimeError("Invalid operands for '-' operation: {} and {}".format(self, other))

    def __truediv__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value / other.value)
        else:
            raise VirtualMachineRuntimeError("Invalid operands for '/' operation: {} and {}".format(self, other))

    def __str__(self):
        return "NumberValue({})".format(self.value)


class IdentifierValue(Value):
    def __init__(self, value: str):
        super().__init__()

        self.value = value

    def __str__(self):
        return "IdentifierValue(\"{}\")".format(self.value)


class BuiltinFunctionValue(Value):
    def __init__(self, name: str, function: Callable):
        super().__init__()
        self._name = name
        self._function = function

    @property
    def name(self) -> str:
        return self._name

    @property
    def function(self) -> Callable:
        return self._function

    def call(self, *args):
        return self._function(*args)

    def __str__(self):
        return "BuiltinFunctionValue({})".format(self._function)


class CustomFunctionValue(Value):
    def __init__(self, name: str, instruction_address: int, declaration_scope):
        super().__init__()
        self._name = name
        self._instruction_address = instruction_address
        self._declaration_scope = declaration_scope

    @property
    def instruction_address(self):
        return self._instruction_address

    @property
    def name(self):
        return self._name

    @property
    def declaration_scope(self):
        return self._declaration_scope

    def __str__(self):
        return "CustomFunctionValue(name=\"{}\", instruction_address={})".format(self._name, self._instruction_address)
