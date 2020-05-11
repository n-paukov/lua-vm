from compiler.ast.ast_nodes.common import FunctionParameter, ValueName
from compiler.ast.ast_nodes.node import ASTNode
from compiler.ast.parse_nodes.helpers import raw_value_name_to_ast_node
from compiler.ast.parse_nodes.statement import StatementNode
from compiler.ast.ast_nodes.statements import AssignmentStatement as ASTAssignmentStatement, \
    FunctionDeclarationStatement as ASTFunctionDeclarationStatement, ReturnStatement as ASTReturnStatement, \
    BreakStatement as ASTBreakStatement, ForLoopStatement as ASTForLoopStatement
from compiler.ast.ast_nodes.expressions import FunctionCallExpression as ASTFunctionCallExpression, ValueExpression, \
    ExpressionsTuple


class AssignmentStatement(StatementNode):
    _fields_spec = ["lvalue=attr_lvalue", "rvalue=attr_rvalue", "local=attr_local"]
    _rules = ["lb_assignment_statement", "lb_local_lvalue_declaration_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTAssignmentStatement(self.lvalue.get_ast_node(), self.rvalue.get_ast_node(), self.local is not None)


class FunctionDeclarationStatement(StatementNode):
    _fields_spec = ["top_level_name", "class_level_name",
                    "parameters=function_body.function_parameters_list.lvalue_identifiers_list",
                    "ellipsis=function_body.function_parameters_list.ellipsis",
                    "body=function_body.block"]
    _rules = ["lb_function_declaration_statement"]

    def get_ast_node(self) -> ASTNode:
        parameters = []

        if self.parameters is not None:
            for name in self.parameters.NAME:
                parameters.append(ValueName(name))

        return ASTFunctionDeclarationStatement(
            raw_value_name_to_ast_node(self.top_level_name.value,
                                       self.class_level_name.value if self.class_level_name is not None else None),
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
            self.args.get_ast_node() if self.args else ExpressionsTuple([]), True)


class ConditionalStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=attr_then_block",
                    "elif=statement_elseif_item", "else_block=attr_else_block"]
    _rules = ["lb_conditional_statement"]


class ConditionalElseIfStatement(StatementNode):
    _fields_spec = ["condition=expression", "then_block=block"]
    _rules = ["statement_elseif_item"]


class ForLoopStatement(StatementNode):
    _fields_spec = ["counter_name=attr_counter", "start=attr_start", "end=attr_end", "step=attr_step", "body=block"]
    _rules = ["lb_for_statement"]

    def get_ast_node(self) -> ASTNode:
        return ASTForLoopStatement(raw_value_name_to_ast_node(self.counter_name, None),
                                   self.start.get_ast_node(),
                                   self.end.get_ast_node(),
                                   self.step.get_ast_node() if self.step is not None else None,
                                   self.body.get_ast_node())
