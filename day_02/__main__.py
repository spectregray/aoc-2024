import os
import timeit
from pathlib import Path
from collections import defaultdict

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
    part_2_brute_execution_time = timeit.timeit('part_2_brute()', globals=globals(), number=1)
    print(f"Part 1: {part_1()} took: {part_1_execution_time:.4f} seconds.")
    print(f"Part 2: {part_2()} took: {part_2_execution_time:.4f} seconds.")
    print(f"Part 2 Brute: {part_2_brute()} took: {part_2_brute_execution_time:.4f} seconds.")

def parse(file_path):
    global parsed
    parsed = []
    with open(file_path, 'r') as file:
        for line in file:
            num_strings = line.split(" ")
            nums = list(map(lambda x: int(x), num_strings))
            parsed.append(nums)

"""
Part 1: O(n)
Check if first difference is increasing or decreasing, then compares the rest of
the numbers in the report to see if they follow the same pattern.  
"""
def part_1():
    safe_count = 0

    for report in parsed:
        is_increasing = report[0] - report[1] < 0
        for i, number in enumerate(report[1:]):
            diff = report[i] - number
            if (diff < 0) != is_increasing:
                break
            if not (1 <= abs(diff) <= 3):
                break
        else:
            safe_count += 1

    return safe_count

"""
Part 2: O(n) solution, brute force below this

For an input.txt with 1000 lines:
1000x Runtime average: 0.0029 seconds
1000x Brute Force Runtime average: 0.0064 seconds
"""
def part_2():
    """
    Helpers
    """
    def attempt_skip(i):
        """
        Attempt to skip the number at index i by checking if the difference
        between i - 1 and i + 1 is still valid.
        """
        if i - 1 >= 0 and i + 1 < len(report):
            return is_valid_diff(report[i - 1] - report[i + 1])
        return True

    def is_valid_diff(diff):
        return (diff < 0) == is_increasing and (1 <= abs(diff) <= 3)
    
    """
    Main body 
    """
    safe_count = 0

    for report in parsed:
        normalized_set = set() # values 0, -1, or 1
        is_increasing = None # boolean
        skip_index = None

        """
        Based on the first 3 differences, finds out if the rest of the report
        should be predominantly increasing or decreasing. Fails entire report
        early if no two differences are the same.
        """
        for i in range(min(len(report) - 1, 4)):
            diff = report[i] - report[i + 1]
            normalized_diff = diff / abs(diff) if diff != 0 else 0
            if normalized_diff in normalized_set:
                is_increasing = diff < 0
                break
            normalized_set.add(normalized_diff)
        else:
            continue # if first 3 diff are all unique, this report will fail regardless

        """
        Iterates through the report. If an invalid difference has been found,
        records index of the index to be removed. If another invalid difference 
        is found after, fails.
        """
        for i in range(len(report) - 1):
            if skip_index == i:
                prev_diff = report[i - 1] - report[i + 1]
                if not is_valid_diff(prev_diff):
                    break
            else:
                diff = report[i] - report[i + 1]

                if not is_valid_diff(diff):
                    if skip_index is not None:
                        break
                    """
                    If we reach an invalid pair, we should check if the report 
                    works with either of the values removed. We greedily check
                    the second value of the pair first.
                    """
                    if attempt_skip(i + 1):
                        skip_index = i + 1
                    elif attempt_skip(i):
                        skip_index = i
                    if skip_index is None:
                        break
        else:
            safe_count += 1

    return safe_count

"""
Part 2: Brute force
O(n^2)
"""
def part_2_brute():
    safe_count = 0

    # checks if the report is all increasing or all decreasing and does not contain a 0 diff
    def is_valid_report(report):
        normalized_diff_set = set()
        for i, num in enumerate(report[1:]):
            diff = report[i] - num
            if not (1 <= abs(diff) <= 3):
                return False
            normalized = diff / abs(diff) if diff != 0 else 0
            normalized_diff_set.add(normalized)
        return False if 0 in normalized_diff_set else len(normalized_diff_set) == 1

    for report in parsed:
        if is_valid_report(report):
            safe_count += 1
        else:
            # try removing each number in the report and checking if the rest is valid
            for i in range(len(report)):
                new_report = report[:i] + report[i + 1:]
                if is_valid_report(new_report):
                    safe_count += 1
                    break

    return safe_count

if __name__ == '__main__':
    main()