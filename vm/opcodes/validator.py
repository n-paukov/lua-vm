from vm.opcodes.opcodes import OPCode, OPCodeType, OPCodesDefinitions


class OPCodesValidator:
    @classmethod
    def is_opcode_valid(cls, opcode: OPCode):
        if not isinstance(opcode.type, OPCodeType):
            return False

        opcode_definition = OPCodesDefinitions.get_definition(opcode.type)
        args = opcode_definition.args

        if args is None:
            args = []

        if len(opcode.args) != len(args):
            return False

        for i in range(len(opcode.args)):
            arg_specification = args[i]
            arg_type = arg_specification.type

            if not isinstance(opcode.args[i], arg_type):
                return False

        return True
