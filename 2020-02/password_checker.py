import re

from utils.file_handler import FileHandler


class PasswordEntry:
    min = None
    max = None
    letter = None
    password = None
    parse_line_expression = r"(?P<min>\d+)-(?P<max>\d+) (?P<letter>\w+): (?P<password>\w+)"

    def __init__(self, line):
        self.line = line
        self.parse_line()

    def parse_line(self):
        regex = re.compile(self.parse_line_expression)
        parsed_line = regex.search(self.line)
        if parsed_line:
            self.min = int(parsed_line.group("min"))
            self.max = int(parsed_line.group("max"))
            self.letter = parsed_line.group("letter")
            self.password = parsed_line.group("password")

    def is_password_valid(self):
        number_of_letters_in_password = self.password.count(self.letter)
        return self.max >= number_of_letters_in_password >= self.min


class PasswordChecker:
    def __init__(self, entries):
        self.password_entries = [PasswordEntry(entry) for entry in entries]
        self.valid_passwords = 0

    def check_passwords(self):
        for entry in self.password_entries:
            if entry.is_password_valid():
                self.valid_passwords += 1

        return self.valid_passwords


if __name__ == "__main__":
    file_handler = FileHandler('input.txt')
    file_handler.load_str()
    password_checker = PasswordChecker(file_handler.file_lines)
    print("{} valid passwords found.".format(password_checker.check_passwords()))
