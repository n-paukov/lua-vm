from compiler.ast.ast_nodes.common import LiteralNode, LiteralType, ValueName
from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.expression import ExpressionNode
from compiler.ast.parse_nodes.helpers import raw_value_name_to_ast_node
from compiler.ast.parse_nodes.node import ParseNode
from compiler.ast.ast_nodes.expressions import ExpressionsTuple as ASTExpressionsTuple, ValueExpression, \
    BinaryOperationExpression as ASTBinaryOperationExpression, BinaryExpressionType, \
    FunctionCallExpression as ASTFunctionCallExpression


class ExpressionsTuple(ExpressionNode):
    _fields_spec = ["expressions=expressions"]
    _rules = ["lvalue_handle", "rvalue_handle"]

    def get_ast_node(self) -> ASTNode:
        expressions = []

        for expression in self.expressions:
            expressions.append(expression.get_ast_node())

        return ASTExpressionsTuple(expressions)


class LiteralExpression(ExpressionNode):
    _fields_spec = ["nil_value",
                    "boolean_value",
                    "number_value",
                    "string_value"]

    _rules = ["lb_nil_literal_expression", "lb_false_literal_expression",
              "lb_true_literal_expression", "lb_number_literal_expression", "lb_string_literal_expression"]

    def get_ast_node(self) -> ASTNode:
        if self.nil_value:
            return LiteralNode(LiteralType.NIL)
        elif self.boolean_value:
            return LiteralNode(LiteralType.BOOLEAN, bool(self.boolean_value.value))
        elif self.number_value:
            return LiteralNode(LiteralType.NUMBER, float(self.number_value.value))
        elif self.string_value:
            return LiteralNode(LiteralType.STRING, str(self.string_value.value))
        else:
            raise NotImplementedError


class LocalAssignmentExpr(ExpressionNode):
    _fields_spec = ["left", "op", "right"]
    _rules = ["local_variables_statement"]


class AssignableExpression(ExpressionNode):
    _fields_spec = ["expression_value"]
    _rules = ["expression_assignable"]

    def get_ast_node(self) -> ASTNode:
        return ValueExpression(self.expression_value.get_ast_node())


class LeftValueIdentifiersList(ExpressionNode):
    _fields_spec = ["NAME"]
    _rules = ["lvalue_identifiers_list"]

    def get_ast_node(self) -> ASTNode:
        raise NotImplementedError


class ValueNameExpression(ExpressionNode):
    _fields_spec = ["top_level_name", "class_level_name"]
    _rules = ["expression_value"]

    def get_ast_node(self) -> ASTNode:
        return raw_value_name_to_ast_node(self.top_level_name.value,
                                          self.class_level_name.value if self.class_level_name is not None else None)


class BinaryOperationExpression(ExpressionNode):
    _fields_spec = ["left", "operation", "right"]
    _rules = ["lb_binary_term_expression", "lb_binary_expr_expression", "lb_concat_expression",
              "lb_logic_equal_expression", "lb_logic_and_expression",
              "lb_logic_or_expression", "lb_bit_expression"]

    def get_ast_node(self) -> ASTNode:
        operation = self.operation.value

        if operation == "+":
            expression_type = BinaryExpressionType.ADD
        elif operation == "-":
            expression_type = BinaryExpressionType.SUBTRACT
        elif operation == "*":
            expression_type = BinaryExpressionType.MULTIPLY
        elif operation == "/":
            expression_type = BinaryExpressionType.DIVIDE
        else:
            raise NotImplementedError

        return ASTBinaryOperationExpression(self.left.get_ast_node(), self.right.get_ast_node(),
                                            expression_type)


class FunctionCallExpression(ExpressionNode):
    _fields_spec = ["callable=expression_call.expression_callable", "args=expression_call.rvalue_handle"]
    _rules = ["lb_call_expression"]

    def get_ast_node(self) -> ASTNode:
        return ASTFunctionCallExpression(self.callable.get_ast_node(),
                                         self.args.get_ast_node())

# class CallableHandle(ExpressionNode):
#     _fields_spec = ["callable=callable_handle", "args=args_expression"]
#     _rules = ["call_expression"]
