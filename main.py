import astpretty
from compiler.ast.builder import ASTBuilder
from utils.files import read_all_text

def main():
    builder = ASTBuilder(read_all_text('./tests/test.lua'))
    ast = builder.get_tree()

    astpretty.pprint(ast)


if __name__ == '__main__':
    main()
