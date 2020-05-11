import astpretty

from compiler.ast.ast_nodes.printer import print_tree, pformat
from compiler.ast.builder import ASTBuilder
from compiler.opcodes_compiler import OPCodesCompiler
from utils.files import read_all_text, write_all_text
from vm.opcodes.IO import OPCodesIO
from vm.opcodes.opcodes import OPCode, OPCodeType
from vm.vm import VirtualMachine


def main():
    builder = ASTBuilder(read_all_text('./tests/test.lua'))
    print_tree(builder.get_tree())
    # write_all_text("./tests/test_ast.txt", pformat(builder.get_tree()))

    bytecode = OPCodesCompiler.compile(read_all_text('./tests/test.lua'))
    print(OPCodesIO.get_program_text(bytecode))
    # write_all_text("./tests/test_bytecode.txt", OPCodesIO.get_program_text(bytecode))

    virtual_machine = VirtualMachine(bytecode)
    virtual_machine.load_standard_library()

    virtual_machine.run()


if __name__ == '__main__':
    main()
