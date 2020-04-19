from compiler.parse_nodes.expressions import LocalAssignmentExpr, BinaryOperationExpression, BinaryOperationNode, \
    ExpressionsTuple, AssignableExpression
from compiler.parse_nodes.script import Script, StatementsBlock
from compiler.parse_nodes.statements import ReturnStatement, FunctionDeclarationStatement, FunctionCall, \
    FunctionCallNode, AssignmentStatement


class NodesTransformerContext:
    @staticmethod
    def get_available_nodes():
        return [Script, StatementsBlock, ReturnStatement, FunctionDeclarationStatement, LocalAssignmentExpr,
                FunctionCall, FunctionCallNode, BinaryOperationExpression, AssignableExpression,
                BinaryOperationNode, AssignmentStatement, ExpressionsTuple]
