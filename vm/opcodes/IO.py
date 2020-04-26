from typing import List

from vm.exceptions.common import OPCodeValidationError
from vm.opcodes.opcodes import OPCodeType, OPCode, OPCodesDefinitions
from vm.opcodes.validator import OPCodesValidator


class OPCodesIO:
    @staticmethod
    def get_program_text(opcodes: List[OPCode]) -> str:
        text = ""

        line_index = 0

        for opcode in opcodes:
            if not OPCodesValidator.is_opcode_valid(opcode):
                raise OPCodeValidationError

            opcode_definition = OPCodesDefinitions.get_definition(opcode.type)

            text += "{}:\t\t {} {}\n".format(line_index, opcode_definition.name,
                                         " ".join([str(arg) for arg in opcode.args]))

            line_index += 1

        return text
