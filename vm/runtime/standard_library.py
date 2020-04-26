from vm.exceptions.common import VirtualMachineInvalidOperationError
from vm.runtime.value import Value, NumberValue, StringValue, NilValue, BuiltinFunctionValue, CustomFunctionValue, \
    BooleanValue


class GeneralFunctions:
    @classmethod
    def print(cls, *args):
        printed_args = []

        for arg in args:
            printed_args.append(cls._get_value_representation(arg))

        print(*printed_args)

        return NilValue()

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


class IO:
    @staticmethod
    def write(*args):
        GeneralFunctions.print(*args)

    @staticmethod
    def read(format_string):
        return str(input())
