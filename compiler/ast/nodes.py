from typing import List

from antlr_ast.ast import AliasNode


class ASTNode(AliasNode):
    pass


class Script(ASTNode):
    _fields_spec = ["block=block"]
    _rules = ["root"]


class LocalAssignmentExpr(ASTNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["local_variables_statement"]


class CallStatement(AliasNode):
    _fields_spec = ["function_call"]
    _rules = ["call_statement"]


class FunctionCallNode(AliasNode):
    _fields_spec = ["varpointer", "varexpr", "args"]
    _rules = ["function_call"]


class BinaryExprExpression(AliasNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["binary_expr_expression"]


class ValueHandleExpression(AliasNode):
    _fields_spec = ["handle", "args"]
    _rules = ["value_handle_expression"]


class BinaryOperationNode(AliasNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["equal_expression"]


class NodesTransformerContext:
    @staticmethod
    def get_available_nodes():
        return [Script, LocalAssignmentExpr, CallStatement, FunctionCallNode, BinaryExprExpression,
                ValueHandleExpression, BinaryOperationNode]
