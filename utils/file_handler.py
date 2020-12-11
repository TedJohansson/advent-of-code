class FileHandler:
    file_lines = []

    def __init__(self, file_name):
        self.file_name = file_name

    def load_int(self):
        with open(self.file_name) as f:
            self.file_lines = [int(x) for x in f.readlines()]

    def load_str(self):
        with open(self.file_name) as f:
            self.file_lines = [x.strip("\n") for x in f.readlines()]

    def join_on_not_empty(self):
        joined_lines = []
        joined_line = ""
        for idx, line in enumerate(self.file_lines):
            if len(line) > 0:
                joined_line = f"{joined_line} {line}"
                if idx == len(self.file_lines)-1:
                    joined_lines.append(joined_line)
            else:
                joined_lines.append(joined_line)
                joined_line = ""
        self.file_lines = joined_lines
