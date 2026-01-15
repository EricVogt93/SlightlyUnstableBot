class BoolBitConverter:
    """Convert between boolean values and database bit values."""

    @staticmethod
    def bool_to_bit(value: bool) -> int:
        """Convert boolean to database bit (0 or 1)."""
        return 1 if value else 0

    @staticmethod
    def bit_to_bool(value: int) -> bool:
        """Convert database bit to boolean."""
        return value == 1
