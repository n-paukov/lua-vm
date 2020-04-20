from typing import Optional

from compiler.ast.ast_nodes.common import ValueName, LiteralNode, LiteralType


def raw_value_name_to_ast_node(top_level_name: str, class_level_name: Optional[str]):
    if class_level_name:
        return ValueName(LiteralNode(LiteralType.IDENTIFIER, class_level_name),
                         LiteralNode(LiteralType.IDENTIFIER, top_level_name))
    else:
        return ValueName(LiteralNode(LiteralType.IDENTIFIER, top_level_name))
