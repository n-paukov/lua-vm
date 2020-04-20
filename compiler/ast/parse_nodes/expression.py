from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.node import ParseNode


class ExpressionNode(ParseNode):
    def get_ast_node(self) -> ASTNode:
        raise NotImplementedError
