import os
from typing import List


def first_calibration(input_file_path: str) -> List:
    print('Calibrating frequency...')
    with open(input_file_path) as input_file:
        return [int(input_signal) for input_signal in input_file]


def second_calibration(inputs: List):
    print('Calibrating frequency...')
    frequency_at_point = []
    previous_value = 0
    for input_frequency in inputs:
        frequency_at_point.append(previous_value + input_frequency)
        previous_value = frequency_at_point[-1]

    current_frequency = frequency_at_point[-1]
    while True:
        for input_frequency in inputs:
            current_frequency += input_frequency
            if current_frequency in frequency_at_point:
                return current_frequency


if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input.txt')
    first_result = first_calibration(file_path)
    print(f'First calibration done, final frequency {sum(first_result)}')
    second_result = second_calibration(first_result)
    print(f'Second calibration done, final frequency {second_result}')

