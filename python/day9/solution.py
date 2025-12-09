#!/usr/bin/python3
import logging
import sys
from io import IOBase
#import re 
#import math
from dataclasses import dataclass
import math
from pprint import pprint
import bisect
from functools import cache


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
        processed = list(map(str.strip,input_file.readlines()))
        return processed # will be passed as first argument to workSolution
    
    def workSolution(self,processed_input:list, starter_val:int) -> int:
        red_tiles = [tuple(map(int,line.split(','))) for line in processed_input] #sorted([tuple(map(int,line.split(','))) for line in processed_input], key=lambda item: (item[0], item[1]))
        solution = findLargestArea(red_tiles) if starter_val == part1 else findInternalRectangle(red_tiles)
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 50 # expected result of part 1 test
        return solution == 24 # expected result of part 2 test

def findLargestArea(red_tiles:list[tuple]) -> int:
    largest = 0
    for idx,(x1,y1) in enumerate(red_tiles):
        #logging.debug(f"{idx},{x1},{y1}")
        for (x2,y2) in red_tiles:
            this_area = (abs(x1-x2)+1)*(abs(y2-y1)+1)
            if this_area > largest:
                largest = this_area
                #logging.debug(f"New largest aread: {largest}")
    return largest

# with open('input','r') as cache_file:
#     poly_data = cache_file.readlines()
# poly = [tuple(map(int,line.split(','))) for line in poly_data]

# turns out (from research) I need a ray-intersecting algorithm to find if points are inside or outside a polygon. Borrowing and adapting this from Rosetta code
def isPointInside(xp,yp,poly):
    inside = False
    for (x1,y1),(x2,y2) in zip(poly,poly[1:] + poly[:1]):
        if (xp == x1 == x2 and min(y1,y2) <= yp <= max(y1,y2)) or (yp == y1 ==y2 and min(x1,x2) <= xp <= max(x1,x2)):
            return True
        if (y1 > yp) != (y2 > yp) and (xp < (x2-x1)*(yp-y1)/(y2-y1)+x1):
            inside = not inside
    return inside

def rectValid(x1,y1,x2,y2,poly):
    # for x in range(min(x1,x2),max(x1,x2)):
    #     for y in range(min(y1,y2),max(y1,y2)):
    #         if not isPointInside(x,y,poly):
    #             return False
    x1,x2 = sorted((x1,x2))
    y1,y2 = sorted((y1,y2))
    for (ex1,ey1),(ex2,ey2) in zip(poly,poly[1:] + poly[:1]):
        if ey1 == ey2: # horizontal edge; y remains the same
            if y1 < ey1 < y2:
                if max(ex1,ex2) > x1 and min(ex1,ex2) < x2:
                    return False
        else: # vertical edge; x remains the same
            if x1 < ex1 < x2:
                if max(ey1,ey2) > y1 and min(ey1,ey2) < y2:
                    return False
    return True

def findInternalRectangle(red_tiles:list[tuple]) -> int:
    largest = 0
    for idx,(x1,y1) in enumerate(red_tiles[:-1]):
        for jdx,(x2,y2) in enumerate(red_tiles[idx+1:]):
            if isPointInside(x1,y2,red_tiles) and isPointInside(x2,y1,red_tiles): # check if unnamed corners are even valid
                this_area = (abs(x1-x2)+1)*(abs(y2-y1)+1)
                if this_area > largest and rectValid(x1,y1,x2,y2,red_tiles): # potential new largest rectangle; now assess if entirely within
                    largest = this_area
    #logging.debug(f"2,1 is {ispointinside(2,1,red_tiles)}")
    #logging.debug(f"11,5 is {ispointinside(11,5,red_tiles)}")
    return largest

def old_findInternalRectangle(red_tiles:list[tuple]) -> int:
    x_map = {}
    x_points = []
    y_map = {}
    y_points = []
    x_lines = {}
    y_lines = {}
    largest = 0
    for idx, (x,y) in enumerate(red_tiles):
        if x not in x_map:
            x_map[x] = [y]
        else:
            x_map[x].append(y)
        if x not in x_points:
            x_points.append(x)
        if y not in y_map:
            y_map[y] = [x]
        else:
            y_map[y].append(x)
        if y not in y_points:
            y_points.append(y)
        next_idx = (idx + 1) % len(red_tiles) # wrap around if the last item
        if red_tiles[next_idx][0] == x: # if x is same, new line on y axis
            if x not in x_lines:
                x_lines[x] = [(y,red_tiles[next_idx][1])]
            else:
                x_lines[x].append((y,red_tiles[next_idx][1]))
        else: # y is same, so new line on x axis
            if y not in y_lines:
                y_lines[y] = [(x,red_tiles[next_idx][0])]
            else:
                y_lines[y].append((x,red_tiles[next_idx][0]))
    x_points = sorted(x_points)
    y_points = sorted(y_points)
    for idx,(x1,y1) in enumerate(red_tiles):
        if idx == len(red_tiles) - 1:
            break
        logging.debug(f" on point {x1},{y1}")
        for x2,y2 in red_tiles[idx+1:]:
            kill = False
            this_area = (abs(x1-x2)+1)*(abs(y2-y1)+1)
            if this_area > largest: # potential larger rectangle
                logging.debug(f"Checking area between {x1},{y1} and {x2},{y2}")
                # make sure that no points exist inside potential rectangle
                x_between = x_points[x_points.index(min(x1,x2))+1:x_points.index(max(x1,x2))]
                y_between = y_points[y_points.index(min(y1,y2))+1:y_points.index(max(y1,y2))]
                logging.debug(f"x between: {x_between}")
                logging.debug(f"y between: {y_between}")
                y_points_on_x_between = list(set([y for x in [x_map[x] for x in x_between] for y in x]))
                x_points_on_y_between = list(set([x for y in [y_map[y] for y in y_between] for x in y]))
                logging.debug(f"y points to eval: {y_points_on_x_between}")
                logging.debug(f"x points to eval: {x_points_on_y_between}")
                for y in y_points_on_x_between:
                    if y in y_between:
                        kill = True
                        break
                for x in x_points_on_y_between:
                    if x in x_between:
                        kill = True
                        break
                if kill:
                    continue
                # make sure that a line exists on all four sides on or outside rectangle
                logging.debug(f"Point check passes")
                kill = True
                for x in x_points[:x_points.index(min(x1,x2))+1]: # check left
                    for line in x_lines[x]:
                        if min(line) < max(y1,y2) and max(line) > min(y1,y2): # overlap with rectangle area
                            logging.debug(f"found a passing line: {x} -> {line}")
                            kill = False
                            break
                    if not kill: # found overalp
                        break
                if kill:
                    continue
                kill = True
                for x in x_points[x_points.index(max(x1,x2)):]: # check right
                    for line in x_lines[x]:
                        if min(line) < max(y1,y2) and max(line) > min(y1,y2): # overlap with rectangle area
                            logging.debug(f"found a passing line: {x} -> {line}")
                            kill = False
                            break
                    if not kill: # found overalp
                        break
                if kill:
                    continue
                kill = True
                for y in y_points[:y_points.index(min(y1,y2))+1]: # check below
                    for line in y_lines[y]:
                        if min(line) < max(x1,x2) and max(line) > min(x1,x2): # overlap with rectangle area
                            logging.debug(f"found a passing line: {y} -> {line}")
                            kill = False
                            break
                    if not kill: # found overalp
                        break
                if kill:
                    continue
                kill = True
                for y in y_points[y_points.index(max(y1,y2)):]: # check above
                    for line in y_lines[y]:
                        if min(line) < max(x1,x2) and max(line) > min(x1,x2): # overlap with rectangle area
                            logging.debug(f"found a passing line: {y} -> {line}")
                            kill = False
                            break
                    if not kill: # found overalp
                        break
                if kill:
                    continue

                # update largest
                if kill:
                    logging.debug("Line check failed. Continuing...")
                largest = this_area
                logging.debug(f"New largest area: {largest}")

    #INFO:root:Solution: 4629432496 == TOO HIGH
    return largest

def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()