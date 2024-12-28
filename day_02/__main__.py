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
Attempt at single iteration solution. It comes pretty close but misses an edge case.

O(n)
"""
def part_2():
    safe_count = 0

    for report in parsed:
        """
        We can look at the first 3 differences to tell whether the report should
        be predominantly increasing or decreasing. We give a "freebee" to one 
        faulty difference.
        """
        diff_set = set()
        is_increasing = None
        for i, number in enumerate(report[1:min(4, len(report))]):
            diff = report[i] - number
            normalized_diff = diff / abs(diff) if diff != 0 else 0
            if normalized_diff in diff_set and diff != 0: 
                # we found a diff that appears 2x
                is_increasing = diff < 0
                break
            else:
                diff_set.add(normalized_diff)
        else: # case where no diff appeared twice or a 0 appeared twice
            continue
        
        def is_valid(diff):
            return (diff < 0) == is_increasing and (1 <= abs(diff) <= 3)
        
        invalid_diff_count = 0
        prev_unsafe_i = None

        def validate_remove_i(i):
            nonlocal invalid_diff_count
            if i - 1 >= 0:
                left_diff = report[i - 1] - report[i]
                invalid_diff_count -= 1 if not is_valid(left_diff) else 0
            if i + 1 < len(report):
                right_diff = report[i] - report[i + 1]
                invalid_diff_count -= 1 if not is_valid(right_diff) else 0
                new_diff = report[i - 1] - report[i + 1]
                invalid_diff_count += 1 if not is_valid(new_diff) else 0
            return invalid_diff_count == 0

        for i, number in enumerate(report[1:]):
            diff = report[i] - number
            invalid_diff_count += 1 if not is_valid(diff) else 0

            if (diff < 0) != is_increasing or not (1 <= abs(diff) <= 3):
                if prev_unsafe_i is None:
                    prev_unsafe_i = i + 2
                    if i + 2 < len(report):
                        diff = report[i + 1] - report[i + 2]
                        invalid_diff_count += 1 if not is_valid(diff) else 0
                    if validate_remove_i(i) or validate_remove_i(i + 1):
                        continue
                    else:
                        break # removing either does not work, so this report fails
                else:
                    break
        else:
            safe_count += 1

    return safe_count

"""
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