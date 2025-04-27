



class MedicalTestOrder:
    def __init__(self):
        self.ordered_tests = []

    def add_test(self, enum_value):
        self.ordered_tests.append(enum_value)

    def get_all_tests(self):
        return [test.value for test in self.ordered_tests]