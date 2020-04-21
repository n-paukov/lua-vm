from vm.exceptions.common import VirtualMachineRuntimeError


class Value:
    def __init__(self):
        pass


class StringValue(Value):
    def __init__(self, value: str):
        super().__init__()

        self.value = value

    def __str__(self):
        return "StringValue(\"{}\")".format(self.value)


class NumberValue(Value):
    def __init__(self, value: float):
        super().__init__()

        self.value = value

    def __add__(self, other):
        if isinstance(other, StringValue):
            return str(self.value) + other.value
        elif isinstance(other, NumberValue):
            return NumberValue(self.value + other.value)
        else:
            raise VirtualMachineRuntimeError("Invalid operands for '+' operation: {} and {}".format(self, other))

    def __str__(self):
        return "NumberValue({})".format(self.value)
