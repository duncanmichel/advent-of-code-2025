
import logging

logging.basicConfig(level=logging.INFO)

#input_name = "input.test"
input_name = "input"

def check_invalid_for_interval(id_str:str,interval:int):
    first_seg = id_str[:interval]
    seg_start = 0
    for jump in range(interval,len(id_str)+1,interval):
        if first_seg != id_str[seg_start:jump]:
            logging.debug(f"interval check for: {id_str}, interval {interval}: ({seg_start}:{interval}) {first_seg} does not match {id_str[seg_start:interval]}")
            return False 
        seg_start = jump
    return True

def check_invalid_for_seg_size(id_str:str):
    for segments in range(2,len(id_str)+1):
        logging.debug(f"seg check for: {id_str}, segments: {segments}")
        if len(id_str) % segments == 0:
            interval = len(id_str) // segments
            if check_invalid_for_interval(id_str,interval):
                return True 
    return False

def find_invalid(start:int,end:int) -> list:
    invalid_ids_temp = []
    for id in range(start,end+1):
        id_str = str(id)
        if check_invalid_for_seg_size(id_str):
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
        assert solution == 4174379265
        print("TEST PASSED")
    except:
        print("TEST FAILURE")

print(f"Sum of invalid IDs: {solution}")