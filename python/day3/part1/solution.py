
import logging

testing_state = False
logging_level = logging.DEBUG if testing_state else logging.INFO

logging.basicConfig(level=logging_level)

test_filename = "input.test"
live_filename = "input"
input_filename = test_filename if testing_state else live_filename

def find_best_joltage(bank_joltages:list) -> int:
    last = len(bank_joltages) - 2
    second_battery = bank_joltages[last+1]
    first_battery = bank_joltages[last]
    last -= 1
    while last >= 0:
        if bank_joltages[last] >= first_battery: # re-assign first battery
            #logging.debug(f"Updating first battery to {bank_joltages[last]}")
            if first_battery > second_battery: # check if second battery should be updated
                #logging.debug(f"Updating second battery to {first_battery}")
                second_battery = first_battery
            first_battery = bank_joltages[last]
        last -= 1
    logging.debug(f"Returning best voltage of {10*first_battery + second_battery}")
    return 10*first_battery + second_battery

def solve(banks:list) -> int:
    voltages = []
    for bank in banks:
        logging.debug(f"testing {bank}")
        bank_joltages = list(map(int, bank.strip()))
        voltages.append(find_best_joltage(bank_joltages))
    return sum(voltages)

def process_input(input_file):
    processed = input_file.readlines()
    return processed

def test_input(solution:int) -> bool:
    return solution == 357

def main():
    with open(input_filename,'r') as input_file:
        processed = process_input(input_file)

    solution = solve(processed)

    #testing
    if testing_state:
        try:
            assert test_input(solution)
            print("TEST PASSED")
        except:
            print("TEST FAILURE")

    logging.info(f"Solution: {solution}")

if __name__ == "__main__":
    main()