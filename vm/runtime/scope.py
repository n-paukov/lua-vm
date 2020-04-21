from __future__ import annotations

from typing import Optional

from vm.runtime.value import Value


class Scope:
    def __init__(self, parent: Optional[Scope] = None):
        self._parent = parent
        self._values = {}

    def has_local_value(self, name: str):
        return self._values.get(name) is not None

    def get_local_value(self, name: str, default=None) -> Value:
        return self._values.get(name, default)

    def set_local_value(self, name: str, value: Value):
        self._values[name] = value

    def has_value(self, name: str):
        return self.get_value(name, None) is not None

    def get_value(self, name: str, default=None) -> Value:
        if self.has_local_value(name):
            return self.get_local_value(name)
        else:
            if self._parent is not None:
                return self._parent.get_value(name)
            else:
                return default

    def set_value(self, name: str, value: Value):
        if self.has_local_value(name):
            self.set_local_value(name, value)
        else:
            if self._parent is not None:
                self._parent.set_value(name, value)
            else:
                self.set_local_value(name, value)
