import re
from dataclasses import dataclass, field

from typing import List

from aoc_four.fields import YearField, HeightField, RegexField, ChoiceField, Field
from utils.file_handler import FileHandler


@dataclass
class Paper:
    byr: YearField = YearField(min_year=1920, max_year=2002, required=True)
    iyr: YearField = YearField(min_year=2010, max_year=2020, required=True)
    eyr: YearField = YearField(min_year=2020, max_year=2030, required=True)
    hgt: HeightField = HeightField(required=True)
    hcl: RegexField = RegexField(regex=r"^#[0-9a-f]{6}$", required=True)
    ecl: ChoiceField = ChoiceField(choices=["amb", "blu", "brn", "gry", "grn", "hzl", "oth"], required=True)
    pid: RegexField = RegexField(regex=r"^\d{9}$", required=True)
    invalid_fields: List[str] = field(default_factory=list)
    valid: bool = True

    def __init__(self):
        self.byr = YearField(min_year=1920, max_year=2002, required=True)
        self.iyr = YearField(min_year=2010, max_year=2020, required=True)
        self.eyr = YearField(min_year=2020, max_year=2030, required=True)
        self.hgt = HeightField(required=True)
        self.hcl = RegexField(regex=r"^#[0-9a-f]{6}$", required=True)
        self.ecl = ChoiceField(choices=["amb", "blu", "brn", "gry", "grn", "hzl", "oth"], required=True)
        self.pid = RegexField(regex=r"^\d{9}$", required=True)
        self.invalid_fields = []
        self.valid = True

    def load_data(self, paper_dict):
        self.byr.load_value(paper_dict.get('byr'))
        self.iyr.load_value(paper_dict.get('iyr'))
        self.eyr.load_value(paper_dict.get('eyr'))
        self.hgt.load_value(paper_dict.get('hgt'))
        self.hcl.load_value(paper_dict.get('hcl'))
        self.ecl.load_value(paper_dict.get('ecl'))
        self.pid.load_value(paper_dict.get('pid'))

    def get_fields(self):
        return [a for a in dir(self) if not a.startswith('__') and isinstance(getattr(self, a), Field)]

    def validate(self):
        for validate_field in self.get_fields():
            field_to_validate = getattr(self, validate_field)
            field_to_validate.validate()
            if not field_to_validate.valid:
                self.invalid_fields.append(f"{validate_field} is not valid")
                self.valid = False


class Papers:

    def __init__(self, lines):
        self.papers = [self.parse_line(line) for line in lines]
        self.valid_papers = 0
        self.invalid_papers = 0

    @property
    def report(self):
        return f"There are {self.valid_papers} valid papers and {self.invalid_papers} invalid papers"

    @classmethod
    def parse_line(cls, line):
        attributes = re.findall(r"[\w'#]+", line)
        attributes_iter = iter(attributes)
        return cls.dict_to_paper(dict(zip(attributes_iter, attributes_iter)))

    @classmethod
    def dict_to_paper(cls, paper_dict: dict):
        paper = Paper()
        paper.load_data(paper_dict)
        return paper

    def validate_papers(self):
        for paper in self.papers:
            paper.validate()
            if len(paper.invalid_fields) > 0:
                paper.valid = False
                self.invalid_papers += 1
            else:
                self.valid_papers += 1


if __name__ == "__main__":
    file_handler = FileHandler("input.txt")
    file_handler.load_str()
    file_handler.join_on_not_empty()
    papers = Papers(file_handler.file_lines)
    papers.validate_papers()
    print(papers.report)
