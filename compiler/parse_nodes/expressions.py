from compiler.parse_nodes.expression import ExpressionNode
from compiler.parse_nodes.node import ParseNode


class ExpressionsTuple(ExpressionNode):
    _fields_spec = ["expressions=expressions"]
    _rules = ["lvalue_handle", "rvalue_handle"]


class LocalAssignmentExpr(ExpressionNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["local_variables_statement"]


class AssignableExpression(ExpressionNode):
    _fields_spec = ["expression_value=expression_value"]
    _rules = ["expression_assignable"]


class BinaryOperationExpression(ExpressionNode):
    _fields_spec = ["left", "operation", "right"]
    _rules = ["lb_binary_term_expression", "lb_binary_expr_expression", "lb_concat_expression",
              "lb_logic_equal_expression", "lb_logic_and_expression",
              "lb_logic_or_expression", "lb_bit_expression"]


class BinaryOperationNode(ParseNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["equal_expression"]


# class CallExpression(ExpressionNode):
#     _fields_spec = ["callable=callable_handle", "args=args_expression"]
#     _rules = ["call_expression"]


# class CallableHandle(ExpressionNode):
#     _fields_spec = ["callable=callable_handle", "args=args_expression"]
#     _rules = ["call_expression"]
