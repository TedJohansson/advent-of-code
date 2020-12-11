from utils.file_handler import FileHandler


class Group:
    def __init__(self, submission):
        self.submission = submission

    def get_value(self):
        return len(set(self.submission.replace(" ", "")))

    def get_intersect_value(self):
        individual_answers = [set(x) for x in self.submission.split(" ")]
        del individual_answers[0]
        u = individual_answers[0].intersection(*individual_answers)
        return len(u)


class FormCalculator:
    def __init__(self, lines):
        self.groups = [Group(line) for line in lines]

    def calculate(self):
        return sum([group.get_value() for group in self.groups])

    def calculate_intersect(self):
        return sum([group.get_intersect_value() for group in self.groups])


if __name__ == "__main__":
    file_handler = FileHandler("input.txt")
    file_handler.load_str()
    file_handler.join_on_not_empty()
    form_calculator = FormCalculator(file_handler.file_lines)
    print(form_calculator.calculate())
    print(form_calculator.calculate_intersect())
