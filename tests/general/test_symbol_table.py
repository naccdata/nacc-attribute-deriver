from nacc_attribute_deriver.symbol_table import SymbolTable


class TestSymbolTable:
    def test_empty(self):
        table = SymbolTable()
        assert table.get("dummy") is None

    def test_non_empty(self):
        table = SymbolTable({"a": {"b": {"c": 1}}})
        assert table.get("a") == {"b": {"c": 1}}
        assert table.get("a.b") == {"c": 1}
        assert table.get("a.b.c") == 1
        assert table.get("a.b.c.d") is None

    def test_set(self):
        table = SymbolTable()
        table["a.b.c"] = {"d": 1}
        assert table.get("a.b.c.d") == 1
        assert table["a.b.c.d"] == 1

        table["a.b.e.d"] = 2
        assert table.get("a.b.e.d") == 2

        table["a.b.c.d"] = 3
        assert table.get("a.b.c.d") == 3

    def test_initialized(self):
        table = SymbolTable(
            {"a": {"b": {"x": 1}}, "s": {"a": {"y": 2, "d": ["alpha", "beta"]}}}
        )
        assert table.get("a.b.x") == 1
        assert table.get("s.a.y") == 2
        table["a.b.c"] = {"d": 1}
        assert table.get("a.b.c.d") == 1
        assert table["a.b.c.d"] == 1

        table["a.b.e.d"] = 2
        assert table.get("a.b.e.d") == 2

        table["a.b.c.d"] = 3
        assert table.get("a.b.c.d") == 3

        assert table.get("s.a.d") == ["alpha", "beta"]

    def test_zero_value(self):
        table = SymbolTable({"a": 0})
        assert table.get("a") is not None
        assert table.get("a") == 0

    def test_pop(self):
        table = SymbolTable(
            {"a": 0, "b": 1, "c": 2, "nested": {"d": {"e": 3}, "f": 4, "g": {"h": 5}}}
        )

        assert table.pop("b") == 1
        assert table.pop("z") is None
        assert table.pop("nested.d.e") == 3
        assert table.pop("nested.g") == {"h": 5}
        assert table.pop("nested.key.not.in.dict", "my_default") == "my_default"

        assert table.to_dict() == {"a": 0, "c": 2, "nested": {"d": {}, "f": 4}}

    def test_mutability(self):
        """Test this in the way the Attribute Curation gear uses it.

        Weird bug discovered when starting dict (subject.info) was
        empty, caused it to not be globally mutated, but was fine if
        subject.info was NOT empty (happened to be the case for any
        subjects relevant to MQT which is why it wasn't really noticed
        before).

        Issue was related to the original empty table being overwritten
        in __setitem__ when it was nested; handled by changing condition
        to "if obj is not None" instead of just "if not obj"
        """

        # if starting dict is empty
        subject_table = SymbolTable({})

        table = SymbolTable({})
        table["subject.info"] = subject_table.to_dict()
        table["file.info"] = {}

        table["subject.info.derived.dummy"] = 10

        assert subject_table.to_dict() == {"derived": {"dummy": 10}}

        # if starting dict is not empty
        subject_table = SymbolTable({"hello": "world"})

        table = SymbolTable({})
        table["subject.info"] = subject_table.to_dict()
        table["file.info"] = {}

        table["subject.info.derived.dummy"] = 10

        assert subject_table.to_dict() == {"hello": "world", "derived": {"dummy": 10}}
