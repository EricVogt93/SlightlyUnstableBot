class BoolBitConverter:

    @staticmethod
    def bool_to_bit(b):
        if b:
            return 2
        return 1

    @staticmethod
    def bit_to_bool(b):
        if b == '2':
            return False
        return True
