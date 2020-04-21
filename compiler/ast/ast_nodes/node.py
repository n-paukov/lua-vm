from compiler.opcodes.context import OPCodesCompilationContext


class ASTNode:
    _printable_fields = []

    def __init__(self):
        pass

    def generate_opcodes(self, context: OPCodesCompilationContext):
        raise NotImplementedError
