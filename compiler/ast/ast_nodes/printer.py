import contextlib
from typing import Any
from typing import Generator
from typing import Tuple
from typing import Union

from compiler.ast.ast_nodes.node import ASTNode


def _is_sub_node(node: Any) -> bool:
    return isinstance(node, ASTNode)


def _is_leaf(node: ASTNode) -> bool:
    for field in node._printable_fields:
        attr = getattr(node, field)
        if _is_sub_node(attr):
            return False

        elif isinstance(attr, (list, tuple)):
            for val in attr:
                if _is_sub_node(val):
                    return False
    else:
        return True


def _fields(n: ASTNode) -> Tuple[str, ...]:
    return n._printable_fields


def _leaf(node: ASTNode) -> str:
    if isinstance(node, ASTNode):
        return '{}({})'.format(
            type(node).__name__,
            ', '.join(
                '{}={}'.format(
                    field,
                    _leaf(getattr(node, field)),
                )
                for field in _fields(node)
            ),
        )
    elif isinstance(node, list):
        return '[{}]'.format(
            ', '.join(_leaf(x) for x in node),
        )
    else:
        return repr(node)


def pformat(node: Union[ASTNode, None, str], indent: str = '    ', _indent: int = 0) -> str:
    if node is None:
        return repr(node)
    elif isinstance(node, str):  # pragma: no cover (ast27 typed-ast args)
        return repr(node)
    elif _is_leaf(node):
        return _leaf(node)
    else:
        class state:
            indent = _indent

        @contextlib.contextmanager
        def indented() -> Generator[None, None, None]:
            state.indent += 1
            yield
            state.indent -= 1

        def indentstr() -> str:
            return state.indent * indent

        def _pformat(el: Union[ASTNode, None, str], _indent: int = 0) -> str:
            return pformat(
                el, indent=indent,
                _indent=_indent,
            )

        out = type(node).__name__ + '(\n'
        with indented():
            for field in _fields(node):
                attr = getattr(node, field)
                if attr == []:
                    representation = '[]'
                elif (
                        isinstance(attr, list) and
                        len(attr) == 1 and
                        isinstance(attr[0], ASTNode) and
                        _is_leaf(attr[0])
                ):
                    representation = f'[{_pformat(attr[0])}]'
                elif isinstance(attr, list):
                    representation = '[\n'
                    with indented():
                        for el in attr:
                            representation += '{}{},\n'.format(
                                indentstr(), _pformat(el, state.indent),
                            )
                    representation += indentstr() + ']'
                elif isinstance(attr, ASTNode):
                    representation = _pformat(attr, state.indent)
                else:
                    representation = repr(attr)
                out += f'{indentstr()}{field}={representation},\n'
        out += indentstr() + ')'
        return out


def print_tree(node: ASTNode):
    print(pformat(node))
