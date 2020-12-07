from math import ceil

from utils.file_handler import FileHandler


class Seat:
    def __init__(self, binary, max_row_idx, max_column_idx):
        self.binary = binary
        self.min_row_idx = 0
        self.max_row_idx = max_row_idx
        self.min_column_idx = 0
        self.max_column_idx = max_column_idx
        self.row = None
        self.column = None

    @property
    def seat_id(self):
        return (self.row * 8) + self.column

    @property
    def row_data(self):
        return self.binary[:7]

    @property
    def column_data(self):
        return self.binary[7:]

    def find_row(self):
        for data_point in self.row_data:
            if data_point == "F":
                self.max_row_idx = self.max_row_idx - ceil((self.max_row_idx - self.min_row_idx) / 2)
            elif data_point == "B":
                self.min_row_idx = self.min_row_idx + ceil((self.max_row_idx - self.min_row_idx) / 2)
        if self.max_row_idx == self.min_row_idx:
            self.row = self.max_row_idx

    def find_column(self):
        for data_point in self.column_data:
            if data_point == "L":
                self.max_column_idx = self.max_column_idx - ceil((self.max_column_idx - self.min_column_idx) / 2)
            elif data_point == "R":
                self.min_column_idx = self.min_column_idx + ceil((self.max_column_idx - self.min_column_idx) / 2)
        if self.max_column_idx == self.min_column_idx:
            self.column = self.max_column_idx

    def find_seat(self):
        self.find_row()
        self.find_column()


class SeatFinder:
    def __init__(self, num_rows, num_columns, lines):
        self.seats = [Seat(line, num_rows-1, num_columns-1) for line in lines]
        self.highest_seat_id = 0
        self.seat_ids = []

    def populate_seats(self):
        for seat in self.seats:
            seat.find_seat()
            self.seat_ids.append(seat.seat_id)
            if seat.seat_id > self.highest_seat_id:
                self.highest_seat_id = seat.seat_id

    def find_missing_seat_id(self):
        sorted_seat_ids = sorted(self.seat_ids)
        for idx, seat_id in enumerate(sorted_seat_ids):
            if seat_id == max(sorted_seat_ids) or seat_id == min(sorted_seat_ids):
                continue
            if seat_id+1 != sorted_seat_ids[idx+1]:
                print(f"Your seat is {seat_id+1}")
                return
            if seat_id-1 != sorted_seat_ids[idx-1]:
                print(f"Your seat is {seat_id-1}")
                return


if __name__ == "__main__":
    file_handler = FileHandler("input.txt")
    file_handler.load_str()
    seat_finder = SeatFinder(128, 8, file_handler.file_lines)
    seat_finder.populate_seats()
    print(f"{seat_finder.highest_seat_id} is the highest seat ID")
    seat_finder.find_missing_seat_id()
