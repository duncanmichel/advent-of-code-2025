#!/usr/bin/python3
import logging
import sys
from io import IOBase

TESTING_STATE = False
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants
MIN=0
MAX=1

class Solver:
    def __init__(self):
        test_filename = "input.test"
        live_filename = "input"
        self.input_filename = test_filename if TESTING_STATE else live_filename

    def process_input(self,input_file):
        assert isinstance(input_file, IOBase)
        logging.info("'process_input' Not Implemented")
        return None
    
    def read_input(self):
        try:
            with open(self.input_filename,'r') as input_file:
                processed = self.process_input(input_file)
            return processed
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"General Error: {e}")
            sys.exit(1)
    
    def work_solution(self,processed_input,initialization):
        assert processed_input == None
        assert initialization == 0
        logging.info("'work_solution' Not Implemented")
        return None
    
    def test_input(self,solution,initialization) -> bool:
        assert solution == None
        assert initialization == 0
        logging.info("'test_input' Not Implemented")
        return False
    
    def solve(self,initialization):
        solution = self.work_solution(self.read_input(),initialization) if initialization != 0 else None
        #testing
        if TESTING_STATE:
            try:
                assert self.test_input(solution,initialization)
                logging.debug("TEST PASSED")
            except:
                logging.error("TEST FAILURE")

        logging.info(f"Solution: {solution}")

class ContextualSolver(Solver):
    def __init__(self):
        super().__init__()

    def process_input(self,input_file):
        processed = list(map(str.strip,input_file.readlines()))
        return processed # will be passed as first argument to work_solution
    
    def work_solution(self,processed_input:list, starter_val:int) -> int:
        solution = 0
        midpoint = processed_input.index('')
        raw_ranges = processed_input[:midpoint]
        available_ingredients = list(map(int,processed_input[midpoint+1:]))
        #logging.debug(f"{fresh_ranges}\n{available_ingredients}")
        fresh_ranges = []
        for range in raw_ranges:
            fresh_ranges.append(list(map(int,range.split('-'))))
        fresh_ranges = sorted(fresh_ranges, key=lambda x: x[0])
        #logging.debug(f"Initial raw ranges: {fresh_ranges}")
        last_range = []
        while last_range != fresh_ranges:
            last_range = fresh_ranges
            fresh_ranges = aggregate_ranges(fresh_ranges)
            #logging.debug(f"Aggregated range: {fresh_ranges}")
        if starter_val == part1:
            for ingredient in available_ingredients:
                if determine_fresh(fresh_ranges,ingredient):
                    logging.debug(f"Ingredient: {ingredient} is fresh")
                    solution += 1
        else:
            solution = calc_all_fresh_ids(fresh_ranges)
        
        return solution
    
    def test_input(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 3 # expected result of part 1 test
        return solution == 14 # expected result of part 2 test

def calc_all_fresh_ids(fresh_ranges:list[list[int]]) -> int:
    ids = 0
    for range in fresh_ranges:
        ids += range[MAX] - range[MIN] + 1
    return ids

def determine_fresh(fresh_ranges:list[list[int]], ingredient:int) -> bool:
    # check outside any bounds
    if ingredient > fresh_ranges[-1][MAX]:
        return False 
    for range in fresh_ranges:
        if ingredient < range[MIN]: # outside any bounds check
            return False 
        elif ingredient <= range[MAX]: # passes initial bounds check and falls inside current range
            return True
    return False

def aggregate_ranges(fresh_ranges:list[list[int]]) -> list[list[int]]:
    final_ranges = [fresh_ranges[0]]
    for range in fresh_ranges[1:]:
        i=0
        while i < len(final_ranges):
            if range[MIN] <= final_ranges[i][MAX]: # break when current range min is less than or equal to indexed final range's max
                break
            i += 1
        if i == len(final_ranges): # current range outside bounds of any existing range
            final_ranges.append(range)
        elif range[MAX] > final_ranges[i][MAX]: # increase the max of indexed final range max
            final_ranges[i][MAX] = range[MAX]
        # in the "else" case, the current range is discarded because it is entirely overlapped by an existing range

    return final_ranges

def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()