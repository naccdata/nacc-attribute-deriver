from collections import deque
from typing import Any, Iterator, MutableMapping, Optional


class SymbolTable(MutableMapping):
    """Implements a dictionary like object for using metadata paths as keys."""

    def __init__(self,
                 symbol_dict: MutableMapping = None,
                 separator: str = '.') -> None:
        self.__table = {}
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
            obj = table.get(sub_key)
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

    def __iter__(self) -> Iterator:
        return self.__table.__iter__()

    def __len__(self) -> int:
        return len(self.__table)

    def __str__(self) -> str:
        return str(self.__table)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, dict):
            return self.to_dict() == other

        return self.to_dict() == other.to_dict()

    def to_dict(self) -> MutableMapping:
        return self.__table

    def compress(
        self,
        table: MutableMapping = None,
        parent_key: str = None,
    ) -> MutableMapping:
        """Compress the table by flattening all keys."""
        if not table:
            table = self.__table

        items = []
        for k, v in table.items():
            compressed_key = f'{parent_key}{self.__separator}{k}' if parent_key else k

            if isinstance(v, MutableMapping):
                items.extend(
                    self.compress(table=v, parent_key=compressed_key).items())
            else:
                items.append((compressed_key, v))

        return dict(items)
