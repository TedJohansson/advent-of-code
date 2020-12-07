import re


class Field:
    value: str = None

    def __init__(self, required=False):
        self.value = ''
        self.required = required
        self.valid = True
        self.errors = []

    def validate(self):
        if not self.valid:
            return
        validations = [x for x in self.__dir__() if x.startswith('validate_')]

        for validation in validations:
            if not getattr(self, validation)():
                self.valid = False

    def load_value(self, value):
        if self.required and value is None:
            self.errors.append("Missing required field")
            self.valid = False
        else:
            self.valid = True
            self.value = value


class YearField(Field):
    value: int = None

    def __init__(self, min_year=1900, max_year=2020, length=4, required=False):
        super().__init__(required)
        self.min_year = min_year
        self.max_year = max_year
        self.length = length

    def validate_between(self):
        if self.value < self.min_year or self.value > self.max_year:
            self.errors.append(f"{self.value} is not between {self.min_year} and {self.max_year}")
            return False
        return True

    def validate_format(self):
        if len(str(self.value)) != self.length:
            self.errors.append(f"{self.value} is not of length {self.length}")
            return False
        return True

    def load_value(self, value):
        super(YearField, self).load_value(value)
        if self.value:
            self.value = int(self.value)


class HeightField(Field):

    def __init__(self, required=False):
        super().__init__(required)

    def validate_height(self):
        if "cm" in self.value:
            if 150 <= int(self.value.replace('cm', '')) <= 193:
                return True
            self.errors.append(f"less than 150 or higher than 193 is not a valid height in cm")
            return False
        if "in" in self.value:
            if 59 <= int(self.value.replace('in', '')) <= 76:
                return True
            self.errors.append(f"less than 59 or higher than 76 is not a valid height in IN")
            return False

        return False


class RegexField(Field):

    def __init__(self, regex, required=False):
        super().__init__(required)
        self.regex = regex

    def validate_regex(self):
        if not re.match(self.regex, self.value):
            self.errors.append(f"{self.value} is not a valid value")
            return False
        return True


class ChoiceField(Field):

    def __init__(self, choices, required=False):
        super().__init__(required)
        self.choices = choices

    def validate_choice(self):
        if self.value not in self.choices:
            self.errors.append(f"{self.value} is not a valid choice")
            return False
        return True

