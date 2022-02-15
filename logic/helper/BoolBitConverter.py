class BoolBitConverter:

    @staticmethod
    def bool_to_bit(b):
        if b:
            return 1
        return 0

    @staticmethod
    def bit_to_bool(b):
        if b == 1:
            return True
        return False
