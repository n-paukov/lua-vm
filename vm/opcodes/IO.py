from typing import List

from vm.exceptions.common import OPCodeValidationError
from vm.opcodes.opcodes import OPCodeType, OPCodeBinaryTestMode, OPCode, OPCodesDefinitions
from vm.opcodes.validator import OPCodesValidator


class OPCodesIO:
    @staticmethod
    def get_program_text(opcodes: List[OPCode]) -> str:
        text = ""

        for opcode in opcodes:
            if not OPCodesValidator.is_opcode_valid(opcode):
                raise OPCodeValidationError

            opcode_definition = OPCodesDefinitions.get_definition(opcode.type)

            text += "{} {}\n".format(opcode_definition.name, " ".join([str(arg) for arg in opcode.args]))

        return text
