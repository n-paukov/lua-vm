from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.node import ParseNode
from compiler.ast.ast_nodes.script import Script as ASTScript, \
    StatementsBlock as ASTStatementsBlock


class Script(ParseNode):
    _fields_spec = ["statements_block=block"]
    _rules = ["root"]

    def get_ast_node(self) -> ASTNode:
        return ASTScript(self.statements_block.get_ast_node())


class StatementsBlock(ParseNode):
    _fields_spec = ["statements", "return_statement=return_statement"]
    _rules = ["block"]

    def get_ast_node(self) -> ASTNode:
        statements = []

        for statement in self.statements:
            statements.append(statement.get_ast_node())

        if self.return_statement:
            statements.append(self.return_statement.get_ast_node())

        return ASTStatementsBlock(statements)
