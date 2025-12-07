#!/usr/bin/python3
import logging
import sys
from io import IOBase
import re 
import math

TESTING_STATE = False
SUBMIT = True
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants
SPLIT='^'

class Solver:
    def __init__(self):
        test_filename = "input.test"
        live_filename = "input"
        self.input_filename = live_filename if SUBMIT else test_filename

    def processInput(self,input_file):
        assert isinstance(input_file, IOBase)
        logging.info("'processInput' Not Implemented")
        return None
    
    def readInput(self):
        try:
            with open(self.input_filename,'r') as input_file:
                processed = self.processInput(input_file)
            return processed
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"General Error: {e}")
            sys.exit(1)
    
    def workSolution(self,processed_input,initialization):
        assert processed_input == None
        assert initialization == 0
        logging.info("'workSolution' Not Implemented")
        return None
    
    def testInput(self,solution,initialization) -> bool:
        assert solution == None
        assert initialization == 0
        logging.info("'testInput' Not Implemented")
        return False
    
    def solve(self,initialization):
        solution = self.workSolution(self.readInput(),initialization) if initialization != 0 else None
        #testing
        if TESTING_STATE:
            try:
                assert self.testInput(solution,initialization)
                logging.debug("TEST PASSED")
            except:
                logging.error("TEST FAILURE")

        logging.info(f"Solution: {solution}")

class ContextualSolver(Solver):
    def __init__(self):
        super().__init__()

    def processInput(self,input_file):
        processed = list(map(str.strip,input_file.readlines()))
        return processed # will be passed as first argument to workSolution
    
    def workSolution(self,processed_input:list, starter_val:int) -> int:
        beams = [0 for x in range(len(processed_input[0]))]
        beams[processed_input[0].index('S')] = 1
        for row in processed_input[1:]:
            beams = determine_splits(beams,row,starter_val)
        return sum(beams)
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 21 # expected result of part 1 test
        return solution == 40 # expected result of part 2 test

def determine_splits(beams:list[int],row:list[str],starter_val:int) -> (list[bool],int):
    idx = 1
    logging.debug(''.join(list(map(str,[beams[i] if beams[i] else '.' for i in range(len(beams))]))))
    logging.debug(row)
    while idx < len(row) - 1:
        if beams[idx] and row[idx] == SPLIT:
            # when I changed this to solve part2, I ruined the solution to part1, but was basically incrementing a counter of "splits" here
            beams[idx-1] = 1 if starter_val == part1 else beams[idx-1] + beams[idx]
            beams[idx+1] = 1 if starter_val == part1 else beams[idx+1] + beams[idx]
            beams[idx] = 0
            idx += 2
        else:
            idx += 1
    return beams

def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()