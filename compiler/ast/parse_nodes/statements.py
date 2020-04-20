from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.statement import StatementNode
from compiler.ast.ast_nodes.statements import AssignmentStatement as ASTAssignmentStatement, \
    ExpressionsTuple as ASTExpressionsTuple


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


class ReturnStatement(StatementNode):
    _fields_spec = ["rvalue=rvalue_handle"]
    _rules = ["lb_block_end_return_statement"]


class BreakStatement(StatementNode):
    _fields_spec = []
    _rules = ["lb_block_end_break_statement"]


class FunctionCallStatement(StatementNode):
    _fields_spec = ["top_level_name=function_call_statement.top_level_name",
                    "class_level_name=function_call_statement.class_level_name",
                    "args=function_call_statement.rvalue_handle"]
    _rules = ["lb_call_statement"]


class ConditionalStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=attr_then_block",
                    "elif=statement_elseif_item", "else_block=attr_else_block"]
    _rules = ["lb_conditional_statement"]


class ConditionalElseIfStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=block"]
    _rules = ["statement_elseif_item"]
