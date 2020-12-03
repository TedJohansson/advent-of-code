from utils.file_handler import FileHandler


class MapRow:
    def __init__(self, row):
        self.row = row

    def is_tree(self, idx):
        if idx >= len(self.row):
            idx = (idx % len(self.row))
        return self.row[idx] == "#"


class AreaMap:
    trees_encountered = 0
    current_location = [0, 0]
    scan_complete = False
    velocity_x = 0
    velocity_y = 0

    def __init__(self, map_lines):
        self.map_rows = [MapRow(row) for row in map_lines]
        self.reset_scan()

    def move(self):
        self.current_location[0] += self.velocity_y
        self.current_location[1] += self.velocity_x

    def check_for_tree(self):
        if self.current_location[0] < len(self.map_rows):
            if self.map_rows[self.current_location[0]].is_tree(self.current_location[1]):
                self.trees_encountered += 1
        else:
            self.scan_complete = True

    def scan_map(self):
        while not self.scan_complete:
            self.check_for_tree()
            self.move()

    def reset_scan(self):
        self.trees_encountered = 0
        self.current_location = [0, 0]
        self.scan_complete = False
        self.velocity_x = 0
        self.velocity_y = 0

    def load_theory(self, theory: dict):
        self.reset_scan()
        self.velocity_x = theory["velocity_x"]
        self.velocity_y = theory["velocity_y"]


class Scan:
    def __init__(self, area_map: AreaMap, theories: list):
        self.area_map = area_map
        self.theories = theories
        self.sum_routes = 1
        self.quickest_route = None

    def check_theories(self):
        for theory in self.theories:
            self.area_map.load_theory(theory)
            self.area_map.scan_map()
            self.calculate_result(theory)

    def calculate_result(self, theory):
        self.sum_routes *= self.area_map.trees_encountered
        theory["trees_encountered"] = self.area_map.trees_encountered
        if self.quickest_route and self.quickest_route["trees_encountered"] < theory["trees_encountered"]:
            return
        self.quickest_route = theory


if __name__ == "__main__":
    file_handler = FileHandler("input.txt")
    file_handler.load_str()
    theories_to_scan = [
        {"velocity_x": 3, "velocity_y": 1, "trees_encountered": 0},
        {"velocity_x": 1, "velocity_y": 1, "trees_encountered": 0},
        {"velocity_x": 5, "velocity_y": 1, "trees_encountered": 0},
        {"velocity_x": 7, "velocity_y": 1, "trees_encountered": 0},
        {"velocity_x": 1, "velocity_y": 2, "trees_encountered": 0}
    ]
    area_map_obj = AreaMap(file_handler.file_lines)

    scan = Scan(area_map_obj, theories_to_scan)
    scan.check_theories()

    print(f"{scan.sum_routes} is all the routes multiplied")
    print(f"""{scan.quickest_route['velocity_x']}x:{scan.quickest_route['velocity_y']}y has least trees with \
{scan.quickest_route['trees_encountered']} trees encountered""")

