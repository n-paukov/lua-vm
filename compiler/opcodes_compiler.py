from typing import List

from compiler.ast.builder import ASTBuilder
from compiler.opcodes.context import OPCodesCompilationContext
from vm.opcodes.opcodes import OPCode


class OPCodesCompiler:
    @staticmethod
    def compile(raw_program_text: str) -> List[OPCode]:
        builder = ASTBuilder(raw_program_text)

        ast_tree = builder.get_tree()
        context = OPCodesCompilationContext()
        ast_tree.generate_opcodes(context)

        return context.program
