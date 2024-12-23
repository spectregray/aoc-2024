import os
import timeit
from pathlib import Path
from collections import Counter

parsed = None

def main():
    dir_name = Path(__file__).parent.name
    file_name = "input.txt"
    file_path = os.path.join(dir_name, file_name)

    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        raise SystemExit(0)

    parse(file_path)
    part_1_execution_time = timeit.timeit('part_1()', globals=globals(), number=1) 
    part_2_execution_time = timeit.timeit('part_2()', globals=globals(), number=1) 
    print(f"Part 1: {part_1()} took: {part_1_execution_time:.4f} seconds.")
    print(f"Part 2: {part_2()} took: {part_2_execution_time:.4f} seconds.")

def parse(file_path):
    global parsed
    parsed = [[], []]
    with open(file_path, 'r') as file:
        for line in file:
            first_str = line[:line.find(' ')]
            second_str = line[line.rfind(' ') + 1:]
            parsed[0].append(int(first_str))
            parsed[1].append(int(second_str))

"""
Just sort and iterate through both lists simultaneously to find distance.
"""
def part_1():
    distance = 0

    parsed[0].sort()
    parsed[1].sort()

    for i in range(len(parsed[0])):
        distance += abs(parsed[0][i] - parsed[1][i])

    return distance

"""
Use a counter for the "right" list.
"""
def part_2():
    similarity = 0

    right_list_counter = Counter(parsed[1])

    for num in parsed[0]:
        similarity += num * right_list_counter[num]

    return similarity

if __name__ == '__main__':
    main()