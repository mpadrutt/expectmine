import pytest
from expectmine.io.io.cli_io import CliIo
from expectmine.io.io.dict_io import DictIo


def test_initialize_dict_io():
    io = DictIo({})

    assert isinstance(io, DictIo)


def test_initialize_cli_io():
    io = CliIo()
    assert isinstance(io, CliIo)


def test_get_primitive_value_dict_io():
    io = DictIo({"str": "string", "float": 1.23, "int": 1, "bool": True})

    assert io.string("str", "") == "string"
    assert io.number("float", "") == 1.23
    assert io.number("int", "") == 1
    assert io.boolean("bool", "")


def test_key_not_found_dict_io():
    with pytest.raises(ValueError):
        io = DictIo({})

        io.string("str", "")
