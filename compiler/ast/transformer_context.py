from compiler.ast.parse_nodes.expressions import LocalAssignmentExpr, BinaryOperationExpression, \
    ExpressionsTuple, AssignableExpression, FunctionCallExpression, LiteralExpression, ValueNameExpression, \
    LeftValueIdentifiersList, UnaryOperationExpression, LeftValueIdentifierNameExpression
from compiler.ast.parse_nodes.script import Script, StatementsBlock
from compiler.ast.parse_nodes.statements import ReturnStatement, FunctionDeclarationStatement, FunctionCallStatement, \
    AssignmentStatement, ConditionalStatement, ConditionalElseIfStatement, ForLoopStatement


class NodesTransformerContext:
    @staticmethod
    def get_available_nodes():
        return [Script, StatementsBlock, ReturnStatement, FunctionDeclarationStatement, LocalAssignmentExpr,
                FunctionCallStatement, BinaryOperationExpression, AssignableExpression, FunctionCallExpression,
                LiteralExpression, ValueNameExpression, LeftValueIdentifiersList,
                AssignmentStatement, ExpressionsTuple, ConditionalStatement, ForLoopStatement,
                ConditionalElseIfStatement, UnaryOperationExpression, LeftValueIdentifierNameExpression]
