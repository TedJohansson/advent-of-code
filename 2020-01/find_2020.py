class AccountingMistakeFinder:
    def __init__(self, accounting_file_name: str, sum_number: int):
        self.sum_number = sum_number
        with open(accounting_file_name) as accounting_file:
            self.accounting_entries = [int(x) for x in accounting_file.readlines()]

    def find_equal(self, idx, value, sum_triple=False):
        for second_idx, entry in enumerate(self.accounting_entries[idx+1:]):
            if sum_triple:
                for third_idx, third_entry in enumerate(self.accounting_entries[second_idx+1:]):
                    if entry + value + third_entry == self.sum_number:
                        return entry * third_entry
            else:
                if entry + value == self.sum_number:
                    return entry
        return None

    def find_the_triple(self):
        for idx, entry in enumerate(self.accounting_entries):
            second_entry = self.find_equal(idx, entry, True)
            if second_entry:
                return entry * second_entry

    def find_the_dues(self):
        for idx, entry in enumerate(self.accounting_entries):
            second_entry = self.find_equal(idx, entry)
            if second_entry:
                return entry * second_entry


if __name__ == "__main__":
    find_it = AccountingMistakeFinder("input.txt", 2020)
    print("The two numbers equal: {}".format(find_it.find_the_dues()))
    print("The three numbers equal: {}".format(find_it.find_the_triple()))
