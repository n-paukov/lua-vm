import astpretty

from compiler.ast.ast_nodes.printer import print_tree
from compiler.ast.builder import ASTBuilder
from utils.files import read_all_text

def main():
    builder = ASTBuilder(read_all_text('./tests/test.lua'))
    ast = builder.get_tree()

    #astpretty.pprint(ast)

    vv = ast.get_ast_node()
    print_tree(vv)


if __name__ == '__main__':
    main()
