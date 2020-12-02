import re

from utils.file_handler import FileHandler


class PasswordEntry:
    first_num = None
    second_num = None
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
            self.first_num = int(parsed_line.group("min"))
            self.second_num = int(parsed_line.group("max"))
            self.letter = parsed_line.group("letter")
            self.password = parsed_line.group("password")

    def is_password_valid_min_max(self):
        number_of_letters_in_password = self.password.count(self.letter)
        return self.second_num >= number_of_letters_in_password >= self.first_num

    def find_in_location(self, idx):
        if len(self.password) >= idx:
            return 1 if self.password[idx] == self.letter else 0
        return 0

    def is_password_valid_position(self):
        letters_in_position = self.find_in_location(self.first_num-1) + self.find_in_location(self.second_num-1)
        return letters_in_position == 1


class PasswordChecker:
    def __init__(self, entries):
        self.password_entries = [PasswordEntry(entry) for entry in entries]
        self.valid_passwords_min_max = 0
        self.valid_passwords_position = 0

    def check_passwords_min_max(self):
        for entry in self.password_entries:
            if entry.is_password_valid_min_max():
                self.valid_passwords_min_max += 1

        return self.valid_passwords_min_max

    def check_passwords_position(self):
        for entry in self.password_entries:
            if entry.is_password_valid_position():
                self.valid_passwords_position += 1

        return self.valid_passwords_position


if __name__ == "__main__":
    file_handler = FileHandler('input.txt')
    file_handler.load_str()
    password_checker = PasswordChecker(file_handler.file_lines)
    print("{} valid min & max passwords found.".format(password_checker.check_passwords_min_max()))
    print("{} valid in position passwords found.".format(password_checker.check_passwords_position()))
