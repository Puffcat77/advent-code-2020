# --- Day 14: Docking Data ---
# As your ferry approaches the sea port, the captain asks for your help again.
# The computer system that runs this port isn't compatible with the docking program
# on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.
#
# After a brief inspection, you discover that the sea port's computer system uses
# a strange bitmask system in its initialization program. Although you don't have
# the correct decoder chip handy, you can emulate it in software!
#
# The initialization program (your puzzle input) can either update the bitmask or
# write a value to memory. Values and memory addresses are both 36-bit unsigned integers.
# For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.
#
# The bitmask is always given as a string of 36 bits, written with the most
# significant bit (representing 2^35) on the left and the least significant bit
# (2^0, that is, the 1s bit) on the right. The current bitmask is applied to
# values immediately before they are written to memory: a 0 or 1 overwrites
# the corresponding bit in the value, while an X leaves the bit in the value unchanged.
#
# For example, consider the following program:
#
# mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# This program starts by specifying a bitmask (mask = ....).
# The mask it specifies will overwrite two bits in every written value: the 2s bit
# is overwritten with 0, and the 64s bit is overwritten with 1.
#
# The program then attempts to write the value 11 to memory address 8. By expanding
# everything out to individual bits, the mask is applied as follows:
#
# value:  000000000000000000000000000000001011  (decimal 11)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001001001  (decimal 73)
# So, because of the mask, the value 73 is written to memory address 8 instead.
# Then, the program tries to write 101 to address 7:
#
# value:  000000000000000000000000000001100101  (decimal 101)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001100101  (decimal 101)
# This time, the mask has no effect, as the bits it overwrote were already the
# values the mask tried to set. Finally, the program tries to write 0 to address 8:
#
# value:  000000000000000000000000000000000000  (decimal 0)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001000000  (decimal 64)
# 64 is written to address 8 instead, overwriting the value that was there previously.
#
# To initialize your ferry's docking program, you need the sum of all values left in
# memory after the initialization program completes. (The entire 36-bit address space
# begins initialized to the value 0 at every address.) In the above example, only two
# values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
#
# Execute the initialization program. What is the sum of all values left in memory after it completes?
# (Do not truncate the sum to 36 bits.)
def getBinaryValue(value):
    res = []
    while value > 0:
        res = [str(value % 2)] + res
        value //= 2
    res = ['0']*(36-len(res)) + res
    return res


def getMaxBinIndex(value, mask):
    if mask.count('1') > 0 and value.count('1') > 0:
        return min(value.index('1'), mask.index('1'))
    elif mask.count('1') == 0 and value.count('1') > 0:
        return value.index('1')
    elif mask.count('1') > 0 and value.count('1') == 0:
        return mask.index('1')
    else:
        return len(value) - 1


def applyMask(mask: [str], value: int):
    value = getBinaryValue(value)
    valueLen = len(value)
    maxBinIndex = getMaxBinIndex(value, mask)
    res = ['0'] * 36
    for i in range(valueLen - 1, maxBinIndex - 1, -1):
        res[i] = mask[i] if mask[i] != 'X' else value[i]
    return res


class MemoryCell:
    bitString: [str]
    value: int

    def changeValueAccordingToMask(self, value: int, mask: [str]):
        self.bitString = applyMask(mask, value)
        self.value = parseBinaryToInt(self.bitString)
        pass


class Command:
    cell: int
    value: int

    def __init__(self, cell, value):
        self.cell = cell
        self.value = value


class DataChunk:
    chunkNumber: int
    mask: [str]
    commands: [Command]

    def __init__(self, i,  mask: [str]):
        self.chunkNumber = i
        self.mask = mask
        self.commands = []

    def addCommand(self, command: str):
        cell = int(command[4: command.index(']')])
        value = int(command[command.index('= ') + 2:])
        self.commands.append(Command(cell, value))


def parseBinaryToInt(binStr):
    res = 0
    maxIndex = binStr.index('1') if binStr.count('1') > 0 else 35
    for i in range(35, maxIndex - 1, -1):
        res += 2**(35 - i) if binStr[i] == '1' else 0
    return res


def partOne(data):
    res = 0
    memory = {}
    for d in data:
        mask = d.mask
        for c in d.commands:
            memory[c.cell] = MemoryCell()
            memory[c.cell].changeValueAccordingToMask(c.value, mask)
    for m in memory.keys():
        res += memory[m].value
    return res


# --- Part Two ---
# For some reason, the sea port's computer system still can't communicate with your
# ferry's docking program. It must be using version 2 of the decoder chip!
#
# A version 2 decoder chip doesn't modify the values being written at all.
# Instead, it acts as a memory address decoder. Immediately before a value is written
# to memory, each bit in the bitmask modifies the corresponding bit of the destination
# memory address in the following way:
#
# If the bitmask bit is 0, the corresponding memory address bit is unchanged.
# If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
# If the bitmask bit is X, the corresponding memory address bit is floating.
# A floating bit is not connected to anything and instead fluctuates unpredictably.
# In practice, this means the floating bits will take on all possible values, potentially
# causing many memory addresses to be written all at once!
#
# For example, consider the following program:
#
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# When this program goes to write to memory address 42, it first applies the bitmask:
#
# address: 000000000000000000000000000000101010  (decimal 42)
# mask:    000000000000000000000000000000X1001X
# result:  000000000000000000000000000000X1101X
# After applying the mask, four bits are overwritten, three of which are different,
# and two of which are floating. Floating bits take on every possible combination of values;
# with two floating bits, four actual memory addresses are written:
#
# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# 000000000000000000000000000000111010  (decimal 58)
# 000000000000000000000000000000111011  (decimal 59)
# Next, the program is about to write to memory address 26 with a different bitmask:
#
# address: 000000000000000000000000000000011010  (decimal 26)
# mask:    00000000000000000000000000000000X0XX
# result:  00000000000000000000000000000001X0XX
# This results in an address with three floating bits, causing writes to eight memory addresses:
#
# 000000000000000000000000000000010000  (decimal 16)
# 000000000000000000000000000000010001  (decimal 17)
# 000000000000000000000000000000010010  (decimal 18)
# 000000000000000000000000000000010011  (decimal 19)
# 000000000000000000000000000000011000  (decimal 24)
# 000000000000000000000000000000011001  (decimal 25)
# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# The entire 36-bit address space still begins initialized to the value 0 at every address,
# and you still need the sum of all values left in memory at the end of the program.
# In this example, the sum is 208.
#
# Execute the initialization program using an emulator for a version 2 decoder chip.
# What is the sum of all values left in memory after it completes?
def applyMaskToMemoryIndex(mask: [str], index: [str]):
    valueLen = len(index)
    res = ['0'] * 36
    for i in range(valueLen - 1, -1, -1):
        res[i] = mask[i] if mask[i] != '0' else index[i]
    return res


def getMultipleCells(cell):
    cells = [[]]
    for i in range(len(cell) - 1, -1, -1):
        c = cell[i]
        if c != 'X':
            cells = [[c] + e for e in cells]
        else:
            cells = [['0'] + e for e in cells] + [['1'] + e for e in cells]
    return cells


def partTwo(data):
    res = 0
    memory = {}
    for d in data:
        mask = d.mask
        for command in d.commands:
            cells = map(parseBinaryToInt, getMultipleCells(applyMaskToMemoryIndex(mask, getBinaryValue(command.cell))))
            for c in cells:
                memory[c] = command.value
    for m in memory.keys():
        res += memory[m]
    # answer = 3817372618036
    # print(f'Answer is {answer} and actual is {res}. Difference is {answer - res}')
    return res


def parseData(data: [str]):
    result = []
    i = -1
    for s in data:
        if s[:4] == 'mask':
            i += 1
            result.append(DataChunk(i, [sym for sym in s[s.index('= ') + 2:]]))
            continue
        if s[:3] == 'mem':
            result[-1].addCommand(s)
            continue
    return result


def task(data):
    chunks = parseData(data)
    print(partOne(chunks))
    print(partTwo(chunks))
