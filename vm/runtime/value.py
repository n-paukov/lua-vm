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

    def __neg__(self):
        raise VirtualMachineInvalidOperationError("Invalid operand for unary '-' operation: {}".format(self))

    def __eq__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '==' operation: {} and {}".format(self, other))

    def __lt__(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '<' operation: {} and {}".format(self, other))

    def __ne__(self, other):
        try:
            return self.__eq__(other).boolean_not()
        except VirtualMachineInvalidOperationError:
            raise VirtualMachineInvalidOperationError(
                "Invalid operands for '~=' operation: {} and {}".format(self, other))

    def __ge__(self, other):
        try:
            return self.__lt__(other).boolean_not()
        except VirtualMachineInvalidOperationError:
            raise VirtualMachineInvalidOperationError(
                "Invalid operands for '>=' operation: {} and {}".format(self, other))

    def __le__(self, other):
        try:
            return self.__lt__(other).boolean_or(self.__eq__(other))
        except VirtualMachineInvalidOperationError:
            raise VirtualMachineInvalidOperationError(
                "Invalid operands for '<=' operation: {} and {}".format(self, other))

    def __gt__(self, other):
        try:
            return self.__le__(other).boolean_not()
        except VirtualMachineInvalidOperationError:
            raise VirtualMachineInvalidOperationError(
                "Invalid operands for '>' operation: {} and {}".format(self, other))

    def call(self, *args):
        raise VirtualMachineInvalidOperationError("Impossible to call value: {}".format(self))

    def concat(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for '..' operation: {} and {}".format(self, other))

    def boolean_and(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for 'and' operation: {} and {}".format(self, other))

    def boolean_or(self, other):
        raise VirtualMachineInvalidOperationError("Invalid operands for 'or' operation: {} and {}".format(self, other))

    def boolean_not(self):
        raise VirtualMachineInvalidOperationError("Invalid operand for 'not' operation: {}".format(self))


class StringValue(Value):
    def __init__(self, value: str):
        super().__init__()

        self.value = value

    def __str__(self):
        return "StringValue(\"{}\")".format(self.value)

    def __eq__(self, other):
        if isinstance(other, StringValue):
            return BooleanValue(self.value == other.value)
        else:
            super().__eq__(other)

    def __lt__(self, other):
        if isinstance(other, StringValue):
            return BooleanValue(self.value <= other.value)
        else:
            super().__lt__(other)

    def concat(self, other):
        if isinstance(other, StringValue):
            return StringValue(self.value + other.value)
        else:
            super().concat(other)


class BooleanValue(Value):
    def __init__(self, value: bool):
        super().__init__()

        self.value = value

    def __str__(self):
        return "BooleanValue({})".format(self.value)

    def boolean_and(self, other):
        if isinstance(other, BooleanValue):
            return BooleanValue(self.value and other.value)
        else:
            super().boolean_and(other)

    def boolean_or(self, other):
        if isinstance(other, BooleanValue):
            return BooleanValue(self.value or other.value)
        else:
            super().boolean_or(other)

    def boolean_not(self):
        return BooleanValue(not self.value)

    def __eq__(self, other):
        if isinstance(other, BooleanValue):
            return BooleanValue(self.value == other.value)
        else:
            super().__eq__(other)

    def __lt__(self, other):
        if isinstance(other, BooleanValue):
            return BooleanValue(self.value <= other.value)
        else:
            super().__lt__(other)


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
            super().__add__(other)

    def __mul__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value * other.value)
        else:
            super().__mul__(other)

    def __sub__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value - other.value)
        else:
            super().__sub__(other)

    def __truediv__(self, other):
        if isinstance(other, NumberValue):
            return NumberValue(self.value / other.value)
        else:
            super().__truediv__(other)

    def __str__(self):
        return "NumberValue({})".format(self.value)

    def __eq__(self, other):
        if isinstance(other, NumberValue):
            return BooleanValue(self.value == other.value)
        else:
            super().__eq__(other)

    def __lt__(self, other):
        if isinstance(other, NumberValue):
            return BooleanValue(self.value <= other.value)
        else:
            super().__lt__(other)


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
