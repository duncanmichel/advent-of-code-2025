
import logging

logging.basicConfig(level=logging.INFO)

#input_name = "input.test"
input_name = "input"

def find_invalid(start:int,end:int) -> list:
    invalid_ids_temp = []
    for id in range(start,end+1):
        id_str = str(id)
        if len(id_str) % 2 == 0:
             midpoint = len(id_str) // 2
             if id_str[:midpoint] == id_str[midpoint:]:
                 invalid_ids_temp.append(id)
                 logging.debug(f"Invalid ID found: {id}")
    return invalid_ids_temp

def solve(list_of_ranges:list) -> int:
    invalid_ids = []
    for id_range in list_of_ranges:
        start_str,end_str = id_range.split('-')
        invalid_ids += find_invalid(int(start_str),int(end_str))
    return sum(invalid_ids)

with open(input_name,'r') as input_file:
    ranges = input_file.readlines()[0].split(',')

solution = solve(ranges)

#testing
if input_name == 'input.test':
    try:
        assert solution == 1227775554
        print("TEST PASSED")
    except:
        print("TEST FAILURE")

print(f"Sum of invalid IDs: {solution}")