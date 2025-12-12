#!/usr/bin/python3
import logging
import sys
from io import IOBase
#import re 
#import math
from dataclasses import dataclass
from pprint import pprint
#import itertools


TESTING_STATE = True
SUBMIT = True
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants


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
        processed = input_file.read()
        return processed # will be passed as first argument to workSolution
    
    def workSolution(self,processed_input:list, starter_val:int) -> int:
        solution = 0
        *gifts_s,area_s = processed_input.split('\n\n')
        gift_dict = {}
        for gift in gifts_s:
            gift_id,gift_def = gift.split(':')
            gift_dict[int(gift_id)] = gift_def.count('#')
        logging.debug(gift_dict)
        for line in area_s.split('\n'):
            dimensions,gift_list_str = line.split(': ')
            w,l = tuple(map(int,dimensions.split('x')))
            gift_list = list(map(int,gift_list_str.split()))
            if checkBounds(gift_dict,gift_list,w,l):
                solution += 1
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 2 # expected result of part 1 test
        return solution == 999 # expected result of part 2 test

def checkBounds(gift_dict:dict,gift_list:list[int],width:int,length:int) -> bool:
    return sum([x*gift_dict[i] for i,x in enumerate(gift_list)]) < width*length

def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()