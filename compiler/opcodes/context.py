from typing import List

from vm.opcodes.IO import OPCodesIO
from vm.opcodes.opcodes import OPCode


class OPCodesCompilationContext:
    def __init__(self):
        self._opcodes: List[OPCode] = []

    @property
    def program(self) -> List[OPCode]:
        return self._opcodes

    @property
    def program_text(self) -> str:
        return OPCodesIO.get_program_text(self._opcodes)

    def add_opcode(self, opcode: OPCode):
        self._opcodes.append(opcode)
