import math

from vm.exceptions.common import VirtualMachineInvalidOperationError
from vm.runtime.value import Value, NumberValue, StringValue, NilValue, BuiltinFunctionValue, CustomFunctionValue, \
    BooleanValue


class GeneralIOFunctions:
    @classmethod
    def print(cls, *args):
        printed_args = []

        for arg in args:
            printed_args.append(cls._get_value_representation(arg))

        print(*printed_args)

        return NilValue()

    @classmethod
    def read(cls):
        return StringValue(input())

    @staticmethod
    def _get_value_representation(value: Value):
        if isinstance(value, NumberValue):
            return str(value.value)
        elif isinstance(value, StringValue):
            return str(value.value)
        elif isinstance(value, NilValue):
            return 'nil'
        elif isinstance(value, BooleanValue):
            return 'true' if value.value else 'false'
        elif isinstance(value, BuiltinFunctionValue):
            return 'builtin_function_instance(name=\"{}\")'.format(value.name)
        elif isinstance(value, CustomFunctionValue):
            return 'function_instance(name=\"{}\", addr={})'.format(value.name, value.instruction_address)
        else:
            raise VirtualMachineInvalidOperationError(
                "Impossible to get value representation for value {}".format(value))


class GeneralMathFunctions:
    @classmethod
    def sin(cls, arg: NumberValue):
        return NumberValue(math.sin(arg.value))


class GeneralConversionsFunctions:
    @classmethod
    def tostring(cls, arg: Value):
        if isinstance(arg, NumberValue):
            return StringValue(str(arg.value))
        elif isinstance(arg, BooleanValue):
            return StringValue('true' if arg.value else 'false')
        elif isinstance(arg, NilValue):
            return StringValue('nil')
        elif isinstance(arg, StringValue):
            return StringValue(arg.value)
        elif isinstance(arg, BuiltinFunctionValue):
            return StringValue(arg.name)
        elif isinstance(arg, CustomFunctionValue):
            return StringValue(arg.name)
        else:
            raise VirtualMachineInvalidOperationError(
                "Impossible to cast to string value {}".format(arg))

    @classmethod
    def tonumber(cls, arg: Value):
        if isinstance(arg, NumberValue):
            return NumberValue(arg.value)
        elif isinstance(arg, BooleanValue):
            return NumberValue(int(arg.value))
        elif isinstance(arg, StringValue):
            return NumberValue(float(arg.value))
        else:
            raise VirtualMachineInvalidOperationError(
                "Impossible to cast to number value {}".format(arg))
