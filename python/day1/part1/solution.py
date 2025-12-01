
import logging

logging.basicConfig(level=logging.INFO)

def rotate_left(start:int, distance:int) -> int:
    final = start - (distance % 100)
    return 100 + final if final < 0 else final

def rotate_right(start:int, distance:int) -> int:
    final = start + (distance % 100)
    return final - 100 if final >= 100 else final

class RotateIterator:
    def __init__(self,sequence):
        self._sequence = sequence
        self._index = 0
        self._position = 50
        self._zero_ct = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index < len(self._sequence):
            seq = self._sequence[self._index].strip()
            direction,distance = seq[0],int(seq[1:])
            match direction:
                case "L":
                    self._position = rotate_left(self._position,distance)
                case "R":
                    self._position = rotate_right(self._position,distance)
            if self._position == 0:
                self._zero_ct += 1
            self._index += 1
            logging.debug(f"[dbg] Sequence: {seq}; New Position: {self._position}")
            return self._zero_ct
        else:
            raise StopIteration
        
    

with open('input','r') as input_file:
    sequences = input_file.readlines()

for item in RotateIterator(sequences):
    zct = item

print(f"Final Count: {zct}")