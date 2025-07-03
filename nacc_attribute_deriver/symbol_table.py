from collections import deque
from typing import Any, Dict, Iterator, MutableMapping, Optional


class SymbolTable(MutableMapping[str, Any]):
    """Implements a dictionary like object for using metadata paths as keys."""

    def __init__(
        self,
        symbol_dict: Optional[MutableMapping[str, Any]] = None,
        separator: str = ".",
    ) -> None:
        self.__table: Dict[str, Any] = {}
        self.__separator = separator

        # interpret metadata paths
        if symbol_dict:
            for key, value in symbol_dict.items():
                self[key] = value

    def __setitem__(self, key: str, value: Any) -> None:
        table = self.__table
        key_list = deque(key.split(self.__separator))
        while key_list:
            sub_key = key_list.popleft()
            obj = table.get(sub_key, None)
            if not obj:
                if not key_list:
                    table[sub_key] = value
                    return

                table[sub_key] = {}
                table = table[sub_key]
                continue

            if not key_list:
                table[sub_key] = value
                return

            if not isinstance(obj, dict):
                raise KeyError("Key %s maps to atomic value", key)

            table = obj

    def __getitem__(self, key: str) -> Optional[Any]:
        value = self.__table
        key_list = key.split(self.__separator)
        while key_list:
            sub_key = key_list.pop(0)
            if not isinstance(value, dict):
                raise KeyError("Key %s maps to atomic value", key)

            if sub_key not in value:
                raise KeyError("Key %s does not exist", key)

            value = value[sub_key]

        return value

    def __contains__(self, key: Any) -> bool:
        if not isinstance(key, str) or self.__separator not in key:
            return key in self.__table

        value = self.__table
        key_list = key.split(self.__separator)
        while key_list:
            sub_key = key_list.pop(0)
            if not isinstance(value, dict):
                raise KeyError()

            if sub_key in value:
                value = value[sub_key]
            else:
                return False

        return True

    def __delitem__(self, key: Any) -> None:
        return

    def __iter__(self) -> Iterator[str]:
        return self.__table.__iter__()

    def __len__(self) -> int:
        return len(self.__table)

    def __str__(self) -> str:
        return str(self.__table)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self.to_dict() == other

        return self.to_dict() == other.to_dict()

    def to_dict(self) -> MutableMapping[str, Any]:
        return self.__table

    def pop(self, key: str, default: Any = None) -> Any:
        """Implement the pop method."""
        # we know it's there, need to manually pop
        table = self.__table
        key_parts = key.split(self.__separator)

        for k in key_parts[:-1]:
            if isinstance(table, dict) and k in table:
                table = table[k]
            else:
                return default

        last_key = key_parts[-1]
        if isinstance(table, dict) and last_key in table:
            return table.pop(last_key)

        return default
