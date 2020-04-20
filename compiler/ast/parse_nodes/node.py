from antlr_ast.ast import AliasNode

from compiler.ast.ast_nodes.node import ASTNode


class ParseNode(AliasNode):
    def get_ast_node(self) -> ASTNode:
        raise NotImplementedError()
