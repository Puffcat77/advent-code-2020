import math
# Day 1: Report Repair
# Before you leave, the Elves in accounting just need you to fix your expense report (your puzzle input);
# apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.
#
# For example, suppose your expense report contained the following:
#
# 1721
# 979
# 366
# 299
# 675
# 1456
# In this list, the two entries that sum to 2020 are 1721 and 299.
# Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.
#
# Of course, your expense report is much larger. Find the two entries that sum to 2020;
# what do you get if you multiply them together?


def getMultiplicationOfTwo(data):
    maximum = 2020
    values = [-1] * (maximum + 1)
    for d in data:
        values[d] = d
    i = 0
    length = maximum
    while i < length/2:
        pair = length - i
        if values[i] != -1 and values[pair] != -1:
            return values[i] * values[pair]
        i += 1

# --- Part Two ---
# The Elves in accounting are thankful for your help;
# one of them even offers you a starfish coin they had
# left over from a past vacation. They offer you a second one if you can
# find three numbers in your expense report that meet the same criteria.
#
# Using the above example again, the three entries that sum to 2020 are
# 979, 366, and 675. Multiplying them together produces the answer, 241861950.
#
# In your expense report, what is the product of the three entries that sum to 2020?


def getMultiplicationOfThree(data):
    maximum = 2020
    values = [-1] * (maximum + 1)
    for d in data:
        values[d] = d
    length = maximum
    third = math.floor(length/3)
    for i in range(third + 1):
        if values[i] != -1:
            for j in range(i + 1, 2 * third + 1):
                if values[j] != -1:
                    for k in range(j + 1, length):
                        if (values[i] + values[j] + values[k] == 2020
                                and values[k] != -1):
                            return values[i] * values[j] * values[k]


def task(data):
    data = [int(x) for x in data]
    print(getMultiplicationOfTwo(data))
    print(getMultiplicationOfThree(data))
