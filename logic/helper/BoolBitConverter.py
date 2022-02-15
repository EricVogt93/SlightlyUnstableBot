class BoolBitConverter:

    @staticmethod
    def bool_to_bit(b):
        if b:
            return 1
        return 0

    @staticmethod
    def bit_to_bool(b):
        if b == b'\x00':
            return False
        return True
