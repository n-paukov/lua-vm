from enum import Enum
from typing import Optional, Tuple, Union

from compiler.ast.ast_nodes.node import ASTNode
from compiler.opcodes.context import OPCodesCompilationContext
from vm.opcodes.opcodes import OPCode, OPCodeType


class LiteralType(Enum):
    STRING = 0
    NUMBER = 1
    IDENTIFIER = 2
    BOOLEAN = 3
    NIL = 4


class LiteralNode(ASTNode):
    _printable_fields = ["_type", "_value"]

    def __init__(self, literal_type: LiteralType, value: Optional[Union[int, str, float, bool]] = None):
        super().__init__()
        self._type = literal_type
        self._value = value

    def __str__(self):
        return "Literal(type={}, value={})".format(self._type, self._value)

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def value_representation(self):
        value = ""

        if self._type == LiteralType.STRING:
            value = self._value
        elif self._type == LiteralType.NUMBER:
            value = str(self._value)
        elif self._type == LiteralType.IDENTIFIER:
            value = str(self._value)
        elif self._type == LiteralType.BOOLEAN:
            value = str(self._value).lower()
        elif self._type == LiteralType.NIL:
            value = str(self._value)

        return value

    def generate_opcodes(self, context: OPCodesCompilationContext):
        context.add_opcode(OPCode(OPCodeType.PUSH, [self.value_representation]))


class ValueName(ASTNode):
    _printable_fields = ["full_name"]

    def __init__(self, name: LiteralNode, class_name: Optional[LiteralNode] = None):
        super().__init__()
        self._name = name
        self._class_name = class_name

    @property
    def is_class_value(self) -> bool:
        return self._class_name is not None

    @property
    def class_name(self):
        return self._class_name

    @property
    def name(self):
        return self._name

    @property
    def full_name(self):
        if self._class_name is not None:
            return "{}:{}".format(self._class_name.value, self._name.value)
        else:
            return "{}".format(self._name.value)

    def __str__(self):
        if self._class_name is not None:
            return "ValueName(\"{}\")".format(self.full_name)

    def generate_opcodes(self, context: OPCodesCompilationContext):
        context.add_opcode(OPCode(OPCodeType.PUSH, [self.full_name]))


class FunctionParameter:
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_ellipsis(self):
        return self._name == '...'
