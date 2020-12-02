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
