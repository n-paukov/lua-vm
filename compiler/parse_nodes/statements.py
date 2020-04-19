from compiler.parse_nodes.node import ParseNode
from compiler.parse_nodes.statement import StatementNode


class AssignmentStatement(StatementNode):
    _fields_spec = ["lvalue=lvalue_handle", "rvalue=rvalue_handle"]
    _rules = ["lb_assignment_statement"]


class FunctionDeclarationStatement(StatementNode):
    _fields_spec = ["top_level_name", "class_level_name",
                    "parameters=function_body.function_parameters_list.lvalue_identifiers_list",
                    "ellipsis=function_body.function_parameters_list.ellipsis",
                    "body=function_body.block"]
    _rules = ["lb_function_declaration_statement"]


class ReturnStatement(StatementNode):
    _fields_spec = ["expressions=expressions_tuple"]
    _rules = ["return_statement"]


class FunctionCall(StatementNode):
    _fields_spec = ["function_call"]
    _rules = ["call_statement"]


class FunctionCallNode(ParseNode):
    _fields_spec = ["varpointer", "varexpr", "args"]
    _rules = ["function_call"]
