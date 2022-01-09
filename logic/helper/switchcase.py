class switchcase:
    case_dictionary = None
    switch = None

    def __init__(self, case_dictionary, switch):
        self.case_dictionary = case_dictionary
        self.switch = switch

    def compare(self):
        for case, method in self.case_dictionary:
            if case == self.switch:
                return method
        return "No matching case existing!"

    def compare(self, contains: bool):
        if not contains:
            return

        for case in self.case_dictionary:
            if case in self.switch:
                return self.case_dictionary[case]
        return "UnknownError"
