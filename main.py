from day_1 import task as task1
from day_2 import task as task2
from day_3 import task as task3
from day_4 import task as task4
from day_5 import task as task5
from day_6 import task as task6
from day_7 import task as task7
from day_8 import task as task8
from day_9 import task as task9
from day_10 import task as task10
from day_11 import task as task11
from day_12 import task as task12
from day_13 import task as task13
from day_14 import task as task14


def getData(path):
    with open(path) as f:
        data = f.readlines()
        data = [x.strip() for x in data]
    return data


def getDataWithEmptyLines(path):
    lines = []
    i = 0
    with open(path) as f:
        for line in f:
            if line != '\n':
                if i < len(lines):
                    lines[i] += ' ' + line
                else:
                    lines.append(line)
            else:
                i += 1
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines


if __name__ == '__main__':
    # task1.task(getData('day_1/input.txt'))
    # task2.task(getData('day_2/input.txt'))
    # task3.task(getData('day_3/input.txt'))
    # task4.task(getDataWithEmptyLines('day_4/input.txt'))
    # task5.task(getData('day_5/input.txt'))
    # task6.task(getDataWithEmptyLines('day_6/input.txt'))
    # task7.task(getData('day_7/input.txt'))
    # task8.task(getData('day_8/input.txt'))
    # task9.task(getData('day_9/input.txt'))
    # task10.task(getData('day_10/input.txt'))
    # task11.task(getData('day_11/input.txt'))
    # task12.task(getData('day_12/input.txt'))
    # task13.task(getData('day_13/input.txt'))
    task14.task(getData('day_14/input.txt'))
