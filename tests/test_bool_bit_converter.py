"""Tests for BoolBitConverter utility class."""
import pytest
from logic.helper.BoolBitConverter import BoolBitConverter


class TestBoolToBit:
    """Tests for bool_to_bit conversion."""

    def test_true_returns_one(self):
        assert BoolBitConverter.bool_to_bit(True) == 1

    def test_false_returns_zero(self):
        assert BoolBitConverter.bool_to_bit(False) == 0

    def test_truthy_value_returns_one(self):
        assert BoolBitConverter.bool_to_bit(1) == 1
        assert BoolBitConverter.bool_to_bit("non-empty") == 1

    def test_falsy_value_returns_zero(self):
        assert BoolBitConverter.bool_to_bit(0) == 0
        assert BoolBitConverter.bool_to_bit("") == 0
        assert BoolBitConverter.bool_to_bit(None) == 0


class TestBitToBool:
    """Tests for bit_to_bool conversion."""

    def test_one_returns_true(self):
        assert BoolBitConverter.bit_to_bool(1) is True

    def test_zero_returns_false(self):
        assert BoolBitConverter.bit_to_bool(0) is False

    def test_other_values_return_false(self):
        assert BoolBitConverter.bit_to_bool(2) is False
        assert BoolBitConverter.bit_to_bool(-1) is False
