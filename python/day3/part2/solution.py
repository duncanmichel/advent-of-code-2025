
import logging

testing_state = False
logging_level = logging.DEBUG if testing_state else logging.INFO

logging.basicConfig(level=logging_level)

test_filename = "input.test"
live_filename = "input"
input_filename = test_filename if testing_state else live_filename

battery_count = 12

def voltage_size(selected_batteries:list[int]) -> int: #list of selected batteries in reverse order
    voltage = 0
    index = 0
    #logging.debug(f"calculating voltage of {selected_batteries}")
    while index < len(selected_batteries):
        voltage += (10**index) * selected_batteries[index]
        index += 1
    return voltage

def update_selected(selected_batteries:list[int],current_battery:int) -> list[int]:
    if current_battery < selected_batteries[-1]:
        return selected_batteries
    index = len(selected_batteries) - 2
    movable = selected_batteries[-1]
    while index >= 0 and movable >= selected_batteries[index]:
        temp = selected_batteries[index]
        selected_batteries[index] = movable
        movable = temp
        index -= 1
    selected_batteries[-1] = current_battery
    return selected_batteries

def fill_battery(bank_joltages:list[int]) -> list[int]:
    starting_battery = [0] * battery_count
    bank_index = len(bank_joltages)-1
    battery_index = 0
    for i in range(0,battery_count):
        starting_battery[battery_index+i] = bank_joltages[bank_index-i]
    logging.debug(f"Initial battery: {starting_battery}")
    return starting_battery

def find_best_joltage(bank_joltages:list[int]) -> int:
    last = len(bank_joltages) - (battery_count + 1)
    selected_batteries = fill_battery(bank_joltages)
    while last >= 0:
        selected_batteries = update_selected(selected_batteries, bank_joltages[last])
        last -= 1
    logging.debug(f"Returning best voltage of {voltage_size(selected_batteries)}\n")
    return voltage_size(selected_batteries)

def solve(banks:list) -> int:
    voltages = []
    for bank in banks:
        logging.debug(f"testing {bank.strip()}")
        bank_joltages = list(map(int, bank.strip()))
        voltages.append(find_best_joltage(bank_joltages))
    return sum(voltages)

def process_input(input_file):
    processed = input_file.readlines()
    return processed

def test_input(solution:int) -> bool:
    return solution == 3121910778619

def main():
    with open(input_filename,'r') as input_file:
        processed = process_input(input_file)

    solution = solve(processed)

    #testing
    if testing_state:
        try:
            assert test_input(solution)
            logging.debug("TEST PASSED")
        except:
            logging.error("TEST FAILURE")

    logging.info(f"Solution: {solution}")

if __name__ == "__main__":
    main()