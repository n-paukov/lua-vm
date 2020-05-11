from compiler.ast.ast_nodes.common import LiteralNode, LiteralType, ValueName
from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.expression import ExpressionNode
from compiler.ast.parse_nodes.helpers import raw_value_name_to_ast_node
from compiler.ast.parse_nodes.node import ParseNode
from compiler.ast.ast_nodes.expressions import ExpressionsTuple as ASTExpressionsTuple, ValueExpression, \
    BinaryOperationExpression as ASTBinaryOperationExpression, BinaryExpressionType, \
    FunctionCallExpression as ASTFunctionCallExpression, UnaryExpressionType, \
    UnaryOperationExpression as ASTUnaryOperationExpression


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
            return LiteralNode(LiteralType.BOOLEAN, self.boolean_value.value == 'true')
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


class ValueNameExpression(ExpressionNode):
    _fields_spec = ["top_level_name", "class_level_name"]
    _rules = ["expression_value"]

    def get_ast_node(self) -> ASTNode:
        return raw_value_name_to_ast_node(self.top_level_name.value,
                                          self.class_level_name.value if self.class_level_name is not None else None)


class LeftValueIdentifierNameExpression(ExpressionNode):
    _fields_spec = ["name=NAME"]
    _rules = ["lvalue_name"]

    def get_ast_node(self) -> ASTNode:
        return ValueExpression(raw_value_name_to_ast_node(self.name.children.pop(), None))


class LeftValueIdentifiersList(ExpressionNode):
    _fields_spec = ["names=NAME"]
    _rules = ["lvalue_identifiers_list"]

    def get_ast_node(self) -> ASTNode:
        values_names = []

        for identifier in self.names:
            values_names.append(ValueExpression(raw_value_name_to_ast_node(str(identifier), None)))

        return ASTExpressionsTuple(values_names)


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
        elif operation == "and":
            expression_type = BinaryExpressionType.BOOLEAN_AND
        elif operation == "or":
            expression_type = BinaryExpressionType.BOOLEAN_OR
        elif operation == "==":
            expression_type = BinaryExpressionType.CMP_EQ
        elif operation == ">":
            expression_type = BinaryExpressionType.CMP_GT
        elif operation == "<":
            expression_type = BinaryExpressionType.CMP_LT
        elif operation == "<=":
            expression_type = BinaryExpressionType.CMP_LE
        elif operation == ">=":
            expression_type = BinaryExpressionType.CMP_GE
        elif operation == "~=":
            expression_type = BinaryExpressionType.CMP_NE
        elif operation == "..":
            expression_type = BinaryExpressionType.CONCAT
        else:
            raise NotImplementedError

        return ASTBinaryOperationExpression(self.left.get_ast_node(), self.right.get_ast_node(),
                                            expression_type)


class UnaryOperationExpression(ExpressionNode):
    _fields_spec = ["operation", "right"]
    _rules = ["lb_unary_expression"]

    def get_ast_node(self) -> ASTNode:
        operation = self.operation.value

        if operation == "-":
            expression_type = UnaryExpressionType.MINUS
        elif operation == "not":
            expression_type = UnaryExpressionType.NOT
        else:
            raise NotImplementedError

        return ASTUnaryOperationExpression(self.right.get_ast_node(), expression_type)


class FunctionCallExpression(ExpressionNode):
    _fields_spec = ["callable=expression_call.expression_callable", "args=expression_call.rvalue_handle"]
    _rules = ["lb_call_expression"]

    def get_ast_node(self) -> ASTNode:
        return ASTFunctionCallExpression(self.callable.get_ast_node(),
                                         self.args.get_ast_node() if self.args else ASTExpressionsTuple([]), False)

# class CallableHandle(ExpressionNode):
#     _fields_spec = ["callable=callable_handle", "args=args_expression"]
#     _rules = ["call_expression"]
