import os
import timeit
from pathlib import Path

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
    print(f"Part 1: {part_1()}. Took: {part_1_execution_time:.4f} seconds.")
    print(f"Part 2: {part_2()}. Took: {part_2_execution_time:.4f} seconds.")

def parse(file_path):
    global parsed
    with open(file_path, 'r') as file:
        for line in file:
            pass

def part_1():
    pass

def part_2():
    pass

if __name__ == '__main__':
    main()