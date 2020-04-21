from compiler.ast.ast_nodes.common import FunctionParameter, ValueName
from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.helpers import raw_value_name_to_ast_node
from compiler.ast.parse_nodes.statement import StatementNode
from compiler.ast.ast_nodes.statements import AssignmentStatement as ASTAssignmentStatement, \
    FunctionDeclarationStatement as ASTFunctionDeclarationStatement, ReturnStatement as ASTReturnStatement, \
    BreakStatement as ASTBreakStatement
from compiler.ast.ast_nodes.expressions import FunctionCallExpression as ASTFunctionCallExpression, ValueExpression


class AssignmentStatement(StatementNode):
    _fields_spec = ["lvalue=lvalue_handle", "rvalue=rvalue_handle"]
    _rules = ["lb_assignment_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTAssignmentStatement(self.lvalue.get_ast_node(), self.rvalue.get_ast_node())


class FunctionDeclarationStatement(StatementNode):
    _fields_spec = ["top_level_name", "class_level_name",
                    "parameters=function_body.function_parameters_list.lvalue_identifiers_list",
                    "ellipsis=function_body.function_parameters_list.ellipsis",
                    "body=function_body.block"]
    _rules = ["lb_function_declaration_statement"]

    def get_ast_node(self) -> ASTNode:
        parameters = []

        for name in self.parameters.NAME:
            parameters.append(ValueName(name))

        return ASTFunctionDeclarationStatement(
            raw_value_name_to_ast_node(self.top_level_name.value, self.class_level_name.value),
            parameters,
            self.body.get_ast_node())


class ReturnStatement(StatementNode):
    _fields_spec = ["rvalue=rvalue_handle"]
    _rules = ["lb_block_end_return_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTReturnStatement(self.rvalue.get_ast_node())


class BreakStatement(StatementNode):
    _fields_spec = []
    _rules = ["lb_block_end_break_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTBreakStatement()


class FunctionCallStatement(StatementNode):
    _fields_spec = ["top_level_name=function_call_statement.top_level_name",
                    "class_level_name=function_call_statement.class_level_name",
                    "args=function_call_statement.rvalue_handle"]
    _rules = ["lb_call_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTFunctionCallExpression(
            ValueExpression(raw_value_name_to_ast_node(self.top_level_name, self.class_level_name)),
            self.args.get_ast_node())


class ConditionalStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=attr_then_block",
                    "elif=statement_elseif_item", "else_block=attr_else_block"]
    _rules = ["lb_conditional_statement"]


class ConditionalElseIfStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=block"]
    _rules = ["statement_elseif_item"]
