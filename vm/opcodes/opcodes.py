from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional

from vm.exceptions.common import OPCodeValidationError


class OPCodeType(Enum):
    # Declares a function (save pointer to function in current scope)
    # Example: function test
    FUNCTION = auto()

    # Returns from the function (the return value should be pushed to the stack)
    # Example: return
    RETURN = auto()

    # Pushes value to the stack
    # Example: push 10, push var
    PUSH = auto()

    # Pops value from the stack
    # Example: pop
    POP = auto()

    # Gets value from the stack and assigns in to the variable in current scope
    # Example: assign var
    ASSIGN = auto()

    # Pops value from the stack and calls it
    # Example: call
    CALL = auto()

    # Gets two values from the stack, sums them and pushes result
    # Example: sum
    SUM = auto()

    # Gets two values from the stack, compares their values and pushes result
    # Modes: EQ, NE, LT, GT, LE, GE
    # Example: binary_test EQ
    BINARY_TEST = auto()

    # Gets value from the stack, tests it and pushes result
    # Example: unary_test
    UNARY_TEST = auto()

    # Jumps to the label
    # Example: jump start
    JUMP = auto()

    # Jumps to the label if test was failed
    # Example: jump_neg start
    JUMP_NEG = auto()

    # Jumps to the label if test was succeed
    # Example: jump_pos start
    JUMP_POS = auto()

    # Gets two values from the stack, subtracts them and pushes result
    # Example: subtract
    SUBTRACT = auto()

    # Gets two values from the stack, multiplies them and pushes result
    # Example: multiply
    MULTIPLY = auto()

    # Gets two values from the stack, divides them and pushes result
    # Example: divide
    DIVIDE = auto()


class OPCodeBinaryTestMode(Enum):
    EQ = "eq"
    NE = "ne"
    LT = "lt"
    GT = "gt"
    LE = "le"
    GE = "ge"


class OPCodeArgDefinition:
    def __init__(self, arg_type):
        self._type = arg_type

    @property
    def type(self):
        return self._type


class OPCodeDefinition:
    def __init__(self, name: str, args: Optional[List[OPCodeArgDefinition]] = None):
        self._name = name
        self._args = args

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args


class OPCodesDefinitions:
    _opcodes_definitions = {
        OPCodeType.FUNCTION: OPCodeDefinition("function", [OPCodeArgDefinition(str)]),
        OPCodeType.RETURN: OPCodeDefinition("return"),
        OPCodeType.PUSH: OPCodeDefinition("push", [OPCodeArgDefinition(str)]),
        OPCodeType.POP: OPCodeDefinition("pop"),
        OPCodeType.ASSIGN: OPCodeDefinition("assign", [OPCodeArgDefinition(str)]),
        OPCodeType.CALL: OPCodeDefinition("call"),
        OPCodeType.SUM: OPCodeDefinition("sum"),
        OPCodeType.BINARY_TEST: OPCodeDefinition("binary_test", [OPCodeArgDefinition(OPCodeBinaryTestMode)]),
        OPCodeType.UNARY_TEST: OPCodeDefinition("unary_test"),
        OPCodeType.JUMP: OPCodeDefinition("jump"),
        OPCodeType.JUMP_NEG: OPCodeDefinition("jump_neg"),
        OPCodeType.JUMP_POS: OPCodeDefinition("jump_pos"),
        OPCodeType.SUBTRACT: OPCodeDefinition("subtract"),
        OPCodeType.MULTIPLY: OPCodeDefinition("multiply"),
        OPCodeType.DIVIDE: OPCodeDefinition("divide"),
    }

    @classmethod
    def get_definition(cls, opcode_type: OPCodeType) -> OPCodeDefinition:
        return cls._opcodes_definitions.get(opcode_type)


class OPCode:
    def __init__(self, opcode_type: OPCodeType, args=None):
        if args is None:
            args = []

        self._type = opcode_type
        self._args = args

    @property
    def type(self) -> OPCodeType:
        return self._type

    @property
    def args(self) -> Optional[List]:
        return self._args

    @property
    def first_arg(self):
        return self.get_arg(0)

    @property
    def second_arg(self):
        return self.get_arg(1)

    def get_arg(self, arg_index: int):
        return self._args[arg_index]

    def __str__(self):
        return "OPCode(type={}, args={})".format(self._type, self._args)
