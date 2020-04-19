from compiler.parse_nodes.node import ParseNode


class Script(ParseNode):
    _fields_spec = ["statements_block=block"]
    _rules = ["root"]


class StatementsBlock(ParseNode):
    _fields_spec = ["statement", "return=return_statement"]
    _rules = ["block"]
